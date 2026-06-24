import os, sys, unittest
SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "distribution-engine", "scripts"))
sys.path.insert(0, SCRIPTS)

from datetime import date

import schedule
import validate_connectors


def _assets():
    """A small atomized-assets dict spanning several channels, each with a link."""
    return {
        "slug": "q3-launch",
        "pillar_title": "The Q3 Launch Pillar",
        "assets": [
            {"id": "li-1", "channel": "linkedin", "type": "post",
             "title": "LinkedIn one", "link": "https://example.com/a"},
            {"id": "li-2", "channel": "linkedin", "type": "post",
             "title": "LinkedIn two", "link": "https://example.com/b?ref=x"},
            {"id": "x-1", "channel": "x", "type": "tweet",
             "title": "Tweet one", "link": "https://example.com/c"},
            {"id": "x-2", "channel": "x", "type": "tweet",
             "title": "Tweet two", "link": "https://example.com/d"},
            {"id": "em-1", "channel": "email", "type": "newsletter",
             "title": "Email one", "link": "https://example.com/e"},
            {"id": "cv-1", "channel": "carousel", "type": "carousel",
             "title": "Carousel one", "link": "https://example.com/f"},
            {"id": "sv-1", "channel": "short_video", "type": "video",
             "title": "Short video one", "link": "https://example.com/g"},
        ],
    }


class ScheduleTests(unittest.TestCase):
    START = date(2026, 7, 1)
    WEEKS = 3

    def setUp(self):
        self.assets = _assets()
        self.sch = schedule.schedule(self.assets, start=self.START, weeks=self.WEEKS)

    def test_count_matches_number_of_assets(self):
        self.assertEqual(self.sch["count"], len(self.assets["assets"]))
        self.assertEqual(len(self.sch["items"]), len(self.assets["assets"]))

    def test_campaign_and_metadata_propagated(self):
        self.assertEqual(self.sch["campaign"], "q3-launch")
        self.assertEqual(self.sch["pillar_title"], "The Q3 Launch Pillar")
        self.assertEqual(self.sch["start"], self.START.isoformat())
        self.assertEqual(self.sch["weeks"], self.WEEKS)

    def test_every_item_date_on_or_after_start(self):
        for r in self.sch["items"]:
            d = date.fromisoformat(r["date"])
            self.assertGreaterEqual(
                d, self.START,
                f"asset {r['asset_id']} scheduled {d} before start {self.START}")

    def test_links_carry_utm_source_and_campaign(self):
        for r in self.sch["items"]:
            self.assertIn("utm_source=", r["link"], r["asset_id"])
            self.assertIn("utm_campaign=", r["link"], r["asset_id"])
            # campaign value should be the slug
            self.assertIn("utm_campaign=q3-launch", r["link"], r["asset_id"])
            # medium is always present too
            self.assertIn("utm_medium=", r["link"], r["asset_id"])

    def test_utm_source_matches_channel(self):
        for r in self.sch["items"]:
            self.assertIn(f"utm_source={r['channel']}", r["link"], r["asset_id"])

    def test_link_separator_respects_existing_query(self):
        # li-2 already has a query string, so utm params join with '&', not a 2nd '?'
        li2 = next(r for r in self.sch["items"] if r["asset_id"] == "li-2")
        self.assertEqual(li2["link"].count("?"), 1)
        self.assertIn("ref=x", li2["link"])
        self.assertIn("&utm_source=", li2["link"])

    def test_items_sorted_by_datetime(self):
        dts = [r["datetime"] for r in self.sch["items"]]
        self.assertEqual(dts, sorted(dts))

    def test_item_fields_present_and_consistent(self):
        for r in self.sch["items"]:
            # datetime starts with the date, and time is its HH:MM
            self.assertTrue(r["datetime"].startswith(r["date"]), r)
            self.assertEqual(r["status"], "scheduled")
            self.assertEqual(r["datetime"][11:16], r["time"])

    def test_empty_link_stays_empty(self):
        # An asset without a link should produce an empty link (no UTM stamping).
        assets = _assets()
        assets["assets"].append(
            {"id": "li-3", "channel": "linkedin", "type": "post",
             "title": "no link", "link": ""})
        sch = schedule.schedule(assets, start=self.START, weeks=self.WEEKS)
        row = next(r for r in sch["items"] if r["asset_id"] == "li-3")
        self.assertEqual(row["link"], "")


class ValidateTests(unittest.TestCase):
    def _registry(self, statuses, infra):
        """statuses: dict id->status; build a connectors registry + infra."""
        names = {
            "email": "Email (Mailchimp)",
            "social": "Social (Buffer)",
            "measurement": "Measurement (GA4)",
            "keyword": "Keyword (Ahrefs)",
        }
        conns = []
        for cid, status in statuses.items():
            conns.append({
                "id": cid,
                "name": names.get(cid, cid),
                "status": status,
                "detail": f"{cid} is {status}",
                "blocker": "needs owner" if status in ("fail", "blocked") else "",
            })
        return {
            "validated_on": "2026-06-24",
            "connectors": conns,
            "infra": infra,
        }

    def _full_infra(self):
        return {
            "owned_list_exists": True,
            "signup_form_live": True,
            "first_pillar_live": True,
            "copy_signed_off": True,
            "domain_warmup_complete": True,
            "first_sequence_sent": True,
        }

    def test_can_sell_false_when_infra_flags_missing(self):
        reg = self._registry(
            {"email": "pass", "social": "pass", "measurement": "pass"},
            infra={},  # no infra flags
        )
        summary = validate_connectors.compute(reg)
        self.assertFalse(summary["can_sell"])
        # The infra-driven gates must be the open items.
        self.assertIn("owned_list_captures", summary["phase5_open_items"])
        self.assertIn("one_pillar_live_with_engagement", summary["phase5_open_items"])
        self.assertIn("cold_outbound_warm_and_sent", summary["phase5_open_items"])

    def test_can_sell_true_when_everything_passes(self):
        reg = self._registry(
            {"email": "pass", "social": "pass", "measurement": "pass"},
            infra=self._full_infra(),
        )
        summary = validate_connectors.compute(reg)
        self.assertTrue(summary["can_sell"])
        self.assertEqual(summary["phase5_open_items"], [])

    def test_phase5_gate_is_seven_booleans(self):
        reg = self._registry(
            {"email": "pass", "social": "fail", "measurement": "fallback"},
            infra=self._full_infra(),
        )
        gate = validate_connectors.compute(reg)["phase5_gate"]
        self.assertIsInstance(gate, dict)
        self.assertEqual(len(gate), 7)
        for k, v in gate.items():
            self.assertIsInstance(v, bool, k)

    def test_counts_reflect_statuses(self):
        reg = self._registry(
            {"email": "pass", "social": "fallback", "measurement": "fail",
             "keyword": "pass"},
            infra=self._full_infra(),
        )
        counts = validate_connectors.compute(reg)["counts"]
        self.assertEqual(counts.get("pass"), 2)
        self.assertEqual(counts.get("fallback"), 1)
        self.assertEqual(counts.get("fail"), 1)
        self.assertEqual(sum(counts.values()), len(reg["connectors"]))

    def test_email_or_social_gate_true_with_one_fallback(self):
        # email fails but social falls back -> publishing gate still true.
        reg = self._registry(
            {"email": "fail", "social": "fallback", "measurement": "pass"},
            infra=self._full_infra(),
        )
        gate = validate_connectors.compute(reg)["phase5_gate"]
        self.assertTrue(gate["email_or_social_publishes"])

    def test_email_or_social_gate_true_with_email_pass(self):
        reg = self._registry(
            {"email": "pass", "social": "fail", "measurement": "pass"},
            infra=self._full_infra(),
        )
        gate = validate_connectors.compute(reg)["phase5_gate"]
        self.assertTrue(gate["email_or_social_publishes"])

    def test_email_or_social_gate_false_when_both_fail(self):
        reg = self._registry(
            {"email": "fail", "social": "blocked", "measurement": "pass"},
            infra=self._full_infra(),
        )
        gate = validate_connectors.compute(reg)["phase5_gate"]
        self.assertFalse(gate["email_or_social_publishes"])

    def test_measurement_gate_requires_pass(self):
        # fallback measurement is NOT enough for the measurement gate.
        reg = self._registry(
            {"email": "pass", "social": "pass", "measurement": "fallback"},
            infra=self._full_infra(),
        )
        summary = validate_connectors.compute(reg)
        self.assertFalse(summary["phase5_gate"]["measurement_real_numbers"])
        self.assertFalse(summary["can_sell"])
        self.assertIn("measurement_real_numbers", summary["phase5_open_items"])

    def test_by_status_groups_ids(self):
        reg = self._registry(
            {"email": "pass", "social": "pass", "measurement": "fail"},
            infra=self._full_infra(),
        )
        by = validate_connectors.compute(reg)["by_status"]
        self.assertEqual(sorted(by.get("pass", [])), ["email", "social"])
        self.assertEqual(by.get("fail"), ["measurement"])


if __name__ == "__main__":
    unittest.main()

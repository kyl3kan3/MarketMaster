import os, sys, unittest
SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "distribution-engine", "scripts"))
sys.path.insert(0, SCRIPTS)

from lib import common as c
import diagnose


STRONG_PILLAR = """# 7 Tactics That Doubled Our Conversion Rate

3 experiments changed everything for our team last quarter.

## Why most landing pages fail

Most pages bury the offer below the fold. We measured 42 sessions and found
that 68% of visitors never scrolled past the hero. That is a lot of wasted
intent. The fix was structural, not cosmetic.

- Lead with the outcome, not the feature
- Put the form above the fold
- Cut the hero copy to one sentence

## The numbers that mattered

Our conversion rate moved from 2.1% to 4.3% in 30 days. Revenue per visitor
climbed 47%. These are not vanity metrics.

## What to do next

Run the same audit on your own funnel this week. If you want the full
checklist, subscribe to the newsletter and we will send the template.

Read more at https://example.com/guide for the deep dive.
"""

WEAK_BLURB = "In this post we are going to talk a little bit about some stuff."


class TestDiagnoseShape(unittest.TestCase):
    def test_required_keys_present(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        for key in (
            "title", "word_count", "pillar_score", "headings", "findings",
            "atomization_opportunities", "quotable_lines", "score_breakdown",
        ):
            self.assertIn(key, d)

    def test_types(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        self.assertIsInstance(d["title"], str)
        self.assertIsInstance(d["word_count"], int)
        self.assertIsInstance(d["pillar_score"], int)
        self.assertIsInstance(d["headings"], list)
        self.assertIsInstance(d["findings"], list)
        self.assertIsInstance(d["atomization_opportunities"], list)
        self.assertIsInstance(d["quotable_lines"], list)
        self.assertIsInstance(d["score_breakdown"], dict)


class TestPillarScore(unittest.TestCase):
    def test_strong_beats_weak(self):
        strong = diagnose.diagnose(STRONG_PILLAR)
        weak = diagnose.diagnose(WEAK_BLURB)
        self.assertGreater(strong["pillar_score"], weak["pillar_score"])

    def test_strong_is_substantially_higher(self):
        # Not just barely higher: the strong pillar should clear a real margin.
        strong = diagnose.diagnose(STRONG_PILLAR)
        weak = diagnose.diagnose(WEAK_BLURB)
        self.assertGreaterEqual(strong["pillar_score"] - weak["pillar_score"], 30)

    def test_score_within_bounds(self):
        for text in (STRONG_PILLAR, WEAK_BLURB, "", "a", "#" * 5,
                     "1234567890 " * 200, "subscribe " * 500):
            d = diagnose.diagnose(text)
            self.assertGreaterEqual(d["pillar_score"], 0)
            self.assertLessEqual(d["pillar_score"], 100)
            self.assertIsInstance(d["pillar_score"], int)

    def test_breakdown_sums_consistent_with_score(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        total = sum(d["score_breakdown"].values())
        self.assertEqual(d["pillar_score"], max(0, min(100, total)))


class TestCTA(unittest.TestCase):
    def test_cta_present_true_when_term_present(self):
        d = diagnose.diagnose("Please subscribe to our newsletter today.")
        self.assertTrue(d["cta_present"])
        self.assertEqual(d["score_breakdown"]["cta"], 15)

    def test_cta_present_false_when_absent(self):
        d = diagnose.diagnose("Here is a plain paragraph with no call to action.")
        self.assertFalse(d["cta_present"])
        self.assertEqual(d["score_breakdown"]["cta"], 0)

    def test_strong_pillar_has_cta(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        self.assertTrue(d["cta_present"])


class TestHasData(unittest.TestCase):
    def test_has_data_true_with_digits(self):
        d = diagnose.diagnose("We saw a 42% lift in signups.")
        self.assertTrue(d["has_data"])

    def test_has_data_false_without_digits(self):
        d = diagnose.diagnose("We saw a big lift in signups, no numbers here.")
        self.assertFalse(d["has_data"])


class TestStructureAndFindings(unittest.TestCase):
    def test_headings_extracted(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        texts = [h["text"] for h in d["headings"]]
        self.assertIn("Why most landing pages fail", texts)
        self.assertTrue(any(h["level"] == 1 for h in d["headings"]))
        self.assertTrue(any(h["level"] == 2 for h in d["headings"]))

    def test_title_from_h1(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        self.assertEqual(d["title"], "7 Tactics That Doubled Our Conversion Rate")

    def test_weak_blurb_findings_flag_problems(self):
        d = diagnose.diagnose(WEAK_BLURB)
        joined = " ".join(d["findings"]).lower()
        self.assertIn("cta", joined)
        self.assertTrue(any("structure" in f.lower() for f in d["findings"]))

    def test_clean_pillar_atomization_opportunities(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        # H2 sections should become atomization opportunities.
        self.assertTrue(any("Why most landing pages fail" in o
                            for o in d["atomization_opportunities"]))


class TestRenderMd(unittest.TestCase):
    def test_returns_string_with_title(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        md = diagnose.render_md(d)
        self.assertIsInstance(md, str)
        self.assertIn(d["title"], md)

    def test_contains_score(self):
        d = diagnose.diagnose(STRONG_PILLAR)
        md = diagnose.render_md(d)
        self.assertIn(f"{d['pillar_score']}/100", md)


if __name__ == "__main__":
    unittest.main()

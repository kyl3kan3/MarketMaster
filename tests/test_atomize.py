import os, sys, unittest
SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "distribution-engine", "scripts"))
sys.path.insert(0, SCRIPTS)

import atomize


PILLAR = """# The 5 Distribution Mistakes Killing Your Growth

Most founders never distribute their content the right way. Here's the
truth about reach.

## Mistake One: Posting Once
The biggest mistake is publishing once and moving on. Nobody sees a single
post. You always need to atomize every pillar into many channel atoms.

## Mistake Two: Ignoring The Hook
The best posts start with a strong hook. Stop burying your point at the
bottom. Start every post with the punchline.

## Mistake Three: No Funnel
The fastest way to grow is to send every reader to one signup page. Most
creators forget the call to action entirely.
"""

SIGNUP = "https://example.com/join-now"

EXPECTED_CHANNELS = {"linkedin", "x", "email", "carousel", "short_video"}


class AtomizeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = atomize.atomize(PILLAR, SIGNUP)

    def test_top_level_shape(self):
        r = self.result
        self.assertIsInstance(r, dict)
        self.assertEqual(r["pillar_title"], "The 5 Distribution Mistakes Killing Your Growth")
        self.assertEqual(r["slug"], "the-5-distribution-mistakes-killing-your-growth")
        self.assertEqual(r["signup_url"], SIGNUP)

    def test_asset_count_matches_assets(self):
        r = self.result
        self.assertEqual(r["asset_count"], len(r["assets"]))
        self.assertGreater(r["asset_count"], 0)

    def test_channels_cover_required_set(self):
        channels = {a["channel"] for a in self.result["assets"]}
        self.assertTrue(
            EXPECTED_CHANNELS.issubset(channels),
            f"missing channels: {EXPECTED_CHANNELS - channels}",
        )

    def test_at_least_one_needs_human(self):
        flags = [a.get("needs_human") for a in self.result["assets"]]
        self.assertIn(True, flags)

    def test_voice_marker_in_linkedin_body(self):
        li = next(a for a in self.result["assets"] if a["channel"] == "linkedin")
        self.assertIn("[VOICE", li["body"])
        self.assertTrue(li["needs_human"])

    def test_every_asset_carries_signup_link(self):
        for a in self.result["assets"]:
            self.assertEqual(a["link"], SIGNUP, f"{a['id']} link mismatch")

    def test_default_signup_url(self):
        r = atomize.atomize(PILLAR)
        self.assertEqual(r["signup_url"], atomize.DEFAULT_SIGNUP)
        for a in r["assets"]:
            self.assertEqual(a["link"], atomize.DEFAULT_SIGNUP)

    def test_render_md_mentions_title(self):
        md = atomize.render_md(self.result)
        self.assertIsInstance(md, str)
        self.assertIn(self.result["pillar_title"], md)
        # the signup url and at least one asset title should surface too
        self.assertIn(SIGNUP, md)


if __name__ == "__main__":
    unittest.main()

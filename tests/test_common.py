import os, sys, unittest
SCRIPTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills", "distribution-engine", "scripts"))
sys.path.insert(0, SCRIPTS)

from lib import common as c


class TestSlugify(unittest.TestCase):
    def test_basic_lowercase_and_hyphens(self):
        self.assertEqual(c.slugify("Hello World"), "hello-world")

    def test_strips_punctuation_and_edges(self):
        self.assertEqual(c.slugify("  The Quick, Brown Fox!  "), "the-quick-brown-fox")

    def test_collapses_multiple_separators(self):
        self.assertEqual(c.slugify("a---b___c"), "a-b-c")

    def test_empty_falls_back_to_pillar(self):
        self.assertEqual(c.slugify("!!!"), "pillar")
        self.assertEqual(c.slugify(""), "pillar")

    def test_truncates_to_60_chars(self):
        out = c.slugify("x" * 100)
        self.assertEqual(len(out), 60)
        self.assertEqual(out, "x" * 60)


class TestTitleAndH1(unittest.TestCase):
    def test_first_h1_returns_text(self):
        self.assertEqual(c.first_h1("# My Title\n\nbody"), "My Title")

    def test_first_h1_ignores_h2(self):
        self.assertEqual(c.first_h1("## Sub\n\n# Real\n"), "Real")

    def test_first_h1_none_when_absent(self):
        self.assertIsNone(c.first_h1("no headings here"))

    def test_title_of_uses_h1(self):
        self.assertEqual(c.title_of("# Pillar Title\nrest"), "Pillar Title")

    def test_title_of_first_nonblank_line_when_no_h1(self):
        self.assertEqual(c.title_of("\n\n  Plain first line\nmore"), "Plain first line")

    def test_title_of_fallback_when_blank(self):
        self.assertEqual(c.title_of("   \n\n  ", fallback="None Found"), "None Found")


class TestHeadings(unittest.TestCase):
    def test_headings_levels_and_text(self):
        md = "# One\n\n## Two\n\n### Three\n"
        self.assertEqual(
            c.headings(md),
            [
                {"level": 1, "text": "One"},
                {"level": 2, "text": "Two"},
                {"level": 3, "text": "Three"},
            ],
        )

    def test_headings_empty(self):
        self.assertEqual(c.headings("just text, no headings"), [])


class TestWords(unittest.TestCase):
    def test_words_splits_on_non_word(self):
        self.assertEqual(c.words("Hello, world! 123"), ["Hello", "world", "123"])

    def test_words_keeps_apostrophes(self):
        self.assertEqual(c.words("don't stop"), ["don't", "stop"])


class TestSentences(unittest.TestCase):
    def test_sentences_splits_on_terminators(self):
        out = c.sentences("First one. Second one! Third one?")
        self.assertEqual(out, ["First one.", "Second one!", "Third one?"])

    def test_sentences_empty_text(self):
        self.assertEqual(c.sentences("   \n  "), [])

    def test_sentences_no_split_on_lowercase_follow(self):
        # split only when followed by uppercase/digit
        out = c.sentences("Mr. smith went home.")
        self.assertEqual(out, ["Mr. smith went home."])


class TestParagraphs(unittest.TestCase):
    def test_paragraphs_split_on_blank_lines(self):
        out = c.paragraphs("Para one.\n\nPara two.\n\n\nPara three.")
        self.assertEqual(out, ["Para one.", "Para two.", "Para three."])

    def test_paragraphs_strips_markdown_headings(self):
        out = c.paragraphs("# Heading\n\nBody text here.")
        self.assertEqual(out, ["Heading", "Body text here."])


class TestLinks(unittest.TestCase):
    def test_markdown_link_extracts_url(self):
        self.assertEqual(
            c.links("see [docs](https://example.com/docs) now"),
            ["https://example.com/docs"],
        )

    def test_bare_url_extracted(self):
        self.assertEqual(
            c.links("visit https://bare.example.org for more"),
            ["https://bare.example.org"],
        )

    def test_dedupes_preserving_order(self):
        text = (
            "[a](https://one.com) and https://two.com and "
            "https://one.com again and https://two.com"
        )
        self.assertEqual(c.links(text), ["https://one.com", "https://two.com"])

    def test_no_links(self):
        self.assertEqual(c.links("plain text without urls"), [])


class TestKeywords(unittest.TestCase):
    def test_drops_stopwords_and_short_words(self):
        # "the", "is", "of", "and" are stopwords; "is" also < 4 chars
        text = "Marketing marketing marketing the the strategy strategy growth"
        kw = c.keywords(text, limit=8)
        self.assertNotIn("the", kw)
        self.assertEqual(kw[0], "marketing")  # most frequent first
        self.assertIn("strategy", kw)
        self.assertIn("growth", kw)

    def test_respects_limit(self):
        text = "alpha bravo charlie delta echo foxtrot golf hotel india"
        self.assertEqual(len(c.keywords(text, limit=3)), 3)

    def test_short_words_excluded(self):
        # "cat" is 3 chars -> excluded even though repeated
        self.assertNotIn("cat", c.keywords("cat cat cat doggo doggo"))


class TestHashtags(unittest.TestCase):
    def test_hashtags_prefix_and_strip(self):
        tags = c.hashtags("Growth growth growth marketing marketing", n=2)
        self.assertTrue(all(t.startswith("#") for t in tags))
        self.assertIn("#growth", tags)

    def test_hashtags_count(self):
        text = "alpha alpha bravo bravo charlie charlie delta delta"
        self.assertEqual(len(c.hashtags(text, n=2)), 2)


class TestUtm(unittest.TestCase):
    def test_adds_question_mark_when_no_query(self):
        out = c.utm("https://x.com/page", "twitter", "social", "launch")
        self.assertEqual(
            out,
            "https://x.com/page?utm_source=twitter&utm_medium=social&utm_campaign=launch",
        )

    def test_uses_ampersand_when_query_exists(self):
        out = c.utm("https://x.com/page?a=1", "li", "social", "c1")
        self.assertTrue(out.startswith("https://x.com/page?a=1&utm_source=li"))
        self.assertIn("&utm_medium=social", out)
        self.assertIn("&utm_campaign=c1", out)

    def test_all_three_params_present(self):
        out = c.utm("https://x.com", "s", "m", "c")
        self.assertIn("utm_source=s", out)
        self.assertIn("utm_medium=m", out)
        self.assertIn("utm_campaign=c", out)


class TestQuotables(unittest.TestCase):
    def test_returns_punchy_strong_lines(self):
        text = (
            "You should always start now. "
            "This boring filler sentence is here for padding only. "
            "Stop wasting time today."
        )
        q = c.quotables(text)
        self.assertIn("You should always start now.", q)
        self.assertIn("Stop wasting time today.", q)

    def test_filters_too_short_sentences(self):
        # "Go now." is < 4 words -> excluded
        text = "Go now. You should always begin right here today friend."
        q = c.quotables(text)
        self.assertNotIn("Go now.", q)

    def test_excludes_sentences_without_score(self):
        # plain neutral sentence with no strong word / digit, but in length range
        # length range gives +1 so it would be included; use a long one (>30 words) to drop
        long_sent = " ".join(["word"] * 35) + "."
        text = "Bland statement with nothing special inside of it at all here. " + long_sent
        q = c.quotables(text)
        self.assertNotIn(long_sent, q)

    def test_respects_limit(self):
        sents = " ".join(
            f"Strong claim number {i} is always the best thing." for i in range(20)
        )
        self.assertLessEqual(len(c.quotables(sents, limit=5)), 5)

    def test_strong_numeric_lines_rank_high(self):
        text = (
            "We grew revenue by 80% in one quarter flat. "
            "Just a calm ordinary little remark sitting around here doing nothing much."
        )
        q = c.quotables(text)
        self.assertEqual(q[0], "We grew revenue by 80% in one quarter flat.")


class TestStripMarkdown(unittest.TestCase):
    def test_strips_heading_hashes(self):
        self.assertEqual(c.strip_markdown("# Title").strip(), "Title")

    def test_link_becomes_text(self):
        out = c.strip_markdown("see [click here](https://x.com) ok")
        self.assertIn("click here", out)
        self.assertNotIn("https://x.com", out)
        self.assertNotIn("[", out)

    def test_strips_emphasis_chars(self):
        out = c.strip_markdown("**bold** and _italic_ and `code`")
        self.assertNotIn("*", out)
        self.assertNotIn("_", out)
        self.assertNotIn("`", out)
        self.assertIn("bold", out)
        self.assertIn("italic", out)

    def test_removes_frontmatter(self):
        text = "---\ntitle: x\nfoo: bar\n---\nReal body content."
        out = c.strip_markdown(text)
        self.assertNotIn("title: x", out)
        self.assertIn("Real body content.", out)


if __name__ == "__main__":
    unittest.main()

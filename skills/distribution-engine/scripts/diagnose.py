#!/usr/bin/env python3
"""Mode 1 — DIAGNOSE.

Read a real piece of content (a "pillar") and score it for distribution
readiness: structure, hook, CTA, scannability, and where it can be atomized.
The engine does the mechanics; voice and judgment stay with the human.

Usage:
    python3 diagnose.py PILLAR.md [--out OUTDIR]

Outputs (in OUTDIR, default ./out):
    diagnose.json   machine-readable diagnostics (fed to atomize.py)
    diagnose.md     human-readable report
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path

from lib import common as c

WEAK_OPENERS = ("in this", "in today's", "as a", "we are", "i am", "this is a",
                "have you ever", "let me", "welcome")
CTA_TERMS = ("subscribe", "sign up", "signup", "join", "download", "book a",
             "get the", "grab the", "learn more", "read more", "link in",
             "register", "newsletter", "free guide", "waitlist")


def _hook(text: str) -> dict:
    sents = c.sentences(text)
    first = sents[0] if sents else ""
    wc = len(c.words(first))
    lower = first.lower()
    weak = any(lower.startswith(w) for w in WEAK_OPENERS)
    strong = (
        first.endswith("?")
        or any(ch.isdigit() for ch in first)
        or lower.startswith(("how ", "why ", "what ", "stop", "the secret",
                             "nobody", "most "))
    )
    score = 2
    if strong:
        score += 2
    if weak:
        score -= 2
    if wc > 25:
        score -= 1
    return {
        "first_sentence": first,
        "word_count": wc,
        "looks_weak": weak,
        "looks_strong": strong,
        "score_0_5": max(0, min(5, score + 1)),
    }


def _scannability(text: str) -> dict:
    sents = c.sentences(text)
    paras = c.paragraphs(text)
    avg_sent = (sum(len(c.words(s)) for s in sents) / len(sents)) if sents else 0
    long_sents = [s for s in sents if len(c.words(s)) > 25]
    long_paras = [p for p in paras if len(c.sentences(p)) > 5]
    bullets = sum(
        1 for ln in text.splitlines() if ln.lstrip().startswith(("-", "*", "•"))
    )
    return {
        "avg_sentence_words": round(avg_sent, 1),
        "long_sentences": len(long_sents),
        "long_paragraphs": len(long_paras),
        "bullet_lines": bullets,
        "paragraph_count": len(paras),
    }


def diagnose(text: str) -> dict:
    wds = c.words(c.strip_markdown(text))
    wc = len(wds)
    hs = c.headings(text)
    lks = c.links(text)
    lower = text.lower()
    cta_present = any(t in lower for t in CTA_TERMS)
    has_data = any(ch.isdigit() for ch in text)
    hook = _hook(text)
    scan = _scannability(text)
    quotable = c.quotables(text)

    # Pillar-readiness score (0-100), transparent and weighted.
    parts = {
        "length": min(20, int(wc / 40)),            # ~800 words -> full 20
        "structure": min(20, len(hs) * 4),          # 5+ headings -> full
        "hook": hook["score_0_5"] * 3,              # up to 15
        "cta": 15 if cta_present else 0,
        "evidence": (10 if has_data else 0) + min(5, len(lks) * 2),
        "scannability": 15
        - min(15, scan["long_sentences"] + scan["long_paragraphs"] * 2),
    }
    score = max(0, min(100, sum(parts.values())))

    opportunities = []
    for h in hs:
        if h["level"] in (2, 3):
            opportunities.append(f"Section '{h['text']}' -> 1 social post + 1 carousel slide")
    if quotable:
        opportunities.append(f"{len(quotable)} quotable lines -> X/LinkedIn one-liners")
    if wc > 600:
        opportunities.append("Long enough to spin a short-form video script + email teaser")

    findings = []
    if hook["looks_weak"]:
        findings.append("Opening line is generic — rewrite as a hook (question / number / bold claim).")
    if not cta_present:
        findings.append("No clear CTA — add a funnel to the signup form.")
    if not has_data:
        findings.append("No numbers/data — add proof points; they travel well as atoms.")
    if scan["long_paragraphs"]:
        findings.append(f"{scan['long_paragraphs']} dense paragraph(s) — break up for scannability.")
    if len(hs) < 3:
        findings.append("Thin structure — add headings so sections become atomizable units.")
    if not findings:
        findings.append("Clean. Proceed to atomize.")

    return {
        "title": c.title_of(text),
        "slug": c.slugify(c.title_of(text)),
        "word_count": wc,
        "reading_minutes": max(1, math.ceil(wc / 200)),
        "headings": hs,
        "links": lks,
        "cta_present": cta_present,
        "has_data": has_data,
        "hook": hook,
        "scannability": scan,
        "keywords": c.keywords(text),
        "quotable_lines": quotable,
        "atomization_opportunities": opportunities,
        "pillar_score": score,
        "score_breakdown": parts,
        "findings": findings,
    }


def render_md(d: dict) -> str:
    lines = [
        f"# Diagnose — {d['title']}",
        "",
        f"**Pillar-readiness score: {d['pillar_score']}/100**",
        "",
        f"- Words: {d['word_count']}  ·  Reading time: ~{d['reading_minutes']} min",
        f"- Headings: {len(d['headings'])}  ·  Links: {len(d['links'])}  "
        f"·  CTA present: {'yes' if d['cta_present'] else 'NO'}  "
        f"·  Has data: {'yes' if d['has_data'] else 'NO'}",
        f"- Hook score: {d['hook']['score_0_5']}/5  "
        f"·  Avg sentence: {d['scannability']['avg_sentence_words']} words",
        "",
        "## Score breakdown",
    ]
    for k, v in d["score_breakdown"].items():
        lines.append(f"- {k}: {v}")
    lines += ["", "## Findings (fix before/while atomizing)"]
    lines += [f"- {f}" for f in d["findings"]]
    lines += ["", "## Atomization opportunities"]
    lines += [f"- {o}" for o in d["atomization_opportunities"]]
    if d["quotable_lines"]:
        lines += ["", "## Quotable lines (raw material for atoms)"]
        lines += [f"- \"{q}\"" for q in d["quotable_lines"][:8]]
    lines += ["", "_The engine flags structure; you supply the voice._", ""]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Diagnose a content pillar.")
    ap.add_argument("pillar", help="Path to the content file (.md/.txt)")
    ap.add_argument("--out", default="out", help="Output directory")
    args = ap.parse_args(argv)

    text = c.read_text(args.pillar)
    d = diagnose(text)
    outdir = Path(args.out)
    c.write_json(outdir / "diagnose.json", d)
    c.write_text(outdir / "diagnose.md", render_md(d))
    print(c.banner(f"DIAGNOSE  ·  {d['title']}  ·  {d['pillar_score']}/100"))
    for f in d["findings"]:
        print(f"  - {f}")
    print(f"  -> {outdir/'diagnose.json'}\n  -> {outdir/'diagnose.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

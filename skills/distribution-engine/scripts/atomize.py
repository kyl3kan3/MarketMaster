#!/usr/bin/env python3
"""Mode 2 — ATOMIZE.

Break one pillar into channel-ready atoms: LinkedIn post, X thread + singles,
an email teaser, a Canva carousel outline, and a Higgsfield short-form script.

The engine builds the *structure* of each atom and marks `[VOICE]` slots and a
`needs_human` flag where your hook/voice/judgment must land. Nothing here
fabricates a finished, on-voice post — that is deliberate.

Usage:
    python3 atomize.py PILLAR.md [--out OUTDIR] [--signup-url URL]

Outputs:
    assets.json     structured atoms (fed to schedule.py and the connectors)
    atomized.md     human-readable pack
"""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from lib import common as c

DEFAULT_SIGNUP = "https://YOURDOMAIN.com/signup"


def _section_points(text: str) -> list[tuple[str, str]]:
    """Return (heading, first-paragraph) pairs for H2/H3 sections."""
    out = []
    hs = c.headings(text)
    lines = text.splitlines()
    # crude: pair each H2/H3 with the next non-empty paragraph below it
    idx = {h["text"]: i for i, ln in enumerate(lines)
           for h in hs if ln.strip().endswith(h["text"])}
    for h in hs:
        if h["level"] not in (2, 3):
            continue
        start = idx.get(h["text"], 0) + 1
        buf = []
        for ln in lines[start:]:
            if ln.startswith("#"):
                break
            if ln.strip():
                buf.append(ln.strip())
            elif buf:
                break
        out.append((h["text"], c.strip_markdown(" ".join(buf))[:280]))
    return out


def atomize(text: str, signup_url: str = DEFAULT_SIGNUP) -> dict:
    title = c.title_of(text)
    slug = c.slugify(title)
    quote = c.quotables(text)
    tags = c.hashtags(text, 4)
    sections = _section_points(text)
    hook = quote[0] if quote else title
    assets: list[dict] = []

    # 1) LinkedIn post -------------------------------------------------------
    body_pts = [f"- {q}" for q in quote[1:4]] or [f"- {s}" for s in (
        sections[0][1].split(". ")[:3] if sections else [])]
    assets.append({
        "id": f"{slug}-li",
        "channel": "linkedin",
        "type": "post",
        "title": f"LinkedIn: {title}",
        "hook": hook,
        "body": "\n".join([
            f"{hook}",
            "",
            "[VOICE: one line of personal context — why this matters to you]",
            "",
            *body_pts,
            "",
            "[VOICE: the one takeaway you want them to remember]",
        ]),
        "hashtags": tags,
        "link": signup_url,
        "link_placement": "first comment (LinkedIn deprioritizes in-post links)",
        "needs_human": True,
    })

    # 2) X thread ------------------------------------------------------------
    thread = [hook + " 🧵"]
    for q in quote[1:6]:
        thread.append(textwrap.shorten(q, width=270, placeholder="…"))
    thread.append(f"If this helped, the full breakdown + more: {signup_url}")
    assets.append({
        "id": f"{slug}-x-thread",
        "channel": "x",
        "type": "thread",
        "title": f"X thread: {title}",
        "tweets": thread,
        "link": signup_url,
        "needs_human": True,
    })

    # 3) X singles -----------------------------------------------------------
    for i, q in enumerate(quote[:3], 1):
        assets.append({
            "id": f"{slug}-x-{i}",
            "channel": "x",
            "type": "single",
            "title": f"X single #{i}",
            "body": textwrap.shorten(q, width=240, placeholder="…"),
            "link": signup_url,
            "needs_human": True,
        })

    # 4) Email teaser --------------------------------------------------------
    assets.append({
        "id": f"{slug}-email",
        "channel": "email",
        "type": "newsletter",
        "title": f"Email: {title}",
        "subject": textwrap.shorten(title, width=60, placeholder="…"),
        "preview": (quote[0] if quote else title)[:90],
        "body": "\n".join([
            f"## {title}",
            "",
            "[VOICE: a 2-3 sentence personal intro in your voice]",
            "",
            "Here's the short version:",
            *[f"- {q}" for q in quote[:4]],
            "",
            f"Read / watch the full thing and join the list: {signup_url}",
        ]),
        "link": signup_url,
        "needs_human": True,
    })

    # 5) Canva carousel outline ---------------------------------------------
    slides = [{"n": 1, "role": "hook", "text": hook}]
    pool = quote[1:] or [s[0] for s in sections]
    for i, q in enumerate(pool[:7], 2):
        slides.append({"n": i, "role": "point", "text": textwrap.shorten(
            q, width=120, placeholder="…")})
    slides.append({"n": len(slides) + 1, "role": "cta",
                   "text": f"Want more? Join the list → {signup_url}"})
    assets.append({
        "id": f"{slug}-carousel",
        "channel": "carousel",
        "type": "canva",
        "title": f"Carousel: {title}",
        "slides": slides,
        "link": signup_url,
        "produce_with": "references/design-canva.md",
        "needs_human": False,
    })

    # 6) Higgsfield short-form script ---------------------------------------
    beats = quote[1:4] or [s[1][:80] for s in sections[:3]]
    assets.append({
        "id": f"{slug}-short",
        "channel": "short_video",
        "type": "higgsfield",
        "title": f"Short video: {title}",
        "script": {
            "hook_0_2s": hook,
            "beats": [textwrap.shorten(b, width=120, placeholder="…") for b in beats],
            "cta": f"Follow + join the list: {signup_url}",
            "aspect": "9:16",
            "captions": "burn-in (most viewing is muted)",
        },
        "link": signup_url,
        "produce_with": "references/video-higgsfield.md",
        "needs_human": False,
    })

    return {
        "pillar_title": title,
        "slug": slug,
        "signup_url": signup_url,
        "hashtags": tags,
        "asset_count": len(assets),
        "assets": assets,
    }


def render_md(a: dict) -> str:
    out = [f"# Atomized pack — {a['pillar_title']}", "",
           f"Signup funnel: `{a['signup_url']}`  ·  {a['asset_count']} atoms",
           "", "> `[VOICE]` markers are where your hook/voice must land. "
           "The engine made the frame; you finish it.", ""]
    for at in a["assets"]:
        out.append(f"## {at['title']}  `({at['channel']}/{at['type']})`")
        if "body" in at:
            out += ["", "```", at["body"], "```"]
        if "tweets" in at:
            out += [""] + [f"{i+1}. {t}" for i, t in enumerate(at["tweets"])]
        if "slides" in at:
            out += [""] + [f"- Slide {s['n']} ({s['role']}): {s['text']}"
                           for s in at["slides"]]
        if "script" in at:
            s = at["script"]
            out += ["", f"- Hook (0-2s): {s['hook_0_2s']}"]
            out += [f"- Beat: {b}" for b in s["beats"]]
            out += [f"- CTA: {s['cta']}  ·  {s['aspect']}  ·  {s['captions']}"]
        if at.get("hashtags"):
            out.append("")
            out.append("Hashtags: " + " ".join(at["hashtags"]))
        out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Atomize a pillar into channel atoms.")
    ap.add_argument("pillar")
    ap.add_argument("--out", default="out")
    ap.add_argument("--signup-url", default=DEFAULT_SIGNUP)
    args = ap.parse_args(argv)

    text = c.read_text(args.pillar)
    a = atomize(text, args.signup_url)
    outdir = Path(args.out)
    c.write_json(outdir / "assets.json", a)
    c.write_text(outdir / "atomized.md", render_md(a))
    print(c.banner(f"ATOMIZE  ·  {a['pillar_title']}  ·  {a['asset_count']} atoms"))
    for at in a["assets"]:
        flag = "  (needs your voice)" if at.get("needs_human") else ""
        print(f"  - {at['channel']:<12} {at['type']:<11} {at['id']}{flag}")
    print(f"  -> {outdir/'assets.json'}\n  -> {outdir/'atomized.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Shared helpers for the Distribution Engine pipeline.

Stdlib only — no third-party dependencies — so the engine runs whether or not
Code Execution has network/package access. Every script imports from here.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# --- IO ---------------------------------------------------------------------

def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def write_text(path: str | Path, text: str) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def read_json(path: str | Path) -> dict:
    return json.loads(read_text(path))


def write_json(path: str | Path, data) -> Path:
    return write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def eprint(*args) -> None:
    print(*args, file=sys.stderr)


# --- Text utilities ---------------------------------------------------------

_FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.DOTALL)
_MD_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
_BARE_URL = re.compile(r"(?<!\()\bhttps?://[^\s)]+")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)
_WORD = re.compile(r"[A-Za-z0-9']+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9])")

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "then", "to", "of", "in", "on",
    "for", "with", "as", "at", "by", "from", "is", "are", "was", "were", "be",
    "been", "this", "that", "these", "those", "it", "its", "your", "you", "we",
    "our", "they", "their", "i", "me", "my", "so", "do", "how", "why", "what",
    "can", "will", "just", "not", "no", "yes", "more", "most", "than", "into",
}


def strip_markdown(text: str) -> str:
    """Rough plain-text view of markdown for counting/analysis."""
    text = _FRONTMATTER.sub("", text)
    text = _MD_LINK.sub(r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`>#]", "", text)
    return text


def first_h1(text: str) -> str | None:
    for m in _HEADING.finditer(text):
        if len(m.group(1)) == 1:
            return m.group(2).strip()
    return None


def title_of(text: str, fallback: str = "Untitled pillar") -> str:
    h1 = first_h1(text)
    if h1:
        return h1
    for line in text.splitlines():
        if line.strip():
            return strip_markdown(line).strip()[:120]
    return fallback


def headings(text: str) -> list[dict]:
    return [
        {"level": len(m.group(1)), "text": m.group(2).strip()}
        for m in _HEADING.finditer(text)
    ]


def words(text: str) -> list[str]:
    return _WORD.findall(text)


def sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", strip_markdown(text)).strip()
    if not flat:
        return []
    return [s.strip() for s in _SENT_SPLIT.split(flat) if s.strip()]


def paragraphs(text: str) -> list[str]:
    body = strip_markdown(text)
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


def links(text: str) -> list[str]:
    out = [m.group(2) for m in _MD_LINK.finditer(text)]
    out += _BARE_URL.findall(text)
    # de-dupe, preserve order
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def keywords(text: str, limit: int = 8) -> list[str]:
    counts: dict[str, int] = {}
    for w in words(text.lower()):
        if len(w) < 4 or w in STOPWORDS:
            continue
        counts[w] = counts.get(w, 0) + 1
    return [w for w, _ in sorted(counts.items(), key=lambda kv: -kv[1])][:limit]


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "pillar"


def hashtags(text: str, n: int = 4) -> list[str]:
    return ["#" + re.sub(r"[^a-z0-9]", "", k) for k in keywords(text, n)]


# --- Links / UTM ------------------------------------------------------------

def utm(url: str, source: str, medium: str, campaign: str) -> str:
    sep = "&" if "?" in url else "?"
    return (
        f"{url}{sep}utm_source={source}&utm_medium={medium}"
        f"&utm_campaign={campaign}"
    )


# Quotable = short, punchy, ideally carries a number or a strong claim.
_STRONG = re.compile(
    r"\b(\d+%?|never|always|stop|start|most|every|nobody|everyone|"
    r"the secret|the truth|here's|biggest|fastest|worst|best)\b",
    re.IGNORECASE,
)


def quotables(text: str, limit: int = 12) -> list[str]:
    scored = []
    for s in sentences(text):
        wc = len(words(s))
        if wc < 4 or wc > 30:
            continue
        score = 0
        if _STRONG.search(s):
            score += 2
        if any(ch.isdigit() for ch in s):
            score += 1
        if 6 <= wc <= 18:
            score += 1
        if score:
            scored.append((score, s))
    scored.sort(key=lambda t: (-t[0], len(t[1])))
    return [s for _, s in scored[:limit]]


def banner(line: str) -> str:
    bar = "=" * max(8, len(line) + 4)
    return f"{bar}\n| {line}\n{bar}"

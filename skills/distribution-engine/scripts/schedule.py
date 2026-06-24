#!/usr/bin/env python3
"""Mode 4 — SCHEDULE.

Spread the atomized assets across a posting calendar, respecting a per-channel
cadence, and stamp every link with UTM tags so the Optimize loop (GA4) can read
results back. The engine produces the calendar; a human or a Zap executes it.

Usage:
    python3 schedule.py assets.json [--start YYYY-MM-DD] [--weeks N] [--out OUTDIR]

Outputs:
    schedule.json, schedule.csv, schedule.md
"""
from __future__ import annotations

import argparse
import csv
import io
from datetime import date, datetime, timedelta
from pathlib import Path

from lib import common as c

# posts per week + a default hour (local) per channel
CADENCE = {
    "linkedin": (2, "09:00"),
    "x": (5, "12:00"),
    "email": (1, "08:00"),
    "carousel": (1, "10:00"),
    "short_video": (2, "17:00"),
}
MEDIUM = {"linkedin": "social", "x": "social", "email": "email",
          "carousel": "social", "short_video": "social"}
# preferred weekdays per channel (Mon=0)
DOW = {"linkedin": [1, 3], "x": [0, 1, 2, 3, 4], "email": [2],
       "carousel": [3], "short_video": [1, 4]}


def _slots(channel: str, start: date, weeks: int) -> list[datetime]:
    per_week, hh = CADENCE.get(channel, (1, "09:00"))
    h, m = (int(x) for x in hh.split(":"))
    days = DOW.get(channel, [1, 3])[:per_week] or [1]
    out = []
    for w in range(weeks):
        wk_start = start + timedelta(days=7 * w)
        monday = wk_start - timedelta(days=wk_start.weekday())
        for d in days:
            day = monday + timedelta(days=d)
            if day >= start:
                out.append(datetime(day.year, day.month, day.day, h, m))
    return sorted(out)


def schedule(assets: dict, start: date, weeks: int) -> dict:
    campaign = assets.get("slug", "pillar")
    by_channel: dict[str, list[dict]] = {}
    for a in assets["assets"]:
        by_channel.setdefault(a["channel"], []).append(a)

    rows = []
    for channel, items in by_channel.items():
        slots = _slots(channel, start, weeks)
        for i, a in enumerate(items):
            when = slots[i % len(slots)] if slots else datetime(
                start.year, start.month, start.day, 9, 0)
            # stagger overflow into later weeks
            when += timedelta(days=7 * (i // max(1, len(slots))))
            link = c.utm(a.get("link", ""), channel, MEDIUM.get(channel, "social"),
                         campaign) if a.get("link") else ""
            rows.append({
                "datetime": when.isoformat(timespec="minutes"),
                "date": when.date().isoformat(),
                "time": when.strftime("%H:%M"),
                "channel": channel,
                "asset_id": a["id"],
                "type": a.get("type", ""),
                "title": a.get("title", ""),
                "link": link,
                "needs_human": a.get("needs_human", False),
                "status": "scheduled",
            })
    rows.sort(key=lambda r: r["datetime"])
    return {
        "pillar_title": assets.get("pillar_title"),
        "campaign": campaign,
        "start": start.isoformat(),
        "weeks": weeks,
        "count": len(rows),
        "items": rows,
    }


def to_csv(sch: dict) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["date", "time", "channel", "type", "asset_id", "title",
                "needs_human", "link", "status"])
    for r in sch["items"]:
        w.writerow([r["date"], r["time"], r["channel"], r["type"], r["asset_id"],
                    r["title"], r["needs_human"], r["link"], r["status"]])
    return buf.getvalue()


def to_md(sch: dict) -> str:
    out = [f"# Schedule — {sch['pillar_title']}", "",
           f"Campaign `{sch['campaign']}`  ·  {sch['count']} posts  "
           f"·  starts {sch['start']}  ·  {sch['weeks']} weeks", "",
           "| Date | Time | Channel | Asset | Voice? | Link |",
           "|---|---|---|---|---|---|"]
    for r in sch["items"]:
        voice = "✍️" if r["needs_human"] else ""
        link = "✓" if r["link"] else ""
        out.append(f"| {r['date']} | {r['time']} | {r['channel']} | "
                   f"{r['asset_id']} | {voice} | {link} |")
    out += ["", "_Execute via Zapier→Buffer, a Buffer queue, or manually "
            "(see references/social-linkedin-x.md). Email finishes in Mailchimp._", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Schedule atomized assets.")
    ap.add_argument("assets")
    ap.add_argument("--start", default=(date.today() + timedelta(days=1)).isoformat())
    ap.add_argument("--weeks", type=int, default=3)
    ap.add_argument("--out", default="out")
    args = ap.parse_args(argv)

    assets = c.read_json(args.assets)
    start = datetime.strptime(args.start, "%Y-%m-%d").date()
    sch = schedule(assets, start, args.weeks)
    outdir = Path(args.out)
    c.write_json(outdir / "schedule.json", sch)
    c.write_text(outdir / "schedule.csv", to_csv(sch))
    c.write_text(outdir / "schedule.md", to_md(sch))
    print(c.banner(f"SCHEDULE  ·  {sch['count']} posts over {sch['weeks']} weeks"))
    for r in sch["items"]:
        print(f"  {r['date']} {r['time']}  {r['channel']:<12} {r['asset_id']}")
    print(f"  -> {outdir/'schedule.csv'}\n  -> {outdir/'schedule.md'}"
          f"\n  -> {outdir/'schedule.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

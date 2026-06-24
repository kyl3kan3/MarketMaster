#!/usr/bin/env python3
"""Distribution Engine — CLI entry point.

Chains the four modes:  diagnose -> atomize -> validate -> schedule.

    python3 engine.py diagnose PILLAR.md
    python3 engine.py atomize  PILLAR.md --signup-url https://you.com/signup
    python3 engine.py validate
    python3 engine.py schedule out/assets.json --weeks 3
    python3 engine.py run      PILLAR.md --signup-url https://you.com/signup

`run` executes the whole chain and drops every artifact in --out (default ./out).
All modes are stdlib-only, so they work whether or not Code Execution is on; if
scripts can't run at all, follow the same steps by hand from SKILL.md.
"""
from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import atomize as m_atomize          # noqa: E402
import diagnose as m_diagnose        # noqa: E402
import schedule as m_schedule        # noqa: E402
import validate_connectors as m_validate  # noqa: E402
from lib import common as c          # noqa: E402


def cmd_run(args) -> int:
    out = args.out
    rc = m_diagnose.main([args.pillar, "--out", out])
    rc |= m_atomize.main([args.pillar, "--out", out, "--signup-url", args.signup_url])
    rc |= m_validate.main(["--out", out])
    start = (date.today() + timedelta(days=1)).isoformat()
    rc |= m_schedule.main([str(Path(out) / "assets.json"), "--out", out,
                           "--start", start, "--weeks", str(args.weeks)])
    print(c.banner("RUN COMPLETE"))
    print(f"  Artifacts in ./{out}: diagnose.* atomized.* assets.json "
          f"validation-report.md readiness.json schedule.*")
    print("  Next: finish [VOICE] slots, produce carousel/video via the "
          "connector playbooks, then execute the schedule.")
    return rc


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="engine", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="mode", required=True)

    p = sub.add_parser("diagnose"); p.add_argument("pillar"); p.add_argument("--out", default="out")
    p = sub.add_parser("atomize"); p.add_argument("pillar"); p.add_argument("--out", default="out")
    p.add_argument("--signup-url", default=m_atomize.DEFAULT_SIGNUP)
    p = sub.add_parser("validate"); p.add_argument("--out", default="out")
    p.add_argument("--registry", default=str(m_validate.DEFAULT_REGISTRY))
    p.add_argument("--set", action="append", default=[]); p.add_argument("--infra", action="append", default=[])
    p = sub.add_parser("schedule"); p.add_argument("assets"); p.add_argument("--out", default="out")
    p.add_argument("--start", default=(date.today() + timedelta(days=1)).isoformat())
    p.add_argument("--weeks", type=int, default=3)
    p = sub.add_parser("run"); p.add_argument("pillar"); p.add_argument("--out", default="out")
    p.add_argument("--signup-url", default=m_atomize.DEFAULT_SIGNUP); p.add_argument("--weeks", type=int, default=3)

    args = ap.parse_args(argv)
    if args.mode == "diagnose":
        return m_diagnose.main([args.pillar, "--out", args.out])
    if args.mode == "atomize":
        return m_atomize.main([args.pillar, "--out", args.out, "--signup-url", args.signup_url])
    if args.mode == "validate":
        a = ["--out", args.out, "--registry", args.registry]
        for s in args.set: a += ["--set", s]
        for s in args.infra: a += ["--infra", s]
        return m_validate.main(a)
    if args.mode == "schedule":
        return m_schedule.main([args.assets, "--out", args.out, "--start", args.start,
                                "--weeks", str(args.weeks)])
    if args.mode == "run":
        return cmd_run(args)
    ap.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Mode 3 — VALIDATE.

Read the connector registry (connectors.json) and report which distribution
paths are live, which fall back, and which are blocked — then compute the
Phase 5 "can-sell" readiness gate. A read-only or missing action is a finding,
not a failure: fallbacks count toward readiness; hard fails do not.

Usage:
    python3 validate_connectors.py [--registry connectors.json] [--out OUTDIR]
    python3 validate_connectors.py --set keyword=pass --set measurement=pass
    python3 validate_connectors.py --infra owned_list_exists=true

Outputs:
    validation-report.md
    readiness.json
"""
from __future__ import annotations

import argparse
from pathlib import Path

from lib import common as c

ICON = {"pass": "PASS ✅", "fallback": "FALLBACK 🟡", "fail": "FAIL ❌",
        "blocked": "BLOCKED ⛔", "held": "HELD ⏸"}
HERE = Path(__file__).resolve().parent
DEFAULT_REGISTRY = HERE / "connectors.json"


def _truthy(v: str) -> bool:
    return str(v).strip().lower() in ("1", "true", "yes", "y", "on")


def compute(reg: dict) -> dict:
    conns = reg["connectors"]
    infra = reg.get("infra", {})
    by = {x["status"]: [] for x in conns}
    for x in conns:
        by.setdefault(x["status"], []).append(x["id"])

    def st(cid):
        return next((x["status"] for x in conns if x["id"] == cid), "fail")

    # Phase 5 readiness gate (definition of done / can-sell).
    gate = {
        "skill_triggers_and_packages":  # the skill exists + runs the pipeline
            True,
        "email_or_social_publishes":
            st("email") in ("pass", "fallback") or st("social") in ("pass", "fallback"),
        "owned_list_captures":
            bool(infra.get("owned_list_exists")) and bool(infra.get("signup_form_live")),
        "one_pillar_live_with_engagement":
            bool(infra.get("first_pillar_live")),
        "copy_client_grade":
            bool(infra.get("copy_signed_off")),
        "measurement_real_numbers":
            st("measurement") == "pass",
        "cold_outbound_warm_and_sent":
            bool(infra.get("domain_warmup_complete")) and bool(infra.get("first_sequence_sent")),
    }
    can_sell = all(gate.values())
    return {
        "validated_on": reg.get("validated_on"),
        "counts": {k: len(v) for k, v in by.items() if v},
        "by_status": {k: v for k, v in by.items() if v},
        "phase5_gate": gate,
        "phase5_open_items": [k for k, v in gate.items() if not v],
        "can_sell": can_sell,
        "infra": infra,
    }


def render_md(reg: dict, summary: dict) -> str:
    out = [f"# Validate — connector readiness ({reg.get('validated_on')})", ""]
    out.append("| Connector | Status | Detail |")
    out.append("|---|---|---|")
    for x in reg["connectors"]:
        out.append(f"| {x['name']} | {ICON.get(x['status'], x['status'])} | {x['detail']} |")
    out += ["", "## Counts",
            "  ·  ".join(f"{k}: {v}" for k, v in summary["counts"].items()), ""]
    out += ["## Phase 5 — can-sell gate"]
    for k, v in summary["phase5_gate"].items():
        out.append(f"- [{'x' if v else ' '}] {k}")
    out += ["", f"**Can sell: {'YES ✅' if summary['can_sell'] else 'NOT YET'}**"]
    if summary["phase5_open_items"]:
        out += ["", "Open before selling:"]
        out += [f"- {i}" for i in summary["phase5_open_items"]]
    out += ["", "## Blockers needing the account owner"]
    for x in reg["connectors"]:
        if x["status"] in ("fail", "blocked") and x.get("blocker"):
            out.append(f"- **{x['name']}** — {x['blocker']}")
    out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate connectors + readiness gate.")
    ap.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    ap.add_argument("--out", default="out")
    ap.add_argument("--set", action="append", default=[], metavar="id=status",
                    help="Override a connector status (persists to the registry).")
    ap.add_argument("--infra", action="append", default=[], metavar="key=bool",
                    help="Set an infra flag (persists to the registry).")
    args = ap.parse_args(argv)

    reg = c.read_json(args.registry)
    changed = False
    for kv in args.set:
        cid, _, status = kv.partition("=")
        for x in reg["connectors"]:
            if x["id"] == cid:
                x["status"] = status
                changed = True
    for kv in args.infra:
        key, _, val = kv.partition("=")
        reg.setdefault("infra", {})[key] = _truthy(val)
        changed = True
    if changed:
        c.write_json(args.registry, reg)

    summary = compute(reg)
    outdir = Path(args.out)
    c.write_json(outdir / "readiness.json", summary)
    c.write_text(outdir / "validation-report.md", render_md(reg, summary))
    print(c.banner("VALIDATE  ·  connector readiness"))
    for x in reg["connectors"]:
        print(f"  {ICON.get(x['status'], x['status']):<12} {x['name']}")
    print(f"  Can sell: {'YES' if summary['can_sell'] else 'NOT YET'} "
          f"({len(summary['phase5_open_items'])} open)")
    print(f"  -> {outdir/'validation-report.md'}\n  -> {outdir/'readiness.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

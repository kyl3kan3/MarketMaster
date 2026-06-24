# MarketMaster — the Distribution Engine

Turn **one** piece of content into a **full multi-channel distribution package**
and push it live. MarketMaster is packaged as a Claude Code **skill** plus a
stdlib-only Python pipeline, so it runs whether or not Code Execution is enabled.

> Creation isn't the bottleneck anymore — distribution is. This engine does the
> mechanics; you supply the hooks, voice, and judgment.

**Going live?** Start with **[`GO-LIVE.md`](GO-LIVE.md)** — the master launch
checklist — plus the step-by-step guides in [`docs/`](docs/) (owned-audience
setup, GA4 AI-search channel, cold-email warmup, keyword brief).

## The four-mode engine

```
DIAGNOSE → ATOMIZE → VALIDATE → SCHEDULE → (Distribute) → (Optimize ↺)
```

| Mode | What it does |
|---|---|
| **Diagnose** | Scores a pillar for distribution-readiness and finds atomization points |
| **Atomize** | Splits it into LinkedIn / X / email / carousel / short-video atoms |
| **Validate** | Checks every connector (live / fallback / blocked) + the can-sell gate |
| **Schedule** | Lays atoms on a calendar with UTM-tagged links for measurement |

## Quick start

```bash
cd skills/distribution-engine/scripts

# full chain on a real pillar:
python3 engine.py run ../examples/sample-pillar.md \
    --signup-url https://YOURDOMAIN.com/signup --weeks 3

# or one mode at a time:
python3 engine.py diagnose ../examples/sample-pillar.md
python3 engine.py atomize  ../examples/sample-pillar.md --signup-url https://you.com/signup
python3 engine.py validate
python3 engine.py schedule out/assets.json --weeks 3
```

Outputs land in `scripts/out/`: `diagnose.*`, `atomized.*`, `assets.json`,
`validation-report.md`, `readiness.json`, `schedule.*`.

## Install as a skill

```bash
bash scripts/package_skill.sh      # → dist/distribution-engine.skill
```

Install via **Settings → Capabilities → Skills**, then trigger by intent —
say *"help me distribute this post"* (no need to name the skill).

## Layout

```
skills/distribution-engine/
├── SKILL.md                  # the engine brain (modes, routing, guardrails)
├── scripts/                  # runnable pipeline (stdlib only)
│   ├── engine.py             #   CLI: diagnose | atomize | validate | schedule | run
│   ├── diagnose.py atomize.py validate_connectors.py schedule.py
│   ├── lib/common.py         #   shared text/IO helpers
│   └── connectors.json       #   connector registry + live status
├── references/               # per-connector playbooks (exact MCP calls + fallbacks)
│   └── connectors.md email-mailchimp.md social-linkedin-x.md
│       keyword-ahrefs-semrush.md design-canva.md video-higgsfield.md
│       measurement-ga4.md outbound-apollo.md domain-warmup.md
├── assets/signup-form.html   # owned-audience capture (UTM-aware)
└── examples/sample-pillar.md # sample content to run the pipeline on
scripts/package_skill.sh      # build the installable .skill
validation-tracker.md         # phased go-live tracker + live connector status
```

## Connector status (validated 2026-06-23)

| Connector | Status |
|---|---|
| Higgsfield (video) · Canva (carousels) · Apollo (build) | ✅ live |
| Mailchimp (email) · LinkedIn/X (social) | 🟡 fallback (draft / manual) |
| Ahrefs · Semrush (keyword) · GA4 (measurement) | ❌ plan/auth blocked |
| Domain warmup | ⛔ not started (day-one item) |

See `validation-tracker.md` and `skills/distribution-engine/references/connectors.md`
for the full board and the owner-only unblockers.

## Guardrails
- Outward actions (sending, publishing, activating outreach) require explicit
  human go-ahead — drafts and **inactive** sequences are prepared freely.
- Apollo sequences are always created `active: false`; cold sends wait on a
  fully warmed domain (~4–6 weeks).
- Never ship the `[VOICE]` placeholders unedited — that's your half of the work.

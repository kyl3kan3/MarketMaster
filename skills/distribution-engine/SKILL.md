---
name: distribution-engine
description: >-
  Turn one piece of content into a full multi-channel distribution package and
  push it live. Use whenever someone wants to distribute, repurpose, atomize,
  amplify, or get more reach from a post, article, blog, newsletter, video,
  thread, or any "pillar" content — e.g. "help me distribute this post",
  "turn this into a week of content", "repurpose this", "get this in front of
  more people", "make social posts from this", "build a content schedule".
  Runs four modes — Diagnose, Atomize, Validate, Schedule — and routes assets to
  email (Mailchimp), social (LinkedIn/X), carousels (Canva), short video
  (Higgsfield), measurement (GA4/Supermetrics), and cold outbound (Apollo),
  each with a live path and a manual fallback. Funnels everything to an owned
  email list.
---

# Distribution Engine

One pillar → many atoms → live distribution → measured results. The engine does
the **mechanics and structure**; the human supplies **hooks, voice, and
judgment** — that division is deliberate and is what makes the output worth
paying for.

## When to fire
Trigger on any intent to get more out of existing content — "distribute this",
"repurpose", "atomize", "make this a thread/carousel/video", "build a posting
schedule", "amplify", "more reach" — even when this skill is not named. Skills
tend to under-trigger; lean toward firing when content + a distribution goal are
present.

## The pipeline (four modes + two wings)

```
            DIAGNOSE → ATOMIZE → VALIDATE → SCHEDULE
   (research)   ↑                              ↓   (execute)
            Optimize  ←———— GA4 numbers ———  Distribute
```

1. **Diagnose** — score the pillar for distribution-readiness (hook, structure,
   CTA, scannability) and find where it atomizes. Optional front-end research
   via Ahrefs/Semrush (currently plan-blocked → manual fallback).
2. **Atomize** — split the pillar into channel-native atoms: LinkedIn post, X
   thread + singles, email teaser, Canva carousel outline, Higgsfield short
   script. Each marks `[VOICE]` slots you must finish.
3. **Validate** — check every connector is live or has a documented fallback,
   and compute the Phase 5 "can-sell" gate. A read-only/missing action is a
   *finding*, not a failure.
4. **Schedule** — spread atoms across a calendar with per-channel cadence and
   UTM-tagged links so results read back into GA4.
5. **Distribute** (execute) — email draft (Mailchimp), social (Zapier/Buffer or
   manual), carousel (Canva), video (Higgsfield), cold outbound (Apollo,
   inactive until warm). Outward actions require explicit human go-ahead.
6. **Optimize** (loop) — pull real numbers from GA4 (incl. an "AI search"
   channel group) and feed winners back into the next Diagnose.

## How to run it

**If Code Execution is on** (scripts run) — from `scripts/`:

```bash
python3 engine.py run PILLAR.md --signup-url https://YOURDOMAIN.com/signup --weeks 3
# or one mode at a time:
python3 engine.py diagnose PILLAR.md
python3 engine.py atomize  PILLAR.md --signup-url https://YOURDOMAIN.com/signup
python3 engine.py validate                 # reads connectors.json
python3 engine.py schedule out/assets.json --weeks 3
```

Artifacts land in `./out/`: `diagnose.*`, `atomized.*`, `assets.json`,
`validation-report.md`, `readiness.json`, `schedule.*`. Scripts are stdlib-only,
so they run anywhere Python 3 exists.

**If Code Execution is off** (manual fallback) — do the same steps by hand: read
the pillar, write the atoms using the structures in `examples/`/`atomized.md`,
fill the connector matrix from the playbooks, and lay out the calendar. The
manual path is acceptable and produces the same artifacts.

## Connector routing → playbooks

| Need | Connector | Status (2026-06-23) | Playbook |
|---|---|---|---|
| Email | Mailchimp (Gmail fallback) | 🟡 fallback (no MCP send) | `references/email-mailchimp.md` |
| Social | LinkedIn / X | 🟡 fallback (manual/Zapier) | `references/social-linkedin-x.md` |
| Keyword + AI-citation | Ahrefs / Semrush | ❌ plan-blocked | `references/keyword-ahrefs-semrush.md` |
| Carousels | Canva | ✅ pass (no brand kit yet) | `references/design-canva.md` |
| Short video | Higgsfield | ✅ pass (Ultra, ~2k credits) | `references/video-higgsfield.md` |
| Measurement | Supermetrics / GA4 | ❌ needs login | `references/measurement-ga4.md` |
| Cold outbound | Apollo | ✅ build only (warm-gated) | `references/outbound-apollo.md` |
| Warmup | (process) | ⛔ not started | `references/domain-warmup.md` |

Always read the connector's playbook before executing it — each carries the
exact MCP tool calls and the live-vs-fallback decision.

## Guardrails (do not skip)
- **Outward actions need explicit go-ahead.** Sending email, publishing a post,
  or activating outreach touches real accounts/audiences — confirm in the same
  turn before doing it. Drafts and inactive sequences are fine to prepare.
- **Apollo sequences are created `active: false`.** Activation
  (`apollo_emailer_campaigns_approve`) happens only after the domain is warm, a
  sender is set, contacts are enrolled, and the human confirms.
- **Warmup is a hard floor** (~4–6 weeks). Never promise working cold outbound
  before it is warm. Start warmup on day one regardless.
- **Voice is human.** Never ship the `[VOICE]` placeholders as-is. The engine
  frames; the human finishes. That is the quality bar and the value.

## Owned-audience funnel
Every atom points to one signup form (`assets/signup-form.html`) with UTM tags.
Followers are rented; the list is owned. Stand up the list + form first, or the
whole engine has nowhere to convert to.

## Definition of done (can-sell gate)
Run `python3 engine.py validate` — it computes the seven Phase 5 checks. Sell
only when all are green: skill packages on demand; email + one social channel
publish (auto or clean manual); a real list captures signups; one pillar has
gone live with measurable engagement; copy is client-grade unedited;
measurement returns real numbers; cold outbound has warmed and sent once.

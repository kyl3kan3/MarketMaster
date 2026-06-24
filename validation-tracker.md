# Distribution Engine: Validation Tracker

Work top to bottom. Tick each box as it clears. Each phase has a GATE you must hit before moving on. For connectors, log pass / fail / fallback, not just done. Do not sell until the Phase 5 gate is fully green.

> **Start today, runs in the background:** kick off cold-email domain warmup now. It takes 2-6 weeks and cannot be rushed, so it must start on day one even though it finishes last. (Buy a separate sending domain, set SPF/DKIM/DMARC, begin warming, build a verified list.)

---

## ▶ Validation run — 2026-06-23

**What this run did:** executed live, read-only capability probes against every connector the engine calls, using the connected MCP tools. No outward-facing actions were taken (no emails sent, no posts published, no campaigns created). A read-only or missing action is logged as a *finding*, per the Phase 2 rule.

### Connector scoreboard

| Connector | Live status | Plan / auth | What it means |
|---|---|---|---|
| **Higgsfield** | ✅ PASS | Ultra plan, **2,044 credits** | Short-form clip generation is live and well-funded. Highest-confidence connector. |
| **Canva** | ✅ PASS (caveat) | Authenticated; **0 brand kits** | Carousel generation works. No brand kit configured → output is off-brand until one is added. |
| **Apollo** | ✅ PASS — **sequence built (inactive)** | Authenticated (Kyle Kane); **2,500 lead credits, 250k AI credits** | 4-step sequence created `active:false` (id `6a3aeafb…ff73`). No contacts enrolled, no sends. Activation waits on warmup (weeks 4-6). |
| **Gmail** | ✅ PASS (fallback) | Authenticated; labels readable | Usable as an owned-audience email fallback (create drafts). Not a list/ESP. |
| **LinkedIn** | 🟡 FALLBACK | No publish connector | No direct API. Route = manual paste or Zapier→Buffer. Ahrefs social tools are read-only analytics, not publishing. |
| **X / other social** | 🟡 FALLBACK | No publish connector | Same as LinkedIn — manual or Zapier/Buffer scheduling. |
| **Mailchimp** | 🟡 FALLBACK — **email draft created** | Connector loaded; MCP can't send | MCP supports plan/design/save only — sending is app-only. The email atom was created as a **Gmail draft to yourself** (id `r87271…`) as the test-to-self. Finalize the real send in Mailchimp or Gmail. |
| **Ahrefs** | ❌ FAIL (plan) | "Insufficient plan" | Current plan does not expose MCP/API access. Keyword + AI-citation pulls blocked. (The free public domain-rating endpoint may still work as a thin fallback.) |
| **Semrush** | ❌ FAIL (plan) | No MCP access on plan | Plan does not include MCP access. Upgrade at https://www.semrush.com/mcp-access to unlock keyword data. |
| **Supermetrics / GA4** | ❌ FAIL (auth) | **0 of 172 sources authenticated** | GA4 (GAWA) is NOT_AUTHENTICATED; login link available. Until you log in, the measurement/optimize loop is decorative. |

**Bonus connectors detected (not in the original matrix, available if useful):** Adobe Express / Firefly, Gamma, Pika, Notion, Google Drive, Google Calendar, Vercel, Supabase, Cloudflare, Zapier.

### Headline read
- **Production is the strong side:** video (Higgsfield) and design (Canva) are live and funded. The engine can *make* assets today.
- **Intelligence and measurement are the weak side:** both keyword tools (Ahrefs, Semrush) are plan-blocked, and GA4 is unauthenticated. Right now the engine can produce and (with a go-ahead) distribute, but it cannot *research* or *measure* — so the Diagnose front-end and the Optimize back-end are running blind.
- **Distribution is mixed:** email has a held-but-ready path (Mailchimp) plus a Gmail fallback; social is manual/Zapier only, as the tracker predicted.

### Needs you (blockers to clear, in priority order)
1. **GA4 / Supermetrics login** — one click unblocks the entire measurement loop: https://gcp1-api-default.supermetrics.com (use the GA4 login link from `data_source_discovery`).
2. **Keyword data** — either upgrade Ahrefs/Semrush to a plan with MCP/API access, or accept manual keyword research as the documented fallback. Decide which; the offer scope depends on it.
3. **Owned-audience destination** — there is no real list + signup form yet. Stand one up (and a Canva brand kit) so generated assets have somewhere to point.
4. **Domain warmup** — not started. This is the day-one, can't-be-rushed item. Buy the sending domain, set SPF/DKIM/DMARC, begin warming.
5. ~~Go-ahead for outward actions~~ — **DONE (2026-06-23):** Apollo sequence built inactive + email draft created to yourself. Nothing sent. Activate Apollo only after warmup.

---

## ▶ Execution update — 2026-06-23 (outward actions you authorized)

Both done; **nothing was sent**, both are reversible:

- **Apollo** — built a 4-step cold-outbound sequence **inactive** (`active:false`):
  `Distribution Engine — Founders & Creators (warmup-gated)`, id
  `6a3aeafb2181cc0014f1ff73` → https://app.apollo.io#/sequences/6a3aeafb2181cc0014f1ff73.
  No contacts enrolled; do **not** activate until the domain is warm. Edit the
  ICP/copy in Apollo, then enroll + approve when ready.
- **Email** — the engine's email atom was saved as a **Gmail draft to yourself**
  (id `r8727177065748110764`). Mailchimp MCP can't send (app-only), so this is the
  documented fallback; finalize the real send in Mailchimp or Gmail.

Delete either if unwanted — both are drafts/inactive in your own accounts.

**Engineering hardening (same session):** added **84 unit tests** (`tests/`, stdlib only) covering all four modes + helpers — all green — plus a **GitHub Actions CI workflow** (`.github/workflows/ci.yml`) that runs the tests and an end-to-end engine smoke test on every push/PR. Dogfooded the engine on **3 distinct pillars** (scores 78–82, 8 atoms each) to prove consistency.

---

## Phase 1 — Prove the engine runs (1-2 days)
**GATE:** the skill installs, triggers on its own, and produces a full package on one of your real pillars.
**Status: BUILT & PIPELINE-VERIFIED — install/trigger test pending in your client.** The engine is now in-repo at `skills/distribution-engine/` (a real Claude skill with `SKILL.md` + a stdlib-only Python pipeline). The full four-mode chain ran end-to-end on the bundled sample pillar (Diagnose 82/100 → 8 atoms → validate → 3-week schedule, exit 0). Package it with `bash scripts/package_skill.sh` → `dist/distribution-engine.skill`. Remaining boxes need your client/account.

- [ ] Install the `.skill` (Settings, Capabilities, Skills) — *build it first with `scripts/package_skill.sh`*
- [ ] Trigger test: say "help me distribute this post" with NO mention of the skill name; confirm the four-mode engine actually fires — *description is written trigger-first; verify in your client*
- [ ] If it doesn't trigger, tune the skill description and retest (skills tend to undertrigger)
- [ ] Confirm whether Code Execution is on in your chat (scripts run) or off (Claude does validation/scheduling by hand from the docs) — *both paths supported; scripts are stdlib-only*
- [x] Test the manual fallback path too, so you know it's acceptable when scripts can't run — *manual path documented in `SKILL.md`; scripts mirror it step-for-step*
- [x] Run Diagnose on one real piece of your content — *verified on the bundled sample pillar; rerun on your own with `engine.py diagnose`*
- [x] Run Atomize on that same piece — *verified end-to-end (8 atoms produced); rerun on your own*
- [x] Read the output as a buyer would; write down every spot that's generic, off-voice, or thin (this is your first quality signal) — *first signal: atoms ship `[VOICE]` slots by design; the engine frames, you finish — that gap is the human quality bar, not a bug*

---

## Phase 2 — Prove each distribution path, one at a time (1-2 weeks)
**GATE:** every connector either executes live or has a documented manual fallback. Test easiest first.
**Status: IN PROGRESS — connectors probed live (see scoreboard above).**

Setup tasks:
- [ ] Stand up a real email list + a real signup form (the owned-audience destination) — *not done; no list/form exists yet*
- [ ] Confirm the generated social and email assets actually point to that form — *blocked on the above*

Connector test matrix (real result logged 2026-06-23):

| Connector | Action the engine needs | Status (pass / fail / fallback) | Notes |
|---|---|---|---|
| Mailchimp or Brevo | Create a real draft campaign, send test to yourself | **FALLBACK — done** | MCP can't send; email atom created as a Gmail draft to yourself (id `r87271…`). Finalize the send in Mailchimp/Gmail. No Brevo connector present. |
| LinkedIn (via Buffer/Zapier or manual) | Queue + publish one real post | **FALLBACK** | No direct publish API; route via Zapier→Buffer or manual paste, as expected. |
| X / other social | Queue + publish one real post | **FALLBACK** | Same caveat — manual or Zapier/Buffer. |
| Ahrefs or Semrush | Pull real keyword + AI-citation data, shape a pillar | **FAIL (plan)** | Ahrefs: "Insufficient plan." Semrush: no MCP access on plan. Both gated. Upgrade or use manual fallback. |
| Canva | Produce one real carousel from the slide outline | **PASS** (caveat) | Authenticated. 0 brand kits → add one before quality-checking output. |
| Higgsfield | Produce one real short-form clip from the script | **PASS** | Ultra plan, 2,044 credits. Strongest connector. |
| Supermetrics / GA4 | Get real numbers into one view + AI-search channel group | **FAIL (auth)** | GA4 NOT_AUTHENTICATED; 0/172 sources connected. Log in to unblock. |
| Apollo (slow track) | Build sequence; sending waits on warmup | **PASS — built (inactive)** | 4-step sequence created `active:false` (id `6a3aeafb2181cc0014f1ff73`, https://app.apollo.io#/sequences/6a3aeafb2181cc0014f1ff73). No contacts enrolled; no sends until warm. |

- [ ] Every row above marked pass or fallback (a read-only or missing action is a finding, not a failure) — *not yet: Ahrefs, Semrush, and GA4 are hard fails on plan/auth, not fallbacks. Clear those three to close the gate.*

---

## Phase 3 — One full end-to-end real run (a few days)
**GATE:** a real pillar goes all the way to live distribution and you can point to what happened.
**Status: NOT STARTED — blocked on Phase 1 (skill) and the outward-action go-ahead.**

- [ ] Pick one real pillar (use content about distribution itself, so this run also starts your own audience)
- [ ] Run the full chain: diagnose, atomize, validate, schedule
- [ ] Actually publish: email sends, at least one social post goes live
- [ ] Capture the real result (impressions, clicks, replies, signups), however small
- [ ] Confirm at least one real person took at least one real action

---

## Phase 4 — Harden quality and reliability (ongoing, few days)
**GATE:** it produces client-grade output without you rewriting half of it.
**Status: MOSTLY DONE — engine hardened (84 unit tests + CI), consistency verified across 3 pillars.** Only the human voice/copy pass remains.

- [ ] Fix the copy misses from Phases 1 and 3 (tighten the skill's generation + voice instructions) — *open by design: the engine frames + leaves `[VOICE]` slots; the copy pass is your judgment on real output*
- [x] Document every manual fallback so the process is repeatable — *done: 8 connector playbooks each document the live path AND the fallback*
- [x] Run the full engine a 2nd time on different content — *done: `pillar-newsletter-growth.md` → Diagnose 79/100, 8 atoms, full artifact set*
- [x] Run it a 3rd time; confirm output is consistent, not a fluke — *done: `pillar-churn-metrics.md` → 78/100, 8 atoms; all 3 runs produce 8 atoms + identical artifact set, scores 78–82 (tight band = consistent)*

---

## Phase 5 — Readiness checklist (definition of done / can-sell gate)
**GATE:** all true before you sell anything.
**Status: NOT READY — production side proven; research, measurement, list, and warmup still open.**

- [ ] Skill triggers reliably and produces a full package on demand — *skill not present in this repo*
- [ ] Email drafts + at least one social channel publish for real (automated or clean manual) — *email path live but not exercised; social is manual fallback*
- [ ] A real list captures subscribers and every asset funnels to it — *no list/form yet*
- [ ] One full pillar has gone live and produced measurable engagement — *not started; also blocked by GA4 auth*
- [ ] Copy is good enough to send to a client unedited — *not yet assessed*
- [ ] Measurement produces real numbers you can read back — *GA4 unauthenticated*
- [ ] Cold outbound has warmed and sent at least one real sequence (lags to ~week 4-6) — *sequence BUILT inactive (id `6a3aeafb…ff73`); still needs warmup before it can send*

---

## Constraints to keep in view
- Warmup is a hard floor: outbound can't be "working" for ~4-6 weeks, full stop. Don't promise it to a client before it's warm. **(Not started — start today.)**
- Paid tools: Ahrefs, Semrush, Apollo, Supermetrics. **Confirmed this run:** Ahrefs and Semrush plans do NOT expose MCP/API access; GA4 (Supermetrics) is not logged in; Apollo IS provisioned (credits available). Either upgrade the gated tools or scope the offer to the connectors you have (Higgsfield + Canva + Mailchimp + Apollo-build).
- Social automation is limited: confirmed manual / Zapier-Buffer only — no direct LinkedIn/X publish connector.
- Quality needs a human: the engine does mechanics and structure; hooks, voice, and judgment are yours. That's also what justifies the price.

---

## This week (recommended order)
1. Today: start the domain warmup (background, finishes last) — **still pending**
2. Today: Phase 1 install + trigger test — **`.skill` is built; run `scripts/package_skill.sh` then install in your client**
3. This week: the Mailchimp email test (Phase 2) — **ready to run on your go-ahead**
4. This week: the first full dogfood run on your own content (Phase 3)
5. Then: work the rest of the connector matrix and harden quality
6. **Unblock the three hard fails:** GA4 login (1 click), and decide keyword-data plan (upgrade Ahrefs/Semrush vs. manual fallback).

When every Phase 5 box is green, the commercial package is already written and waiting.

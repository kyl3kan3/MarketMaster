# Distribution Engine: Validation Tracker

Work top to bottom. Tick each box as it clears. Each phase has a GATE you must hit before moving on. For connectors, log pass / fail / fallback, not just done. Do not sell until the Phase 5 gate is fully green.

> **Start today, runs in the background:** kick off cold-email domain warmup now. It takes 2-6 weeks and cannot be rushed, so it must start on day one even though it finishes last. (Buy a separate sending domain, set SPF/DKIM/DMARC, begin warming, build a verified list.)

---

## Phase 1 — Prove the engine runs (1-2 days)
**GATE:** the skill installs, triggers on its own, and produces a full package on one of your real pillars.

- [ ] Install the `.skill` (Settings, Capabilities, Skills)
- [ ] Trigger test: say "help me distribute this post" with NO mention of the skill name; confirm the four-mode engine actually fires
- [ ] If it doesn't trigger, tune the skill description and retest (skills tend to undertrigger)
- [ ] Confirm whether Code Execution is on in your chat (scripts run) or off (Claude does validation/scheduling by hand from the docs)
- [ ] Test the manual fallback path too, so you know it's acceptable when scripts can't run
- [ ] Run Diagnose on one real piece of your content
- [ ] Run Atomize on that same piece
- [ ] Read the output as a buyer would; write down every spot that's generic, off-voice, or thin (this is your first quality signal)

---

## Phase 2 — Prove each distribution path, one at a time (1-2 weeks)
**GATE:** every connector either executes live or has a documented manual fallback. Test easiest first.

Setup tasks:
- [ ] Stand up a real email list + a real signup form (the owned-audience destination)
- [ ] Confirm the generated social and email assets actually point to that form

Connector test matrix (log the real result for each):

| Connector | Action the engine needs | Status (pass / fail / fallback) | Notes |
|---|---|---|---|
| Mailchimp or Brevo | Create a real draft campaign, send test to yourself | | start here, highest value/easiest |
| LinkedIn (via Buffer/Zapier or manual) | Queue + publish one real post | | direct API is limited; expect Buffer or manual |
| X / other social | Queue + publish one real post | | same caveat as LinkedIn |
| Ahrefs or Semrush | Pull real keyword + AI-citation data, shape a pillar | | paid; confirm plan exposes it |
| Canva | Produce one real carousel from the slide outline | | check quality bar |
| Higgsfield | Produce one real short-form clip from the script | | check quality bar |
| Supermetrics / GA4 | Get real numbers into one view + AI-search channel group | | if no numbers, optimize loop is decorative |
| Apollo (slow track) | Build sequence; sending waits on warmup | | started in Phase 0; sends week 4-6 |

- [ ] Every row above marked pass or fallback (a read-only or missing action is a finding, not a failure)

---

## Phase 3 — One full end-to-end real run (a few days)
**GATE:** a real pillar goes all the way to live distribution and you can point to what happened.

- [ ] Pick one real pillar (use content about distribution itself, so this run also starts your own audience)
- [ ] Run the full chain: diagnose, atomize, validate, schedule
- [ ] Actually publish: email sends, at least one social post goes live
- [ ] Capture the real result (impressions, clicks, replies, signups), however small
- [ ] Confirm at least one real person took at least one real action

---

## Phase 4 — Harden quality and reliability (ongoing, few days)
**GATE:** it produces client-grade output without you rewriting half of it.

- [ ] Fix the copy misses from Phases 1 and 3 (tighten the skill's generation + voice instructions)
- [ ] Document every manual fallback so the process is repeatable
- [ ] Run the full engine a 2nd time on different content
- [ ] Run it a 3rd time; confirm output is consistent, not a fluke

---

## Phase 5 — Readiness checklist (definition of done / can-sell gate)
**GATE:** all true before you sell anything.

- [ ] Skill triggers reliably and produces a full package on demand
- [ ] Email drafts + at least one social channel publish for real (automated or clean manual)
- [ ] A real list captures subscribers and every asset funnels to it
- [ ] One full pillar has gone live and produced measurable engagement
- [ ] Copy is good enough to send to a client unedited
- [ ] Measurement produces real numbers you can read back
- [ ] Cold outbound has warmed and sent at least one real sequence (lags to ~week 4-6)

---

## Constraints to keep in view
- Warmup is a hard floor: outbound can't be "working" for ~4-6 weeks, full stop. Don't promise it to a client before it's warm.
- Paid tools: Ahrefs, Semrush, Apollo, Supermetrics. Confirm your plans expose what the skill calls for, or scope the offer to the connectors you have.
- Social automation is limited: assume manual or Buffer-style scheduling until proven otherwise.
- Quality needs a human: the engine does mechanics and structure; hooks, voice, and judgment are yours. That's also what justifies the price.

---

## This week (recommended order)
1. Today: start the domain warmup (background, finishes last)
2. Today: Phase 1 install + trigger test
3. This week: the Mailchimp/Brevo email test (Phase 2, easiest real win)
4. This week: the first full dogfood run on your own content (Phase 3)
5. Then: work the rest of the connector matrix and harden quality

When every Phase 5 box is green, the commercial package is already written and waiting.

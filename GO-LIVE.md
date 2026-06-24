# GO-LIVE — Master Launch Checklist (here → "can sell")

> One sequenced path from where the Distribution Engine is **today** to the
> **Phase 5 can-sell gate** in [`validation-tracker.md`](./validation-tracker.md).
> Everything is split into **DONE** (shipped, verified, reversible) and
> **OWNER-TODO** (needs your accounts, judgment, or a calendar to clear).
>
> The single hard constraint that shapes the whole timeline: **domain warmup takes
> 2–6 weeks and cannot be rushed.** It finishes last but must start on day one, so
> it sits at the top of OWNER-TODO. Start it today and the rest of the work runs in
> parallel underneath it. See [`docs/warmup-schedule.md`](./docs/warmup-schedule.md).

**Last updated:** 2026-06-24 · **Phase 5 status:** NOT READY (production side proven; research, measurement, list, warmup still open)

---

## At a glance

| # | Owner item | Single concrete action | Unlocks |
|---|---|---|---|
| 1 | Domain warmup | Buy sending domain, set SPF/DKIM/DMARC, start warmup tool today | Apollo activation (wks 4–6) — the cold-outbound Phase 5 box |
| 2 | GA4 login | One click on the Supermetrics GA4 login link | Entire measurement loop; the "measurable engagement" + "real numbers" boxes |
| 3 | Keyword plan decision | Decide: upgrade Ahrefs/Semrush **or** accept manual fallback | Diagnose front-end + closes the two keyword hard-fails; sets offer scope |
| 4 | List + form + brand kit | Stand up an ESP list, a public signup form, and a Canva brand kit | Owned-audience destination; on-brand assets; the "real list" box |
| 5 | Copy / voice pass | Read real engine output as a buyer; fill `[VOICE]` slots, tighten hooks | "Copy good enough to send unedited" box |

Clear all five (and let warmup finish) → every Phase 5 box goes green → ship the commercial package.

---

## ✅ DONE — shipped, verified, reversible (no further action)

These are real, validated, and merged. Do not redo them.

- **Engine built & in-repo.** Real Claude skill at `skills/distribution-engine/`
  (`SKILL.md` + stdlib-only Python pipeline). Four modes (Diagnose → Atomize →
  Validate → Schedule) run end-to-end; full chain verified on the sample pillar
  (Diagnose 82/100 → 8 atoms → validate → 3-week schedule, exit 0).
- **84 unit tests, all green.** `tests/`, stdlib only, covering all four modes +
  helpers.
- **Green CI.** `.github/workflows/ci.yml` runs the unit tests **and** an
  end-to-end engine smoke test on every push/PR.
- **Consistency proven.** Dogfooded on **3 distinct pillars** (scores 78–82,
  8 atoms each) — tight band = consistent output, not a fluke.
- **All connectors validated (live, read-only probes, 2026-06-23).** Scoreboard
  in `validation-tracker.md`. Production side is the strong side:
  - **Higgsfield — PASS, clip produced** (real 9:16 short; Ultra plan, 2,044 credits).
  - **Canva — PASS, carousel produced** (real 8-slide carousel, 4 variants).
  - **Apollo — PASS, sequence built INACTIVE** (see below).
  - **Gmail — PASS (fallback)** owned-audience email draft path.
  - **Mailchimp / LinkedIn / X — FALLBACK** documented (MCP can't send / no publish
    API; manual or Zapier→Buffer).
  - The three **hard fails (Ahrefs, Semrush, GA4)** are surfaced as OWNER-TODO #2/#3.
- **Apollo sequence built INACTIVE.** 4-step warmup-gated sequence
  `Distribution Engine — Founders & Creators`, id
  **`6a3aeafb2181cc0014f1ff73`**, `active:false`, **no contacts enrolled, nothing
  sent**. https://app.apollo.io#/sequences/6a3aeafb2181cc0014f1ff73
- **Real carousel + clip produced** (the two PASS rows above) — proof the engine
  can *make* client-grade assets today.
- **Email atom test-to-self created.** Gmail draft to yourself
  (id `r8727177065748110764`) as the documented send fallback. Nothing sent.
- **Merged to main.** Engine, tests, CI, and connector playbooks are on `main`.
- **All manual fallbacks documented.** 8 connector playbooks each document the
  live path AND the fallback.

---

## ☐ OWNER-TODO — needs you (sequenced; start #1 today)

Each item lists the **single concrete action** and **what it unlocks**. Items 2–5
can run in parallel underneath the warmup clock.

### 1. Domain warmup — START TODAY (the day-one, can't-be-rushed item)
- **Action:** Buy a **separate** sending domain, publish **SPF + DKIM + DMARC**
  DNS records (DMARC at `p=none` to start), create 1–3 real-name mailboxes, turn
  on a warmup tool at ~10/day, and begin the week-by-week ramp. Full runbook +
  DNS templates + ramp table: [`docs/warmup-schedule.md`](./docs/warmup-schedule.md).
- **Unlocks:** After the **2–6 week** ramp completes (auth passes, healthy ramp,
  bounce <2–3%), you may **activate the Apollo sequence**
  (`6a3aeafb2181cc0014f1ff73`) — closing the *"cold outbound has warmed and sent
  at least one real sequence"* Phase 5 box. **Nothing else unlocks this; it is the
  critical path.** Start it before anything below.

### 2. GA4 login (one click)
- **Action:** Open the Supermetrics GA4 (GAWA) login link from
  `data_source_discovery` and authenticate the GA4 source
  (https://gcp1-api-default.supermetrics.com). Currently **0 of 172 sources
  authenticated**.
- **Unlocks:** The entire measurement/optimize loop — the *"measurement produces
  real numbers you can read back"* box and (with a live run) the *"measurable
  engagement"* box. Until this is done, the Optimize back-end runs blind.

### 3. Keyword plan decision
- **Action:** Make ONE decision: either **upgrade Ahrefs and/or Semrush** to a
  plan that exposes MCP/API access (Ahrefs currently "Insufficient plan"; Semrush
  upgrade at https://www.semrush.com/mcp-access), **or** explicitly **accept manual
  keyword research** as the documented fallback (brief in
  `docs/keyword-brief-distribution.md`).
- **Unlocks:** The Diagnose front-end's keyword/AI-citation inputs and closes the
  two keyword hard-fails in Phase 2. **This decision sets the offer scope** — what
  you can promise a client depends on whether keyword intelligence is automated or
  manual.

### 4. List + signup form + brand kit
- **Action:** Stand up a real **ESP list** and a public **signup form** (the
  owned-audience destination; setup steps in `docs/owned-audience-setup.md`), then
  add a **Canva brand kit** so generated carousels are on-brand. Point every
  generated social/email asset at that form.
- **Unlocks:** The *"a real list captures subscribers and every asset funnels to
  it"* box, removes the "off-brand until a brand kit exists" caveat on Canva
  output, and gives the whole engine somewhere to send traffic.

### 5. Copy / voice pass
- **Action:** Run the engine on **your own** real pillar, read the output **as a
  buyer**, fill the `[VOICE]` slots, and tighten every hook/line that is generic,
  off-voice, or thin. The engine frames the structure on purpose and leaves voice
  to you — that gap is the human quality bar.
- **Unlocks:** The *"copy is good enough to send to a client unedited"* box — the
  last quality gate before selling.

---

## Phase 5 gate — definition of done (mirror of `validation-tracker.md`)

Sell only when **all** are green:

| Phase 5 box | Cleared by | State today |
|---|---|---|
| Skill triggers reliably + full package on demand | DONE (build) + install/trigger test in your client | ☐ verify in client |
| Email drafts + ≥1 social channel publishes for real | Item 4 (list/form) + one live run | ☐ |
| A real list captures subscribers; assets funnel to it | **Item 4** | ☐ |
| One full pillar live with measurable engagement | **Item 2** (GA4) + one live run | ☐ |
| Copy good enough to send to a client unedited | **Item 5** | ☐ |
| Measurement produces real numbers you can read back | **Item 2** (GA4) | ☐ |
| Cold outbound warmed + sent ≥1 real sequence | **Item 1** (warmup → activate `6a3aeafb…ff73`) | ☐ (lags to wk 4–6) |

When every row is green, the commercial package is already written and waiting.

---

## Recommended order

1. **Today:** kick off **#1 domain warmup** (background clock — finishes last, so it
   must start first) and click **#2 GA4 login** (frees the measurement loop immediately).
2. **This week:** make the **#3 keyword decision** (sets scope) and build the
   **#4 list + form + brand kit**.
3. **This week / next:** do the first full live run on your own pillar and the
   **#5 copy/voice pass**.
4. **Weeks 4–6:** when warmup's gate goes green, enroll contacts and **activate the
   Apollo sequence** — the final Phase 5 box.

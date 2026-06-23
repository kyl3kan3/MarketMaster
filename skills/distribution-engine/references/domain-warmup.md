# Cold-email domain warmup (the day-one background task) — Distribution Engine Playbook

> **Engine mode(s):** N/A (process) — but it GATES `outbound-apollo.md` (cold outbound cannot activate until this completes).
> **Live status (validated 2026-06-23):** N/A (process) — not started; must start on day one because it cannot be rushed.

## What this is for
This is the **hard floor** of the Distribution Engine timeline: cold outbound cannot be
considered "working" for roughly **4–6 weeks**, full stop. Warmup builds the sending reputation
of a dedicated cold-email domain so that, when the Apollo sequence finally activates, mail lands
in the inbox instead of spam.

It is a paradox to plan around: warmup **finishes last** but must **start on day one**, because
the ramp is calendar-bound and cannot be sped up. There are **NO MCP tools** for this — it is an
infrastructure + process runbook executed by the user (or their ops/IT). Track it as a
**date-based countdown / gating checkbox**, not as a connector and not as a one-shot test.

## Primary path (live)
- **Exact MCP tools:** *none.* Warmup is infrastructure + process; no Distribution Engine tool
  performs it. Your job is to drive the runbook, track the countdown, and hold the gate.
- **Step-by-step (numbered):**

1. **Buy a SEPARATE sending domain.** Register a distinct domain (e.g. a `.com` close to the
   brand name) used ONLY for cold outreach, so a deliverability hit can never threaten the
   primary domain's reputation. Optionally redirect it to the main site for legitimacy.

2. **Set up authentication.** Add **SPF**, **DKIM**, and **DMARC** DNS records for the sending
   domain. Start **DMARC at `p=none`** for monitoring, then tighten (to quarantine/reject) once
   alignment is confirmed. Optionally add **BIMI** later, once DMARC is aligned and enforced.

3. **Create sending mailboxes.** Stand up **1–3 mailboxes** on the new domain using **real
   names**, each with a complete profile and a proper signature. More than ~3 per domain spreads
   reputation too thin early on.

4. **Turn on a warmup service.** Enable an automated inbox-warmup tool that auto-sends and
   auto-replies to build positive engagement signals. **Start tiny** (~5–10 emails/day per
   mailbox) and **ramp gradually over 2–6 weeks**. Rough ramp:
   - **Week 1:** ~10/day
   - **Week 2:** ~20/day
   - **Week 3:** ~40/day
   - **Week 4+:** ~50+/day
   **Never spike volume** — sudden jumps look like spam and undo the ramp.

5. **Build a verified, permission-aware list in parallel.** While warmup runs, assemble a
   **verified opt-in / permission-aware** recipient list and run it through an **email verifier**
   to keep the bounce rate low (**<2–3%**). Bounces and spam complaints are exactly what burn a
   domain — clean the list before the first real send, not after.

6. **Hold modest volume, monitor, then activate.** Keep daily volume modest and engagement
   high; monitor deliverability/inbox placement throughout the ramp. **Only AFTER the ramp
   completes** do you activate the Apollo sequence — see `outbound-apollo.md` → the
   `mcp__Apollo_io__apollo_emailer_campaigns_approve` (approve) step.

## Fallback path
- **There is no shortcut.** If warmup has not run for the full ramp, the fallback is simply to
  **wait** and keep building (write copy, build the audience, create the INACTIVE Apollo
  sequence per `outbound-apollo.md`). Do not "borrow" the primary domain to send sooner.
- **If warmup stalls or a metric goes bad** (rising bounces/complaints, dropping placement):
  pause sending, **lower volume**, fix the cause (list hygiene, content, auth), and resume the
  ramp from a lower step. Restart the countdown clock if reputation was damaged.
- **If no warmup tool is available:** ramp manually and conservatively by the same schedule, but
  expect this to be slower and riskier; prefer a real warmup service.

## Inputs it needs  /  Outputs it produces
**Inputs:**
- A registered **dedicated sending domain** (separate from the primary).
- **DNS access** to publish SPF/DKIM/DMARC (and optionally BIMI) records.
- A **warmup service** account and an **email verifier**.
- The brand identity (real sender names, signatures) and a **start date** to anchor the
  countdown.

**Outputs:**
- A **warm, authenticated sending domain** with 1–3 reputable mailboxes.
- A **verified, low-bounce recipient list** ready to enroll.
- A satisfied **gating checkbox** ("warmup complete") that unblocks
  `outbound-apollo.md` activation — plus a target activation date for the tracker.

## Quality bar & gotchas
- **Do NOT** send cold campaigns from the **primary domain** — ever. Use the dedicated domain.
- **Do NOT** buy or use **scraped lists** — they spike bounces/complaints and burn the domain.
- **Do NOT** jump straight to high volume — gradual ramp only; never spike.
- **Keep content un-spammy** — avoid spam-trigger words, keep a balanced text-to-link ratio,
  and avoid heavy images/attachments early.
- **Authentication is non-negotiable** — SPF, DKIM, and DMARC must all be in place before any
  real send; start DMARC at `p=none` and tighten.
- **Warmup status is a gating checkbox, not a connector** — represent it in the tracker as a
  date-based countdown that other work plans around.

## How to validate it
The gate is **satisfied** (warmup complete → outbound may activate) only when ALL hold:
- **(a) Auth passes:** a test message from the sending domain passes **SPF, DKIM, and DMARC**
  (check the message headers / a mail-tester style report).
- **(b) Healthy ramp:** the warmup tool reports a **healthy ramp for the full period** (steady,
  un-spiked volume increase across the 2–6 weeks, good warmup engagement, no reputation flags).
- **(c) Low bounce/complaint rates:** verified-list bounce rate stays **<2–3%** and spam
  complaints stay negligible.

Track this as a **date-based countdown**, not a single pass/fail test: re-check (a)–(c) over the
full ramp window, and flip the gate to "warm" only when the calendar period is done AND all three
checks are green. Then, and only then, proceed to `outbound-apollo.md`'s approve step.

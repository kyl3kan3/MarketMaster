# Cold Outbound — Apollo.io (the slow track) — Distribution Engine Playbook

> **Engine mode(s):** Distribute (cold outbound) — gated by domain warmup (see `domain-warmup.md`).
> **Live status (validated 2026-06-23):** PASS (build only) — Apollo is authenticated and provisioned, so you CAN build an inactive sequence now, but you must NOT send until the sending domain is warm.

## What this is for
Cold outbound is the slow track of the Distribution Engine. Use it to reach net-new ICP
contacts who have never heard of the brand, via a multi-step personalized email sequence in
Apollo. It is the LAST channel to go live: realistically it activates ~week 4–6, after the
sending domain finishes warmup. Everything in this file is about **building a review-ready,
INACTIVE sequence now** so it is ready to fire the moment warmup completes.

This file covers building and enrolling only. Activation (real-world sending) is a separate,
gated step described under "Primary path → final gate" and must never happen on a cold domain.

## ⛔ THE HARD RULE (read first)
- Create EVERY sequence INACTIVE. Call `mcp__Apollo_io__apollo_sequences_create` with
  **`active: false`**. No exceptions.
- Activation is a SEPARATE, gated step: `mcp__Apollo_io__apollo_emailer_campaigns_approve`.
  It has real-world consequences (live emails to real people) and may ONLY be done after ALL
  of the following are true:
  1. **(a)** the sending domain is warm (warmup ramp complete — see `domain-warmup.md`),
  2. **(b)** a sender mailbox is selected,
  3. **(c)** contacts are added/enrolled, and
  4. **(d)** the user explicitly confirms activation **in the same turn**.
- If any of (a)–(d) is missing, STOP at the inactive sequence. Do not approve. Report what is
  blocking and hand back to the user.

## Primary path (live)
Exact MCP tools (in call order):
`mcp__Apollo_io__apollo_users_api_profile`,
`mcp__Apollo_io__apollo_usage_stats_credit_usage_stats`,
`mcp__Apollo_io__apollo_emailer_campaigns_search`,
`mcp__Apollo_io__apollo_sequences_create`,
`mcp__Apollo_io__apollo_contacts_search`,
`mcp__Apollo_io__apollo_mixed_people_api_search`,
`mcp__Apollo_io__apollo_contacts_create`,
`mcp__Apollo_io__apollo_email_accounts_index`,
`mcp__Apollo_io__apollo_emailer_campaigns_add_contact_ids`,
`mcp__Apollo_io__apollo_emailer_schedules_index`,
`mcp__Apollo_io__apollo_emailer_campaigns_approve` (gated — final step only).

Step-by-step (numbered):

1. **Confirm auth & credits.** Call `mcp__Apollo_io__apollo_users_api_profile` to confirm the
   account is authenticated. On 2026-06-23 this returned account **Kyle Kane** with **2,500
   lead credits** and **250,000 AI credits** remaining. Then call
   `mcp__Apollo_io__apollo_usage_stats_credit_usage_stats` to confirm lead credits are
   available. (Direct-dial credits are exhausted but irrelevant to email outbound — ignore
   them.) Credit cycle resets ~**2026-07-12**; if a build needs more than the remaining lead
   credits, flag it rather than overspend.

2. **Check for a duplicate sequence.** Call `mcp__Apollo_io__apollo_emailer_campaigns_search`
   with `q_name` set to your intended sequence name. If a matching sequence already exists,
   reuse or rename — do NOT create a duplicate.

3. **Create the sequence INACTIVE.** Call `mcp__Apollo_io__apollo_sequences_create` with:
   - `name` (clear, ICP-specific),
   - `active: false` (mandatory — see THE HARD RULE),
   - **4–6 steps** following best-practice escalation:
     `auto_email` → wait **3d** → `auto_email` → wait **3d** → `auto_email` → `breakup`.
   - Body length **25–85 words**, ideally **≤50**. Subject line **≤9 words**.
   - One CTA per email; personalized opener; plain, specific language.

4. **Build the audience.** Find contacts with `mcp__Apollo_io__apollo_contacts_search`
   (existing contacts) and/or `mcp__Apollo_io__apollo_mixed_people_api_search` (net-new people
   matching the ICP). For people not yet in Apollo as contacts, create them with
   `mcp__Apollo_io__apollo_contacts_create`. Filter to the ICP definition (titles, industries,
   company size). Respect lead-credit budget from step 1.

5. **Pick the sender mailbox.** Call `mcp__Apollo_io__apollo_email_accounts_index` and select
   the sender that belongs to the **warm sending domain**, not the primary domain. (If no warm
   mailbox exists yet, you can still build; just note the gate is unmet.)

6. **Enroll contacts (still not sending).** Call
   `mcp__Apollo_io__apollo_emailer_campaigns_add_contact_ids` to add the contact IDs from step
   4 to the sequence. Enrollment in an INACTIVE sequence does not send anything.

7. **(Optional) Pick send windows.** Call `mcp__Apollo_io__apollo_emailer_schedules_index` to
   choose business-hours/timezone-aware sending windows for when the sequence does go live.

8. **STOP here unless the gate is met.** The build is now a review-ready, inactive sequence
   with an enrolled (not-yet-sending) contact list. Hand back to the user.

9. **Final gate — activate ONLY when (a)–(d) all hold.** Once the domain is warm, a sender is
   selected, contacts are enrolled, and the user explicitly confirms in the same turn, call
   `mcp__Apollo_io__apollo_emailer_campaigns_approve` to activate. This is the only step that
   sends real email. Never reach it on a cold domain.

## Fallback path
- **Domain not warm (the normal case for weeks 1–5):** Build the full inactive sequence and
  enroll contacts, then stop at step 8. Report "built, awaiting warmup" and point to
  `domain-warmup.md` for the countdown. This is expected, not a failure.
- **Lead credits insufficient:** Trim the audience to fit remaining credits, or defer building
  the larger list until the cycle resets (~2026-07-12). Do not exhaust credits mid-build.
- **No warm sender mailbox in `apollo_email_accounts_index`:** Build with a placeholder/no
  sender, document that mailbox selection (gate b) is unmet, and do not approve.
- **Apollo API unavailable / not authenticated:** If `apollo_users_api_profile` does not
  confirm auth, do not attempt to build. Draft the sequence copy and ICP/audience plan as text
  for the user to load manually later, and report the auth failure.
- There is no "send anyway" fallback. If the domain is cold, outbound stays out of scope.

## Inputs it needs  /  Outputs it produces
**Inputs:**
- ICP definition: titles, industries, company size (and optionally geography/seniority).
- The pillar/offer being pitched (what the CTA points to).
- Tone: one of **Direct | Formal | Casual**.
- (For activation only) confirmation that the domain is warm + a selected warm sender mailbox.

**Outputs:**
- An **INACTIVE, review-ready Apollo sequence** (4–6 steps, escalation pattern above) with a
  returned sequence id.
- An **enrolled but not-yet-sending contact list** matched to the ICP.
- A clear status line stating the sequence is inactive and what (if anything) blocks activation.

## Quality bar & gotchas
- **Copy:** short, specific, ONE CTA, personalized opener. Bodies 25–85 words (≤50 ideal),
  subjects ≤9 words. No fluff, no walls of text, no multiple asks.
- **Compliance:** respect CAN-SPAM / GDPR — clear sender identity, a working opt-out, no abuse
  of purchased/scraped lists. Only email people you have a legitimate basis to contact.
- **Never activate on a cold domain.** This is the cardinal sin; it burns deliverability for
  the whole program. Warmup is a hard prerequisite, not a nice-to-have.
- **Always `active: false` at creation.** Treat any sequence created active as a defect.
- **No duplicates** — always run `apollo_emailer_campaigns_search` (q_name) first.
- **Right sender** — send from the dedicated warm domain, never the primary brand domain.
- **Credit discipline** — size the audience to remaining lead credits; cycle resets ~2026-07-12.

## How to validate it
- **Build proof:** `mcp__Apollo_io__apollo_sequences_create` returns a sequence **id** while the
  sequence remains **inactive**. Confirm the sequence exists and is inactive by calling
  `mcp__Apollo_io__apollo_emailer_campaigns_search` (q_name) and seeing it in the results.
- **Enrollment proof:** the contact IDs added via
  `mcp__Apollo_io__apollo_emailer_campaigns_add_contact_ids` are associated with the sequence.
- **Out of scope until warm:** sending/activation
  (`mcp__Apollo_io__apollo_emailer_campaigns_approve`) is explicitly NOT validated here and must
  not run until warmup completes and the user confirms. Validation success = "an inactive,
  enrolled, review-ready sequence exists," nothing more.

# Email — Mailchimp (with Gmail fallback) — Distribution Engine Playbook

> **Engine mode(s):** Distribute, Validate
> **Live status (validated 2026-06-23):** FALLBACK — the Mailchimp MCP connector is loaded and authenticated, but it only supports planning + AI content design + saving + analytics. It does NOT send email and cannot send a test to yourself (sending happens in the Mailchimp web app), and it intentionally refuses single one-off campaigns.

## What this connector is for
Use this connector to design and stage email content for an owned audience, then hand a finished, saved draft to a human who finalizes and sends it inside Mailchimp.

- The engine's responsibility ENDS at a finished, saved Mailchimp draft. A human clicks send.
- Mailchimp's planner works at the level of a MULTI-campaign omnichannel PLAN. It will REFUSE to create a single standalone email/SMS/social asset — that refusal is by design, not a bug.
- There is **NO Brevo connector** available in this toolset, despite the tracker naming the connector "Mailchimp or Brevo." Treat Brevo as unavailable; do not attempt to route to it.
- For tiny / personal sends where a full ESP plan is overkill, use the Gmail fallback to produce a real, sendable draft.

## Primary path (live)
  - Exact MCP tools: `mcp__Intuit_Mailchimp__get_capabilities`, `mcp__Intuit_Mailchimp__campaign_planner`, `mcp__Intuit_Mailchimp__edit_campaign`, `mcp__Intuit_Mailchimp__get_campaign_content`, `mcp__Intuit_Mailchimp__set_active_campaign`, `mcp__Intuit_Mailchimp__save_to_mailchimp`, `mcp__Intuit_Mailchimp__get_analytics`
  - Step-by-step (numbered):
    1. Call `mcp__Intuit_Mailchimp__get_capabilities` FIRST. It is the authoritative answer about what is and is not supported. Relay its response to the user **verbatim** — do not paraphrase or soften it, especially the parts about sending.
    2. Confirm an audience/list already exists in the Mailchimp account. A plan cannot be saved or used without one. If none exists, stop and tell the human to create an audience in Mailchimp (the engine cannot create it).
    3. Build the plan with `mcp__Intuit_Mailchimp__campaign_planner`. It requires `business_context` (at minimum a name + product) and a `time_period`. Frame the request as a multi-campaign plan — do NOT ask it for one standalone email, because it will refuse.
    4. Set the campaign you want to work on with `mcp__Intuit_Mailchimp__set_active_campaign`.
    5. Render and inspect the email with `mcp__Intuit_Mailchimp__get_campaign_content` to confirm copy, layout, and links are correct.
    6. Apply any edits with `mcp__Intuit_Mailchimp__edit_campaign` (it is an AI agent that can change text, visuals, theme, or metadata on an existing campaign). Loop steps 5–6 until the draft meets the quality bar.
    7. Ensure every email asset carries a UTM-tagged link to the owned-audience signup form (see `../assets/signup-form.html`).
    8. Save the finished plan into the user's account with `mcp__Intuit_Mailchimp__save_to_mailchimp`.
    9. STOP. Hand off to a human: instruct them to open Mailchimp, send a test to themselves there, then send/schedule the campaign. The MCP cannot do these last steps.
    10. After the human sends, use `mcp__Intuit_Mailchimp__get_analytics` to pull reporting (opens, clicks, etc.).

## Fallback path (when the live path is unavailable)
Use the owned-email fallback when Mailchimp is blocked, when no audience exists yet, or when the send is very small/personal and does not justify an ESP plan.

  - Exact MCP tools: `mcp__Gmail__create_draft`
  - Step-by-step:
    1. Hand-build the recipient list (a small set of addresses you already have permission to email).
    2. Compose the email body, including the UTM-tagged signup-form link from `../assets/signup-form.html`.
    3. Create the draft with `mcp__Gmail__create_draft`. This produces a real, reviewable Gmail draft.
    4. Tell the human to review and send it from Gmail.
  - Limitations to state plainly: Gmail is **not an ESP**. It does not scale, does not segment, does not track opens/clicks, and has no unsubscribe management. Use only for small/personal sends; route anything larger back through Mailchimp once an audience exists.

## Inputs it needs  /  Outputs it produces
**Inputs:**
- An existing Mailchimp audience/list (for the primary path).
- `business_context`: at minimum a brand/name + the product being promoted.
- A `time_period` for the plan (e.g. a launch window or month).
- The atomized email copy/angle(s) from the Atomize stage.
- The UTM-tagged signup-form URL (`../assets/signup-form.html`).

**Outputs:**
- A saved, finished Mailchimp draft campaign (primary path), ready for a human to test and send.
- OR a real Gmail draft addressed to a hand-built list (fallback).
- Analytics pulled post-send via `get_analytics`.

## Quality bar & gotchas
- **Sending is out of scope.** Never claim the email was sent or tested via MCP. The engine produces drafts only.
- **Relay `get_capabilities` verbatim.** Its "not supported" list is authoritative; do not editorialize.
- **Planner refuses singletons by design.** Always frame work as a multi-campaign plan. A refusal of a one-off ask is expected behavior, not an error.
- **Audience must pre-exist.** Saving a plan without an audience will fail; check first.
- **No Brevo.** Do not promise or attempt Brevo routing.
- Every asset must carry the UTM-tagged signup-form link; an email with no path back to the owned audience fails the bar.
- A blocked or read-only send capability is a **finding to report**, not a pipeline failure.

## How to validate it (a concrete check the engine can run)
1. Call `mcp__Intuit_Mailchimp__get_capabilities` and confirm it returns (connector authenticated). Capture its statement that sending/test-send is unsupported.
2. Confirm at least one audience exists in the account.
3. Create a minimal plan with `mcp__Intuit_Mailchimp__campaign_planner` using a valid `business_context` (name + product) and a `time_period`.
4. Save it with `mcp__Intuit_Mailchimp__save_to_mailchimp` and confirm a draft appears.
5. Confirm the saved draft contains the UTM-tagged signup-form link.
6. PASS = a saved draft exists with the correct link, and the human is told to finish the send in Mailchimp. A read-only/blocked send is recorded as a FINDING, not a FAIL.

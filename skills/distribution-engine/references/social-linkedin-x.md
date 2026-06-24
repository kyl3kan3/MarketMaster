# Social — LinkedIn & X (Twitter) — Distribution Engine Playbook

> **Engine mode(s):** Distribute, Schedule
> **Live status (validated 2026-06-23):** FALLBACK — there is NO direct LinkedIn or X publishing MCP connector. Publishing is done manually or through an automation bridge (Zapier → Buffer/LinkedIn/X).

## What this connector is for
Use this connector to turn atomized content into ready-to-post LinkedIn and X assets, schedule them, and get them live — even though no native publish API exists for either platform.

- The engine **produces and schedules**; a human or an automation Zap **executes** the actual publish.
- There is no first-party LinkedIn or X publish tool in this toolset. Plan around that from the start.

## Primary path (live)
There is no single live publish tool. Use the first of these three real routes that is available, in priority order.

  - Exact MCP tools: `mcp__Zapier__get_configuration_url` (route 1). Routes 2 and 3 have no publish tool — they are human-executed handoffs. Image/carousel assets come from Canva (`mcp__Canva__export-design`).
  - Step-by-step (numbered):
    1. **Atomize per platform.** Produce, for EACH platform, a hook-first post body, hashtags, an image/carousel reference, and a UTM-tagged signup-form link (see "Inputs" and "Quality bar").
    2. **Route 1 — Automation bridge (preferred).** Call `mcp__Zapier__get_configuration_url` to get the setup URL, and have the human configure a Zap that pushes a queued post to Buffer / LinkedIn / X. Zapier is the ONLY automation connector available. Once the Zap exists, the engine's queued post triggers it.
    3. **Route 2 — Buffer (or similar) manual scheduling.** If no Zap, the engine outputs the post body + image + scheduled time, and the human pastes it into Buffer's queue at the given slot.
    4. **Route 3 — Pure manual.** If neither is set up, the engine hands the human a complete, ready-to-post asset and the human posts it directly.
    5. **Record the result.** For whichever route, capture the live permalink for the Validate/Schedule record.

## Fallback path (when the live path is unavailable)
The routes above already degrade gracefully (Zap → Buffer → manual), so "fallback" here means dropping to pure manual handoff (Route 3): deliver a finished asset bundle (body, hashtags, image ref, scheduled time, link placement note) and have the human post it. A documented manual post still counts as a successful distribution.

**Do NOT mistake Ahrefs social tools for a publish path.** Ahrefs exposes `mcp__Ahrefs__social-media-posts`, `mcp__Ahrefs__social-media-post-metrics`, and `mcp__Ahrefs__social-media-channel-metrics` — but these are **READ-ONLY ANALYTICS**, not publishing. They cannot post anything. (Ahrefs is also plan-blocked in this account — see `keyword-ahrefs-semrush.md`.)

## Inputs it needs  /  Outputs it produces
**Inputs:**
- The atomized angle/message for the piece being distributed.
- Brand voice + any platform-specific constraints.
- An image or carousel reference from Canva (e.g. via `mcp__Canva__export-design`).
- The UTM-tagged signup-form URL (`../assets/signup-form.html`).
- The schedule slot(s) from the engine's `schedule.py` calendar.

**Outputs (per platform):**
- **LinkedIn:** a hook-first body. LinkedIn allows ~3000 chars, but front-load the first 2 lines (only those show before "see more"). LinkedIn **deprioritizes outbound links in-post** — the documented best practice is to put the link in the **first comment**, not the body. 3–5 hashtags where appropriate.
- **X (Twitter):** a single post within **280 chars**, or a thread if the idea needs room. 3–5 hashtags where appropriate (fewer is often better on X).
- An image/carousel reference attached to each post.
- A scheduled time per post, plus the recorded permalink once live.

## Quality bar & gotchas
- **Hook first, always.** The first 2 lines (LinkedIn) / first ~10 words (X) must earn the click-to-expand.
- **Respect limits.** X is a hard 280 chars per post — split into a thread rather than truncating meaning. LinkedIn's ceiling is high but front-loading still wins.
- **LinkedIn link placement:** put the UTM link in the first comment, not the post body, to avoid reach suppression.
- **Every post needs a UTM-tagged signup-form link** so traffic is attributable and routes back to the owned audience.
- **Scheduling is owned by the engine.** `schedule.py` outputs the calendar; the human or the Zap executes it. The engine does not "publish on a timer" itself.
- **Ahrefs ≠ publishing.** Its social tools are analytics only and the account is plan-blocked anyway.
- Don't invent a publish tool. If no Zap/Buffer is set up, fall to manual handoff — that is a valid, expected outcome.

## How to validate it (a concrete check the engine can run)
Prove that ONE real post can go live, end to end:
1. Produce one engine-generated post asset (body within limits, hashtags, image ref, UTM link, scheduled slot).
2. Publish it by EITHER (a) firing a test Zap via the Zapier-configured bridge, OR (b) manually posting the asset to LinkedIn/X.
3. Record the resulting **permalink**.
4. PASS = one asset is live with its permalink captured (or a documented manual fallback is in place and exercised). No native publish API is expected, so a working manual/Zap route counts as PASS.

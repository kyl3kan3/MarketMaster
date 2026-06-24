# Measurement (Supermetrics / Google Analytics 4) — Distribution Engine Playbook

> **Engine mode(s):** Validate (did the distribution actually land?) and the **Optimize feedback loop** (reads real numbers back to steer the next cycle).
> **Live status (validated 2026-06-23):** FAIL (auth) — GA4 is **NOT authenticated** in Supermetrics (0 of 172 sources connected); the user must click the login link once to connect.

## What this connector is for
This connector closes the loop. Distribute publishes assets; **Validate** and **Optimize** need
to read what those assets actually did. Specifically it pulls, from GA4 via Supermetrics:

- Sessions / engaged sessions by channel.
- Conversions — especially **signup-form events** (owned-audience growth).
- A custom **"AI search" channel** that isolates traffic arriving from AI assistants
  (ChatGPT, Perplexity, Gemini, Copilot, etc.), so the user can literally see AI-driven traffic.

Without this connector authenticated, the Optimize loop has no ground truth — see the fallback
and the plain-spoken warning at the end.

## Primary path (live)
This path requires GA4 to be authenticated in Supermetrics. As of 2026-06-23 it is **not** —
the steps below are the real sequence to run **once the login link has been clicked**.

  - **Exact MCP tools:**
    - `mcp__Supermetrics_Marketing_Analytics__data_source_discovery`
    - `mcp__Supermetrics_Marketing_Analytics__accounts_discovery`
    - `mcp__Supermetrics_Marketing_Analytics__field_discovery`
    - `mcp__Supermetrics_Marketing_Analytics__data_query`
    - `mcp__Supermetrics_Marketing_Analytics__get_async_query_results`

  - **Step-by-step (numbered):**
    1. **Discover + auth-gate the source.** Call
       `mcp__Supermetrics_Marketing_Analytics__data_source_discovery` with **no `ds_id`** to list
       all sources and their auth status. GA4 is source id **`GAWA`** ("Google Analytics 4").
       Then call it **with `ds_id="GAWA"`** to get its config and, if unauthenticated, the
       `login_link`. If `authentication_status` is `NOT_AUTHENTICATED`, surface that login link
       to the user and stop — nothing downstream will work until they click it.
    2. **Discover the account/property.** Once authenticated, call
       `mcp__Supermetrics_Marketing_Analytics__accounts_discovery` for `GAWA`. GA4 has
       `has_account_list:true` and the account label is **"Property"** — select the correct GA4
       property id.
    3. **Discover fields.** Call `mcp__Supermetrics_Marketing_Analytics__field_discovery` for
       `GAWA` (`has_fields:true`). Pull the exact **metric and dimension field IDs** you need
       (sessions, engaged sessions, conversions/the signup event, source/medium, channel).
       **Use only the field IDs returned here — never display names.**
    4. **Query.** Call `mcp__Supermetrics_Marketing_Analytics__data_query` with the chosen
       `report_type` and put all setting values inside the **`settings` object**. GA4 has
       `is_date_range_required:true`, so a date range is mandatory. Include the property id,
       the field IDs from step 3, and any filters (see the AI-search section below).
    5. **Poll for results.** `data_query` runs async; call
       `mcp__Supermetrics_Marketing_Analytics__get_async_query_results` and **poll until the
       result is ready**, then parse rows.

### High-value artifact: the "AI search" channel grouping
Build a segment of sessions whose **referrer / source** is an AI surface so AI-assistant traffic
is visible as its own channel. In the `data_query` `settings`, add a **source/medium dimension
filter** that matches the AI hosts, e.g.:

`chatgpt.com`, `chat.openai.com`, `perplexity.ai`, `gemini.google.com`,
`copilot.microsoft.com` (extend as new surfaces appear).

Express it as a GA4 `sessionSource` / source-medium dimension filter (contains-any-of those
hosts) inside the query settings, returning sessions/engaged sessions/conversions for that slice.
Label the result the **"AI search" channel** in the Validate and Optimize outputs. Keep the host
list in one place so it is easy to extend.

## Fallback path (when the live path is unavailable)
This is the **current default** because GA4 is unauthenticated. Either:

1. **Read GA4 in its own web UI manually** — open the GA4 property, pull sessions / engaged
   sessions / signup conversions by channel, and build the AI-search view there by filtering
   on the same source hosts. Transcribe the numbers into the Validate report.
2. **UTM + form-backend counts** — the engine already **UTM-tags every distributed asset**, so
   attribute traffic and signups from the UTM parameters plus the **signup form backend's own
   submission counts**. This works without GA4 at all, just at coarser granularity.

Tag findings as `source: ga4-manual` or `source: utm+form-backend` so provenance is clear.

## Inputs it needs  /  Outputs it produces
**Inputs**
- An authenticated `GAWA` source in Supermetrics (the blocker today).
- The GA4 **property id** (from `accounts_discovery`).
- The **field IDs** for the metrics/dimensions (from `field_discovery`).
- The **signup-form event** name (the conversion to count).
- The AI-host list for the AI-search filter.
- A **date range** (required by GA4).

**Outputs**
- Sessions / engaged sessions by channel for the period.
- **Signup conversions** by channel — especially **owned-audience signups**.
- The **AI-search channel** slice (sessions + engaged + conversions from AI surfaces).
- A clean table the Optimize loop can diff against the previous cycle.

## Quality bar & gotchas
- **Auth first, always.** If `data_source_discovery(ds_id="GAWA")` shows anything other than
  `AUTHENTICATED`, stop and surface the `login_link`; do not attempt `data_query`.
- **Field IDs, not names.** Every metric/dimension passed to `data_query` must be a field ID
  returned by `field_discovery`. Display names will silently fail or misbehave.
- **Settings object.** Setting values (property, fields, filters, date range) go inside the
  `settings` object of `data_query`, not at the top level.
- **GA4 needs a date range** (`is_date_range_required:true`) — omitting it errors.
- **`data_query` is async** — you must poll `get_async_query_results`; do not read the immediate
  response as final data.
- Keep the **AI-host list current** — new assistants and changed referrer domains will silently
  drop AI traffic out of the channel if the filter is stale.
- Never invent tool names; only the five `mcp__Supermetrics_Marketing_Analytics__*` tools above
  are used here.

## How to validate it (a concrete check the engine can run)
1. Call `mcp__Supermetrics_Marketing_Analytics__data_source_discovery` with `ds_id="GAWA"`.
2. Inspect `authentication_status`:
   - If **not** `AUTHENTICATED` (current state — `NOT_AUTHENTICATED` on 2026-06-23) → **mark the
     connector FAIL**, surface the returned `login_link` to the user, and fall back to the
     manual / UTM path automatically.
   - If `AUTHENTICATED` → proceed to `accounts_discovery` → `field_discovery` → `data_query` →
     `get_async_query_results` and mark **PASS**.

> **Cost of staying blocked:** until GA4 is authenticated, the Optimize loop has **no real
> numbers** — it is **decorative**. Say so plainly. The single fix is the user clicking the
> `login_link` once for source `GAWA`; do that and the whole Validate/Optimize loop becomes real.

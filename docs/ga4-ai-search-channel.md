# GA4 "AI search" channel — runnable measurement spec (Supermetrics)

> **Status (2026-06-23):** GA4 is **NOT authenticated** in Supermetrics (0/172 sources
> connected). This spec is written so the live path runs the moment the `GAWA` `login_link`
> is clicked. Until then, run the **fallback** at the bottom (UTM + signup-form backend counts).
>
> **Goal:** sessions / engaged sessions / signup conversions by channel, plus an isolated
> **"AI search" channel** (ChatGPT, Perplexity, Gemini, Copilot, Claude, etc.) so AI-assistant
> traffic is visible as its own row in the Validate and Optimize outputs.

All five tools are the REAL Supermetrics MCP tool names. Never substitute or invent others.

---

## 0. Tool sequence at a glance

```
data_source_discovery  (no ds_id)        -> list sources, find GAWA, check auth
data_source_discovery  (ds_id="GAWA")    -> config + login_link if unauthenticated  [AUTH GATE]
accounts_discovery     (ds_id="GAWA")    -> select GA4 property id ("Property" label)
field_discovery        (ds_id="GAWA")    -> resolve metric + dimension FIELD IDs
data_query             (ds_id="GAWA", …) -> async; returns a schedule_id
get_async_query_results(schedule_id=…)   -> poll until ready, parse rows
```

GA4 facts that drive the calls: `ds_id = "GAWA"`, `has_account_list:true`
(account label **"Property"**), `has_fields:true`, `is_date_range_required:true`,
`data_query` is **async** (must poll). All setting values go inside the **`settings` object**.

---

## 1. Exact Supermetrics tool sequence (runnable)

### Step 1 — Discover the source and auth-gate it

```jsonc
// 1a. List every source + auth status; locate GA4.
mcp__Supermetrics_Marketing_Analytics__data_source_discovery {}
//    -> find the entry with id "GAWA" ("Google Analytics 4").

// 1b. Get GA4's config and auth status (and login_link if needed).
mcp__Supermetrics_Marketing_Analytics__data_source_discovery { "ds_id": "GAWA" }
```

**AUTH GATE.** Inspect `authentication_status` from 1b:
- Anything other than `AUTHENTICATED` (today: `NOT_AUTHENTICATED`) → **STOP.** Surface the
  returned `login_link` to the user, mark the connector **FAIL**, and run the **fallback
  (Section 5)**. Do not call `data_query`.
- `AUTHENTICATED` → continue to Step 2.

Also read from 1b (do not hardcode): `report_types`, `common_settings`, `account_labels`,
and confirm `is_date_range_required:true`.

### Step 2 — Discover the GA4 property

```jsonc
mcp__Supermetrics_Marketing_Analytics__accounts_discovery { "ds_id": "GAWA" }
//    -> GA4 has has_account_list:true; account label is "Property".
//    -> pick the MarketMaster GA4 property id from the returned list.
//       Capture it as <PROPERTY_ID> for Step 4 (if exactly one, auto-select it).
```

### Step 3 — Discover field IDs (metrics + dimensions)

```jsonc
mcp__Supermetrics_Marketing_Analytics__field_discovery { "ds_id": "GAWA" }
```

From the response, resolve the **exact field IDs** below and record them. **Use the returned
field IDs verbatim in `data_query` — never display names.** GA4 field IDs in Supermetrics are
typically lowercase API-style ids; the right-hand notes are the GA4 concept each maps to, so you
can match them in the discovery output:

| Purpose | GA4 concept (match in field_discovery output) | Bind to |
|---|---|---|
| Metric: sessions | `sessions` | `<F_SESSIONS>` |
| Metric: engaged sessions | `engagedSessions` | `<F_ENGAGED_SESSIONS>` |
| Metric: conversions / key events | `conversions` (or `keyEvents`) | `<F_CONVERSIONS>` |
| Metric: event count (for the signup event) | `eventCount` | `<F_EVENT_COUNT>` |
| Dimension: channel grouping | `sessionDefaultChannelGroup` | `<D_CHANNEL>` |
| Dimension: session source | `sessionSource` | `<D_SESSION_SOURCE>` |
| Dimension: session source/medium | `sessionSourceMedium` | `<D_SOURCE_MEDIUM>` |
| Dimension: event name (to isolate signup) | `eventName` | `<F_EVENT_NAME>` |

> The signup conversion: if the signup form fires a GA4 **key event / conversion**
> (e.g. `sign_up`, `generate_lead`, or the MarketMaster-specific event), the cleanest count is
> `<F_CONVERSIONS>` filtered to that event name via `<F_EVENT_NAME>`. If it is only a plain
> event (not marked a key event), count it with `<F_EVENT_COUNT>` + an `eventName` filter
> instead. Confirm the exact event name with whoever instrumented the signup form
> (see `owned-audience-setup.md`); bind it as `<SIGNUP_EVENT>` for the filters below.

### Step 4 — Run the query (async)

Two queries. Setting values (property, fields, filters, date range) live inside `settings`.

**4a. Channel breakdown (baseline by channel).**

```jsonc
mcp__Supermetrics_Marketing_Analytics__data_query {
  "ds_id": "GAWA",
  "ds_accounts": ["<PROPERTY_ID>"],
  "settings": {
    "report_type": "<report_type from Step 1b, e.g. 'analytics'>",
    "fields": [
      "<D_CHANNEL>",
      "<F_SESSIONS>",
      "<F_ENGAGED_SESSIONS>",
      "<F_CONVERSIONS>"
    ],
    "date_range_type": "custom",
    "start_date": "2026-05-25",   // required: GA4 is_date_range_required:true
    "end_date":   "2026-06-23",   // align to the Optimize cycle window
    "sort": [{ "field": "<F_SESSIONS>", "direction": "desc" }],
    "max_rows": 100
  }
}
//  -> returns { schedule_id: "<SCHEDULE_ID_4a>" }
```

**4b. The "AI search" channel slice** — same metrics, filtered to AI source hosts (see
Section 2 for the host list + filter object). This returns ONE consolidated AI-search row's
worth of metrics; group by `<D_SESSION_SOURCE>` if you want per-assistant breakdown.

```jsonc
mcp__Supermetrics_Marketing_Analytics__data_query {
  "ds_id": "GAWA",
  "ds_accounts": ["<PROPERTY_ID>"],
  "settings": {
    "report_type": "<same report_type as 4a>",
    "fields": [
      "<D_SESSION_SOURCE>",      // per-assistant rows; drop this field for a single rolled-up row
      "<F_SESSIONS>",
      "<F_ENGAGED_SESSIONS>",
      "<F_CONVERSIONS>"
    ],
    "date_range_type": "custom",
    "start_date": "2026-05-25",
    "end_date":   "2026-06-23",
    "filter": {                  // AI-search source filter — see Section 2
      "operator": "AND",
      "filters": [
        {
          "field": "<D_SESSION_SOURCE>",
          "operator": "MATCH_REGEX",
          "value": "(?i)(chatgpt\\.com|chat\\.openai\\.com|openai\\.com|perplexity\\.ai|gemini\\.google\\.com|bard\\.google\\.com|copilot\\.microsoft\\.com|bing\\.com/chat|claude\\.ai|anthropic\\.com|you\\.com|poe\\.com|phind\\.com|deepseek\\.com|grok\\.com|x\\.ai|mistral\\.ai)"
          // full regex/host list maintained in Section 2 — keep it in one place
        }
      ]
    },
    "max_rows": 100
  }
}
//  -> returns { schedule_id: "<SCHEDULE_ID_4b>" }
```

**4c. Signup conversions by channel** — isolate the signup event, broken out by channel so you
can see which channels (including AI search) actually drive owned-audience signups.

```jsonc
mcp__Supermetrics_Marketing_Analytics__data_query {
  "ds_id": "GAWA",
  "ds_accounts": ["<PROPERTY_ID>"],
  "settings": {
    "report_type": "<same report_type>",
    "fields": [
      "<D_CHANNEL>",
      "<F_EVENT_NAME>",
      "<F_CONVERSIONS>"           // or <F_EVENT_COUNT> if signup is not a key event
    ],
    "date_range_type": "custom",
    "start_date": "2026-05-25",
    "end_date":   "2026-06-23",
    "filter": {
      "operator": "AND",
      "filters": [
        { "field": "<F_EVENT_NAME>", "operator": "EQUAL", "value": "<SIGNUP_EVENT>" }
      ]
    },
    "max_rows": 100
  }
}
//  -> returns { schedule_id: "<SCHEDULE_ID_4c>" }
```

> Note on filter syntax: `operator`/`value`/`MATCH_REGEX`/`EQUAL` are the canonical Supermetrics
> filter shape, but the **exact** operator tokens and the `filter` vs `filters` key are
> source-specific. Confirm them against `common_settings` / any `filter` schema returned by
> `data_source_discovery(ds_id="GAWA")` in Step 1b and adjust the keys to match before sending.

### Step 5 — Poll for results

`data_query` is async. For each `schedule_id`, poll until ready, then parse rows.

```jsonc
mcp__Supermetrics_Marketing_Analytics__get_async_query_results { "schedule_id": "<SCHEDULE_ID_4a>" }
mcp__Supermetrics_Marketing_Analytics__get_async_query_results { "schedule_id": "<SCHEDULE_ID_4b>" }
mcp__Supermetrics_Marketing_Analytics__get_async_query_results { "schedule_id": "<SCHEDULE_ID_4c>" }
//  Repeat each call until status indicates the result is ready (do NOT treat the first
//  response as final). Then read the rows.
```

---

## 2. The "AI search" source list + regex filter

**Canonical AI-host list** (keep this the single source of truth; extend as surfaces appear):

```
chatgpt.com
chat.openai.com
openai.com
perplexity.ai
gemini.google.com
bard.google.com            # legacy Gemini referrer
copilot.microsoft.com
bing.com/chat              # Copilot surfaced via Bing
claude.ai
anthropic.com
you.com
poe.com
phind.com
deepseek.com
grok.com
x.ai
mistral.ai / chat.mistral.ai
```

**Single regex (case-insensitive)** to match `sessionSource` (or `sessionSourceMedium`). This is
the canonical value to drop into the `data_query` `settings.filter` shown in Step 4b:

```
(?i)(chatgpt\.com|chat\.openai\.com|openai\.com|perplexity\.ai|gemini\.google\.com|bard\.google\.com|copilot\.microsoft\.com|bing\.com/chat|claude\.ai|anthropic\.com|you\.com|poe\.com|phind\.com|deepseek\.com|grok\.com|x\.ai|mistral\.ai)
```

**How to express it as a session source/medium filter inside `data_query` `settings`:**

- Filter on dimension `<D_SESSION_SOURCE>` (`sessionSource`) — or `<D_SOURCE_MEDIUM>`
  (`sessionSourceMedium`) if you want medium too. GA4 typically records these as referrals,
  e.g. `chatgpt.com / referral`, `perplexity.ai / referral`.
- Use a **regex / contains-any** operator so one filter covers every host:

```jsonc
"filter": {
  "operator": "AND",
  "filters": [
    {
      "field": "<D_SESSION_SOURCE>",          // sessionSource field ID from field_discovery
      "operator": "MATCH_REGEX",              // or CONTAINS w/ multiple OR'd clauses if regex unsupported
      "value": "(?i)(chatgpt\\.com|chat\\.openai\\.com|openai\\.com|perplexity\\.ai|gemini\\.google\\.com|bard\\.google\\.com|copilot\\.microsoft\\.com|bing\\.com/chat|claude\\.ai|anthropic\\.com|you\\.com|poe\\.com|phind\\.com|deepseek\\.com|grok\\.com|x\\.ai|mistral\\.ai)"
    }
  ]
}
```

- If the source's filter schema does **not** support regex, fall back to an `OR` group of
  `CONTAINS` clauses, one host per clause:

```jsonc
"filter": {
  "operator": "OR",
  "filters": [
    { "field": "<D_SESSION_SOURCE>", "operator": "CONTAINS", "value": "chatgpt.com" },
    { "field": "<D_SESSION_SOURCE>", "operator": "CONTAINS", "value": "perplexity.ai" },
    { "field": "<D_SESSION_SOURCE>", "operator": "CONTAINS", "value": "gemini.google.com" },
    { "field": "<D_SESSION_SOURCE>", "operator": "CONTAINS", "value": "copilot.microsoft.com" },
    { "field": "<D_SESSION_SOURCE>", "operator": "CONTAINS", "value": "claude.ai" }
    // …one clause per host in the list above
  ]
}
```

Label every row returned by this filtered query as the **"AI search" channel** in the Validate
and Optimize outputs. Because GA4's default channel grouping buckets these as Referral/Organic,
this custom filter is what makes AI traffic show up as its own channel.

---

## 3. Metrics to pull (by channel)

| Output column | GA4 metric (Step 3 field ID) | Notes |
|---|---|---|
| Sessions | `<F_SESSIONS>` (`sessions`) | Volume by channel. |
| Engaged sessions | `<F_ENGAGED_SESSIONS>` (`engagedSessions`) | Quality signal; pair with sessions for engagement rate. |
| Conversions | `<F_CONVERSIONS>` (`conversions` / `keyEvents`) | All key events; narrow to signup via `eventName` filter. |
| **Signup conversions** | `<F_CONVERSIONS>` filtered to `<SIGNUP_EVENT>` | **The headline metric** — owned-audience growth. Use `<F_EVENT_COUNT>` instead if signup is not marked a key event. |

Dimensions: `<D_CHANNEL>` (`sessionDefaultChannelGroup`) for the standard per-channel table;
`<D_SESSION_SOURCE>` (`sessionSource`) for the AI-search slice / per-assistant breakdown;
`<F_EVENT_NAME>` (`eventName`) to isolate the signup event.

**The signup-form conversion specifically:** it is the owned-audience growth number the whole
Optimize loop steers on. Count it as the signup GA4 key event (`<SIGNUP_EVENT>`) broken out by
`<D_CHANNEL>` (Query 4c), so you can attribute signups to each channel — including the
**AI-search channel** (run 4c again with the Section 2 AI-source filter added to get
AI-driven signups). Cross-check this number against the signup form backend's own submission
count (Section 5) — they should be in the same ballpark; a large gap means tracking is broken.

---

## 4. Output shape (for the Optimize loop)

Produce one table the Optimize loop can diff against the previous cycle:

| Channel | Sessions | Engaged sessions | Signup conversions | source |
|---|---|---|---|---|
| Organic Search | … | … | … | `ga4` |
| Direct | … | … | … | `ga4` |
| Referral | … | … | … | `ga4` |
| **AI search** | … (4b) | … (4b) | … (4c + AI filter) | `ga4` |
| … | | | | |

Tag provenance on every row: `source: ga4` for the live path, or `source: ga4-manual` /
`source: utm+form-backend` for the fallback so the Optimize loop knows the data's reliability.

---

## 5. Fallback (GA4 stays unauthenticated) — the current default

GA4 is not authenticated today, so this runs **now**. Either path works without Supermetrics.

### 5a. UTM tags from the engine

The distribution engine **UTM-tags every distributed asset**, so attribute traffic and signups
straight from the UTM parameters — no GA4 needed, just coarser granularity:

- Read UTM-tagged landing hits from wherever the engine logs them (server access logs / the app's
  request log / the redirect service). Group by `utm_source` + `utm_medium` + `utm_campaign`.
- Build the **AI-search channel** by matching `utm_source` (and any referrer captured) against
  the **same host list and regex in Section 2** — keep one shared list so live and fallback agree.
- For signups, join UTM params captured at signup time to the channel.

### 5b. Signup-form backend counts

The signup form's backend has its own **submission counts** — the ground-truth owned-audience
number that does not depend on GA4 at all:

- Pull total signups for the period directly from the signup-form backend
  (see `owned-audience-setup.md` for where the form posts / stores submissions).
- If the form persists the originating UTM (or referrer) with each submission, break signups
  down by channel and apply the Section 2 AI-host match to isolate **AI-search signups**.
- This is the authoritative signup total; reconcile the GA4 `<SIGNUP_EVENT>` conversion count
  against it once GA4 is live.

### 5c. (Optional) Manual GA4 web UI

If GA4 access exists outside Supermetrics, open the GA4 property directly, pull
sessions / engaged sessions / signup conversions by channel, and build the AI-search view by
filtering `sessionSource` on the Section 2 hosts. Transcribe into the Validate report.

Tag all fallback findings `source: utm+form-backend` (or `source: ga4-manual`) so provenance
is explicit and the Optimize loop discounts them appropriately versus authenticated GA4.

---

## 6. Quality bar & gotchas

- **Auth first, always.** If `data_source_discovery(ds_id="GAWA")` is not `AUTHENTICATED`,
  surface the `login_link` and run the fallback — never attempt `data_query`.
- **Field IDs, not names.** Every field in `data_query` must be a field ID from
  `field_discovery`. Display names silently fail.
- **Everything in `settings`.** Property, fields, filters, and the date range go inside the
  `settings` object — not at the top level. (`ds_accounts` is the exception: pass the property
  id there, not in `settings`.)
- **GA4 needs a date range** (`is_date_range_required:true`) — omitting it errors. Align the
  window to the Optimize cycle.
- **`data_query` is async** — always poll `get_async_query_results` per `schedule_id`; the first
  response is not the data.
- **Verify filter syntax against discovery.** The `filter` object shape and operator tokens
  (`MATCH_REGEX`, `CONTAINS`, `EQUAL`) are source-specific — confirm against the GA4 config from
  `data_source_discovery(ds_id="GAWA")` before sending; fall back to OR'd `CONTAINS` if regex is
  unsupported.
- **Keep the AI-host list current (Section 2).** New assistants / changed referrer domains will
  silently drop AI traffic out of the channel. One shared list feeds both live and fallback.
- **Only the five `mcp__Supermetrics_Marketing_Analytics__*` tools** above are used here — never
  invent tool names.

> **Cost of staying blocked:** until GA4 is authenticated, the Optimize loop has no real GA4
> numbers and leans on the coarser UTM + form-backend fallback. The single fix is the user
> clicking the `login_link` once for source `GAWA`; do that and the live path above runs as-is.

# Keyword & AI-citation research (Ahrefs / Semrush) — Distribution Engine Playbook

> **Engine mode(s):** Diagnose — front-end research that shapes a pillar (keyword demand, intent clustering, and AI-citation / share-of-voice signal that informs what to write and how to frame it for AI Overviews).
> **Live status (validated 2026-06-23):** FAIL (plan) — BOTH Ahrefs and Semrush MCP access are blocked on the currently connected plans; Diagnose must run on the manual fallback until a plan is upgraded.

## What this connector is for
Use this connector during **Diagnose** to ground a content pillar in real demand and real
AI-citation behavior, not guesswork. It answers three questions:

1. **What are people searching?** — keyword volume, difficulty, matching/related terms, intent.
2. **Who gets cited?** — which domains/pages AI assistants and AI Overviews quote for the
   target questions (share-of-voice), so the pillar can be framed to win those citations.
3. **What's the competitive surface?** — who already ranks / is referenced, and the gap to close.

If this connector is live, Diagnose produces a defensible keyword + citation brief. If it is
blocked (current state), Diagnose still runs, but on judgement + manual research only — see the
cost note at the bottom and scope client offers accordingly.

## Primary path (live)
This path is **NOT currently available** (plan-gated). It is documented so the engine can switch
to it the moment a plan is upgraded.

  - **Exact MCP tools (Ahrefs):**
    - Gate check / health: `mcp__Ahrefs__subscription-info-limits-and-usage`
    - Keyword research: `mcp__Ahrefs__keywords-explorer-overview`,
      `mcp__Ahrefs__keywords-explorer-matching-terms`,
      `mcp__Ahrefs__keywords-explorer-related-terms`
    - AI-citation / AI-Overview share-of-voice: the `mcp__Ahrefs__brand-radar-*` family
      (e.g. `mcp__Ahrefs__brand-radar-sov-overview`,
      `mcp__Ahrefs__brand-radar-cited-domains`,
      `mcp__Ahrefs__brand-radar-cited-pages`,
      `mcp__Ahrefs__brand-radar-ai-responses`)
    - Competitive surface: the `mcp__Ahrefs__site-explorer-*` family
      (e.g. `mcp__Ahrefs__site-explorer-organic-keywords`,
      `mcp__Ahrefs__site-explorer-top-pages`)
    - Last-resort free DR lookup only: `mcp__Ahrefs__public-domain-rating-free`
  - **Exact MCP tools (Semrush):**
    - Gate check: `mcp__Semrush__projects_research`
    - Discovery tools: `mcp__Semrush__keyword_research`, `mcp__Semrush__organic_research`,
      `mcp__Semrush__overview_research`
    - Report execution: `mcp__Semrush__get_report_schema`, `mcp__Semrush__execute_report`

  - **Step-by-step (numbered):**
    1. **Gate Ahrefs.** Call `mcp__Ahrefs__subscription-info-limits-and-usage`. If it returns
       `{"error":"Insufficient plan"}` (the 2026-06-23 result), the rich Ahrefs tools are
       unavailable — do NOT attempt them; skip to the Semrush gate, then the fallback.
    2. **If Ahrefs is live:** run `mcp__Ahrefs__keywords-explorer-overview` on the seed term for
       volume/difficulty, then `mcp__Ahrefs__keywords-explorer-matching-terms` and
       `mcp__Ahrefs__keywords-explorer-related-terms` to expand the cluster.
    3. **AI-citation pass (Ahrefs live):** use the `mcp__Ahrefs__brand-radar-*` family to read
       share-of-voice, cited domains, and cited pages for the target prompts. This is the signal
       that tells you who AI assistants quote — feed it into the pillar's framing and FAQ.
    4. **Competitive surface (Ahrefs live):** use `mcp__Ahrefs__site-explorer-*` on the top
       competitors to map their ranking keywords and top pages; identify the gap.
    5. **Gate Semrush.** Call `mcp__Semrush__projects_research`. If it returns the
       "plan does not include MCP access" notice (the 2026-06-23 result), Semrush is gated —
       skip to the fallback.
    6. **If Semrush is live:** start with a discovery tool (`mcp__Semrush__keyword_research`,
       `mcp__Semrush__organic_research`, or `mcp__Semrush__overview_research`) to identify the
       report you want, then call `mcp__Semrush__get_report_schema` to learn its required
       parameters, then `mcp__Semrush__execute_report` to pull the data. Always follow
       discovery → `get_report_schema` → `execute_report`; never call `execute_report` blind.
    7. Even with one provider live, cross-check volumes between Ahrefs and Semrush where both
       are available — they disagree, and the disagreement is itself signal.

## Fallback path (when the live path is unavailable)
This is the **current default** for Diagnose. It keeps keyword + AI-citation research functional
with zero paid tools. Do all of the following:

1. **Demand harvesting (free):**
   - Type the seed term into Google and record the **autocomplete** suggestions.
   - Open a SERP and scrape the **"People Also Ask"** box; expand a few questions to fan out
     more PAA entries. These are real intent phrases.
   - Run the seed through **free AnswerThePublic** for question/preposition/comparison variants.
2. **Volume/priority (proxy):** without API volumes, rank candidate terms by how often they
   recur across autocomplete + PAA + AnswerThePublic, plus obvious commercial intent. Mark these
   as *estimated*, not measured.
3. **AI-citation / share-of-voice (manual, replaces Brand Radar):**
   - Ask the **target question** to ChatGPT, Perplexity, and Gemini (and Copilot if available).
   - Record **which sources each one cites** for the answer. The overlap across assistants
     approximates the cited-domains / share-of-voice that `mcp__Ahrefs__brand-radar-*` would give.
   - Inspect the live Google **SERP and AI Overview** for the term and note who is referenced.
4. **Output the same brief shape** the live path would (keyword cluster + intent + who-gets-cited
   + gap), but flag every number as manually estimated.

> Note: `mcp__Ahrefs__public-domain-rating-free` may still work even while the plan is gated.
> Treat it strictly as a **last-resort DR lookup for a single domain** — it is NOT a keyword
> source and does NOT replace any of the research above.

## Inputs it needs  /  Outputs it produces
**Inputs**
- Seed keyword(s) / topic for the pillar.
- Target audience + market (country/language) for intent and localization.
- The specific **questions** the pillar should answer (drives the AI-citation pass).
- Competitor domains, if known.

**Outputs**
- A prioritized keyword cluster with intent labels (measured if live, estimated if fallback).
- A who-gets-cited map for the target questions (Brand Radar if live; assistant-cited sources
  if fallback) — the input to AI-Overview-friendly framing.
- A competitive gap summary.
- A clear provenance tag on every figure: `source: ahrefs|semrush|manual-estimate`.

## Quality bar & gotchas
- **Never invent tool names.** Only the `mcp__Ahrefs__*` and `mcp__Semrush__*` names above exist.
- **Always gate before pulling.** Ahrefs `Insufficient plan` and Semrush's "no MCP access" notice
  are hard stops — burning calls against a gated plan wastes turns and produces nothing.
- `mcp__Ahrefs__public-domain-rating-free` working does NOT mean the plan is upgraded; do not
  infer keyword-tool access from it.
- Manual-estimate volumes must be labeled as such in the brief; do not present them as Ahrefs/
  Semrush numbers.
- The AI-citation pass is time-sensitive — assistant citations shift; date-stamp the findings.
- Semrush flow is strictly discovery → `get_report_schema` → `execute_report`; schema first.

## How to validate it (a concrete check the engine can run)
1. Call `mcp__Ahrefs__subscription-info-limits-and-usage`.
   - If it errors (e.g. `{"error":"Insufficient plan"}`) → **Ahrefs = FAIL**.
2. Call `mcp__Semrush__projects_research`.
   - If it returns the "plan does not include MCP access" notice → **Semrush = FAIL**.
3. If **both** fail (current state, 2026-06-23) → mark the connector **FAIL** and have the engine
   **switch to the manual fallback automatically** — do not block Diagnose.
4. To unblock: upgrade Ahrefs to an API/MCP-enabled plan, and/or buy Semrush MCP access at
   <https://www.semrush.com/mcp-access> (traffic analytics:
   <https://www.semrush.com/analytics/traffic/trends-api>). Re-run steps 1–2 to confirm PASS.

> **Cost of staying blocked:** with this connector down, **Diagnose runs on judgement + manual
> research only** — no measured volumes, no Brand Radar share-of-voice. Quality drops and effort
> rises. Say this to the client up front and **scope offers accordingly** rather than implying
> tool-grade keyword data is in the deliverable.

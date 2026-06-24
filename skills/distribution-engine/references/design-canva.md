# Design / carousels — Canva — Distribution Engine Playbook

> **Engine mode(s):** Atomize (turn a slide outline into a real carousel), Distribute
> **Live status (validated 2026-06-23):** PASS (with caveat) — Canva is authenticated, but the account has 0 brand kits configured, so output is off-brand until a brand kit is added.

## What this connector is for
Turn the engine's **Atomize** slide outline into a finished, postable **carousel** — a multi-slide visual asset for LinkedIn and Instagram. Canva generates the design from a prompt or structured spec, lets you inspect it, applies brand identity (when a brand kit exists), resizes it into platform variants, and exports a PNG set or PDF the **Distribute** mode can publish.

Use this connector whenever the deliverable is a slide-based carousel or a single static graphic that benefits from Canva templates and brand assets.

## Primary path (live)
  - Exact MCP tools: `mcp__Canva__generate-design`, `mcp__Canva__generate-design-structured`, `mcp__Canva__get-design-content`, `mcp__Canva__get-design-pages`, `mcp__Canva__get-design-thumbnail`, `mcp__Canva__list-brand-kits`, `mcp__Canva__search-brand-templates`, `mcp__Canva__create-design-from-brand-template`, `mcp__Canva__get-export-formats`, `mcp__Canva__export-design`, `mcp__Canva__resize-design`, `mcp__Canva__comment-on-design`
  - Step-by-step (numbered):
    1. **Check brand identity first.** Call `mcp__Canva__list-brand-kits`. If it returns a brand kit, prefer it. If it returns an empty list (the current 2026-06-23 state), proceed but raise the brand caveat (see Gotchas) — the carousel will be generic, not on-brand.
    2. **Pick a starting point.** If a relevant brand template exists, call `mcp__Canva__search-brand-templates`, then `mcp__Canva__create-design-from-brand-template` to start on-brand. Otherwise, generate net-new.
    3. **Generate the carousel.** Prefer `mcp__Canva__generate-design-structured` when you can pass a per-slide spec (one object per slide from the Atomize outline). Fall back to `mcp__Canva__generate-design` with a single descriptive prompt when a structured spec isn't available. Encode: 6–10 slides, one idea per slide, a strong slide-1 hook, and a final CTA slide pointing to the signup form.
    4. **Inspect the result.** Call `mcp__Canva__get-design-pages` to confirm slide count and order, `mcp__Canva__get-design-content` to verify the copy landed on the right slides, and `mcp__Canva__get-design-thumbnail` for a quick visual sanity check. Fix any slide that is overcrowded or off-message before exporting.
    5. **(Optional) Make platform variants.** Use `mcp__Canva__resize-design` to produce the right ratio per channel (e.g. 1080×1350 portrait for Instagram, square or portrait for LinkedIn).
    6. **Export for posting.** Call `mcp__Canva__get-export-formats` to see what's available for the design, then `mcp__Canva__export-design` to render a **PNG set** (preferred for native carousels) or a **PDF**. Capture the exported file(s) and the Canva design URL.
    7. **(Optional) Leave a note.** Use `mcp__Canva__comment-on-design` to flag follow-ups for a human reviewer (e.g. "no brand kit applied — review colors").
    8. **Hand off to Distribute** with the exported PNG/PDF and the design URL.

## Fallback path (when the live path is unavailable)
- **Missing scope error** — if any tool returns `Missing scopes: [brandkit:read]` (or a similar scope error), instruct the user to **disconnect and reconnect the Canva connector** so a fresh token is minted with the correct scopes, then retry from step 1.
- **No brand kit (current state)** — the live path still runs; treat this as the primary quality risk rather than a hard failure. Generate the carousel, but mark it "off-brand / needs brand kit" in the handoff and recommend the user add a brand kit (colors, logo, fonts) before client-grade output.
- **Generation unavailable** — if `generate-design`/`generate-design-structured` fail, fall back to `mcp__Canva__search-brand-templates` + `mcp__Canva__create-design-from-brand-template` to start from an existing template, then edit and export.
- **No Canva at all** — emit the carousel as a structured slide outline (text + per-slide layout notes) so a human can build it manually or another design connector can pick it up. Do not block the rest of the pipeline.

## Inputs it needs  /  Outputs it produces
- **Inputs:** the carousel **slide outline** produced by the engine's Atomize step (`atomize.py` emits a slide outline) — ideally one entry per slide with a headline and supporting line; the signup-form URL for the CTA slide; optionally a brand kit or brand template ID.
- **Outputs:** an **exported carousel** (a PNG set or a PDF) ready for LinkedIn/Instagram, **plus the Canva design URL** for editing or review. Optionally, resized platform variants.

## Quality bar & gotchas
- **6–10 slides, one idea per slide.** More than 10 loses the reader; fewer than 6 rarely justifies a carousel.
- **Big, readable type.** Mobile-first — assume the slide is viewed small. Avoid dense paragraphs.
- **Strong slide-1 hook.** The first slide decides whether anyone swipes. Lead with the payoff or tension, not a title card.
- **Final slide = CTA to the signup form.** Always close with the signup-form link/action.
- **Brand risk (top gotcha):** with 0 brand kits configured, output uses generic Canva styling and will be **off-brand**. Flag this on every handoff and recommend adding a brand kit before client-grade delivery.
- **Scope errors:** `Missing scopes: [brandkit:read]` means reconnect the connector — it is an auth issue, not a content issue.
- **Always inspect before export.** Generation can drop or merge copy; confirm with `get-design-pages` / `get-design-content` first.

## How to validate it (a concrete check the engine can run)
Produce **ONE** real carousel from a sample slide outline and export it:
1. `mcp__Canva__list-brand-kits` (record whether a brand kit exists).
2. `mcp__Canva__generate-design-structured` (or `generate-design`) from the sample outline.
3. `mcp__Canva__get-design-pages` to confirm slide count.
4. `mcp__Canva__get-export-formats` then `mcp__Canva__export-design`.
5. Record the **design URL** and the **exported file**.

**PASS** if it generates and exports. (Note the no-brand-kit caveat in the result even on PASS.)

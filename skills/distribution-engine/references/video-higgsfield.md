# Short-form video — Higgsfield — Distribution Engine Playbook

> **Engine mode(s):** Atomize (turn a script into a clip), Distribute
> **Live status (validated 2026-06-23):** PASS — Higgsfield is live on the Ultra plan with ~2,044 credits.

## What this connector is for
Turn the engine's **Atomize** short-form video script/storyboard into a finished **vertical short-form clip** for Reels / TikTok / Shorts. Higgsfield generates the video, reframes it to 9:16, can add a voiceover and upscale it, and runs a virality QA pass before the **Distribute** mode publishes. Use this connector whenever the deliverable is a short, hook-driven video clip.

## Primary path (live)
  - Exact MCP tools: `mcp__Higgsfield__balance`, `mcp__Higgsfield__models_explore`, `mcp__Higgsfield__generate_video`, `mcp__Higgsfield__generate_image`, `mcp__Higgsfield__generate_speech`, `mcp__Higgsfield__generate_audio`, `mcp__Higgsfield__motion_control`, `mcp__Higgsfield__reframe`, `mcp__Higgsfield__upscale_video`, `mcp__Higgsfield__virality_predictor`, `mcp__Higgsfield__job_display`
  - Step-by-step (numbered):
    1. **Check credits first.** Call `mcp__Higgsfield__balance`. Credits are finite (~2,044.95 on the `ultra` plan as of 2026-06-23). Confirm there's enough headroom before spending — generation and especially upscales cost credits.
    2. **Pick the right model.** Call `mcp__Higgsfield__models_explore` with `action:'recommend'` plus the goal/script, and use its recommendation **before** generating. Do not skip this — model choice drives quality and cost.
    3. **Generate the clip.** Call `mcp__Higgsfield__generate_video` with the Atomize script/storyboard. Optionally first create a thumbnail or first frame with `mcp__Higgsfield__generate_image`, and use `mcp__Higgsfield__motion_control` when the shot needs directed camera/subject motion.
    4. **Handle long jobs.** Generation may return `{task_id, status}` instead of a finished asset. Poll status with `mcp__Higgsfield__job_display` (or a `show_generations`-style status call) until the job completes; do not proceed on a pending task.
    5. **Reframe to vertical.** If the output isn't already 9:16, call `mcp__Higgsfield__reframe` to make it vertical for shorts/Reels/TikTok.
    6. **(Optional) Voiceover / audio.** Add narration with `mcp__Higgsfield__generate_speech` and/or music/SFX with `mcp__Higgsfield__generate_audio`.
    7. **(Optional) Upscale.** Use `mcp__Higgsfield__upscale_video` to 2K/4K — but only after the QA pass below confirms the clip is worth the credits.
    8. **QA for virality.** Call `mcp__Higgsfield__virality_predictor` to score hook strength / retention risk **before publishing** (and before spending on upscales). If the score is weak, revise the script or first 2 seconds and regenerate.
    9. **Hand off to Schedule/Distribute** with the clip and its virality score.

## Fallback path (when the live path is unavailable)
- **Low / out of credits** — if `mcp__Higgsfield__balance` is too low, skip optional steps (upscale, extra audio) and generate a single lean clip; or defer to the user to top up. Never silently burn the remaining balance on speculative variants.
- **Job stuck pending** — if `mcp__Higgsfield__job_display` shows a task not completing, surface the `task_id` and status rather than blocking the pipeline; retry once before escalating.
- **Wrong model / poor output** — re-run `mcp__Higgsfield__models_explore` with a refined goal and pick a different model before regenerating.
- **Connector down** — emit the finished script + storyboard (with shot notes, captions text, and CTA) so another video connector or a human can produce the clip. Do not block the rest of the run.

## Inputs it needs  /  Outputs it produces
- **Inputs:** the short-form **video script / storyboard** produced by the engine's Atomize step (hook, beats, on-screen captions, CTA); the signup-form action for the end card; optional VO script and target aspect ratio (default 9:16).
- **Outputs:** a **vertical short-form clip** (optionally with baked captions and voiceover), **plus a virality score** from `mcp__Higgsfield__virality_predictor`, and the output asset URL for the Schedule/Distribute step.

## Quality bar & gotchas
- **Hook in the first 1–2 seconds.** If the opening doesn't stop the scroll, nothing else matters — front-load the payoff or tension.
- **Length 15–40s.** Long enough to deliver one idea, short enough to retain.
- **Captions baked in.** Most viewing is muted — burn in captions so the clip works without sound.
- **End card CTA to the signup form.** Always close with the signup action.
- **Credits are finite.** Run `mcp__Higgsfield__virality_predictor` **before** spending credits on `mcp__Higgsfield__upscale_video` — don't upscale a clip that won't perform.
- **Poll long jobs.** Treat `{task_id, status}` responses as pending; never hand off an unfinished task.
- **Pick the model first.** Always `models_explore(action:'recommend')` before `generate_video`.

## How to validate it (a concrete check the engine can run)
Generate **ONE** real short clip from a sample script:
1. `mcp__Higgsfield__balance` (confirm credits).
2. `mcp__Higgsfield__models_explore` with `action:'recommend'`.
3. `mcp__Higgsfield__generate_video` from the sample script; poll `mcp__Higgsfield__job_display` until done.
4. `mcp__Higgsfield__reframe` to 9:16 if needed.
5. `mcp__Higgsfield__virality_predictor` for a score.
6. Record the **output URL** and the **virality score**.

**PASS** if it generates.

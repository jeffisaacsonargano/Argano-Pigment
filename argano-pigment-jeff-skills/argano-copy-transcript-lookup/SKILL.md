---
name: argano-copy-transcript-lookup
description: "Answering what did someone say about X and turning a project call into a model-update plan, from Google Meet Notes by Gemini docs in Drive - search recipe (owned plus shared), reading the FULL transcript in a subagent, verbatim quotes with speaker and timestamp, Gemini quirks, plan-only call plans. Use when the user asks about a call, meeting, transcript, what was decided, who agreed, or wants a plan from a call."
---

# Call transcripts: lookups and call plans

Read-only. Never write to Drive or the model from this skill.

## Find the doc

- "Call transcripts" / "recordings" usually mean the Google Meet **"Notes by Gemini"** Google Docs: a summary plus the full transcript.
- Drive connector (load with ToolSearch, e.g. "google drive search_files"): `search_files` with `title contains 'Notes by Gemini'`, plus `fullText contains '<term>'` and a `modifiedTime` range.
- **Run the search twice: owned, and with `sharedWithMe = true`.** Calls hosted by someone else only show up shared.
- Keep a list of the project's recurring calls and known doc ids in a reference file once you've found them, so later lookups are one step.

## Read it properly

- **Read the full transcript, not the summary.** Decisions often never reach the Gemini summary.
- Transcripts are large: hand each doc (or ~3 docs) to a subagent with the exact question, and ask for verbatim quotes back.
- Gemini quirks: domain terms get misheard ("GAAP" is often written "gap"; "Claude" comes out as cloud / clawed). Search for the likely misspellings too. Speaker labels can be wrong when people talk over each other; say so if a quote's speaker looks off.

## Answer format ("what did X say")

- Lead with the answer in one or two lines.
- Then the quotes: **word for word**, each with call name, date, speaker and timestamp (`<call name> <date>, <speaker>, ~00:06`), plus the doc link or id.
- Say whether it was a decision, a preference, or just discussion, and whether a later call changed it (check newer calls; later usually wins).
- If nothing turned up, say which calls and terms you searched.

## Call → model-update plan

For a call the user wants planned, draft every model change discussed so they can approve it. **Plan only: no model writes until the user says go**, and "go on 1–3" means only those items.

Write `<project plans folder>/Call Plans/<YYYY-MM-DD> <meeting>.md`:
- one numbered item per model change, each with:
  - who asked, with the timestamp and a short quote
  - target app, folder and block, and the formula, query or view change
  - in scope? (check the project's scope and deferrals)
  - dependencies or open questions; flag items where the call didn't reach a firm decision
  - whether to run a regression check before and after
- a separate list of non-model action items (who owes what) and decisions that need no build.

## Changelog
- 2026-10-30: created as a client-neutral copy; call names, people and doc ids removed.

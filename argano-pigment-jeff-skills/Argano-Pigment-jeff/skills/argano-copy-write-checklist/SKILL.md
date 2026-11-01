---
name: argano-copy-write-checklist
description: "Pre- and post-flight checklist for any write to a Pigment model through the MCP connector - scope creep, new blocks when existing ones would do, renames that break readers, unasked-for name prefixes, bulk-approved delete batches, import safety, dev vs production, and claiming done without reading back. Use before any create_, update_, delete_, move_blocks, set_metric_input or add_list_items call, and before saying anything is done or unchanged."
---

# Pigment write checklist

These are the habits a modeler most often has to correct when Claude writes to Pigment. Run through them at write time.

## Project setup (once per client)

Confirm and record in the project's memory:
- which workspace(s), apps and connectors are in scope, and which apps are off-limits (legacy models, other teams' apps)
- whether structure goes development → Test & Deploy only, and whether production takes any direct data writes (inputs, list items) and with what approval
- the sandbox folder convention for proving structural changes first
- the constants folder and naming conventions (see `argano-copy-formula-rules`)
- every downstream reader that depends on block, view or board names (Claude apps, scripts, warehouse exports, spreadsheets)

## Before writing
1. **Right app and connector.** Structure (blocks, formulas, views, boards) is built in development and reaches production only through the client's deploy. Search results can include library blocks shared in from other apps; make sure the block you edit is owned by the target app. Never seed production data from development.
2. **Scope = the approved items, nothing extra.**
   - No repointing, description rewrites or "while I'm here" check metrics.
   - List extras as suggestions instead.
3. **Reuse before you create.**
   - Search for an existing metric, variable or constant that already does the job.
   - Give each new block a one-line justification in the preview. "Why do we need a new metric?" is the most common pushback.
   - Prefer the simpler design.
4. **Placement.**
   - Put new blocks next to their siblings.
   - Constants go in the constants folder.
   - No new subfolders unless asked.
5. **Naming.**
   - Don't add prefixes like double-hash or "zz" to names unless asked. If a name collision forces a temporary rename, say so in the preview.
   - Boolean metric names end in "?".
6. **Renames.** Before renaming any block, view or board, search every downstream reader for the old name (apps, scripts, skills, export configs, spreadsheets). Name-based readers break silently.
7. **Preview** with app, folder, block, and the formula or query text. Wait for "go" unless it's a small direct instruction.
   - Structural changes to financial statements are proven first in a sandbox folder.
   - Formulas: run the `argano-copy-formula-rules` linter.
   - Views and boards: follow `argano-copy-board-view-rules`.
   - About to say something can't be done or is "UI-only"? Check `argano-copy-pigment-capabilities` first.
8. **Risky change** (deletion, formula rewrite on the reporting path, mapping change, cutover)? Take a before-snapshot of the key totals (a regression check).
   - **Deletes go as one bulk-approved batch.** Preview the full list (ids, readers-first order, dependency re-check), and one "go" covers that whole list: run it without asking item by item. Anything not on the previewed list needs a new go.
9. **Changing an access-rights metric's dimensions drops its Data Access Rights rules.** Note it in the preview and re-check afterwards.
10. **Imports from a warehouse.**
    - Select source rows with an allowlist (`WHERE scenario IN (…)`), never a growing `!=` exclusion chain: an exclusion list silently pulls in whatever new value appears upstream.
    - Never "Clear All" on a target whose source can drop rows; a clear-all import can halve a list overnight.
    - Show the user the SQL plus the row count and total per group it would load before saving the config.

## After writing
1. **Read back every block you changed** (`fetch_metric_data`, `get_views`, `get_list_items`) and show the result.
   - A successful write call or `validate_formula` is not verification.
   - Don't say "still live", "didn't move", "hidden" or "new" without a read that proves it.
2. **Key totals must equal their "before" values** unless the change was meant to move them.
3. **Report in this shape:**
   - what changed (names and ids)
   - where
   - how it was verified, with the numbers
   - anything **not** verified, or left for the user (UI-only formatting, borders, Metrics pivot position)

## Changelog
- 2026-10-30: created as a client-neutral copy; project ids and environment rules replaced by "Project setup"; warehouse import rules added.

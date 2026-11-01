---
name: argano-copy-model-harvest
description: "One dated, read-only harvest of a Pigment model (every block with formula, dependencies, tables, folders, boards, views with pivots, Frame bindings) that feeds model maps, lineage diagrams, deletion scans and model reviews - which reads to make, how subagents make them, where to keep the raw pull, and the connector's blind spots. Use whenever the user asks for a model map, lineage, dependency diagram, what reads a block, a full inventory or audit of an app, or before a deletion scan."
---

# Pigment model harvest

Re-pulling a model from scratch for every tool wastes hours. Do **one pull, dated, reused by every tool**. Read-only. Pull development unless the user asks for production.

**Reuse first:** if a harvest since the last structural change exists in the project's data folder (e.g. `data/model-harvest/<date>/`), use it. Check the audit trail (`ModelChange`, `Delete`, `FormulaUpdate`) since its date to decide.

## 1. The reads (superset for every tool)

Have subagents (a smaller model is fine; split by app, and split long paged lists) make, for each app:
- `search_metrics_and_lists` with `showDetails=true`, `includeSharedBlocks=false`, every page (formulas, dimensions, folders, `usedInBoards`)
- `search_tables`, `search_folders`, `search_boards`, `search_frames`
- `search_views`, every page; then `get_views` on the view ids in batches (pivots, incl. joined pivots)
- `get_metric_dependencies` per metric with `withinApplicationId: null` (cross-app readers)
- `get_metric_to_metric_copy_configs` (snapshot / copy sources and targets)

Tell each subagent:
- read-only; make every call even if the result is large (the harness spills it to a file a script can read)
- no summaries of results
- distinct file names if it writes anything (collisions overwrite pages)
- **copy ids from files, never retype them**: subagents mangle id tails
- Wait for every helper to finish before parsing; an early stop leaves silent gaps.

## 2. Keep the raw pull

Copy the subagent transcripts and any spilled tool-result files into `<project data folder>/model-harvest/<YYYY-MM-DD>/`. Temp copies get cleaned up; this is the dated record. Add a `README.md`: date, apps, which reads, known errors.

## 3. Parse with scripts, not by reading

Write (or reuse) small standard-library scripts that pick the tool calls they need out of the transcripts and ignore the rest, so raw rows never fill the main context. One transcript set should feed every tool: model map, deletion scan, model review.

## 4. Blind spots: check these by hand

"No dependents" is not proof a block is unused:
- **Joined view pivots:** views that pivot through a mapping metric (`mappingMetricIds` in `get_views`) depend on it, but `get_metric_dependencies` doesn't list them.
- **List-property formulas:** a list property formula that reads a block isn't a metric dependency. Scan list formulas by name.
- **`get_metric_dependencies` on a list id** returns "Entity not found": call it for metrics only; resolve lists through formula text.
- **`get_views` fails whole batches** when one view has a property column the API can't resolve, or one id is malformed. Use batches of ~20, retry failures one at a time, and record views that still fail in the README.
- **Not visible at all:** app variables, import configs' scope (`referringImportConfigurations` comes back empty), access rights. Say so in any "what reads X" answer.
- **Frames:** a Frame bound to a block breaks when the block (or anything in its chain) is deleted; treat Frame bindings as roots.
- **Folders:** `delete_block` on a folder moves its contents to the app root.
- **Formula links are name-matched** (quoted `'Name'` tokens), not ids. Two blocks with the same name in different apps resolve to the block's own app first.

## 5. Report

Counts per app and type (metrics, lists, tables, boards, views, frames), the harvest folder path, read errors and what they hide, and the blind spots that matter for the user's question.

## Changelog
- 2026-10-30: created as a client-neutral copy; app ids and project tool paths removed.

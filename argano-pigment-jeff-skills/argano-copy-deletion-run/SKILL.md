---
name: argano-copy-deletion-run
description: "How to run a block cleanup (deletion batch) in a Pigment model - reachability scan, keep list, dependency and reader re-checks (copy configs, Frames, joined view pivots, external readers, list-formula readers), regression check before and after, ONE bulk-approved delete batch in readers-first order, read-back, recording what was deleted, and the deploy hand-off. Use whenever the user says delete, clean up or remove unused blocks, asks what can be deleted, or mentions orphans or tidying folders."
---

# Pigment deletion run

Goal: remove dead blocks without moving any reported number. Deletes happen in **development**; production follows through the client's Test & Deploy. Never scan or delete in apps the project has marked off-limits.

Keep a running record per project (in memory or a shared doc): batches done, what's open, and the **keep list** of blocks the user wants kept even if they look unused. Read it before every run.

## 1. Scan (when the user asks "what can we delete")

1. Pull the model read-only (see `argano-copy-model-harvest`): blocks, tables, views with pivots, folders, frames, boards, dependencies. Use subagents in batches, with distinct output file names (parallel subagents writing the same file collide).
2. Classify each block: it's **live** if a root reaches it. Roots are boards in use, imports and copy configs, app variables, automations, access rights, Frame bindings, external readers, other apps, and the keep list.
3. Write a candidates file with tiers (A safe, B needs a look, C the user's call) and ids.

**The scan is blind in places.** Re-check these by hand for every candidate:
- **List-formula readers:** list properties whose formulas read the block. `get_metric_dependencies` misses them; search list formulas by name.
- **Joined view pivots:** views that pivot through mapping metrics (`mappingMetricIds` in `get_views`) depend on them, but dependency tools don't report it.
- **Copy configs:** `get_metric_to_metric_copy_configs` before touching any snapshot/source block.
- **Frames:** a Frame bound to a block breaks when the block goes. Check bindings; the user decides which Frames still matter.
- **External readers:** regression checks, review pages, Claude apps and skills, and views read by name (API exports, audit views, flat exports). Grep the project's app and skill folders for the name.
- **Audit trail:** someone may have written to the block recently. Check `get_audit_trail` on the full id set.

## 2. Preview (one list, one go)

Show the full batch: name, id, app, folder, why it's dead, and the **delete order: readers first** (views and boards → downstream metrics → the block → orphaned upstream → empty folders). Flag inputs with data and anything shared via library separately.

**One "go" covers the whole previewed list.** Run it without asking per item. Anything not on the list needs a new go.

## 3. Run

1. **Regression check before**: snapshot the key totals (financial statements, ingest counts), label `pre-<batch>`.
2. **Delete** in waves, readers first: `delete_views` for views; `delete_block` for metrics, tables, lists and folders. Boards and app variables go through Chrome (routes in `argano-copy-pigment-capabilities`).
   - **Read a folder back empty before deleting it.** `delete_block` on a Folder moves any leftover contents to the app root.
   - "Not found" may mean the user already deleted it in the UI; confirm with the audit trail and count it as gone.
3. **Read back**: search each id (gone), `list_issues` in each app (no new errors).
4. **Regression check after** (`post-<batch>`, compared against pre). If only live data moved (new submissions or imports landed mid-run), confirm that in the audit trail before blaming the deletes.

## 4. Record it

Update the project's deletion record: flip each row to "Deleted" (including blocks found already gone), add new keeps, note what's left.

## 5. Report and hand off

- Counts by type, ids in a collapsed list or the scan data file, the regression verdict (pre → post), the `list_issues` result.
- Remind the user that production still has the blocks until the next Test & Deploy, and offer a production check after it.

## Changelog
- 2026-10-30: created as a client-neutral copy; project ids, tools and records removed.

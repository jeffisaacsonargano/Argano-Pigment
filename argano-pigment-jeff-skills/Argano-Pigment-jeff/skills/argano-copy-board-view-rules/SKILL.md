---
name: argano-copy-board-view-rules
description: "Board and view conventions for Pigment models - which view to edit, data on first open, labels, column and selector order, version selectors, number formats, submission and validation board layout, names frozen after go-live. Load before any create_view, update_view, delete_views, save_draft_views, create_board, update_board or update_board_widgets call, when planning a board layout, or when a view shows nothing or looks wrong."
---

# Pigment board and view rules

These describe what a good result looks like. Where a client's own stakeholders have stated preferences, record them in the project's memory and let them win.

## Which view to touch
1. **Default views can be edited**, with the usual preview. If the user has made a "… Copy 1" for the task at hand, work there.
2. **Start new financial-statement-style tables from a duplicate of an existing formatted table.** `duplicate_block` on a Table keeps its views, formatting and calculated items. Views built from scratch can lose the expand behavior on calculated lines.
3. **Don't make a new, unshared view in one app that a board in another app depends on.** It breaks the board for users without access.

## Every view must show data on first open (default, unasked)
Do all of this by default on every new or rebuilt view, and say in the preview that it's done:
- Put the driving dimensions in rows: version and accounts (or the line items) in rows. Financial-statement views put Metrics first in the row pivots.
- Hide empty rows and columns: `update_view_filters` → `sparseSettings: {showEmptyRows:false, showEmptyColumns:false}`.
- Version page selector: all versions or a variable, **never a fixed version**. Fixed defaults break when that version is deleted. Constants can't drive page selectors.
- **Read it back.** Use `get_views` plus a data fetch to prove values render. Don't claim "hidden" or "showing" without checking.

## Labels and display
- **Board value labels are plain business names:** no code prefixes, no (=)/(+)/(−), no unit suffixes. Block names keep their codes. Label edits create drafts; preview them and save on the user's OK.
- **Member display:** agree one convention per client (e.g. ledger accounts "ID:Name", other dimensions "ID Name"). Exports carry IDs.
- **Number formats:** agree them once (e.g. millions without "M", negatives in parentheses, % to one decimal).
  - These formats are per view and set in the UI (via Chrome, see `argano-copy-pigment-capabilities`). A metric `default_format` also changes the Dashboard.

## Order
- **Columns and page selectors follow the main input grid:** keys first, then the other dimensions in the same order everywhere. Pick the reference grid with the client and reuse its order.

## Submission and validation boards (patterns that have worked)
- **Months across the top.**
- **Required dimensions shaded one color, optional another.** A missing required dimension turns red so the submitter sees why.
- **Hard errors (red) up top; soft flags (yellow) at the bottom.** Soft-flagged lines still flow.
- **Top KPI strip:** row count, valid and invalid amounts and counts, and a red flag when anything is invalid.
- **Filters on every dimension.** Submitters can see others' lines but not edit them, if the client wants that.
- **One default submission board** rather than many near-duplicates; stakeholders tend to dislike "too many boards".
- **Single-owner boards** need no submitter field.
- **Unmapped count:** red, top-right, linked to the unmapped report.

## Financial-statement and reporting views
- **Hierarchies come in as joined pivots** through mapping metrics when that's the model's design. Never restructure the metric for a view.
- **Calculated subtotal lines don't expand.**
- **When migrating from a legacy model, rebuild every legacy reporting view.** Check the legacy app's list so none are missed.

## Names and exports
- **After go-live, never rename or delete boards or views** that exports, spreadsheets or apps read by name. Before any rename, search every reader for the name (see `argano-copy-write-checklist`).
- **Warehouse exports should read dedicated export metrics, not views.** Views hit a render limit (verify the current limit before quoting a number).

## Changelog
- 2026-10-30: created as a client-neutral copy; stakeholder names and project boards removed, patterns kept.

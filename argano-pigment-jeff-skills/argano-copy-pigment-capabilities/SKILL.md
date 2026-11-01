---
name: argano-copy-pigment-capabilities
description: "A verified list of what Claude CAN do in Pigment through the MCP connector and Claude in Chrome, from a scan where Claude wrongly said 'can't' or 'UI-only' many times. Load it before telling the user anything in Pigment can't be done, is UI-only, or needs doing by hand, and whenever a pigment plugin skill or a note says UI-only. Has working MCP calls, proven Chrome click-paths (imports, action buttons, data access rules, number formats, variable ids), untested routes and real limits."
---

# Pigment: what Claude can actually do

**Rule:** before saying "can't" or "UI-only":
1. Check the tables below.
2. If the item isn't listed, or a note says it can't be done, **re-test with one cheap call** (for example `search_metrics_and_lists` to check `aiVisible`). Don't quote an old note.
3. If there's a Chrome route, offer to do it ("I can do this through the Pigment UI in Chrome"), preview it, and run it on the user's go.

Once a route works or fails on a project, record it in this skill (or the project's memory) with the date. Detailed click-paths are in `references/chrome-routes.md`. Facts here were checked in Oct 2026; Pigment's connector changes, so re-test anything surprising.

## 1. MCP calls that work (all were wrongly called impossible at some point)

| Capability | How |
|---|---|
| Delete views | `delete_views`. Refused for drafts, default views and board-embedded views only. |
| Delete folders | `delete_block` with block_type Folder (it moves leftover contents to the app root, so read it back empty first) |
| "Move" a folder | `create_folder`, then `move_blocks`, then `delete_block` on the old folder. The folder gets a new ID; handle subfolders one level at a time. |
| Read copy configs (name/source/target) | `get_metric_to_metric_copy_configs` |
| Create copy configs | `create_metric_copy_config` (identical dimensions required) |
| Conditional formatting | `update_view_formatting` with flat conditions |
| Board action buttons (create) | `update_board_widgets` with an ActionButton widget |
| Overwrite a default view | update, then `save_draft_views`. It reports "Merged". |
| Preview a draft of a view not on any board | `…/application/<appId>/metrics/<metricId>?viewId=<draftId>&displayMode=Grid` |
| Divide by the absolute prior period in calc items | operator `DifferenceRelative` = (l−r)/\|r\| |
| Read lists | `fetch_list_data` (needs AI data access turned on for the list/app) |
| Read Dimension-typed metrics | `fetch_metric_data` |
| Hide empty rows/cols | `update_view_filters` → `sparseSettings` |

**`query_data` was removed** from the connector (~Oct 2026). Reads are `fetch_metric_data` and `fetch_list_data`. Anything that still names `query_data` (old scheduled-task prompts, older plugin skills) needs re-pointing before it runs.

**The pigment plugin skills (v2.0.5) are wrong on two points.** `building-a-full-application` calls conditional formatting UI-only, and `using-list-subsets` says the same of action buttons. Both work through MCP, so this skill wins.

### Connector tools worth trying before calling something UI-only

Not yet proven; try once, read back, and move to the table above if it works:
- `reorder_list_items` (list item order)
- `set_board_permission_metrics` (board permissions)
- `update_view_sorts`, `update_view_chart_config`
- `edit_list_item_history_properties`, `copy_formula_as_user_inputs`
- `calendar_add_time_dimension` / `calendar_remove_time_dimension`, `create_cycle` / `update_cycle`
- `performance_profile_change` and the other `performance_*` tools (follow `pigment:profiling-model-performance`)
- `duplicate_application`, `enable_application_library`, `delete_sandbox`: app-level, so only on the user's explicit ask

## 2. Claude-in-Chrome routes: proven

Use the **Claude-in-Chrome** browser, where the user is signed in to Pigment. Steps are in `references/chrome-routes.md`.

| Gap | Route |
|---|---|
| Create, save and run **imports** (metrics and lists); read import SQL | metric/list ⋯ › Import data, `file_upload` (each file < 10 MB), map columns, Clear-before-import OFF, save config |
| **Press a board action button** (snapshots, clones) | board → button → Start → wait → read back |
| **Data access rights rules**: create, deactivate, retarget | Settings › Roles, permissions & access › Data access rights |
| **View number formats and borders** (%, decimals, parentheses, borders) | table view → Format panel → Whole row → … → Save View |
| **Metrics first in the row pivots** | Pivot panel → focus the Metrics chip → Space, ↑, Space → Save View |
| **App variable IDs and values** | `/application/<appId>/all-settings/variables` plus a read-only JS walk of React fiber props |
| **Per-widget page unlink** | board Edit → widget ⚙ → Widget settings → Selectors Edit → link icon → Apply → Done |
| **Block restore** | block → History → Block restore |
| **Read Test & Deploy item sync (connected/disconnected)** | list → More actions → Settings → General → **Item management**. "Managed separately on each environment" = disconnected; "Deployed to other environments" = connected. A read-only JS loop can walk every list (~5 s each). Role lists have no Settings. |
| **Delete a board** | open the board → ⋯ (top right) → Delete → confirm. Verify with `search_boards`. |
| **Remove one app variable** | `all-settings/variables` → the dimension group's pencil → "Remove" on that variable only → Save. The group's trash icon removes every variable on that dimension. |
| **Read import schedules, Data Flow steps, run history** | app `all-settings/data-flows` → Data Actions, Data Flows (Show details), Scheduling (Show history). Read-only; never click Trigger / Start Data Flow without a go. |
| **Read rendered board values** (calc items, show-value-as) | open the board, wait 30–60 s, `find` + `scroll_to`. Slow but works. |

## 3. Routes to try (untested): offer them, don't promise them

Each needs a preview and the user's go. When one works, move it to section 2 with the date.
- **Duplicate a board:** board ⋯ → Duplicate. `delete_block` doesn't take boards.
- **Dependent-dropdown restrictions:** table → Connect wizard. KB: https://kb.pigment.com/docs/create-dependent-dropdown-on-table. One metric can sit in only one connection.
- **Create app variables:** the same `all-settings/variables` page.
- **Reorder list items:** try `reorder_list_items` first. Chrome fallback: Edit List → sort by a rank/ID property (https://kb.pigment.com/docs/sort-data-pigment).
- **Discard a draft view**, edit import schedules, turn library links off, tick subset membership.
- **Pigment APIs from a local script:**
  - `POST /api/v1/import/push/csv` is proven (OAuth, scope Import).
  - Untested: `import/trigger?configurationId=` (run a saved import headless), `export/view/<viewId>` (rendered values), the Metadata API. KB: https://kb.pigment.com/docs/trigger-import-apis, https://kb.pigment.com/docs/export-data-with-apis, https://kb.pigment.com/docs/retrieve-info-metadata-api

## 4. True limits (say so plainly, and name the unblocker)
- **Audit trail:** gives ids, not names, and logs Claude's MCP writes under the human user. Board, view and variable edits aren't logged. *Unblocker:* the block History panel, or a separate Claude service user.
- **Dependency checks are blind** to where app variables are used and to import/copy-config scope (`referringImportConfigurations` comes back empty). *Unblocker:* a connector update; the Metadata API may partly cover it.
- **Pigment product rules:** no second header row; board layout can't be drafted; buttons can't toggle values; no per-row hidden or read-only property; page selectors can't take constants (use a variable); metric-to-metric copies need identical dimensions; joined pivots need the mapping's dimensions on the view's metrics. *Unblocker:* a Pigment feature request.
- **Custom palette hex values aren't readable.** Ask the user for the slot number.

## Guardrails for every Chrome route
- **Environment rules come from the project.** Before the first write on a new project, confirm with the user which workspace and apps are in scope, whether production takes any direct writes, and which apps are off-limits. Record them in the project's memory.
- **Before acting:** preview what you'll click and change, then wait for the user's go.
- **Approvals:** one "go" covers the exact list or step the user saw in the preview, bulk deletes included. Anything beyond that list needs a new go. Any submit, save or run counts as an irreversible click.
- **Stop and ask** at any impersonation, permission or "used in board(s)" prompt you didn't expect.
- **Verify** afterwards with MCP reads (`fetch_*`, `get_views`, `get_audit_trail` Import row counts). Close the tabs you opened.

## Changelog
- 2026-10-30: created as a client-neutral copy; workspace, app ids and project environment rules removed.

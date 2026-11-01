# Claude-in-Chrome click-paths for Pigment (proven routes)

Base URL: `https://pigment.app/w/<workspace>/application/<appId>/…`. Note the project's workspace slug and app ids in its memory before the first route.

Use `read_page`/`find` for refs, and take a screenshot before any coordinate click. Pigment grids load slowly, so wait 30–60 s before reading.

## Import data into a metric or list
1. **Build the CSV locally.**
   - Keep it **under 10 MB**, the browser upload limit. Drop traceability columns, or split the file.
   - Dates in ISO (`2026-07-01`). Pigment can read `Dec 27` as 27 Dec of the current year.
   - Match items on the list's **Name** or ID property, whichever the target dimension accepts. Some lists only match on Name.
   - Rows with a blank value column are skipped.
2. **Load one test row first** into the target and check it with `fetch_metric_data`.
3. **Open the import.** Go to the metric (`…/metrics/<id>`) or list (`…/lists/<id>`), then ⋯ › **Import data**. Upload with `file_upload`.
4. **Map and set options.**
   - Map each dimension to its column, pick the value column, and set "match items on" per dimension.
   - **Additional options:** keep "Clear values prior to import" **OFF** unless the user asked for a clear.
5. **Save the configuration**, named after the target, then run it.
6. **Read the summary dialog.** It shows rejected values per column. Screenshot it for the user.
7. **Verify.** `get_audit_trail` (Import) shows the row counts. Then `fetch_metric_data` totals against the file totals, version by version.
8. **Saved configs** show their SQL (for warehouse-sourced imports) and a **Run** button. Test & Deploy carries saved configs to production, but never the data.

## Press a board action button
1. Open the board, then `find` the button by its label.
2. Click it, then click **Start** in the confirm dialog. This is an irreversible click, so it needs the user's explicit go for that specific button.
3. Wait for completion, then read the target blocks back through MCP.

## Data access rights rules
1. Go to Settings › Roles, permissions & access › **Data access rights** › Apply configuration.
2. Use **Add a rule**: pick the access-rights metric and target. To retarget or deactivate, edit the rule row.
3. Click **Save configuration**.

Watch out for two things:
- An "Impersonation session is active" prompt can stop a read. Stop and ask the user.
- Changing an access-rights metric's dimensions through MCP silently drops all its rules. Note the targets first, then recreate them here.

## View number formats and borders
1. Open the table view, then the **Format** panel. Select the row, choose **Whole row**, then:
   - borders: the top/right/bottom/left icons
   - percent: Multiplier **%**
   - decimals: ".0←"
2. The first click after a draft fork is often swallowed, so reselect the row and click again.
3. **Save View** and confirm the "used in Board(s)" dialog. This is an irreversible click, so it needs the user's go.
4. `update_view_formatting` can't do any of these: no number formats, and no borders.

## Put Metrics first in the row pivots
1. Open the view's **Pivot** panel.
2. Focus the **Metrics** chip in Rows, press **Space** to pick it up, **↑** to move it up one slot (repeat until it's first), then **Space** to drop.
3. Save View.
4. MCP `update_view_pivots` can push Metrics to LAST, so do this after any pivot edit on a financial-statement-style view.

## App variable IDs and values
1. Open `/application/<appId>/all-settings/variables`. Note: not `/settings/variables`.
2. The page shows no IDs. Run a **read-only** `javascript_tool` walk of the React fiber props on the variable's row text. It returns `{variable:{id, configurationValue:<backing metric id>, …}}`.
3. Use that id in `update_board_page_configurations`.

## Per-widget page unlink
Board **Edit** mode → select the widget → ⚙ → Widget settings → Selectors **Edit** → click the link icon on the page → Apply → Done.

`get_board` doesn't list joined pages, so don't infer anything from their absence.

## Block restore
Block → **History** → Block restore. Pick the timestamp before the bad change, then preview it to the user before restoring.

## Read rendered board values (works, slow)
1. Open the board and wait 30–60 s.
2. `find` the widget title, then `scroll_to` it.
3. Scroll right inside the grid to reach cut-off columns.

This is the only way to see calc-item and show-value-as results until the Export API route is tested.

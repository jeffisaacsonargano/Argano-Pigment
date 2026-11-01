---
name: argano-copy-live-artifact
description: "Building or refreshing a claude.ai artifact (page, Dashboard, Doc) that shows Pigment or warehouse data - harvest, build, republish to the same path, live vs fixed data, read-access approval, merging before republishing, Dashboard limits, a source folder per artifact. Use with artifact-design and artifact-capabilities when the user asks for a dashboard, page or tracker from model or warehouse data, or to refresh or fix one."
---

# Artifacts with live data

Load `artifact-design` (and `artifact-capabilities` before any live data or `window.claude.*` code) as the Artifact tool requires. This skill adds the recipe for model-data artifacts. All data access from a page is **read-only**.

## Where each artifact's source lives

Every artifact gets a build folder in the project's tools folder (e.g. `tools/<name>/`) with a README (refresh steps), the page source or template, and the harvest/build scripts. Never build only in the scratchpad: the next refresh needs to find it. Keep a simple index (a page or a note) listing each artifact's URL and source folder.

## Which data can be live

| Source | Live in the page? | How |
|---|---|---|
| Pigment via a claude.ai connector | Yes | `mcp` capability on that connector, read tools only (`fetch_metric_data`, `fetch_list_data`, `list_issues`, `search_metrics_and_lists`, …) |
| Pigment via a local MCP server (desktop only) | Only when opened in the **desktop app** | `mcp` capability on the host server, read tools only. Web viewers get nothing; say so on the page. |
| Warehouse (e.g. BigQuery) via a claude.ai connector | Yes | Prefer the governed semantic layer if there is one (raw SQL on governed tables may be refused) |
| Local files, recon results, anything else | No | Harvest locally, then attach as a **fixed dataset** / data file and show its as-of time |
| Dashboard *type* | claude.ai connectors only | It can't call local servers, so their numbers go in as fixed datasets |

Pigment boards can't be embedded by iframe. Live numbers through the `mcp` capability are the substitute.

## Recipe

1. **Harvest** with subagents that call the read tools; extract from their transcripts with a script, so raw rows never fill the main context.
2. **Build** with a `build.py` in the folder (template + data → one HTML). Keep text in the HTML and numbers in data.
3. **Approve read access before publishing**: a page that declares an `mcp` capability triggers a standing-access prompt. Tell the user which connector and which read tools it asks for, and get their OK before the first publish.
4. **Publish to the same file path** (or pass the existing `url`) so the link doesn't change. Before republishing an artifact another session or the page itself may have changed, **read it and merge**; a stale publish is refused, and `force` discards someone's work.
5. **Verify** in the browser: open it, check the numbers against the source, check dark mode and phone width. Don't claim a post-write check passed unless you saw the result.
6. **Record it** in the artifact index and the project's memory: URL, source folder, refresh steps.

## Dashboard type limits

- No file downloads. When the user wants to "download to share", publish a plain page with the downloads capability, or copy the HTML to a local folder.
- Content lives in the type's store and is written through ArtifactData; file datasets upload as assets.
- Retitling means updating both the dashboard meta title and the page heading.
- Typed artifacts return only type instructions on an Artifact read: describe them from their store with ArtifactData reads.

## Working around the browser

- To preview a local build, serve the folder with a throwaway `python3 -m http.server` from the scratchpad.
- The built-in browser pane can get signed out of claude.ai; use Claude in Chrome for anything that needs the user's session.

## Page conventions that have worked

- Production first, development muted and labelled. Versions as columns. ✅ / ❌ / NEW obvious at a glance.
- Every number shows its as-of time and source block or table.
- Full-width layout; dark mode must work. Trackers and stars go in the artifact database, not the page source.

## Changelog
- 2026-10-30: created as a client-neutral copy; connector ids, project artifacts and index removed.

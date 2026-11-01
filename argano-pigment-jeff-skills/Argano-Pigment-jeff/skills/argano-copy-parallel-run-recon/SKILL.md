---
name: argano-copy-parallel-run-recon
description: "Tie-out of a new Pigment model against the legacy system it replaces - totals first (net income, balance sheet), then by account and dimension, historical versions, input board to P&L - with a rerunnable specs, subagent fetch, harvest, compare kit. Use when the user asks does the new model tie, recon, what's off vs legacy, baseline or check around a deploy, or why a version, account or dimension differs. Read-only."
---

# Parallel-run recon: new model vs legacy

Everything here is read-only. Never write to the legacy model (ask the user to block it with a hook if the connector can reach it). Agree with the user which pair matters most (usually production new vs production legacy); label anything else, like development numbers, as reference.

## Project setup

Record in the project's memory: the app ids on each side, the connector for each, the reference system's owner (the person who decides what "ties" means, usually accounting), and the kit folder (e.g. `tools/recon/`).

## When the user is about to deploy

Take a **baseline before** the deploy (the same pulls you'll compare after), then rerun after. Otherwise you can't tell what the deploy moved from what was already off.

## Order (what accounting owners usually want)

1. **Totals first:** net income per version, and balance-sheet total assets, liabilities and equity at closed month-ends.
2. **Then by the source system's own dimensions:** account plus the ERP's dimensions/tags.
3. **Never judge a tie by hierarchy line.** Legacy summary lines rarely match the new hierarchy, so line-level compares are only for explaining a gap you already found in 1 or 2.

## Run

1. **Write specs:** one JSON file per area listing each `fetch_metric_data` request (app id + request) for both sides.
2. **Fetch in subagents.** Hand each spec file to a subagent that only calls `fetch_metric_data` with each element's `application_id` + `request`, one at a time. Tell it **not to split oversize results**: the error saves the full result to a file a script can read. Run several in parallel.
3. **Harvest** from the subagents' transcripts with a script, so raw rows never enter the main context. Write each run to `data/<YYYY-MM-DD>[-topic]/`.
4. **Compare** with a script. Cells within $1 count as tied; diffs over a materiality line (e.g. $1K) get a known-cause label or NEW.

### Wait out the recalc
After a data load, snapshot or deploy, Pigment recalculates for minutes. Pull the same total twice a few minutes apart; only compare once they agree. Two pulls minutes apart can differ by orders of magnitude mid-recalc, and big fetches time out. A timeout means wait and retry, not "broken".

## Known gaps (label them, don't re-investigate)

Keep a dated known-gaps list in the project's notes. Typical categories:
- **Retired codes** still in history on one side
- **Accounts the legacy summary mapping drops** (not on its mapping list)
- **Intercompany** handled differently, or missing from the warehouse feed
- **Load windows:** periods that never reached the warehouse, open months the legacy model doesn't have
- **Old reclasses** in stale legacy history that net to zero
- **Not errors:** legacy keeps only required dimensions (rest on a default member) while the new model keeps the full ERP tags, so dimension-level "diffs" are expected

Anything not on the list is **NEW**: say so first.

## Report

- **Production columns first, versions as columns**, months or FY as rows. ✅ ties (to the cent / within $1), ❌ with the gap and its known-cause label, or **NEW**.
- Lead with one line: what ties, what's new. Then the table. Then "Not checked".
- Use business names for apps and lines in anything stakeholders will read.
- Save a note for anything beyond a quick check, and update the known-gaps list.

## Changelog
- 2026-10-30: created as a client-neutral copy; app ids, gaps and figures removed.

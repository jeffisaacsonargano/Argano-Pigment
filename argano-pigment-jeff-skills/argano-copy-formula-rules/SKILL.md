---
name: argano-copy-formula-rules
description: "House formula rules for Pigment models plus a linter (scripts/lint_formula.py) and a change-proposal flow (colored Before/After, impact table, wait for go). Load before EVERY validate_formula, create_metric, update_metric, create_list_property or update_list_property call that sets a formula, and whenever you review, refactor or explain a formula. Where it conflicts with the pigment plugin skills (e.g. on IFBLANK), this skill wins."
---

# Pigment formula rules

These rules apply on top of `pigment:writing-pigment-formulas` and `pigment:writing-performant-formulas`. Where they disagree, this skill wins.

## Project setup (fill in per client)

Before the first formula on a new project, find or ask for these and note them in the project's memory:
- **Constants prefix and folder**: where single-value inputs live (default here: blocks named `CON <List>: <Item>` in a `/00 Constants` folder).
- **Security block prefixes** exempt from the hard-code rule (default: `ARM_`, `BP_`, `SEC_`).
- **Client accounting conventions**: sign convention (natural balance or not), how account category is derived, which lines flip sign. Never assume these; ask the client's accounting owner.
- **Reporting hierarchies**: whether they reach views as joined pivots through mapping metrics or as structural dimensions.

## Always: lint the draft first

```bash
python3 -I <this skill folder>/scripts/lint_formula.py --name "<block name>" <<'EOF'
<formula>
EOF
```

Options: `--constant-prefix "CON "`, `--exempt-prefixes "ARM_,BP_,SEC_"`, `--jsonl file --summary` (one `{"name","formula"}` per line).
- Fix every **HIGH** before calling `validate_formula`, within the scope below.
- If you keep a **MED**, name it in the preview with a one-line reason. **INFO** needs no comment.

## Fix only what the change is about

Lint the whole formula, but the approved change decides what you fix:
- **Logic rewrite** (the user approved new logic): fix its pre-existing HIGHs too, and say so in the preview.
- **Narrow edit** (a coloring rule, a comment, one filter, a rename): leave pre-existing findings alone. List them under "Suggestions" and fix them only on the user's go. A coloring-only request that also "fixes" an IFBLANK is scope creep.

## The rules

Background and Pigment product facts are in `references/rules-background.md`.

1. **No IFBLANK. Write `IF(ISDEFINED(x), …)`.** (R01)
   - `IFBLANK(flag, FALSE)`: use `flag`, or `IF(ISDEFINED(x), TRUE)`.
   - `IFBLANK(x, 0)`, `IFBLANK(x, "")`, `IFBLANK(x, <constant>)`: a constant fallback fills every empty cell, so the metric goes dense. Leave the cell blank, or scope the fallback with `IF(ISDEFINED(driver), …)`.
   - Text "fingerprint" keys built from `IFBLANK(tag,"") & "|" & …`: don't. Put the optional-tag checks in their own metrics.
   - Merging two sparse sources: `IF(ISDEFINED(A), A, B)`.
2. **Check booleans are TRUE or BLANK, never FALSE.** (R03/R04)
   - Write `IF(cond, TRUE)` with no else. Use the flag directly (`[FILTER: 'X?']`), not `= TRUE`.
   - Downstream counts and filters depend on blanks.
   - Exception only where the user asked (e.g. amount columns showing `0` on invalid lines).
3. **No hard-coded items, numbers or dates. Use a constant set by manual input.** (R05/R07)
   - Example: `'Data Type'."Actual"` becomes `'CON Data Type: Actual'`.
   - Default/placeholder members (the "000000"-style catch-alls) go through constants too.
   - Security formulas are exempt.
4. **Pick the version explicitly.** No `[REMOVE FIRSTNONBLANK: Version]` or `LASTNONBLANK`. Use `[SELECT: Version = <version constant>]`. Picking by list order breaks the day a version is added, renamed or deleted. (R06)
5. **Only the dimensions the formula uses.** Don't copy Version, Month or User in from a pattern. Unused dimensions on an access-rights metric can blow it up to ~1M cells and multi-second waits.
6. **Apply each modifier once, and push logic upstream rather than stacking.**
   - The same modifier twice on the same dimension is a smell (R08, MED). Ask whether the source metric should carry the dimension instead.
   - A long chain (6+ modifiers) is only an INFO hint. Reporting formulas often need one; don't rewrite for the count alone.
   - **Prove a compact rewrite with data, not just `validate_formula`.** A shorter form can validate and give wrong numbers. If you decline a rewrite, say why.
7. **Every modifier must change the result.** (R11, review only: the linter can't see data)
   - Before keeping an EXCLUDE, FILTER or SELECT, ask what it removes. If an upstream flag or the data already rules those cells out, drop it, or say in the preview why you keep it as a guard.
8. **UX filtering belongs in the view or a hidden filter metric, not in the value formula.**
9. **Test existence with counts, not net sums.** Offsetting lines net to 0 and vanish. Include zero-value combos. (R10)
10. **Reporting metrics stay on the account dimension.** If the client's hierarchy levels are mapping metrics, they reach views as joined pivots; never `[BY: Account -> mapping]` the metric itself. Filtering on the map is fine.
11. **Client accounting conventions live in one place.** Sign flips and category-from-account-number rules go in one property or constant, never as `= 8` literals scattered through formulas. Confirm the rules with the client's accounting owner.
12. **Comment every formula** with a one-line `//` explanation. (R09)
13. **No ISBLANK or ISNOTBLANK.** They are always dense (R02). Use `ISDEFINED`, `IF(ISDEFINED(…))` or `[EXCLUDE: …]`.

## Proposing and applying a change

The user approves every formula change from a preview and usually wants to see the formulas themselves. Formats and the impact table are in `references/change-proposal.md`.

1. **Read the current formula live** before drafting. The Before is what's in the app now, not what memory or a note says.
2. **Draft, lint, `validate_formula`** in the development environment.
3. **Preview in chat:** the colored Before stacked over the After (plus plain text to copy), one line on why, and any Suggestions kept out of scope. For several formulas, also write a note file the user can reread.
4. **Impact by version:** the reporting lines touched (or the top/bottom totals), and any row counts the change affects. For production-bound changes, add whether each version ties before and after.
5. **Wait for go.** "Go on 1–3" means only those items.
6. **Apply in development**, read back, and run the regression check for changes on the reporting path. Structure reaches production only through the client's deploy process.
7. **After deploy**, rerun the impact table in production (read-only) and report what ties.

## Before applying

- [ ] The linter is clean, or each kept MED is explained.
- [ ] `validate_formula` passed.
- [ ] Every referenced block is owned by the app you're editing; library blocks shared in from other apps don't count.
- [ ] For a rewrite of an existing metric: pull values before and after, and check they match or the change is intended.
- [ ] Follow `argano-copy-write-checklist` for scope, preview and read-back.

## Sources

- Pigment KB, IFBLANK (a constant fallback "makes it high density"): https://kb.pigment.com/docs/ifblank-function
- Pigment KB, IF (a BLANK condition takes the else branch): https://kb.pigment.com/docs/if-function
- Pigment Community, isBlank/isDefined/ifBlank/ifDefined. ISBLANK is always dense. ifDefined behaves exactly like if(isDefined()): https://community.pigment.com/technical-tips-182/best-practices-for-using-isblank-isdefined-ifblank-and-ifdefined-3040

## Changelog

- 2026-10-30: created as a client-neutral copy; project-specific conventions replaced by the "Project setup" section.

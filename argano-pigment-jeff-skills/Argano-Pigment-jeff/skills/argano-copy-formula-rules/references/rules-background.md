# Background for the formula rules

## Why these rules exist

They come from reviewing every formula Claude wrote through the Pigment connector on a large multi-app build, and from the modeler's corrections of it. The habits that needed correcting most often, in order:

| Rule | What Claude tended to do | Why it's wrong |
|---|---|---|
| R01 IFBLANK | `IFBLANK(bool, FALSE)` and `IFBLANK(x, "")` inside text keys; rarely `IF(ISDEFINED(` | Constant fallbacks make the metric dense; FALSE breaks blank-based downstream logic |
| R03 boolean FALSE | `IFBLANK(x, FALSE)`, `= TRUE` / `= FALSE` compares | Downstream counts and filters depend on blanks, not FALSE |
| R05 hard-codes | `'List'."Item"` literals; account-digit literals like `'1st Digit' = 8` | Breaks silently when members are renamed or retired; constants are reviewable in one place |
| R06 version by order | `REMOVE FIRSTNONBLANK: Version` | Breaks the day a version is deleted or reordered |
| Unused dims | Version/Month/User dims copied from a pattern | Cell counts explode (one access-rights metric reached ~1M cells) |
| R08 stacking | the same modifier twice; long chains | Usually means the source metric is missing a dimension |
| R11 unneeded modifier | an EXCLUDE guarding cells an upstream flag already excludes | Noise that hides intent and costs calc time |
| Fix scope | "fixing" an IFBLANK during a coloring-only change | Scope creep; unreviewed logic changes |
| R07 filters in formulas | UX filters baked into value formulas | Belongs in the view or a hidden filter metric |
| R10 counts not sums | existence tested with `<> 0` on sums | Offsetting lines net to zero and vanish |
| Comments | most formulas already had `//`; keep it universal | Reviewers and future modelers read the comment first |

To check whether a habit is shrinking on a project, lint every formula written so far with `--jsonl … --summary` and compare counts over time.

## Pigment product facts (checked Oct 2026)

- `IFBLANK(A, B)` returns A where defined, else B. It stays sparse unless B is dense. Constant fallbacks such as `IFBLANK(x, 20)` produce a dense metric (KB).
- `ISDEFINED(x)` returns TRUE or BLANK, so it is sparse. `ISBLANK` and `ISNOTBLANK` return TRUE or FALSE everywhere, so they are always dense (Community, Pigment employee).
- `IFDEFINED(A, B, C)` behaves exactly like `IF(ISDEFINED(A), B, C)` (Community). House style is the `IF(ISDEFINED(` form.
- `IF` with a BLANK condition returns the else branch (KB).
- The `pigment:*` plugin skills rank "IFDEFINED > IFBLANK > IF(ISBLANK())" and recommend IFBLANK chains for overrides. That is superseded here.

# Formula change proposal: formats

## Chat preview (every proposal)

Markdown code blocks can't be colored, so render the formulas inline with the `show_widget` tool if it's available (load its `read_me` first):
- dark code panel, full width; **Before stacked above After** (easier to read than side by side)
- a one-line legend
- also paste the plain Before/After text in the reply, so the user can copy it

Palette:

| Token | Color | Example |
|---|---|---|
| Metric (quoted name, not followed by `.`) | blue `#5cb8ff` | `'Revenue Actuals'` |
| List / dimension (quoted name followed by `.`, or a known dimension) | teal `#3fd0a6` | `'Account'`, `Version` |
| Property (after `.`) | light teal `#9de8d2` | `.'Is Historical?'` |
| Modifier | pink `#f06aa8`, bold | `FILTER`, `EXCLUDE`, `REMOVE SUM`, `BY`, `->` |
| Function | periwinkle `#7aa2ff`, bold | `IF`, `ISDEFINED`, `AND` |
| `//` comment | gray `#8e8e93`, italic | |
| String | green `#5fd17a` | |
| Background / code panel | `#1c1c1e` / `#2c2c2e` | |

## Note file (several formulas, or anything the user will reread)

Write `NOTE - <topic> (<YYYY-MM-DD>).md` in the project's notes folder. For each formula:

```
### <n>. `<block name>` (<app>, <id prefix>)
**Before** (live in <environment> <app>, read <time>)
` ` `
<current formula>
` ` `
**After**
` ` `
<proposed formula>
` ` `
```

(Use real triple backticks; they are spaced here only to keep this file readable.) If the user wants a rendered copy, build a dark full-width HTML version with the same palette and send it with `display: render`.

## Impact table (bottom of the note and in chat)

One row per version. Production columns first when the change is headed to production.

| Version | Before | After | Reference system | Ties? |
|---|---|---|---|---|
| <version> | <total> | <total> | <total> | ✅ to the cent (was short $X) |

Add balance-sheet lines and any affected row counts when the change touches them. Say plainly which versions move and why, and mark anything not checked.

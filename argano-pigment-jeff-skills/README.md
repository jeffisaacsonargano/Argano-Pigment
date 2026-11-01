# argano-copy skills

12 client-neutral copies of my custom Claude skills, made 2026-10-30 for use on other projects. Project-specific content (people, apps, ids, figures, decisions) was removed; each skill has a "Project setup" step or placeholders where a new client's details go.

These are **not installed** on this machine. On the other laptop:

1. Copy the `argano-copy-*` folders you want into `~/.claude/skills/`.
2. Start a new Claude Code session; check the skill list shows them with their full descriptions.
3. On the first session for a new client, let each skill's "Project setup" step record that client's workspace, apps, conventions and off-limits apps in memory.

| Skill | What it does |
|---|---|
| argano-copy-formula-rules | Pigment formula house rules + linter (`scripts/lint_formula.py`) + Before/After change proposals |
| argano-copy-pigment-capabilities | What Claude can really do in Pigment (MCP calls + proven Chrome click-paths) before saying "can't" |
| argano-copy-write-checklist | Before/after checklist for every Pigment write: scope, reuse, renames, deletes, imports, read-back |
| argano-copy-board-view-rules | Board and view conventions: data on first open, labels, selectors, submission-board patterns |
| argano-copy-deletion-run | Safe cleanup of unused blocks: scan, blind-spot re-checks, one approved batch, regression before/after |
| argano-copy-model-harvest | One dated read-only pull of a whole Pigment model, reused by maps, scans and reviews |
| argano-copy-parallel-run-recon | Tie-out of a new model against the legacy system it replaces |
| argano-copy-claude-setup | Taking in skills/plugins, writing your own skills, scheduled tasks |
| argano-copy-stakeholder-writeup | Paste-ready, concise messages and one-pagers for stakeholders |
| argano-copy-transcript-lookup | Answering "what did X say" from Gemini call notes, and call → model-update plans |
| argano-copy-live-artifact | claude.ai artifacts/dashboards built from model or warehouse data |
| argano-copy-demo-film | Short demo/training videos with a bundled caption renderer (`build/render-template.swift`) |

Skill names must be lowercase, so the prefix is `argano-copy-`.

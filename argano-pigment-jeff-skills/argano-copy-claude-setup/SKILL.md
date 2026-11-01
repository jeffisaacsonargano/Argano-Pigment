---
name: argano-copy-claude-setup
description: "Managing Claude's own setup - taking in a downloaded skill, plugin or zip (unpack safely, diff, find which copy loads), fix packs instead of forking shared skills, writing your own skills (YAML description gotchas, naming, changelogs), and scheduled tasks and unattended runs. Use when the user gets a skill or plugin, asks which version is loaded, why a skill didn't load, to build or change a skill, or about a scheduled or nightly run."
---

# Claude setup: skills, plugins, scheduled tasks

## Where things live (what loads)

| Path | What | Who manages it |
|---|---|---|
| `~/.claude/skills/<name>/` | the user's own skills (loaded) | user / Claude |
| `~/.claude/skills-disabled/` (convention) | skills switched off by moving them out | user / Claude |
| `~/.claude/skills/synced/<id>/` | skills synced from the user's claude.ai account | Claude app; don't hand-edit |
| `~/.claude/plugins/…` | org and uploaded plugins | Claude app; update by uploading a newer zip |

**Which copy loaded?** When a skill loads, its "Base directory" line names the folder it came from. Check that before trusting a version: a newly downloaded version doesn't load until it's installed, and the running session keeps the old copy until you **start a new session or reload plugins**. Compare the plugin's `plugin.json` version with the newest zip before saying "you're on the latest".

## Taking in a downloaded skill or plugin

1. Unzip into a **new empty folder in the scratchpad**; run nothing from inside it (use `python3 -I` with paths as arguments if a script must be read or run).
2. Read its SKILL.md / plugin.json: name, version, what it writes, any hooks or scripts.
3. `diff -ru` against the installed copy (and the account-synced copy for `.skill` files). If identical, there's nothing to install.
4. Account-synced skills update through claude.ai sync; uploaded plugins update by uploading the zip in the Claude app (the user's click). Don't make a second local copy of a synced skill in `~/.claude/skills`.
5. Keep the newest zip in one place; offer to trash older duplicates after checking md5. Never delete anything the user has said to keep.

## Shared skills: fix packs, not forks

Skills owned by others get overwritten on update, and local edits are lost. When one is wrong:
- fix it locally only if the user needs it today, keep a backup, and note it;
- write the fix up for the owner: what breaks, why, the exact change with file and line, how it was verified. Paste-ready, plain language.
- Watch for skills that call tools the connector no longer has (e.g. Pigment's `query_data`).

## Writing or editing the user's own skills

- Use a consistent name prefix so the user can tell their skills apart (e.g. `<prefix>-<MM-DD>-<name>`). The description says what it is and lists real trigger phrases. Keep it under ~1,024 characters; details go in `references/`. A skill headed for the claude.ai plugin uploader must keep its description **under 500 characters**.
- **YAML gotcha:** in an unquoted `description:`, a space followed by `#` starts a comment and silently cuts the rest, so the triggers never load. Quote the description, or write "double-hash" instead of `##`, and after saving check the skill list shows the full description. Also avoid an unquoted `: ` inside the description.
- Show the user a diff before saving changes to an existing skill; add a dated `## Changelog` line.

## Scheduled tasks and unattended runs

Create, change or run one only with the user's explicit OK.
- **Unattended runs can't edit scheduled tasks** (that needs a person's approval). So a task can't re-arm itself or another task. Use a fixed tick plus a local gate script that decides whether to do anything; a late or missed tick still catches up.
- **Test runs** only when the user says "run it now".
- **The computer must be awake.** A run due while it sleeps happens late or not at all, and sleep kills in-flight work. Check the run history before assuming a run happened.
- **Prompts go stale.** Keep task prompts short: "read and follow skill X". Steps duplicated in a prompt drift. When a connector or skill changes, list which task prompts mention it and offer the edits.
- Settings, permissions and hooks (`~/.claude/settings.json`) are the user's to change; Claude shouldn't widen its own permissions.

## Changelog
- 2026-10-30: created as a client-neutral copy; personal paths, people and plugin inventory removed.

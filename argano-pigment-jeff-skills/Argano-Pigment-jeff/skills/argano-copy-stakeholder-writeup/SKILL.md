---
name: argano-copy-stakeholder-writeup
description: "Writing what the user sends to project stakeholders - Slack replies, one-pagers, status updates - paste-ready plain text, answer first, concise, real examples kept, business words instead of model codes, no Claude-internals talk, and proofing the user's own edits. Use when the user asks to reply to someone, write a Slack message, draft something to send, explain something to a stakeholder, make a one-pager or status update, or says more concise."
---

# Stakeholder write-ups

The pattern below is what has been accepted again and again; "more concise" is the most common correction.

## Shape

1. **Answer first.** The first line is the answer or the ask. No "Great question", no recap of what they asked.
2. **Short.** Aim for a Slack message, not a document: typically 400–800 characters. Accepted rewrites usually cut drafts by 60–80%.
3. **Keep one or two real examples** (an account, a version, a number). "More concise" means cut words, not examples.
4. **Steps as a short numbered list** when the reader has to do something (UI clicks, where to look).
5. **Close** with the one thing you need from them, if anything. No sign-off fluff.

## Words

- Business names for apps and boards as people see them, not internal abbreviations. Spell out other acronyms once or skip them.
- Business terms over model internals: "the P&L by version", not block ids, formulas or modifier names, unless the reader builds in the tool and asked for them.
- **No token, cost or Claude-internals talk**, and no "absolutely". Don't address the reader by name inside a message the user will post to a group unless asked.
- Impact over stats: what changed for them and why it matters, not counts of blocks or sessions.
- Confidentiality: check what the client allows to be shared outside the team (figures vs structure) before including numbers.

## Paste-ready

- Give the message as plain text the user can paste into Slack: a short lead-in line ("Ready to paste:"), then the message in a quote block or a plain code block. No markdown tables, no headings, no `**` that will paste as literal asterisks.
- For a one-pager or something with screenshots, use a doc or a page and give the link; check images actually render.
- One version only. If there's a real choice of tone or content, ask one short question instead of drafting three.

## Accuracy

- Every number and claim comes from a source you checked in this session (a model read, a recon file, a note). Don't round in a way that changes a tie (say "ties to the cent" only if it does).
- If something isn't verified, say so in one clause.

## When the user edits it themselves

They often rewrite the draft and paste it back. Then just proof it: fix typos and facts, keep their voice and length, and say in one line what you changed ("Your edits read well. I only fixed …"). Don't re-expand it.

## Changelog
- 2026-10-30: created as a client-neutral copy; names and project terms removed.

---
name: evening
description: End-of-day wrap-up — archives completed tasks from memory, rolls over recurring obligations, surfaces tomorrow's items, and optionally writes a daily log to the user's Obsidian vault. Use this whenever the user types /evening, says "wrap up the day" / "close out" / "let's call it", finishes a substantive day of work, or wants to commit memory updates before stopping.
---

# /evening — Daily Wrap

Archive what got done, plan tomorrow, commit.

## Instructions

When the user runs `/evening`, do the following:

### 1. Load config

Read `config.yaml` (and `config.local.yaml` if present, with local overriding). Note whether `vault_dir` is set — controls step 6.

### 2. Identify what got done

Walk through what was discussed and worked on this session/day. Ask the user if anything is unclear ("Did X get finished?").

### 3. Complete actions and projects

For each item confirmed done:

1. Move the completed action from its context in `memory/next-actions.md` to its **Completed** section with the completion date and outcome; keep its ID and context.
2. If the action belonged to an Active project in `memory/projects.md`, choose and link its next unblocked physical action. If the outcome is done, move the project to **Completed** with the date and outcome instead. If blocked externally, move it to **On Hold** and record `[YYYY-MM-DD] Task (Waiting on: Person/Entity)` in `memory/waiting-for.md`.
3. Update the `*Updated:*` timestamp in each changed file.

### 4. Roll over recurring actions

For each routine completed today in `memory/next-actions.md`, record the completed occurrence in **Completed** with its date and outcome; advance the active routine's "Next due" by its cadence. Don't silently mark a missed occurrence done.

### 5. Note tomorrow's top items

Look at `memory/next-actions.md` for actions and routines due tomorrow or carrying over; check `memory/waiting-for.md` for dated follow-ups and `memory/inbox.md` for unprocessed commitments. Surface them briefly. Adjust priorities if the user wants.

### 6. Daily log (if `vault_dir` configured)

If `vault_dir` is set in `config.yaml`, call `/obsidian daily-log` to append today's wrap entry to `${vault_dir}/${vault_daily}/YYYY-MM-DD.md`. Use a `## Wrap` section. Keep to 5-15 lines: what got done, what's carrying over, anything notable.

If `vault_dir` is unset, skip silently — Iantha doesn't keep in-repo daily logs by default.

### 7. Distillation check (Rule E)

Did any pattern repeat 3+ times this session/week? Did any decision get made that should be logged?

- If yes: propose adding to `memory/decisions.md` (with date + Why) or as a standing rule in `CLAUDE.md`.
- Wait for user confirmation before writing.

### 8. Commit & push

Stage updated memory files, commit, and push:

```
evening: YYYY-MM-DD wrap — N tasks archived, M recurring rolled
```

Push to `origin` so memory stays synced across machines.

## Example wrap output (chat)

```
## Wrap — 2026-05-01

Done:
- Iantha v0.1.0 PR opened (#4)
- Franchise tax paid

Carrying over:
- Renew passport (now 6 days overdue — escalate?)

Tomorrow:
- /morning will surface the LLC RA renewal due 2026-05-02
```

## Notes

- Keep the wrap conversational — this isn't a status report, it's a quick close-out
- Use the user's local timezone for "today" / "tomorrow" (`config.yaml: timezone` overrides system TZ)
- If nothing was done today, that's fine — just close cleanly. Don't fabricate.
- Vault daily logs are optional — only happen when `vault_dir` is configured

## Learned from runs

(empty — populated as the skill is used)

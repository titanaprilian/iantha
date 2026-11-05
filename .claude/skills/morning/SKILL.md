---
name: morning
description: Daily start-of-day briefing — reads memory, surfaces today's tasks, overdue items, recurring obligations, and personal-life reminders. Use this whenever the user types /morning, asks "what's on my plate today" / "what should I focus on" / "kick off the day", starts a new day's session and hasn't been briefed yet, or wants a daily standup-style rundown of personal life. If a vault is configured, can also write the briefing to today's daily note.
---

# /morning — Daily Briefing

Read memory, surface what matters today.

## Instructions

When the user runs `/morning`, do the following:

### 1. Load config

Read `config.yaml` (and `config.local.yaml` if present, with local overriding). Note whether `vault_dir` is set — controls steps 6 and 7 below.

### 2. Read memory

- `memory/tasks.md` — all sections
- `memory/priorities.md` — current top focus
- `memory/personal.md` — routines and life context (only what's relevant to today)
- `memory/decisions.md` — recent entries (last 7 days)

If `vault_dir` is set, also read yesterday's daily note (`${vault_dir}/${vault_daily}/YYYY-MM-DD.md`) — specifically look for a `## Wrap` section (carry-over from /evening) or any "tomorrow" / "carrying over" notes. If the file doesn't exist or has no carry-over content, skip silently.

### 3. Identify today's items

From `tasks.md`:

- **Due today**: items with today's date
- **Overdue**: items with a date earlier than today, not archived
- **Recurring due today**: items in the Recurring section whose "Next due" matches today
- **Time-sensitive**: anything in Urgent / Time-sensitive section

### 4. Build the briefing

Output a short, scannable briefing:

```
## Morning Briefing — YYYY-MM-DD

### Today
- [item 1]
- [item 2]

### Overdue
- [item with original due date]

### Watch
- [priorities or things to keep in mind]

### Reminders
- [anything from personal.md routines for today, e.g., "Tuesday gym day"]
```

Sections that are empty: omit them entirely. Don't pad.

If nothing is due today and nothing overdue, say so plainly: "Nothing on the calendar today. Want to plan something?"

### 5. Surface, don't dispatch

This is a briefing, not a work session. Don't start executing tasks unless the user asks.

### 6. Offer task updates

If the user reacts to anything in the briefing ("that's done", "move that to tomorrow", "drop that"), update `memory/tasks.md` accordingly. Confirm and commit.

### 7. Optional vault write (only if `vault_dir` configured)

Offer to write the briefing to `${vault_dir}/${vault_daily}/YYYY-MM-DD.md` via `/obsidian daily-log` with section name `Briefing`. Default to "yes" if the user has confirmed once before; otherwise ask. Skip silently if `vault_dir` is unset.

## Example output

```
## Morning Briefing — 2026-05-01

### Today
- Submit LLC franchise tax payment (due today)
- Coffee with Mei — 2pm, Sightglass

### Overdue
- Renew passport (was due 2026-04-25)

### Watch
- Quitting coffee experiment, day 4 — track headache severity

### Reminders
- Friday gym day
```

## Notes

- Use the user's local timezone for "today" (`config.yaml: timezone` overrides system TZ)
- Keep the briefing under 20 lines unless there's genuinely a lot
- Don't read all memory files — just what's listed in step 2
- If `priorities.md` or `personal.md` is empty (fresh repo), skip those sections silently
- Vault writes are optional — only happen when `vault_dir` is configured

## Learned from runs

(empty — populated as the skill is used)

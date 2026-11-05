---
name: morning
description: Daily start-of-day briefing — reads memory, surfaces today's tasks, overdue items, recurring obligations, and personal-life reminders. Use this whenever the user types /morning, asks "what's on my plate today" / "what should I focus on" / "kick off the day", starts a new day's session and hasn't been briefed yet, or wants a daily standup-style rundown of personal life. If a vault is configured, can also write the briefing to today's daily note.
---

# /morning — Daily Briefing

Read memory, surface what matters today.

## Instructions

When the user runs `/morning`, do the following:

### 1. Load config & target date

Read `config.yaml` (and `config.local.yaml` if it exists, with local overriding).
Determine the target date (default: today; if user requested tomorrow, e.g. "for tomorrow", use tomorrow's date).
Note whether `vault_dir` is set — controls step 8 below.
### 2. Read memory

- `memory/tasks.md` — all sections
- `memory/priorities.md` — current top focus
- `memory/personal.md` — routines and life context (only what's relevant to today)
- `memory/decisions.md` — recent entries (last 7 days)

If `vault_dir` is set, also read yesterday's daily note (`${vault_dir}/${vault_daily}/YYYY-MM-DD.md`) — specifically look for a `## Wrap` section (carry-over from /evening) or any "tomorrow" / "carrying over" notes. If the file doesn't exist or has no carry-over content, skip silently.

### 3. Identify today's items & calendar events

From `tasks.md`:

- **Due today**: items with today's date
- **Overdue**: items with a date earlier than today, not archived
- **Recurring due today**: items in the Recurring section whose "Next due" matches today
- **Time-sensitive**: anything in Urgent / Time-sensitive section

From Google Calendar (via `gws`):
- If `gws` is authenticated, run:
  - For today: `gws calendar +agenda --today --timezone "<timezone>" --format json`
  - For tomorrow: `gws calendar +agenda --tomorrow --timezone "<timezone>" --format json`
- Extract existing events: start time, end time, summary, and location.
- If `gws` is not authenticated or fails, skip calendar silently without breaking the briefing.
### 4. Build the briefing with proposed time blocks (Implementation Intentions)

Synthesize the day using *Atomic Habits* Implementation Intentions ("I will [BEHAVIOR] at [TIME] in [LOCATION]"):
1. Identify existing fixed commitments from Google Calendar to spot open windows.
2. Translate active tasks from `tasks.md` and routines from `personal.md` into concrete, non-overlapping focus blocks. Warn against vague goals (e.g. "learn Go") by sharpening them into measurable mini-goals.
3. Each proposed block should specify:
   - **Time & Location**: Physical workspace / environment.
   - **Implementation Intention / Habit Stack**: "After [ANCHOR], I will [ACTION]..." or "I will [BEHAVIOR] at [TIME] in [LOCATION]".
   - **Boundary / Pre-condition**: e.g., Phone in another room.

Output a short, scannable briefing:

```
## Morning Briefing — YYYY-MM-DD

### Calendar
- HH:MM - HH:MM: Existing event summary

### Proposed Time Blocks (Implementation Intentions)
- **HH:MM - HH:MM** · *[Location]*
  - **Intention**: I will [Behavior] at [Time] in [Location].
  - **Pre-condition / Stack**: [e.g. After Subuh prayer / Phone in another room]
  - **Done criteria**: [Clear deliverable for this block]

### Tasks
- [item 1]
- [item 2]

### Overdue
- [item with original due date]

### Watch
- [priorities or things to keep in mind]

### Reminders
- [routine rules, energy management]
```

Sections that are empty: omit them entirely. Don't pad.

### 5. Propose & Confirm Google Calendar blocks

Prompt the user:
*"Would you like me to schedule these proposed time blocks onto your Google Calendar, or adjust any times?"*

When the user confirms (e.g. "yes", "schedule them", "confirm", or provides adjusted times):
Run `gws calendar +insert` for each approved block with rich metadata:
- `--summary`: Concrete action verb + outcome (not generic "Deep Work").
- `--location`: Physical space + boundary cue (e.g. `Study Desk (Phone in another room)`).
- `--description`: Formatted with:
  ```text
  🎯 Implementation Intention:
  I will [BEHAVIOR] at [TIME] in [LOCATION].

  ✅ Definition of Done:
  - [Measurable outcome]
  - [Focus boundary]

  ⚡ If-Then Rule:
  If I encounter friction or urge to context-switch, I will note it on paper and stay in the work window.
  ```
- Confirm the scheduled events with the user.
### 6. Surface, don't auto-dispatch task work

This is a planning briefing, not a work execution session. Do not start executing the tasks themselves unless the user asks.

### 7. Offer task updates

If the user reacts to anything in the briefing ("that's done", "move that to tomorrow", "drop that"), update `memory/tasks.md` accordingly. Confirm, commit, and push to `origin`.

### 8. Optional vault write (only if `vault_dir` configured)

Offer to write the briefing to `${vault_dir}/${vault_daily}/YYYY-MM-DD.md` via `/obsidian daily-log` with section name `Briefing`. Default to "yes" if the user has confirmed once before; otherwise ask. Skip silently if `vault_dir` is unset.
## Example output

```
## Morning Briefing — 2026-11-06

### Calendar
- 21:00 - 22:00: Simak Regular Meeting

### Proposed Time Blocks
- [ ] 05:30 - 06:30: Subuh & Strength Training (Habit stack: workout clothes)
- [ ] 08:30 - 10:30: Deep Work: Interview Prep (Phone in another room)
- [ ] 14:00 - 15:30: Go Mini-Module Breakdown

### Tasks
- [ ] Verify university graduation checklist and clearance deadlines
- [ ] Submit junior developer applications (3-5 target roles)

### Watch
- Break interview prep and Go tasks into concrete, reachable mini-goals
- December graduation timeline

### Reminders
- Phone-free focus zone during morning deep work
- Save low-friction tasks for the afternoon
```

*Prompt: "Would you like me to schedule these proposed blocks onto your Google Calendar, or adjust any times?"*
## Notes

- Use the user's local timezone for "today" (`config.yaml: timezone` overrides system TZ)
- Keep the briefing under 20 lines unless there's genuinely a lot
- Don't read all memory files — just what's listed in step 2
- If `priorities.md` or `personal.md` is empty (fresh repo), skip those sections silently
- Vault writes are optional — only happen when `vault_dir` is configured

## Learned from runs

(empty — populated as the skill is used)

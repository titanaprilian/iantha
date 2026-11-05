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
### 4. Build the briefing with open focus windows

Synthesize the day:
1. Identify existing fixed commitments from Google Calendar to spot open windows.
2. Map open windows to the user's natural energy rhythms from `personal.md` (e.g. post-Subuh workout, morning deep work focus block, afternoon low-energy block).
3. Present the open windows alongside active priorities and tasks.

Output a short, scannable briefing:

```
## Morning Briefing — YYYY-MM-DD

### Calendar (Fixed)
- HH:MM - HH:MM: Existing event summary

### Open Focus Windows
- **HH:MM - HH:MM** · *[Location]* — [Anchor / Rhythm, e.g. Post-Subuh habit stack]
- **HH:MM - HH:MM** · *[Location]* — [Deep Work: mapped to Priority #1]
- **HH:MM - HH:MM** · *[Location]* — [Afternoon: low-friction or secondary task]

### Tasks Due / Active
- [item 1]
- [item 2]

### Overdue
- [item with original due date]

### Watch
- [priorities or things to keep in mind]

### Reminders
- [routine rules, e.g. phone in another room during study]
```

Sections that are empty: omit them entirely. Don't pad.

### 5. Guided Elicitation (Human Internalization)

**Crucial Rule**: Never invent or fabricate the user's implementation intentions with AI. Per cognitive psychology research (Gollwitzer, 1999; Slamecka & Graf Generation Effect), implementation intentions only trigger automated action initiation if the human actively generates their own commitment and visualizes their obstacles.

Prompt the user to internalize the target block:
> *"You have [Window, e.g. 08:30 - 11:30] open for [Top Priority]. What concrete deliverable will you lock in during this block, and what is your #1 obstacle or distraction risk?"*

### 6. Encode & Insert into Google Calendar

When the user responds with their target deliverable and obstacle (even in raw bullets or informal text):
1. Scaffold their own words into the structured Implementation Intention format:
   - `--summary`: Concrete action verb + outcome from user (e.g. `Draft 3 STAR Behavioral Stories`)
   - `--location`: Physical workspace + boundary cue (e.g. `Study Desk (Phone in another room)`)
   - `--description`:
     ```text
     🎯 Implementation Intention:
     I will [user's behavior] at [time] at [location].

     ✅ Definition of Done:
     - [User's deliverable]
     - [Focus boundary maintained]

     ⚡ If-Then Rule:
     If [user's obstacle/distraction occurs], I will [write it down on paper and stay in the work block].
     ```
2. Run `gws calendar +insert` for the confirmed block.
3. Confirm the scheduled block to the user.
### 7. Surface, don't auto-dispatch task work

This is a planning briefing, not a work execution session. Do not start executing the tasks themselves unless the user asks.

### 8. Offer task updates

If the user reacts to anything in the briefing ("that's done", "move that to tomorrow", "drop that"), update `memory/tasks.md` accordingly. Confirm, commit, and push to `origin`.

### 9. Optional vault write (only if `vault_dir` configured)

Offer to write the briefing to `${vault_dir}/${vault_daily}/YYYY-MM-DD.md` via `/obsidian daily-log` with section name `Briefing`. Default to "yes" if the user has confirmed once before; otherwise ask. Skip silently if `vault_dir` is unset.

## Example output

```
## Morning Briefing — 2026-11-06

### Calendar (Fixed)
- 21:00 - 22:00: Simak Regular Meeting

### Open Focus Windows
- 05:30 - 06:30 · Living Room — Post-Subuh habit stack (strength training)
- 08:30 - 11:30 · Study Desk — Morning Deep Work (Priority #1: Interview prep / Go)
- 14:00 - 15:30 · Study Desk — Afternoon low-friction block (Graduation checklist / App review)

### Tasks Due / Active
- [ ] Verify university graduation checklist and clearance deadlines
- [ ] Submit junior developer applications (3-5 target roles)
- [ ] Break down Go learning into first reachable mini-module

### Watch
- Break interview prep and Go tasks into concrete, reachable mini-goals
- December graduation timeline (~1 month remaining)

### Reminders
- Phone in another room during the 08:30 - 11:30 morning study session
- Save low-friction tasks for the afternoon
```

*Prompt: "You have 08:30 - 11:30 open for Interview Prep. What concrete deliverable will you lock in during this block, and what is your #1 distraction risk?"*
## Notes

- Use the user's local timezone for "today" (`config.yaml: timezone` overrides system TZ)
- Keep the briefing under 20 lines unless there's genuinely a lot
- Don't read all memory files — just what's listed in step 2
- If `priorities.md` or `personal.md` is empty (fresh repo), skip those sections silently
- Vault writes are optional — only happen when `vault_dir` is configured

## Learned from runs

(empty — populated as the skill is used)

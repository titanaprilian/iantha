---
name: morning
description: Daily GTD engagement briefing — check the Google Calendar hard landscape, then match unblocked next actions to context, time, energy, and priority. Elicit Titan's own deliverable and obstacle before inserting any focus block. Use for /morning, "what's on my plate today", "what should I focus on", or a daily standup; optionally write the briefing to the configured vault.
---

# /morning — Daily Briefing

Use the GTD engagement criteria: context, available time, energy, and priority — after respecting calendar commitments. Capture remains separate from clarification and scheduling.

## Instructions

When the user runs `/morning`, do the following:

### 1. Load config & target date

Read `config.yaml` (and `config.local.yaml` if it exists, with local overriding).
Determine the target date (default: today; if user requested tomorrow, e.g. "for tomorrow", use tomorrow's date).

### 2. Read memory

- `memory/inbox.md` — unprocessed time-bound inputs
- `memory/projects.md` — active outcomes and their linked actions
- `memory/next-actions.md` — unblocked actions, due dates, and routines by context
- `memory/waiting-for.md` — externally blocked items and follow-up dates
- `memory/personal.md` — routines and life context (energy windows, boundaries)
- `memory/reference.md` — operational rules, constraints, and tool settings
### 3. Calendar — the hard landscape

- Check `gws auth status`. If authenticated, query Google Calendar for the target date via `gws calendar +agenda --today --timezone "<timezone>" --format json` or `gws calendar +agenda --tomorrow --timezone "<timezone>" --format json`. Extract all-day commitments and event start/end, summary, and location; these are fixed, not candidates to replace with discretionary work. For another requested date, use the calendar API's timeMin/timeMax in the user's local timezone rather than pretending `--today` means that date.
- Calculate actual open windows around fixed commitments, accounting for the remaining day and the user's location. If authentication fails or the calendar query is unavailable, say calendar availability is unverified: give action options, but do not assert that a specific window is free or insert a block until checked. Never silently treat missing calendar data as an empty calendar.

### 4. Match context, time, energy, and priority

- Select only uncompleted, unblocked entries from `memory/next-actions.md`; exclude `## Completed` and all `waiting-for.md` items. Check `projects.md` for the linked Active project; do not present project titles as executable work.
- **Context:** match `@deep-work` to an uninterrupted study workspace, `@admin` / `@computer-light` to light computer time, `@offline` to in-person/physical opportunities, `@comms` to available communication channels. **Time:** compare estimated `[Nm, energy]` to the real open window, allowing the user's 50-minute focus / 10-minute break rhythm. **Energy:** prefer high-energy `@deep-work` in Titan's morning focus hours; low-energy admin work fits later.
- Show dated actions and routines due today or overdue with their original dates; surface dated waiting-for follow-ups and time-sensitive raw inbox entries separately. Do not process inbox items here or promise an unclarified item a slot. If no action meets the constraints, state that instead of fabricating a task.
- Briefly show the calendar commitments, verified open windows, feasible next-action IDs/context/duration/energy, due items, and blockers. Omit empty sections; do not manufacture locations, appointments, free windows, or implementation intentions.

### 5. Elicit the user's implementation intention

Follow `memory/reference.md`: ask Titan which feasible action and window they want, what **concrete deliverable** they will complete, and their **#1 obstacle or distraction risk**. Ask for the physical location and response to that obstacle when not supplied. Do not generate the deliverable, risk, or if-then response with AI. If Titan cannot decide, offer the matching next actions and leave the calendar unchanged.

### 6. Validate and insert the chosen block

- Only after Titan supplies the deliverable, obstacle, response, and physical location, recheck the chosen window against Google Calendar. Confirm the proposed action, time, location, deliverable, and if-then plan with Titan; insert only after confirmation. No insertion if the calendar is unavailable, the slot conflicts, or the intention is still incomplete.
- Use `gws calendar +insert --summary "<user's action verb + deliverable>" --start "<YYYY-MM-DDTHH:MM:SS+OFFSET>" --end "<YYYY-MM-DDTHH:MM:SS+OFFSET>" --location "<user's physical workspace and phone-free boundary>" --description "<I will [user behavior] at [time] in [location]; definition of done [user deliverable]; if [user obstacle], I will [user response]>"`. Use the correct local timezone offset from `config.yaml` and verify the command succeeded before confirming the event.
- Scheduling a focus block does not mark its next action complete; completion requires Titan's confirmation.

### 7. Surface, don't auto-dispatch task work

This is a planning briefing, not a work execution session. Do not start executing the tasks themselves unless the user asks.

### 8. Offer action updates

If the user confirms an action is done, check it off and record the date/outcome in the project log or Completed archive; elicit and link the next action for any ongoing Active project. Advance a completed recurring action's next due date. Commit changed memory and push to `origin`. Use `/clarify` separately to process inbox entries.

## Notes

- Use the user's local timezone (`config.yaml: timezone` overrides system TZ).
- Keep the briefing short and actionable. When the calendar is unavailable, state the availability limit instead of showing invented open windows.
- If `personal.md` is missing details, skip its guidance; do not fill it by inference.

## Learned from runs

(empty — populated as the skill is used)

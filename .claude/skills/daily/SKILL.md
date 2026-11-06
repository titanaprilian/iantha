---
name: daily
description: Daily focus check-in — pulls today's pre-timeboxed schedule from Google Calendar via gws, primes focus boundaries (phone-free, 50/10 rhythm), and highlights today's execution plan. Use for /daily, "start my day", "what's on my plate today", or daily standup.
---

# /daily — Daily Focus Check-in

Execute the timeboxed plan. No planning friction or decision fatigue — read today's schedule from Google Calendar, prime workspace boundaries, and get straight to work.

## Instructions

When the user runs `/daily`, do the following:

### 1. Load config & target date
Read `config.yaml` (and `config.local.yaml` if present) for `timezone` and `user_name`. Default target date is today.

### 2. Pull today's calendar schedule
Check `gws auth status`. Query Google Calendar:
```bash
gws calendar +agenda --today --timezone "<timezone>" --format json
```
Display today's timeboxed agenda chronologically:
- Fixed appointments and meetings
- Timeboxed focus blocks (show scheduled deliverable and boundary from event summary/description)

If Google Calendar is not authenticated or fails, alert Titan immediately so auth can be refreshed.

### 3. Prime focus boundaries
Remind Titan of the environment rules from `memory/personal.md` and `memory/reference.md`:
- **Phone-free boundary**: Phone in another room during `@deep-work` focus blocks.
- **Rhythm**: 50-minute deep work cycles with 10-minute active breaks.

### 4. Fast scan: urgent or overdue items
Quickly check:
- `memory/next-actions.md`: Any action with a hard deadline due today or overdue.
- `memory/waiting-for.md`: Any follow-ups due today.
- `memory/inbox.md`: Any raw input explicitly tagged with today's date.
Mention these in 1–2 bullet points if they exist; omit cleanly if none.

### 5. Transition to execution
Present the first upcoming block and prompt Titan to start. Do not negotiate a new schedule unless Titan explicitly requests changes.

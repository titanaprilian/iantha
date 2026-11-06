---
name: daily-review
description: End-of-day loop closure — confirm completed calendar blocks and actions, log outcomes, sweep loose thoughts to inbox, and preview tomorrow's schedule. Use for /daily-review, "close out the day", "daily review", or daily wrap.
---

# /daily-review — Daily Review & Loop Closure

A fast 2-minute closeout. Confirm what got done today, capture loose thoughts into the inbox, and preview tomorrow's timebox.

## Instructions

When the user runs `/daily-review`, do the following:

### 1. Load config
Read `config.yaml` (and `config.local.yaml` if present) for `timezone` and `user_name`.

### 2. Confirm completed blocks & actions
Review today's timeboxed calendar blocks and `memory/next-actions.md`. Ask Titan:
- Which scheduled actions or focus blocks were completed today?
- What was the concrete outcome?

For each confirmed completion:
1. Mark the action `[x]` and move it to `## Completed` in `memory/next-actions.md` with completion date and outcome:
   `- [x] [YYYY-MM-DD] A## · @context — action [Nm, energy] — outcome`
2. If the action belonged to an Active project in `memory/projects.md`:
   - If the whole project is finished, mark it `Completed` with completion date.
   - If more tasks remain, verify that the next task is staged or capture any new step.
3. For recurring routines (e.g., Subuh prayer + workout), advance "Next due" to the next day.

### 3. Sweep loose thoughts into the inbox
Ask Titan:
> *"Any open loops, thoughts, requests, or ideas from today to get out of your head?"*

Append any responses verbatim to `memory/inbox.md` under `## Unprocessed` (Rule A). Do not clarify or schedule them now; they will be processed during `/weekly-review`.

### 4. Preview tomorrow's schedule
Query Google Calendar for tomorrow:
```bash
gws calendar +agenda --tomorrow --timezone "<timezone>" --format json
```
Show tomorrow's scheduled commitments and timeboxed focus blocks so Titan has full visibility before shutting down.

### 5. Commit & push
Update `*Updated: YYYY-MM-DD HH:MM*` headers on touched memory files, commit, and push:
```bash
git commit -m "review: YYYY-MM-DD daily wrap — N actions completed"
git push origin main
```

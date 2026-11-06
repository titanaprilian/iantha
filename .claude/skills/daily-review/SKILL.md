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

For each confirmed completion, use `scripts/archive_completion.py` so the active list and monthly log stay consistent:

1. Preview the exact record and change:
   ```bash
   python3 scripts/archive_completion.py --id A03 --date YYYY-MM-DD --outcome "confirmed outcome"
   ```
   For a recurring routine, include `--next-due YYYY-MM-DD` with its next scheduled occurrence.
2. After confirming the proposed record matches Titan's report, apply it:
   ```bash
   python3 scripts/archive_completion.py --id A03 --date YYYY-MM-DD --outcome "confirmed outcome" --apply
   ```
3. For a recurring routine, append its occurrence to `memory/archive/completed/YYYY-MM.md`, keep the reusable routine in `memory/next-actions.md`, and update its next due date. One-off actions are removed from the active list after archival.
4. If a completed action belonged to an Active project in `memory/projects.md`:
   - Ask whether the project's outcome is finished. If yes, mark it `Completed` with date and confirmed outcome.
   - If not finished, set `Next Action ID/Name` to the next uncompleted linked action in `memory/next-actions.md`; if no action remains, elicit and add a new concrete next action before ending review.

The script rejects ambiguous IDs, duplicate same-day completion records, missing recurring next-due dates, and attempts to advance one-off tasks. `memory/next-actions.md` is active-only: never retain completed entries or a Completed section there.

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

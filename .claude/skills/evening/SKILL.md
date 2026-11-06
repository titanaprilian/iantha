---
name: evening
description: End-of-day GTD wrap — confirm and check off completed next actions, elicit the next physical step for touched projects, advance completed routines, and surface tomorrow's commitments. Use for /evening, "wrap up the day", "close out", or a daily planning wrap; optionally write to the configured vault.
---

# /evening — Daily Wrap

Confirm completions, keep Active projects moving, and surface tomorrow without processing the inbox by default.

## Instructions

When the user runs `/evening`, do the following:

### 1. Load config

Read `config.yaml` (and `config.local.yaml` if present, with local overriding). Note whether `vault_dir` is set — controls step 6.

### 2. Confirm completed actions

Read `memory/next-actions.md` and `memory/projects.md`; ask Titan which actions actually finished and what the outcome was. Do not infer completion from a calendar event, elapsed time, or a checked box alone. Ask about unclear items.

### 3. Check off actions and keep projects moving

For each confirmed completion:

1. Mark the completed action `[x]` in `memory/next-actions.md`, preserving its ID, context, estimate, and original wording; move it to **Completed** with local completion date and confirmed outcome (`- [x] [YYYY-MM-DD] A## · @context — action [Nm, energy] — outcome`). A project `**Log:**` entry may hold additional detail, but never replace the completed action record with an unverified claim.
2. For every touched Active project, ask Titan whether the outcome is finished. If yes, move it to **Completed** with completion date and outcome. If not, **prompt Titan for the next physical step** with a concrete verb and observable result, context, duration, and energy; add a new unblocked action and replace the `Next Action ID/Name` link immediately. Do not invent a step or leave an Active project linked to its checked-off action. If progress genuinely depends on someone external, move the project **On Hold** and record a dated waiting-for entry instead.
3. If Titan cannot choose a next step, ask whether to consciously put the project **On Hold** (record why, and create a waiting-for entry only for an external dependency). Otherwise leave the discussion open and explicitly report the missing action; never pretend a completed action remains pending or claim the Active-project invariant holds. Update the `*Updated:*` header in each changed file.

### 4. Roll over recurring actions

For each daily routine Titan confirms completed, record that occurrence as `[x]` with the completion date/outcome in **Completed**; leave the reusable routine in its original context and advance "Next due" by one cadence. Never mark a missed occurrence done or advance without confirmation.

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
evening: YYYY-MM-DD wrap — N actions completed, M recurring advanced
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

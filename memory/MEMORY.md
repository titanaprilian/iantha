# Iantha Memory Index

*Updated: 2026-11-06 10:57*

Iantha reads this at session start. This file is an index — full content lives in the per-topic files below.

## Files

| File | Purpose |
|------|---------|
| `inbox.md` | Raw, unclarified inputs awaiting processing |
| `projects.md` | Multi-step outcomes, status, and linked next actions |
| `next-actions.md` | Unblocked physical actions by context, duration, and energy; recurring actions |
| `waiting-for.md` | Externally blocked or delegated items, with date and owner |
| `someday-maybe.md` | Incubating ideas without active commitments |
| `archive/tasks-pre-gtd.md` | Preserved pre-GTD task list; historical reference only |
| `personal.md` | About the user — preferences, routines, people, life context |
| `priorities.md` | Top focus areas, ranked |
| `decisions.md` | Decisions with date and rationale |
| `feedback.md` | Corrections and confirmed approaches from the user |
| `learnings.md` | Operational knowledge, tool gotchas, workflow insights |

## Conventions

- File timestamps use the header `*Updated: YYYY-MM-DD HH:MM*` (user's local timezone)
- Capture ambient tasks, ideas, worries, and time intents verbatim in `inbox.md` as `- [ ] <user's exact words>`; do not classify or schedule on capture. Process each entry interactively with `/clarify`, including the two-minute rule, trash, reference, incubation, projects, next actions, and waiting-for.
- GTD invariant: Every active project in `projects.md` must have at least one unblocked action in `next-actions.md`.
- Use stable action IDs to link projects and actions. Completed actions must be replaced for ongoing projects; move externally blocked outcomes to On Hold until unblocked.
- Contexts in `next-actions.md`: `@deep-work`, `@admin` / `@computer-light`, `@offline`, and `@comms`; record duration and energy for each action.
- Decisions have dates and a `**Why**:` line — without the why, edge cases can't be judged later
- Personal context is silently updated (Rule B); no need to announce small additions
- Daily logs (if used) live in `memory/daily/YYYY-MM-DD.md` — opt-in, not created by default

## On staleness

Memory drifts. If a recalled fact conflicts with what the user just said or what's currently on disk, trust the new information and update the memory entry. Don't act on stale memory.

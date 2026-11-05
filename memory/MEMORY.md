# Iantha Memory Index

Iantha reads this at session start. This file is an index — full content lives in the per-topic files below.

## Files

| File | Purpose |
|------|---------|
| `tasks.md` | All actionable items (urgent / work / personal / recurring / archive) |
| `personal.md` | About the user — preferences, routines, people, life context |
| `priorities.md` | Top focus areas, ranked |
| `decisions.md` | Decisions with date and rationale |
| `feedback.md` | Corrections and confirmed approaches from the user |
| `learnings.md` | Operational knowledge, tool gotchas, workflow insights |

## Conventions

- File timestamps use the header `*Updated: YYYY-MM-DD HH:MM*` (user's local timezone)
- Tasks have priority labels (P0 / P1 / P2 / P3) where useful — not required
- Decisions have dates and a `**Why**:` line — without the why, edge cases can't be judged later
- Personal context is silently updated (Rule B); no need to announce small additions
- Daily logs (if used) live in `memory/daily/YYYY-MM-DD.md` — opt-in, not created by default

## On staleness

Memory drifts. If a recalled fact conflicts with what the user just said or what's currently on disk, trust the new information and update the memory entry. Don't act on stale memory.

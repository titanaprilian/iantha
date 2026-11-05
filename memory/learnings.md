# Learnings

*Updated: 2026-11-05 16:20*

Operational knowledge picked up during sessions. Tool gotchas, workflow insights, patterns that worked or failed.

Different from `decisions.md` (which records *choices*). Different from `feedback.md` (which records user corrections). Learnings are *observations* — things that turned out to be true.

## Workflow

(How tasks actually get done — patterns and sequences that work.)
- Habit stacking around existing anchors: Stacking physical workouts and morning deep focus blocks directly after Subuh prayer eliminates morning decision friction.

## Tools

(Quirks, gotchas, and tips for tools the user relies on.)
- Git remote configuration: Setting `origin` to `git@github.com:titanaprilian/iantha.git` (SSH) and `upstream` to `kiloloop/iantha` enables clean personal pushes while leaving upstream template updates reachable.
- gws OAuth test mode: Personal GCP OAuth app in testing status returns Error 403 access_denied unless user email is added explicitly to the OAuth consent screen's 'Test users' list.
- gws calendar queries: Use `--format json` and pass `--timezone` explicitly (e.g. `config.yaml: timezone`) to prevent terminal wrapping and timezone mismatches.

## Patterns

(Repeating shapes — when X happens, Y usually follows. Useful for prediction and proactive surfacing.)

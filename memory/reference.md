# Reference

*Updated: 2026-11-06 11:20*

Non-actionable knowledge, confirmed operational approaches, and tool configurations.

## User Constraints & Rules

### Implementation Intentions Elicitation
- **Rule**: In `/morning` and `/calendar`, do not auto-generate implementation intentions with AI. Instead, surface open focus windows and elicit the concrete deliverable, physical location, #1 obstacle/distraction risk, and if-then response directly from Titan.
- **Why**: Cognitive psychology research (Gollwitzer 1999, d=0.65; Slamecka & Graf 1978 Generation Effect) shows intentions only trigger automated cue-response actions when actively formulated and internalized by the human. AI-generated intentions are treated as passive calendar noise.
- **How to apply**: Scaffold Titan's own words into Google Calendar metadata (`--summary`, `--location`, `--description`).

### Git Remote & Memory Backups
- **Rule**: Automatically commit and push to `origin` (`git@github.com:titanaprilian/iantha.git`) after every memory update.
- **Why**: Ensures personal context, tasks, and daily logs are safely backed up and synced across workstations without manual intervention.
- **Topology**: `origin` points to `git@github.com:titanaprilian/iantha.git` (SSH), `upstream` points to `kiloloop/iantha`.

### Concrete Mini-Goals
- **Rule**: Reject vague task descriptions (e.g. "learn Go", "interview prep").
- **Why**: Generic goals lack clear completion criteria and cause decision paralysis.
- **How to apply**: Elicit physical starting actions with observable results during `/clarify` and `/weekly-review`.

## Tools & Integrations

### Google Calendar (`gws`)
- **CLI**: `@googleworkspace/cli` (`gws`) manages calendar events and agendas directly.
- **OAuth Test Mode**: Personal GCP OAuth app in testing status returns `Error 403 access_denied` unless the user email is explicitly added to the OAuth consent screen's 'Test users' list.
- **Query Flags**: Use `--format json` and pass `--timezone "<timezone>"` (from `config.yaml`) explicitly to prevent terminal line wrapping and timezone drift.
- **Credentials**: Auth token and desktop client credentials live in `~/.config/gws/`.

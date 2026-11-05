---
name: calendar
description: Google Calendar integration via gws CLI — view today's agenda, inspect upcoming events, and schedule new events or focus blocks. Use whenever the user mentions calendar, agenda, scheduling an event, checking free/busy times, or types /calendar.
---

# /calendar — Google Calendar Integration

Interact with Google Calendar via the `gws` CLI.

## Prerequisite

`@googleworkspace/cli` (`gws`) installed and authenticated:
- Verify auth: `gws auth status`
- Login if needed: `gws auth login -s calendar`

## Instructions

### 1. View Agenda (`/calendar`, `/calendar today`, `/calendar week`)

Retrieve upcoming events using the user's timezone from `config.yaml` (default: system TZ):

- **Today**:
  ```bash
  gws calendar +agenda --today --timezone "<timezone>" --format json
  ```
- **Tomorrow**:
  ```bash
  gws calendar +agenda --tomorrow --timezone "<timezone>" --format json
  ```
- **Week**:
  ```bash
  gws calendar +agenda --week --timezone "<timezone>" --format json
  ```
- **Custom days ahead**:
  ```bash
  gws calendar +agenda --days <N> --timezone "<timezone>" --format json
  ```

Format results cleanly:
```markdown
### Calendar (YYYY-MM-DD)
- HH:MM - HH:MM: Event title
```
If an event is all-day, format without times:
```markdown
- All day: Event title
```

### 2. Schedule an Event or Focus Block (`/calendar add`, "schedule X")

When scheduling personal focus blocks, study sessions, or habit routines, apply *Atomic Habits* **Implementation Intentions**:
- `--summary`: Concrete action verb + outcome (avoid vague titles like "Deep Work").
- `--location`: Physical space + boundary cue (e.g. `Study Desk (Phone in another room)`).
- `--description`: Structured with intention, definition of done, and obstacle plan:
  ```text
  🎯 Implementation Intention:
  I will [BEHAVIOR] at [TIME] in [LOCATION].

  ✅ Definition of Done:
  - [Measurable outcome / deliverable]
  - [Boundary maintained]

  ⚡ If-Then Rule:
  If I encounter distraction or urge to context-switch, I will note it down on paper and stay in the session.
  ```

Execute via `gws calendar +insert`:
```bash
gws calendar +insert \
  --summary "<title>" \
  --start "<YYYY-MM-DDTHH:MM:SS+OFFSET>" \
  --end "<YYYY-MM-DDTHH:MM:SS+OFFSET>" \
  --location "<location>" \
  --description "<formatted description>"
```

Additional optional flags:
- `--meet`: Automatically attach a Google Meet link (for meetings)
- `--attendee "<email>"`: Add participant email

Confirm event details with the user after inserting (title, date/time, and Meet URL if present).
## Notes

- Timezone: Read `config.yaml: timezone`. Ensure ISO 8601 strings include the correct offset.
- Formats: Use `--format json` internally when parsing events to avoid terminal wrapping.
- Errors: If `gws` exits with code 2 (auth error), advise the user to run `gws auth login -s calendar`.

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

When scheduling personal focus blocks, study sessions, or habit routines, first follow `memory/feedback.md`: ask the user for the concrete deliverable, physical location, #1 obstacle/distraction risk, and their own if-then response. Do not AI-generate any of these or insert a block until the user confirms the plan and the requested time is available on Google Calendar. Use the confirmed words to encode *Atomic Habits* Implementation Intentions:
- `--summary`: User's concrete action verb + deliverable (avoid vague titles like "Deep Work").
- `--location`: User's physical workspace + confirmed boundary cue (e.g. `Study Desk (Phone in another room)`).
- `--description`: User's intention, definition of done, and obstacle response:
  ```text
  Implementation Intention:
  I will [user's behavior] at [time] in [location].

  Definition of Done:
  - [user's deliverable]
  - [user's focus boundary]

  If-Then Rule:
  If [user's obstacle/distraction occurs], I will [user's response].
  ```
No placeholder may be inserted as event content.

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

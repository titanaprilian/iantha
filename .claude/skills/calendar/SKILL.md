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

### 2. Schedule an Event (`/calendar add`, "schedule X")

When the user asks to schedule an event or focus block, insert it via `gws calendar +insert`:

```bash
gws calendar +insert \
  --summary "<title>" \
  --start "<YYYY-MM-DDTHH:MM:SS+OFFSET>" \
  --end "<YYYY-MM-DDTHH:MM:SS+OFFSET>"
```

Optional flags:
- `--description "<details>"`: Event notes or agenda
- `--location "<place>"`: Location or room
- `--meet`: Automatically attach a Google Meet link
- `--attendee "<email>"`: Add participant email

Confirm event details with the user after inserting (title, date/time, and Meet URL if present).

## Notes

- Timezone: Read `config.yaml: timezone`. Ensure ISO 8601 strings include the correct offset.
- Formats: Use `--format json` internally when parsing events to avoid terminal wrapping.
- Errors: If `gws` exits with code 2 (auth error), advise the user to run `gws auth login -s calendar`.

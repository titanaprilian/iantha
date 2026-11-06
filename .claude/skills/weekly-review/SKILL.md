---
name: weekly-review
description: Complete GTD weekly review — Get Clear (process inbox), Get Current (calendar, waiting-for, projects and actions), Get Creative (someday/maybe). Use for /weekly-review or when Titan asks to review all commitments for the week.
---

# /weekly-review — Get Clear, Get Current, Get Creative

A guided review, not automatic task execution. Read `config.yaml` and any `config.local.yaml` override for timezone; use the user's local date. Keep existing deadlines and status unchanged unless Titan confirms a change. Do not claim an empty inbox or a verified calendar when either is unavailable.

## 1. Get Clear — collect and process

- Read `memory/inbox.md` in full. Ask Titan about any loose paper, notes, and other uncaptured commitments; append their words verbatim to the inbox under Rule A before processing.
- Invoke `/clarify` to decide every inbox entry one by one. Route trash, reference, someday/maybe, under-two-minute actions, projects plus next actions, standalone actions, and waiting-for as that skill specifies. Let Titan do two-minute actions; do not mark them done until confirmed. Pause on unresolved entries instead of deleting them.
- Re-read the inbox. Report its actual unprocessed count and which decisions are still needed; "inbox empty" only if no captured entries remain.

## 2. Get Current — audit all commitments

- **Waiting for:** Read every open entry in `memory/waiting-for.md`. Ask whether it arrived or needs follow-up; for resolved dependencies, remove/close the waiting entry and make the next physical action available in `memory/next-actions.md`. For still-blocked items, preserve the person/entity, handoff/follow-up date, and any deadline; surface overdue follow-ups without pretending they are actionable work.
- **Calendar, past and coming two weeks:** Check `gws auth status`. If authenticated, use `gws calendar +agenda --days 14 --timezone "<timezone>" --format json` to inspect upcoming commitments across calendars. For the preceding 14 days (including events earlier today), list all calendars with `gws calendar calendarList list --page-all --format json` and for each relevant calendar call `gws calendar events list --params '{"calendarId":"<id>","timeMin":"<local date 14 days ago>T00:00:00<offset>","timeMax":"<local date tomorrow>T00:00:00<offset>","singleEvents":true,"orderBy":"startTime","maxResults":250}' --page-all --format json`; retain correct local offsets at each boundary. Review missed follow-ups and incoming commitments with Titan; capture new ones verbatim to inbox and run `/clarify` on them. If auth, pagination, or a calendar query fails, disclose the gap and do not say the period was reviewed.
- **Projects:** Read `memory/projects.md` and the uncompleted entries in `memory/next-actions.md`. For each **Active** project, verify its linked `Next Action ID/Name` exists under a context heading, is physically executable, unblocked, and has duration and energy. If missing or completed, elicit and add a new physical next action immediately, then update the project link in the same session. If the project is finished, ask Titan and move it to Completed with the date/outcome; if no action is possible pending an external entity, move it On Hold with a dated waiting-for record. Recheck On Hold projects for new availability. Never leave a project Active without a linked, unblocked next action.
- **Actions and routines:** Scan each context list for done items, stale or overdue dates, and recurring "Next due" dates. Check off only confirmed completions; archive the date/outcome in the project log or `next-actions.md` Completed section; advance completed routines. Ask Titan what still matters; do not automatically reschedule overdue work or rewrite priorities.

## 3. Get Creative — incubate and activate intentionally

- Skim `memory/someday-maybe.md` with Titan. Ask which ideas to keep, discard (only with confirmation), or activate. For an activated multi-step idea, elicit an outcome and first unblocked physical action with context, duration, and energy; create the Active project and its linked next action together. A single-step idea becomes a next action. Remove from someday/maybe only after its new home is recorded.
- Recap decisions, missing links, dated follow-ups, inbox remainder, and any unavailable calendar coverage. Update touched files' `*Updated: YYYY-MM-DD HH:MM*` headers in the configured local timezone; commit and push memory changes to `origin`.

## Learned from runs

(empty — populated as the skill is used)

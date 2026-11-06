---
name: weekly-review
description: 2-Step Weekly Review — (1) Clarify inbox into single tasks or projects and collect project tasks, then (2) timebox the tasks directly into Google Calendar for the week. Use for /weekly-review, "plan my week", or weekly planning.
---

# /weekly-review — 2-Step Weekly Planning

The core weekly cadence. Process the entire inbox into concrete tasks and projects, then distribute those tasks directly into Google Calendar as a timeboxed plan for the coming week.

## Instructions

When the user runs `/weekly-review`, execute the following two steps in order:

---

## STEP 1: Review & Clarify

Read `memory/inbox.md` and audit existing items. Empty the inbox line by line by determining the nature of each item:

### 1. Actionable Check
- If **Not actionable**:
  - Trash (confirm with Titan)
  - Reference knowledge $\rightarrow$ `memory/reference.md`
  - Someday/Maybe $\rightarrow$ `memory/someday-maybe.md`
- If **Under 2 minutes**: Prompt Titan to do it now.

### 2. Single Task vs. Project
- If **Single Task**:
  - Assign context (`@deep-work`, `@admin` / `@computer-light`, `@offline`, `@comms`), duration, and energy tag (e.g. `[50m, high-energy]`).
  - Add to `memory/next-actions.md`.
- If **Project** (outcome requiring more than one physical step):
  - Record the project in `memory/projects.md` (`P##`) with title and concrete definition of done.
  - **Collect all its concrete tasks**: Prompt Titan:
    > *"What are all the immediate tasks needed to move this project forward this week?"*
  - Add each collected task into `memory/next-actions.md` linked to the project (`A## · P##`), tagged with context, duration, and energy.

### 3. Waiting For
- If any task is blocked on someone else, record it in `memory/waiting-for.md` with date and owner.

### 4. Audit Existing Projects
- Inspect all Active projects in `memory/projects.md`: ensure every active project has at least one unblocked action in `memory/next-actions.md`.

Once clarified, remove processed items from `memory/inbox.md` and update `*Updated:*` timestamps.

---

## STEP 2: Timebox into Calendar
Take the unblocked tasks from `memory/next-actions.md` and schedule them into Google Calendar for the next 7 days using the deterministic engine `scripts/schedule.py`.

### 1. Compute Proposal with Deterministic Engine
Run `scripts/schedule.py` to generate the mathematically sound, conflict-free proposal:
```bash
python3 scripts/schedule.py --days 7 --dry-run
```
This automatically enforces:
- **Daily Workouts**: 05:30–06:30 (1 hour full block, alternating Strength and Jogging). Color: `10` (Basil Green).
- **Morning MUST-FILL Window**: 08:30–11:30 (3x 50/10 cycles: 08:30–09:20, 09:30–10:20, 10:30–11:20) for `@deep-work`. Color: `9` (Cobalt Blue).
- **Afternoon MUST-FILL Window**: 13:00–15:00 (2x 50/10 cycles: 13:00–13:50, 14:00–14:50) for `@admin` and secondary tasks. Color: `1` (Lavender).
- **Weekend Rules**:
  - Saturday: Workout (05:30–06:30), Make Yogurt (07:00–08:00, Color `5`), Deep Work (08:30–11:30), Afternoon Buffer.
  - Sunday: Jogging (05:30–06:30), Durian Orchard (08:00–10:00, Color `5`), Weekly Review & Rest (14:00–15:00). No deep work on Sunday.
- **Micro-Tasks**: Quick chores (e.g. Chicken Coop at 16:45, Milk run on Friday at 16:30) are cleanly anchored with Color `5` (Banana Yellow).
- **Idempotency**: All events are tagged with `[iantha-task:ID]` in their description so re-running `/weekly-review` on Friday, Sunday, or any day never duplicates events.

### 2. Present Proposal to Titan
Display the day-by-day markdown proposal output by `scripts/schedule.py`. Show explicit time ranges, task titles, and color categories.

Ask Titan for approval:
> *"Does this timebox schedule look good, or would you like to adjust any slots before we write to Google Calendar?"*

### 3. Insert Events to Google Calendar
Upon Titan's confirmation, execute the script with `--apply`:
```bash
python3 scripts/schedule.py --days 7 --apply
```
This inserts all events via `gws` with explicit `colorId`, locations (`Study Desk (Phone in another room)`, etc.), and structured implementation intention descriptions.

### 4. Wrap & Commit
Commit touched files and push:
```bash
git commit -m "review: weekly review and deterministic timeboxing for week of YYYY-MM-DD"
git push origin main
```

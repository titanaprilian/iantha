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

Take the unblocked tasks from `memory/next-actions.md` and schedule them into Google Calendar for the next 7 days.

### 1. Fetch Calendar Hard Landscape
Check `gws auth status` and query Google Calendar for the coming week:
```bash
gws calendar +agenda --days 7 --timezone "<timezone>" --format json
```
Identify fixed commitments (classes, appointments) and locate the open focus windows across the week.

### 2. Propose Timeboxed Schedule
Match tasks from `memory/next-actions.md` to the user's energy patterns from `memory/personal.md`:
- **Morning focus hours**: Schedule `@deep-work` tasks in 50-minute blocks (or 50/10 cycles).
- **Afternoon hours**: Schedule `@admin` and low-friction tasks.
- **Buffers**: Leave ~20-30% buffer so the week does not collapse if an item overruns.

**CRITICAL FORMAT RULE**: Never list cryptic IDs like "A04 · A05" in the proposal table or summary. Titan must be able to read what each task actually is at a glance.

Format the proposal day by day with explicit times and full task titles/deliverables:

```markdown
### 📅 Proposed Weekly Timebox Plan

#### Saturday (YYYY-MM-DD)
- 05:30 - 06:15 · **R01**: Strength training (chest & legs) [@offline]
- 07:00 - 07:30 · **R03**: Make yogurt [@offline]
- 08:00 - 08:50 · **A04** (Golang): Set up Go workspace and write hello-world CLI [@deep-work]
- 09:00 - 09:50 · **A05** (Golang): Practice structs and slices exercises [@deep-work]
- 13:00 - 13:30 · **A14** (Admin): Review university graduation checklist [@admin]

#### Sunday (YYYY-MM-DD)
- 05:30 - 06:15 · **R02**: Jogging session [@offline]
- 08:00 - 08:50 · **A07** (Interview): Practice LeetCode #206 reverse linked list [@deep-work]
- 13:00 - 14:00 · **R04**: Check durian orchard [@offline]
...
```
For each proposed focus block, follow `memory/reference.md`:
- Ask Titan to confirm the slot and deliverable.
- Insert the event using `gws calendar +insert`:
```bash
gws calendar +insert \
  --summary "<action verb + concrete deliverable>" \
  --start "<YYYY-MM-DDTHH:MM:SS+OFFSET>" \
  --end "<YYYY-MM-DDTHH:MM:SS+OFFSET>" \
  --location "<workspace, e.g. Desk (Phone in another room)>" \
  --description "Task: <Action ID>; Definition of done: <deliverable>"
```

### 4. Wrap & Commit
Present the complete weekly timeboxed schedule. Commit all updated memory files and push to `origin`:
```bash
git commit -m "review: weekly review and timeboxing for week of YYYY-MM-DD"
git push origin main
```

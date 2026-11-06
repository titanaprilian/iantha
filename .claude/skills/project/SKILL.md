---
name: project
description: Dedicated project scoping and task breakdown — scopes project outcomes, recommends concrete bite-sized tasks aligned with the user's focus rhythm (50/10), and adds them to next-actions.md. Use for /project, /project P##, or when breaking down staged projects.
---

# /project — Dedicated Project Breakdown

Focuses purely on taking a project from `memory/projects.md`, refining its definition of done, and breaking it down into actionable, concrete tasks ready for calendar timeboxing.

## Instructions

When the user runs `/project` (or `/project [id/title]`), execute the following:

---

## 1. Select Project to Scope

Read `memory/projects.md`.
- If an ID or title was passed (e.g. `/project P01` or `/project Golang`), focus on that project.
- If no argument was passed:
  - List all `Unclarified` or `Active` projects that have no tasks or need further breakdown:
    ```markdown
    ### 📁 Projects Awaiting Breakdown:
    1. P01: Learn Basic Golang
    2. P02: Learn Mock Interview Software Engineer
    3. P03: Read The Pragmatic Programmer
    ...
    Which project would you like to break down? (Enter number or project title)
    ```
  - Let Titan choose.

---

## 2. Refine Outcome & Proactively Recommend Tasks

Once a project is selected:

1. **State the Target Outcome**:
   Confirm or propose a concrete Definition of Done (e.g., *"Outcome: Understand core syntax, structs, and build 1 working CLI tool"*).

2. **Proactively Recommend 3–5 Concrete Tasks**:
   Do not make Titan stare at a blank slate. Present an opinionated, bite-sized task proposal matching Titan's personal context from `memory/personal.md` (e.g., 50-minute deep work cycles, phone in another room, concrete mini-goals):

   ```markdown
   ### 💡 Recommended Tasks for [Project Title]:
   1. [A##] Open tutorial/docs and write down Go syntax essentials (variables, loops, structs) — `@deep-work` [50m, high-energy]
   2. [A##] Initialize repo and build a simple CLI argument parser in Go — `@deep-work` [50m, high-energy]
   3. [A##] Implement error handling and unit tests for the CLI tool — `@deep-work` [50m, high-energy]
   4. [A##] Bookmark 2 official Go reference repositories for idiom review — `@admin` [20m, low-energy]

   **Would you like to log these tasks, modify any, or add your own?**
   ```

---

## 3. Log Tasks & Link to Project

Once Titan confirms or modifies the tasks:

1. **Update `memory/projects.md`**:
   - Set status to `Active`.
   - Update `**Next Action ID/Name:**` to point to the first unblocked task.
   - List the scoped tasks under the project.

2. **Append to `memory/next-actions.md`**:
   - Add all confirmed tasks under their appropriate context heading (`@deep-work`, `@admin`, `@offline`, `@comms`):
     `- [ ] **A## · P##** — [Action verb + observable deliverable]. [Nm, energy]`

3. **Commit & Push**:
   Update timestamps on `memory/projects.md` and `memory/next-actions.md`:
   ```bash
   git commit -m "project: broke down [P##] with N tasks"
   git push origin main
   ```

4. **Prompt Titan**:
   - Check if any other `Unclarified` projects remain in `memory/projects.md`.
   - If yes:
     > *"Logged N tasks for [Project Title] in `memory/next-actions.md`! You still have unclarified projects remaining. Would you like to break down another project with `/project`, or run `/weekly-review` now to timebox your tasks into Google Calendar?"*
   - If all projects are scoped:
     > *"Logged N tasks for [Project Title] in `memory/next-actions.md`! All active projects are now scoped. Ready to timebox your week's tasks into Google Calendar with `/weekly-review`?"*

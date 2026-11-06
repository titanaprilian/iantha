---
name: clarify
description: Interactive GTD clarification workflow — processes inbox items one by one. Checks if inbox is empty, prompts user to categorize each item as a small single task or a project. For projects, guides project creation and collaboratively brainstorms/recommends aligned tasks to schedule.
---

# /clarify — Process & Clarify the Inbox

Turn raw captured inbox items into structured, actionable commitments. Helps the user decide whether an item is a single task or a multi-step project, and collaboratively recommends aligned tasks to break down projects.

## Instructions

When the user runs `/clarify`, execute the following workflow:

---

## 1. Inbox Emptiness Guard

Read `memory/inbox.md`. Scan the `## Unprocessed` section for active `- [ ]` entries.

- **If the inbox is empty** (no unprocessed `- [ ]` items):
  Stop immediately and prompt Titan:
  > *"Your inbox is currently empty! Add at least one task or thought to `memory/inbox.md` first (or tell me what's on your mind right now and I'll capture it) before running `/clarify`."*
  Do not proceed with clarification.

- **If items exist**:
  Report the count of items to process and begin clarifying them **one by one**, in file order.

---

## 2. Process Each Item (One by One)

Quote the raw entry to Titan:
> *"Processing: '[exact raw text]' (Deadline/Context if any)"*

### Step A: Actionable Check
Ask if this is actionable:
- **No**:
  - Trash (confirm with Titan before discarding)
  - Non-actionable knowledge / tool note $\rightarrow$ append to `memory/reference.md`
  - Someday/Maybe $\rightarrow$ append to `memory/someday-maybe.md`
- **Under 2 minutes**:
  - Prompt Titan to do it immediately. Mark done only when confirmed.

### Step B: Single Task vs. Project
Prompt Titan explicitly:
> *"Is this a mere small single task, or is it a project (requires more than one step to complete)?"*

---

### Step C: If It's a Single Task
1. Elicit a concrete physical action verb and observable result.
2. Tag with:
   - **Context**: `@deep-work`, `@admin` / `@computer-light`, `@offline`, or `@comms`
   - **Duration & Energy**: e.g., `[30m, low-energy]`, `[50m, high-energy]`
3. If blocked or waiting on someone $\rightarrow$ record in `memory/waiting-for.md` (`[YYYY-MM-DD] Task (Waiting on: Person/Entity)`).
4. Otherwise $\rightarrow$ append to `memory/next-actions.md`:
   `- [ ] **A## · standalone** — [verb + observable deliverable]. [Nm, energy]`

---

### Step D: If It's a Project
1. **Define the Project**:
   - Determine the project title and explicit **Outcome / Definition of Done**.
   - Create an entry in `memory/projects.md`:
     ```markdown
     ### P## — [Project Title]
     - **Outcome / Done:** [Concrete observable result]
     - **Status:** Active
     - **Next Action ID/Name:** [Will be linked to the first task below]
     ```

2. **Collect & Recommend Project Tasks**:
   Prompt Titan for the tasks related to this project, and **proactively offer recommendations** to help break it down into clean, reachable steps:
   > *"What immediate tasks do you see for this project?*
   > *Here are some recommended concrete steps to consider based on your goal: [Offer 2–3 specific, physical mini-tasks with suggested contexts and 50/10 timeframes] — which of these or your own tasks should we log?"*

3. **Log the Clarified Tasks**:
   For every approved task:
   - Assign context (`@deep-work`, `@admin`, `@offline`, `@comms`), duration, and energy.
   - Append to `memory/next-actions.md` linked to the project:
     `- [ ] **A## · P##** — [verb + observable deliverable]. [Nm, energy]`
   - Ensure the first task is linked in `memory/projects.md` under `Next Action ID/Name`.

---

## 3. Close the Loop

1. Once the disposition of the item (and all its sub-tasks if a project) is confirmed, remove only that processed line from `memory/inbox.md`.
2. Update the `*Updated: YYYY-MM-DD HH:MM*` headers in touched files (`memory/inbox.md`, `memory/projects.md`, `memory/next-actions.md`, `memory/reference.md`).
3. Commit and push:
   ```bash
   git commit -m "clarify: processed '[short summary of item]'"
   git push origin main
   ```
4. Move on to the next unprocessed item, or announce that the inbox is clean.

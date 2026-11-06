---
name: initial
description: Onboarding and intake interview — seeds or updates memory, collects raw tasks into memory/inbox.md, and transitions directly to /clarify. Use when the user types /initial, asks to set up or update their personal context, or wants to dump their current life and tasks. Detects whether the user has already run onboarding and offers to update personal context or focus on capturing inbox items.
---

# /initial — Onboarding & Intake Interview

Get the user from zero to a clarified, timebox-ready system. Asks, doesn't guess; captures raw tasks to `memory/inbox.md`, updates `memory/personal.md` if requested, and transitions directly to `/clarify`.

## Instructions

When the user runs `/initial`, execute the following:

### 1. Detect state: Initial vs Returning

Inspect `memory/personal.md` and `memory/inbox.md`.

- **Returning user** (`personal.md` already has entries like Name, Routines, Preferences):
  Acknowledge existing context immediately:
  > *"Welcome back! Your personal context (routines, preferences) is already set up. Do you want to update any personal preferences/routines, or jump straight into dumping your current inbox tasks for clarification?"*
  - If they want to update personal context $\rightarrow$ proceed to **Step 2 (Personal Context Q&A)** for the specific sections they want to adjust.
  - If they want to dump tasks $\rightarrow$ skip directly to **Step 3 (Inbox Capture)**.

- **Fresh user** (`personal.md` is empty/default):
  Offer the full intake:
  > *"Let's get your system set up. I'll ask a few quick questions to capture your personal context and current tasks, then we'll clarify them."*
  Proceed through **Step 2** and **Step 3**.

---

### 2. Personal Context (Optional for returning users)

Ask conversationally (every question is skippable):
1. **About & Life Context**: Name, primary role, key life situation or deadlines (e.g. graduation, job search).
2. **Routines**: Morning/evening anchors (e.g. Subuh prayer, workouts, regular commitments).
3. **Preferences**: Working rhythm (e.g. 50/10 focus blocks), workspace boundaries (e.g. phone in another room), communication preferences.
4. **People**: Key people worth remembering (collaborators, family, professors).

Save answers directly to `memory/personal.md` under the canonical section headers.

---

### 3. Inbox Capture

Prompt the user to do a complete brain dump:
> *"What's currently on your plate? Dump everything that has your attention — tasks, deadlines, project ideas, worries, open loops, or errands. Don't worry about structuring them yet; just list them out."*

For each item the user provides:
- Append verbatim to `memory/inbox.md` under `## Unprocessed` as:
  `- [ ] <Titan's exact words>`
- Preserve any stated dates, deadlines, or raw notes.
- Do **not** classify, structure, or schedule during this step (Rule A).

---

### 4. Transition to Clarify

Once the user finishes their brain dump:
1. Summarize how many items were captured into `memory/inbox.md`.
2. Update the `*Updated: YYYY-MM-DD HH:MM*` headers in `memory/personal.md` and `memory/inbox.md`.
3. Commit and push:
   ```bash
   git commit -m "initial: update personal context and capture inbox items"
   git push origin main
   ```
4. Immediately prompt to run `/clarify`:
   > *"Captured N items to your inbox. Let's clarify them now into single tasks or projects so we can get them onto your calendar. Ready to run `/clarify`?"*

If the user agrees, immediately execute the `/clarify` workflow.

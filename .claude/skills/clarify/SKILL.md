---
name: clarify
description: Batch GTD clarification — scans the entire inbox, predicts Task vs Project vs Routine for all items at once, prompts user for confirmation, then routes single tasks into next-actions.md and stages projects into projects.md for dedicated breakdown.
---

# /clarify — Batch Inbox Clarification

High-throughput, zero-drag inbox processing. Predicts classifications for the whole inbox in one table instead of agonizing one-by-one, routes single tasks and recurring routines immediately, and stages projects into `memory/projects.md` to be deeply broken down via `/project`.

## Instructions

When the user runs `/clarify`, execute the following workflow:

---

## 1. Empty Inbox Check

Read `memory/inbox.md`. Scan `## Unprocessed` for active items.
- If empty: Stop immediately and notify Titan to add at least one item first.
- If items exist: Proceed to Step 2.

---

## 2. Batch Classification & Prediction

Analyze **all** items in `memory/inbox.md` at once. Categorize each into:
- **Single Task / Routine**: Single actionable step or repeating habit (e.g. *"Throw organic trash"*, *"Buy milk on Friday"*, *"Jogging"*). Predict context (`@deep-work`, `@admin`, `@offline`, `@comms`), duration, and energy.
- **Project**: Multi-step outcomes requiring scoping and multiple tasks (e.g. *"Learn Basic Golang"*, *"Mock Interview Prep"*, *"Read Pragmatic Programmer"*).
- **Someday/Maybe / Non-Actionable**: Aspirational or passive ideas.

Present the entire batch prediction as a clean table:

```markdown
### 📋 Inbox Clarification Batch (N items)

| # | Raw Item | Type | Proposed Context / Cadence | Notes |
|---|---|---|---|---|
| 1 | Learn Basic Golang | 📁 Project | Multi-step | Stage for /project breakdown |
| 2 | Throw organic trash to chicken coop | ⚡ Single Task | @offline [10m, low-energy] | Immediate action |
| 3 | Check durian orchard every sunday | 🔄 Routine | @offline [Sunday cadence] | Recurring routine |
| ... | ... | ... | ... | ... |

**Does this classification look right?** 
Reply with:
- **"Yes"** (or Enter) to approve all and route them immediately.
- Or specify corrections (e.g., *"3 is a single task, not routine"*).
```

---

## 3. Immediate Routing

Once Titan confirms the table:

### A. Projects $\rightarrow$ `memory/projects.md`
- Append confirmed projects under `## Unclarified Projects`:
  ```markdown
  ### P## — [Project Title]
  - **Outcome / Done:** [Short target outcome]
  - **Status:** Unclarified
  - **Tasks:** (Run `/project` or `/project P##` to generate concrete tasks)
  ```
- **Do not** break down projects inside `/clarify`. Keep it fast.

### B. Single Tasks & Routines $\rightarrow$ `memory/next-actions.md`
- Route directly into `memory/next-actions.md` under their respective context headings (`@deep-work`, `@admin`, `@offline`, `@comms`) with duration and energy tags:
  `- [ ] **A## · standalone** — [Action]. [Nm, energy]`
  or for routines:
  `- [ ] **R## · Recurring** — [Routine]. [Cadence] (Next due: YYYY-MM-DD)`

### C. Clean Inbox & Commit
- Clear processed items from `memory/inbox.md`.
- Update `*Updated: YYYY-MM-DD HH:MM*` on touched files.
- Commit and push:
  ```bash
  git commit -m "clarify: batch processed N inbox items into tasks and projects"
  git push origin main
  ```
- Print a summary and prompt Titan:
  > *"Processed N items: M single tasks/routines moved to `next-actions.md`, K projects staged in `projects.md`. Run `/project` to break down your staged projects!"*

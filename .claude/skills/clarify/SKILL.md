---
name: clarify
description: Process captured GTD inbox inputs one by one into trash, reference, someday/maybe, two-minute completion, projects with linked next actions, single actions, or waiting-for. Use when Titan says /clarify, asks to process or empty the inbox, or asks what to do with captured items.
---

# /clarify — Process the Inbox

Turn unprocessed inputs into decisions, not a second task list. Capture happens separately under Rule A; do not pre-sort incoming ambient mentions.

## 1. Prepare

- Read `config.yaml` (and `config.local.yaml` if present) for the user's timezone. Read `memory/inbox.md` from top to bottom, then the five live GTD files plus `memory/learnings.md` and `memory/decisions.md` as needed. Preserve the raw inbox entry and its deadline until resolved. IDs are stable: allocate the next unused `P##` or `A##` by inspecting existing projects, actions, and completed history; never recycle an ID.
- Process exactly one inbox entry at a time, in file order. Quote its original wording to Titan and ask only for missing decisions. Do not treat guesses about outcomes, owners, or due dates as facts; retain unanswered entries in the inbox. Processing may stop at any point without deleting remaining entries.

## 2. Decide and route each entry

1. **Actionable?** Ask what the entry means and what a successful outcome looks like if unclear. If **no**, offer **Trash** (confirm before removing), **Reference** (file factual knowledge in `memory/learnings.md`, or an actual user decision in `memory/decisions.md` with date and `**Why**:`), or **Someday/Maybe** (append the idea to `memory/someday-maybe.md`). Do not turn an aspiration into an active commitment by default.
2. **Under two minutes?** If actionable and the user can do the entire action now in under two minutes, prompt them to do it immediately. Remove the entry only after they confirm it is done; if deferred, continue to the appropriate next-action/waiting-for branch and keep its due date. Do not claim to have completed it for them.
3. **More than one physical step?** If yes, elicit the project outcome/definition of done and **the first concrete, visible physical next action**. Ask for its context (`@deep-work`, `@admin` / `@computer-light`, `@offline`, `@comms`), estimated duration, and energy level. If an unblocked step exists, create `### P## — title` with `**Outcome / Done:**`, `**Status:** Active`, `**Next Action ID/Name:** A## — action` in `memory/projects.md` and `- [ ] **A## · P##** — verb + observable result. [Nm, energy]` under the matching heading in `memory/next-actions.md` in the same update. If all progress depends on someone else, instead create an **On Hold** project and a dated `waiting-for.md` entry; never create a fake next action. Keep stated deadlines.
4. **Single action?** Elicit a physical verb and observable result, context, estimated duration and energy. For an unblocked step, append `- [ ] **A## · standalone** — action. [Nm, energy]` to the matching context in `memory/next-actions.md`, retaining any stated due date. No project is needed.
5. **Waiting on someone?** For a delegated or externally blocked single action (or a project dependency identified in step 3), record `[YYYY-MM-DD] Task (Waiting on: Person/Entity)` in `memory/waiting-for.md`, using the date of handoff or follow-up and preserving any separate original deadline. Do not list a blocked action under an unblocked context. A project with another unblocked step can remain Active with that step and separately track the dependency.

If an item combines multiple commitments, clarify each in turn while preserving the source entry until all parts have been routed. If a requested reference is a document rather than a lesson/decision, ask where Titan wants it stored; do not invent a reference system or store it as an action.

## 3. Close each loop

- Confirm the disposition with Titan; then remove only that processed line from `memory/inbox.md`. Keep its exact text if the decision remains open, the two-minute action is unfinished, or any part has no destination. Never silently empty the inbox or silently discard a captured worry.
- Update `*Updated: YYYY-MM-DD HH:MM*` in the user's local timezone in every changed memory file; preserve existing entries. Confirm what was routed and what remains. Commit changed memory files and `git push origin` after updates.
- Repeat for the next line until the inbox is empty or Titan pauses. An empty inbox is an outcome of resolved decisions, not a deletion target.

## Learned from runs

(empty — populated as the skill is used)

---
name: debrief
description: Capture decisions, learnings, and feedback from the current session into memory/{decisions,learnings,feedback}.md. Use this whenever the user types /debrief, says "let's note what we decided" / "capture this" / "save this for next time", finishes a substantive session worth remembering across sessions, or wants to file a discrete decision with rationale. Single-agent personal version (vs cortex /debrief which is OACP-multi-agent).
---

# /debrief — Session Capture

Pull decisions, learnings, and feedback out of a session and into memory.

## Instructions

When the user runs `/debrief`, do the following:

### 1. Identify session content

Review what was discussed this session. Look for three categories of capturable content:

- **Decisions**: choices made that will affect future behavior (e.g., "we'll use X instead of Y", "stop doing Z")
- **Learnings**: operational knowledge discovered (tool gotchas, workflow insights, patterns that worked or failed)
- **Feedback**: corrections or confirmed approaches the user gave you ("don't do X", "yes exactly, keep doing that")

### 2. Propose decisions.md entries

For each decision, propose an entry:

```
## YYYY-MM-DD: [short title]
**Decision**: [what was decided]
**Why**: [reasoning]
**Notes**: [anything else relevant]
```

Show each proposal to the user. Apply only what they confirm.

### 3. Propose learnings.md entries

For each learning, propose an entry under the appropriate section (Workflow / Tools / Patterns):

```
- [short title]: [what was learned, in one or two lines]
```

Show, confirm, apply.

### 4. Propose feedback.md entries

For corrections or confirmed approaches, propose:

```
## [short rule]
**Why**: [the reason the user gave]
**How to apply**: [when this kicks in]
```

Include the *why* — it lets future-you judge edge cases.

### 5. Apply with confirmation

Apply each confirmed entry. Skip ones the user vetoes.

### 6. Commit & push

Stage updated memory files, commit, and push:

```
debrief: YYYY-MM-DD — N decisions, M learnings, K feedback
```

Push to `origin` so memory stays synced across machines.

## Notes

- Be selective. Not every session has decisions worth capturing. Skip silently if there's nothing real.
- Don't fabricate. If a "learning" is actually just routine work, don't promote it.
- If there's nothing to capture, say so: "No new entries this session."
- This skill is for substantive sessions — quick chats don't need a debrief.

## Learned from runs

(empty — populated as the skill is used)

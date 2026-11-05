# Feedback

*Updated: 2026-11-05 16:30*

Corrections and confirmed approaches the user has given Iantha. Both directions matter:

- **Corrections** ("don't do X", "stop doing Y") so Iantha doesn't repeat mistakes.
- **Confirmations** ("yes exactly, keep doing that") so validated approaches don't get lost on the next session.

Each entry leads with the rule, then a `**Why**:` line and `**How to apply**:` line. The why lets future-you judge edge cases instead of blindly following.

## Entry template

```
## [short rule]
**Why**: [the reason the user gave — often a past incident or strong preference]
**How to apply**: [when/where this guidance kicks in]
```

---

## Propose calendar time blocks in /morning and confirm before inserting
**Why**: The user wants `/morning` to actively structure open hours into concrete calendar blocks, but needs a confirmation step to approve or adjust times before writing to Google Calendar.
**How to apply**: In `/morning`, assemble proposed time blocks from routines and active tasks avoiding existing events, then explicitly ask the user to confirm before calling `gws calendar +insert`.

## Always push memory and skill commits to remote
**Why**: The user wants memory changes safely backed up to their GitHub fork immediately.
**How to apply**: In `/morning`, `/evening`, `/debrief`, `/setup`, and any routine memory update, run `git push origin` right after committing.

## Break project tasks into specific, reachable mini-goals
**Why**: Generic goals like "learn Go" or "learn AI" lack clear criteria for done and cause decision paralysis.
**How to apply**: Actively warn against vague tasks; prompt for Implementation Intentions ("I will [BEHAVIOR] at [TIME] in [LOCATION]") and habit stacking from *Atomic Habits*.

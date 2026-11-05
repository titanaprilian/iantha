# Decisions

*Updated: 2026-11-05 17:05*

Decisions the user has made. New entries go at the top (most recent first). Each entry needs a date and a `**Why**:` line — without the why, edge cases can't be judged later.

## Entry template

```
## YYYY-MM-DD: [short title]
**Decision**: [what was decided]
**Why**: [reasoning — constraints, tradeoffs, motivation]
**Notes**: [optional context]
```

---

## 2026-11-05: Human-elicited Implementation Intentions over AI generation
**Decision**: In `/morning`, do not auto-generate implementation intentions with AI. Instead, surface open focus windows and elicit the concrete deliverable and distraction risk directly from the user, then scaffold the user's words into Google Calendar metadata.
**Why**: Cognitive psychology research (Gollwitzer 1999, d=0.65; Slamecka & Graf 1978 Generation Effect) demonstrates that implementation intentions only trigger automated cue-response actions when actively generated and internalized by the human. AI-generated intentions lack personal commitment and are treated as passive calendar noise.
**Notes**: Elicitation prompt targets concrete deliverable + #1 distraction risk for the day's primary focus block.

## 2026-11-05: Integrate Google Calendar via gws CLI instead of Obsidian vault
**Decision**: Use `@googleworkspace/cli` (`gws`) with Google OAuth desktop client to manage calendar events and integrate daily schedule directly into `/morning` and `/calendar` skills.
**Why**: User prefers managing calendar events in Google Calendar over an Obsidian markdown vault.
**Notes**: Auth token and client credentials stored locally in `~/.config/gws/`.

## 2026-11-05: Push to personal fork on every memory update
**Decision**: Set remote origin to `git@github.com:titanaprilian/iantha.git` and automatically push to `origin` on every memory/skill commit.
**Why**: Ensures all personal context, tasks, and daily logs are backed up and synced across machines without manual git steps.
**Notes**: Upstream template tracked at `https://github.com/kiloloop/iantha.git`.

## 2026-11-05: Phone-free study sessions
**Decision**: No phone in the study area during deep work / study sessions; phone is kept in another room or out of reach.
**Why**: Protect focus and energy during exhaustive morning learning blocks (interview prep and Go concepts).
**Notes**: Eliminates friction and temptation to context switch.

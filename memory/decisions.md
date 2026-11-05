# Decisions

*Updated: 2026-11-05 16:20*

Decisions the user has made. New entries go at the top (most recent first). Each entry needs a date and a `**Why**:` line — without the why, edge cases can't be judged later.

## Entry template

```
## YYYY-MM-DD: [short title]
**Decision**: [what was decided]
**Why**: [reasoning — constraints, tradeoffs, motivation]
**Notes**: [optional context]
```

---

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

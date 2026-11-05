---
name: setup
description: First-run onboarding interview — offers to seed the blank memory files with the user's real life through a short, skippable Q&A, writes the answers into the live `.md` files in canonical format, then runs /morning on the real data. Use this whenever the user types /setup or /first-run, on a fresh clone with blank memory when they want to get started instead of learning-as-you-talk, or later to gap-fill memory sections that are still empty. Offered, never forced — a decline keeps the default learn-as-you-go behavior.
---

# /setup — First-Run Onboarding Interview

Get the user from a blank clone to their own filled memory in one sitting — by asking, not by guessing. Offered, never forced; every question skippable; writes only to the live `.md` files.

## Instructions

When the user runs `/setup` (or you offer it and they accept), do the following:

### 1. Load config + detect memory state

- Read `config.yaml` (and `config.local.yaml` if present, with local overriding). Note `timezone` (falls back to system TZ) and `user_name`.
- Inspect the four live memory files — `memory/tasks.md`, `memory/personal.md`, `memory/priorities.md`, `memory/decisions.md`. For each, decide **blank** vs **filled**: a file is blank if it still matches the template (only section headers + parenthetical placeholders, no real content). The `*.md.example` seeds are *not* the live files — never treat sample content as filled state.
- This sets the mode:
  - **First-run** — all four blank → offer the full interview.
  - **Gap-fill** — some filled, some blank (or a filled file with empty sections) → only interview the gaps; frame it as *"filling in what's still missing,"* not a fresh start.

### 2. Offer — don't force

- Open with a single line, no preamble:
  > *"Want me to ask a few quick questions to set up your memory, or just learn as we go?"*
- If the user **declines**: stop cleanly. The default learn-as-you-talk behavior (Rule B auto-capture) continues — that's the intended path, not a fallback. Don't re-offer this session, don't nag.
- This respects `personal.md`'s blank-on-purpose stance: the interview is the opt-in, not the default.

### 3. Run the interview — short, skippable

- ~5–8 questions, a few minutes total. Ask **a few at a time**, conversationally — not a wall of questions.
- **Every question is skippable; partial answers are fine.** If the user says "skip", "that's enough", or "rest later", stop asking and write what you have.
- Question set (each maps to a target file/section):

  | # | Question | Lands in |
  |---|----------|----------|
  | 1 | Name, role, what you're working on broadly | `personal.md` → About + Life Context |
  | 2 | Your top 3 focus areas right now | `priorities.md` → Top 3 |
  | 3 | Current tasks + any deadlines | `tasks.md` → Urgent / Work / Personal |
  | 4 | Routines worth knowing (gym, weekly review, standing commitments) | `personal.md` → Routines |
  | 5 | Key people (family, close colleagues) | `personal.md` → People |
  | 6 | Anything time-bound coming up (trips, events, renewals) | `tasks.md` + `priorities.md` → Watch |
  | 7 | How you like things (communication style, scheduling habits) | `personal.md` → Preferences |
  | 8 | Any standing decisions worth recording | `decisions.md` (only if one surfaces) |

- **Gap-fill mode**: skip any question whose target section is already filled. Ask only what's missing.
- Keep it light. This is intake, not an interrogation — let the user bail at any point.

### 4. Write answers to the live files in canonical format

- Write to the **live `.md` files only** — never the `*.md.example` seeds, and never copy seed content into live memory.
- Preserve each file's section structure and the `*Updated: YYYY-MM-DD HH:MM*` timestamp convention (user's local timezone per config). Use the `*.md.example` files as the format reference for what filled content looks like.
- Routing:
  - `personal.md` → About, Preferences, Routines, People, Life Context
  - `tasks.md` → Urgent (deadline ≤ 2 days), Work, Personal — honor Rule A's deadline-based placement; add `[P1]`/`[P2]` labels only where the user signaled urgency
  - `priorities.md` → Top 3, Active, Watch
  - `decisions.md` → only if a real decision surfaced — with a date and a `**Why**:` line (no why → don't log it as a decision)
- **Don't fabricate.** Write only what the user actually said. Leave a section blank rather than padding it with placeholder-looking content — a half-filled file the user can trust beats a full one they can't.
- Update the `*Updated:*` timestamp on every file you touch.

### 5. Close the loop — first real briefing

- Run `/morning` on the freshly seeded data. This is the user's first *real* briefing (not the sample-data demo), built from what they just told you.
- If `vault_dir` is configured, `/morning` will offer its usual daily-note write — let it.

### 6. Offer to graduate off first-run

Now that real data exists, the first-run scaffolding is dead weight — it loads every session but only applies to a blank clone. Offer to clear it all in one move (per CLAUDE.md First-Run Notes):

> *"Your memory's seeded with your real data now — want me to clear out the first-run setup scaffolding? (the sample seeds + the demo notes that only apply to a fresh clone)"*

- On **yes**, graduate in a single commit (`chore: graduate off first-run scaffolding`):
  1. `git rm memory/*.md.example` — the sample seeds
  2. Drop the first-run demo banner from `memory/MEMORY.md`
  3. Remove the whole **`## First-Run Notes`** section from `CLAUDE.md` — it's blank-clone-only
  4. Remove the **fresh-clone demo** paragraph from `.claude/skills/morning/SKILL.md` step 2
  - **Keep** the `/setup` skill itself + its Daily Ops row — it stays useful for gap-filling empty sections later.
- On **no**: leave everything — it's harmless, and the scaffolding stays. Don't re-ask this session.

### 7. Commit & push

- Stage the updated live memory files, commit, and push:
  ```
  setup: seed memory from first-run interview
  ```
- Push to `origin` so memory stays synced across machines.

## Notes

- **Offered, never forced.** A decline is final for the session — the learn-as-you-talk default takes over, no nagging.
- **Re-runnable.** On partially-filled memory, `/setup` only interviews the empty sections — useful well beyond literal first run, and harmless to re-run.
- **Skippable throughout.** Every question can be skipped; partial answers are fine. Never block on completeness.
- **Live files only.** Writes go to `memory/*.md`, never `*.md.example`. Sample content is never copied into live memory.
- **No fabrication.** Capture only what the user states; leave unanswered sections blank.
- Use the user's local timezone for any dates written (`config.yaml: timezone` overrides system TZ).

## Learned from runs

(empty — populated as the skill is used)

---
name: housekeep
description: Weekly hygiene pass over Iantha's memory, skills, git state, and (optional) vault. Flags stale tasks, drift in memory file timestamps, uncommitted changes, vault `_to-delete/` clutter, and skills with bloated "Learned from runs" sections. Use this whenever the user types /housekeep, mentions cleaning up / "things feel cluttered" / "let's tidy up", asks for a weekly check-in, or it's been a week since the last housekeep commit.
---

# /housekeep — Weekly Memory & Skill Audit

Slim weekly hygiene pass. Scoped to Iantha's own memory, skills, git, and (if configured) vault. Single-user — no agent inboxes, no cross-project coordination.

The scan parts (memory drift, learned-section overflow, stale tasks) are bundled in `scripts/audit.py` so each invocation runs the same recipe deterministically. The proposal-and-apply parts stay LLM-driven because they need user judgment.

## When to invoke

User typed `/housekeep`, OR another skill (e.g., a CLAUDE.md rule) explicitly delegates to it.

This skill does not auto-trigger from inside itself — Iantha can suggest it during /morning or /evening if it's been a week since the last housekeep commit, but the user always initiates.

## Steps

### 1. Run the audit script

```bash
python3 .claude/skills/housekeep/scripts/audit.py
```

The script auto-detects the repo root (walks up from itself looking for `memory/` + `.claude/`). Pass `--repo-root <path>` to override.

This produces a report covering:

- **Memory drift**: files under `memory/` whose `*Updated:*` header is older than 30 days (excluding `learnings.md` and `feedback.md`, which are intentionally low-churn). Files without an `*Updated:*` header are skipped — they're treated as never-touched templates.
- **Skills with bloated learned sections**: skills whose `## Learned from runs` section has more than 5 entries. Suggests `/consolidate-learning <skill>`.
- **Stale tasks**: uncompleted dated actions or routines in `memory/next-actions.md`, waiting-for follow-ups in `memory/waiting-for.md`, and dated unprocessed inputs in `memory/inbox.md` older than 30 days.

Surface the report to the user.

### 1b. First-run graduation check (LLM-driven)

If the live memory files now hold real content but first-run scaffolding is still present, offer to graduate it off — the scaffolding loads every session yet only applies to a blank clone.

- **Detect**: the live `memory/*.md` have real content (not just templates) **and** any of these still exist: `memory/*.md.example` seeds, a `## First-Run Notes` section in `CLAUDE.md`, or the first-run demo banner in `memory/MEMORY.md`.
- **If both**, offer once: *"You're well past first-run — want me to clear out the setup scaffolding? (sample seeds + the demo notes that only apply to a fresh clone)"*
- **On yes**, run the same graduation as `/setup` step 6: `git rm memory/*.md.example`, drop the MEMORY.md banner, remove the CLAUDE.md `## First-Run Notes` section + the `morning/SKILL.md` fresh-clone demo paragraph — one commit (`chore: graduate off first-run scaffolding`). Keep the `/setup` skill (re-runnable for gap-fill).
- Skip silently if memory is still blank (genuine fresh clone) or the scaffolding is already gone.

### 2. Git state (LLM-driven)

Run `git status` and `git log -5 --oneline`. If memory files have uncommitted changes, propose a commit. If the working tree has untracked files in `memory/` or `.claude/`, ask the user before committing them.

### 3. Vault hygiene (only if `vault_dir` configured)

- Call `/obsidian lint` and surface the findings.
- Review `${vault_dir}/_to-delete/`. Flag items older than 14 days for human deletion (the lint script also covers this — don't double-report).

### 4. Reading list (only if `vault_dir` configured)

Open `${vault_dir}/reading-list.md`. Flag items in "Action Required" older than 14 days — surface to the user, ask if any should be dropped or escalated.

### 5. Propose actions, apply with confirmation

For each finding from steps 1–4, propose what to do. The user approves per item. Apply only what they confirm. Commit per category:

```
housekeep: archive 3 stale tasks
housekeep: vault — sweep _to-delete (5 items)
```

Don't auto-archive. The user owns their tasks and vault.

## Example report (from audit.py)

```
## Housekeep audit — 2026-05-01

### Memory drift (>30d unchanged, excluding frozen files) (2)
  - personal.md: last updated 2026-03-25 (37d ago)
  - priorities.md: last updated 2026-03-30 (32d ago)

### Skills with bloated learned sections (>5 entries) (1)
  - obsidian: 7 entries

### Tasks with no movement in 30+ days (1)
  - next-actions.md: - [ ] [2026-03-12] Renew car registration (date in line: 2026-03-12)

Total findings: 4
```

## Out of scope

This skill is deliberately thin. Iantha is single-user and personal — no agent inboxes, GitHub issues, market checks, cost audits, or multi-project coordination. If you need any of that, look at Iris.

## Notes

- Default cadence: weekly. The skill is non-destructive — every change is proposed, not applied.
- Skip vault steps silently if `vault_dir` is unset.
- If everything is clean: "All clear. Last housekeep YYYY-MM-DD."

## Learned from runs

(empty — populated as the skill is used)

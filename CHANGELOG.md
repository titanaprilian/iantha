# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Dedicated GTD memory files: `inbox.md`, `projects.md`, `next-actions.md`, `waiting-for.md`, `someday-maybe.md`, and `reference.md`.
- `.claude/skills/clarify/SKILL.md` — interactive GTD inbox decision tree with the two-minute rule, reference, incubation, project/action linking, and waiting-for routing.
- `.claude/skills/weekly-review/SKILL.md` — 2-step weekly planning: (1) clarify inbox into tasks/projects and collect all project tasks, then (2) timebox the week into Google Calendar via `gws`.
- `.claude/skills/daily/SKILL.md` — daily focus check-in to pull today's timeboxed calendar schedule and prime workspace boundaries (renamed from `/morning`).
- `.claude/skills/daily-review/SKILL.md` — daily loop closure to confirm completed blocks, sweep loose thoughts to inbox, and preview tomorrow (renamed from `/evening`).

### Changed
- Fixed Google Calendar event insertion payloads to use the API's valid `end.dateTime` field.

- Renamed `/morning` to `/daily` and `/evening` to `/daily-review` to align with the timeboxed calendar workflow.
- Streamlined memory architecture to pure GTD: pruned redundant template files (`priorities.md`, `decisions.md`, `feedback.md`, `learnings.md`) into a single `reference.md` and personal context in `personal.md`.
- Pruned obsolete non-GTD skills: removed `/obsidian` (replaced by direct Google Calendar integration via `gws`), `/housekeep` (superseded by `/weekly-review`), `/consolidate-learning`, and `/debrief`.
- `AGENTS.md` / `CLAUDE.md` and `memory/MEMORY.md` updated to enforce clean GTD invariants without vault or static priority overhead.
## [0.1.1] - 2026-06-23

### Added

- `.claude/skills/setup/SKILL.md` — first-run onboarding interview (`/setup`). Offered (never forced) on a fresh clone with blank memory; asks ~5–8 skippable questions and writes the answers into the live memory files in canonical format, then runs `/morning` on the real data and offers to **graduate off the first-run scaffolding** (sample seeds + the demo notes that only apply to a blank clone). Re-runnable to gap-fill empty sections later.
- `AGENTS.md` (symlink → `CLAUDE.md`) and `.agents/skills/` (symlink → `.claude/skills/`) — **dual Claude Code + Codex support from one clone.** Both runtimes load the same persona/rules and run the same `SKILL.md` files; Claude Code reads `CLAUDE.md` / `.claude/skills/`, Codex reads `AGENTS.md` / `.agents/skills/`. No renames, no copies — `memory/` and `config.yaml` are shared as-is.

### Changed

- `CLAUDE.md` — Daily Ops table lists `/setup`; First-Run Notes wires the one-line `/setup` offer (decline keeps the learn-as-you-talk default, never re-offered). The "delete the samples" step is now a full graduation: removes the First-Run Notes section + the `morning` demo paragraph too, so first-run scaffolding stops loading every session once the user is established.
- `.claude/skills/morning/SKILL.md` — fresh-clone demo invites the user to run `/setup` to seed real data.
- `.claude/skills/housekeep/SKILL.md` — adds a first-run graduation check: offers to clear the scaffolding if memory is filled but it's still present.
- `memory/MEMORY.md` — first-run demo banner points to `/setup` as the path to fill memory.
- `README.md` — Setup section is now template-first (private repo via "Use this template", so memory is private + pushable across machines); `/setup` covered in quickstart + Daily Use table.
- `README.md` — "Using with Codex / other runtimes" section reframed around the shipped symlinks: Iantha runs on both runtimes from the same clone (a shared-files table + clone-and-go on Codex), instead of documenting a manual port. Privacy line broadened to cover any runtime/model provider.
- `.claude/skills/obsidian/scripts/init_vault.py` — the "this looks like an Iantha repo, not a vault" guard now also rejects a dir containing `AGENTS.md` (catches a Codex-ported repo, not just a Claude Code one).
- `.claude/skills/consolidate-learning/SKILL.md` — added its own `## Learned from runs` section. It manages that convention across all skills but was the only one missing it; now consistent and able to capture its own lessons.

## [0.1.0] - 2026-05-01

### Added

- `.claude/skills/obsidian/SKILL.md` — vault read/write primitives (modes: init, daily-log, briefing, weekly, reading-list, decision, archive, lint). No-op if `vault_dir` unset.
- `.claude/skills/obsidian/scripts/{init_vault,lint_vault,archive}.py` — helper scripts for the obsidian skill.
- `.claude/skills/housekeep/SKILL.md` — weekly memory and skill audit (single-agent).
- `.claude/skills/housekeep/scripts/audit.py` — helper script for the housekeep skill.
- `.claude/skills/consolidate-learning/SKILL.md` — audit "Learned from runs" sections and promote/merge/prune.
- `config.yaml` — optional vault config (`vault_dir` plus subdirs). All settings optional.
- `vault-template/VAULT.md` — starter handbook for the user's vault root (PARA-aligned).

### Changed

- `CLAUDE.md` — Daily Ops table now lists 6 in-repo skills; added Shared Skills section (`kiloloop/oacp-skills`) and Multi-runtime section (`kiloloop/cortex`); Rule G (reading list, opt-in); Rule D vault-aware.
- `README.md` — knowledge-base positioning and Karpathy reference; Knowledge Base mode section; Shared Skills; Multi-runtime; v0.2.0 roadmap; `config.local.yaml` note.
- `.claude/skills/morning/SKILL.md` — loads `config.yaml`; optional vault peek and briefing write.
- `.claude/skills/evening/SKILL.md` — loads `config.yaml`; optional vault daily-log via `/obsidian daily-log`.
- `.gitignore` — adds `config.local.yaml` for personal overrides.

## [0.0.1] - 2026-04-30

### Added

- `CLAUDE.md` — persona, behavioral rules, memory map, daily ops table.
- `README.md` — public-facing intro: setup, daily use, customize.
- `.gitignore` — minimal exclusions (`.DS_Store`, swap files, IDE artifacts).
- `.claude/skills/{morning,evening,debrief}/SKILL.md` — initial 3-skill slate.
- `memory/{MEMORY,tasks,personal,priorities,decisions,feedback,learnings}.md` — 7 memory templates.

### Removed

- Legacy cortex-dev bootstrap content (CHANGELOG, CODE_OF_CONDUCT, CONTRIBUTING, DEVELOPMENT, LICENSE, SECURITY, SSOT, configs, claude/codex skill scaffolds). LICENSE re-added in this `oss-scaffolding` branch.

[0.1.1]: https://github.com/kiloloop/iantha/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/kiloloop/iantha/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/kiloloop/iantha/releases/tag/v0.0.1

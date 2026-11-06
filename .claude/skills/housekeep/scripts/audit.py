#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kiloloop
# SPDX-License-Identifier: Apache-2.0
"""Iantha housekeep audit.

Scans memory/ and .claude/skills/ for drift signals:
- Memory files with *Updated:* older than --memory-stale-days
- Skills with "## Learned from runs" sections containing more than --learned-max entries
- Stale dated actions, routines, waiting-for follow-ups, and inbox inputs in the live GTD lists

Output is a human-readable report. Does NOT modify any files.

Usage (from iantha repo root):
    python .claude/skills/housekeep/scripts/audit.py
    python .claude/skills/housekeep/scripts/audit.py --memory-stale-days 30 --learned-max 5
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

UPDATED_RE = re.compile(r"^\*Updated:\s*(\d{4}-\d{2}-\d{2})(?:\s+\d{2}:\d{2})?\s*\*?", re.MULTILINE)
LEARNED_HEADER_RE = re.compile(r"^##\s*Learned from runs\s*$", re.IGNORECASE | re.MULTILINE)
LEARNED_ENTRY_RE = re.compile(r"^[-*]\s+\S", re.MULTILINE)
DATE_BRACKET_RE = re.compile(r"\[(\d{4}-\d{2}-\d{2})\]|Next due: (\d{4}-\d{2}-\d{2})")

# Files under memory/ that are intentionally low-churn — exclude from drift flagging.
FROZEN_MEMORY = {"learnings.md", "feedback.md"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Iantha repo root (default: auto-detect by walking up from this script)",
    )
    parser.add_argument("--memory-stale-days", type=int, default=30)
    parser.add_argument("--learned-max", type=int, default=5)
    parser.add_argument("--task-stale-days", type=int, default=30)
    args = parser.parse_args()

    if args.repo_root:
        root = Path(args.repo_root).expanduser().resolve()
    else:
        root = _autodetect_repo_root()
    memory = root / "memory"
    skills = root / ".claude" / "skills"

    if not memory.exists() or not skills.exists():
        print(f"ERROR: {root} doesn't look like an Iantha repo (no memory/ or .claude/skills/).", file=sys.stderr)
        return 1

    today = datetime.now().date()
    memory_drift = _scan_memory_drift(memory, today, args.memory_stale_days)
    learned_overflow = _scan_learned_sections(skills, args.learned_max)
    stale_tasks = _scan_stale_tasks(
        [memory / "next-actions.md", memory / "waiting-for.md", memory / "inbox.md"],
        today,
        args.task_stale_days,
    )

    print(f"## Housekeep audit — {today.isoformat()}")
    print()
    _section(
        f"Memory drift (>{args.memory_stale_days}d unchanged, excluding frozen files)",
        [f"{name}: last updated {date} ({age}d ago)" for name, date, age in memory_drift],
    )
    _section(
        f"Skills with bloated learned sections (>{args.learned_max} entries)",
        [f"{name}: {count} entries" for name, count in learned_overflow],
    )
    _section(
        f"Tasks with no movement in {args.task_stale_days}+ days",
        stale_tasks,
    )

    total = len(memory_drift) + len(learned_overflow) + len(stale_tasks)
    print(f"\nTotal findings: {total}")
    return 0


def _scan_memory_drift(
    memory: Path, today: datetime.date, threshold_days: int
) -> list[tuple[str, str, int]]:
    """Files without *Updated:* are treated as never-touched templates and skipped.
    Only files that *had* a header now older than the threshold count as drift."""
    drift: list[tuple[str, str, int]] = []
    for p in sorted(memory.glob("*.md")):
        if p.name in FROZEN_MEMORY:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        match = UPDATED_RE.search(text)
        if not match:
            continue
        try:
            d = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        except ValueError:
            continue
        age = (today - d).days
        if age > threshold_days:
            drift.append((p.name, match.group(1), age))
    return drift


def _scan_learned_sections(skills: Path, max_entries: int) -> list[tuple[str, int]]:
    overflow: list[tuple[str, int]] = []
    for skill_md in sorted(skills.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        match = LEARNED_HEADER_RE.search(text)
        if not match:
            continue
        section = text[match.end():]
        next_header = re.search(r"^##\s", section, re.MULTILINE)
        if next_header:
            section = section[: next_header.start()]
        entries = LEARNED_ENTRY_RE.findall(section)
        if len(entries) > max_entries:
            overflow.append((skill_md.parent.name, len(entries)))
    return overflow


def _scan_stale_tasks(
    task_files: list[Path], today: datetime.date, threshold_days: int
) -> list[str]:
    stale: list[str] = []
    cutoff = today - timedelta(days=threshold_days)
    for task_file in task_files:
        if not task_file.exists():
            continue
        for line in task_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped.startswith("- [") or stripped.startswith("- [x]"):
                continue
            m = DATE_BRACKET_RE.search(stripped)
            if not m:
                continue
            date = m.group(1) or m.group(2)
            try:
                d = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                continue
            if d < cutoff:
                stale.append(
                    f"{task_file.name}: {stripped[:80]}{'...' if len(stripped) > 80 else ''} "
                    f"(date in line: {date})"
                )
    return stale

def _autodetect_repo_root() -> Path:
    """Walk up from this script's location until we find memory/ + .claude/."""
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        if (parent / "memory").is_dir() and (parent / ".claude").is_dir():
            return parent
    return Path.cwd().resolve()


def _section(title: str, items: list) -> None:
    if not items:
        print(f"### {title}\n  (clean)\n")
        return
    print(f"### {title} ({len(items)})")
    for item in items:
        print(f"  - {item}")
    print()


if __name__ == "__main__":
    sys.exit(main())

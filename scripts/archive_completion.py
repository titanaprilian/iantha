#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Archive a confirmed GTD action completion into its monthly log.

One-off actions are removed from next-actions.md. Recurring routines remain active
and require an explicit --next-due date. Preview is the default; pass --apply to
write both files.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

ACTION_ID_RE = re.compile(r"\*\*([A-Z]\d+)\s*·")
NEXT_DUE_RE = re.compile(r"\s*\(Next due:\s*\d{4}-\d{2}-\d{2}\)\s*$")
UPDATED_RE = re.compile(r"^\*Updated:.*\*$", re.MULTILINE)


def local_timestamp(repo_root: Path) -> str:
    """Use configured timezone for memory timestamps; fallback to system local time."""
    timezone = ""
    config = repo_root / "config.yaml"
    if config.exists():
        match = re.search(r"^timezone:\s*[\"']?([^\"'#\s]+)", config.read_text(encoding="utf-8"), re.MULTILINE)
        if match:
            timezone = match.group(1)
    now = dt.datetime.now(ZoneInfo(timezone)) if timezone else dt.datetime.now().astimezone()
    return now.strftime("%Y-%m-%d %H:%M")


def update_timestamp(content: str, timestamp: str) -> str:
    header = f"*Updated: {timestamp}*"
    if UPDATED_RE.search(content):
        return UPDATED_RE.sub(header, content, count=1)
    lines = content.splitlines()
    insert_at = 1 if lines and lines[0].startswith("# ") else 0
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, header)
    return "\n".join(lines) + "\n"


def complete_action(
    next_actions_path: Path,
    archive_dir: Path,
    action_id: str,
    completed_on: dt.date,
    outcome: str,
    next_due: dt.date | None = None,
    apply: bool = False,
) -> str:
    """Preview or apply one action completion; return the proposed archive record."""
    content = next_actions_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    matches: list[tuple[int, str, str]] = []
    context = "@unknown"
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("## @deep-work"):
            context = "@deep-work"
        elif stripped.startswith("## @admin") or stripped.startswith("## @computer-light"):
            context = "@admin"
        elif stripped.startswith("## @offline"):
            context = "@offline"
        elif stripped.startswith("## @comms"):
            context = "@comms"
        if not stripped.startswith("- [ ]"):
            continue
        match = ACTION_ID_RE.search(stripped)
        if match and match.group(1) == action_id:
            matches.append((index, stripped, context))

    if len(matches) != 1:
        raise ValueError(f"Expected exactly one active action with ID {action_id}; found {len(matches)}.")

    index, line, context = matches[0]
    recurring = action_id.startswith("R") or "· Recurring**" in line
    if recurring and next_due is None:
        raise ValueError(f"{action_id} is recurring; provide --next-due YYYY-MM-DD.")
    if recurring and next_due <= completed_on:
        raise ValueError("--next-due must be after the confirmed completion date.")
    if not recurring and next_due is not None:
        raise ValueError(f"{action_id} is not recurring; --next-due is only valid for routines.")

    body = line.split("—", 1)[1].strip() if "—" in line else line
    body = NEXT_DUE_RE.sub("", body).strip()
    record = f"- [x] [{completed_on.isoformat()}] {action_id} · {context} — {body} — {outcome.strip()}"

    if apply:
        archive_dir.mkdir(parents=True, exist_ok=True)
    archive_path = archive_dir / f"{completed_on:%Y-%m}.md"
    if archive_path.exists():
        archive_content = archive_path.read_text(encoding="utf-8")
        duplicate = re.search(rf"^- \[x\] \[{completed_on.isoformat()}\] {re.escape(action_id)} ·", archive_content, re.MULTILINE)
        if duplicate:
            raise ValueError(f"{action_id} already has a completion record for {completed_on.isoformat()}.")
    else:
        archive_content = f"# Completed Actions — {completed_on:%Y-%m}\n\n## Entries\n"

    timestamp = local_timestamp(next_actions_path.parent.parent)
    if "## Entries" not in archive_content:
        archive_content = archive_content.rstrip() + "\n\n## Entries\n"
    archive_content = archive_content.rstrip() + "\n" + record + "\n"
    archive_content = update_timestamp(archive_content, timestamp)

    if recurring:
        replacement = re.sub(
            r"\(Next due:\s*\d{4}-\d{2}-\d{2}\)",
            f"(Next due: {next_due.isoformat()})",
            line,
        )
        if replacement == line:
            raise ValueError(f"{action_id} has no parseable Next due date to advance.")
        lines[index] = replacement
    else:
        del lines[index]
    updated_next_actions = update_timestamp("\n".join(lines) + "\n", timestamp)

    if apply:
        next_actions_path.write_text(updated_next_actions, encoding="utf-8")
        archive_path.write_text(archive_content, encoding="utf-8")
        return f"Archived {action_id} to {archive_path}; updated {next_actions_path}."

    disposition = f"keep routine; next due {next_due.isoformat()}" if recurring else "remove one-off from active list"
    return (
        f"DRY RUN — {action_id}: {disposition}\n"
        f"Archive: {archive_path}\n"
        f"{record}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, help="Stable action ID, e.g. A03 or R05")
    parser.add_argument("--date", required=True, help="Confirmed local completion date (YYYY-MM-DD)")
    parser.add_argument("--outcome", required=True, help="Short user-confirmed completion outcome")
    parser.add_argument("--next-due", help="Required for recurring routines; next scheduled date YYYY-MM-DD")
    parser.add_argument("--apply", action="store_true", help="Write the changes; without this flag only preview")
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root")
    args = parser.parse_args()

    try:
        completed_on = dt.date.fromisoformat(args.date)
        next_due = dt.date.fromisoformat(args.next_due) if args.next_due else None
        result = complete_action(
            args.repo_root / "memory" / "next-actions.md",
            args.repo_root / "memory" / "archive" / "completed",
            args.id,
            completed_on,
            args.outcome,
            next_due,
            args.apply,
        )
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

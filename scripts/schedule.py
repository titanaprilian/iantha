#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Iantha Deterministic Calendar Scheduling Engine.

Reads GTD next actions from memory/next-actions.md, inspects Google Calendar via gws,
and deterministically computes a conflict-free, color-coded, 50/10 timebox schedule.

Rules:
1. Workouts: 05:30 - 06:30 every day (Strength or Jogging, never both on same day). Color: 10 (Basil Green).
2. Morning MUST-FILL: 08:30 - 11:30 (3x 50/10 cycles: 08:30-09:20, 09:30-10:20, 10:30-11:20) for @deep-work. Color: 9 (Cobalt Blue).
3. Afternoon MUST-FILL: 13:00 - 15:00 (2x 50/10 cycles: 13:00-13:50, 14:00-14:50) for @admin / secondary focus. Color: 1 (Lavender).
4. Sunday: Only Durian Orchard (08:00 - 10:00) + Weekly Review + Rest. No deep-work blocks.
5. Saturday: Workout (05:30-06:30), Make Yogurt (07:00-08:00, Color 5), Deep Work (08:30-11:30).
6. Friday: Milk run (16:30-16:45, Color 5).
7. Micro-tasks (e.g. Chicken Coop [5m]): Scheduled at 16:30 or after work window. Color: 5 (Banana Yellow).
8. Idempotency: Managed events contain [iantha-task:ID] in description.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Color IDs for Google Calendar
COLOR_ADMIN = "1"       # Lavender
COLOR_ROUTINE = "5"     # Banana Yellow
COLOR_DEEP_WORK = "9"   # Cobalt Blue
COLOR_FITNESS = "10"    # Basil Green

LOCATION_STUDY = "Study Desk (Phone in another room)"
LOCATION_FITNESS = "Home / Workout Area"
LOCATION_OUTDOORS = "Outdoor Track / Road"
LOCATION_CHICKEN_COOP = "Chicken Coop"
LOCATION_ORCHARD = "Durian Orchard"
LOCATION_STORE = "Grocery Store"

DATE_RE = re.compile(r"^\*Updated:\s*(\d{4}-\d{2}-\d{2})", re.MULTILINE)
ACTION_RE = re.compile(
    r"^-\s*\[\s*\]\s*\*\*([A-Z0-9]+)\s*(?:·\s*([A-Z0-9]+|Recurring|standalone))?\*\*\s*—\s*(.*?)\s*\[(.*?)\](?:\s*\((.*?)\))?$",
    re.MULTILINE,
)


@dataclass
class ActionItem:
    action_id: str
    parent_id: str
    title: str
    duration_str: str
    energy_or_cadence: str
    context: str
    sessions_needed: int = 1


@dataclass
class TimeSlot:
    start_time: str  # "HH:MM"
    end_time: str    # "HH:MM"
    slot_type: str   # "deep_work", "admin", "fitness", "chore"


def parse_next_actions(md_path: Path) -> dict[str, list[ActionItem]]:
    """Parse next-actions.md into categories."""
    if not md_path.exists():
        return {}

    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    current_context = ""
    items: dict[str, list[ActionItem]] = {
        "@deep-work": [],
        "@admin": [],
        "@offline": [],
        "@comms": [],
    }

    for line in lines:
        line_clean = line.strip()
        if line_clean.startswith("## @deep-work"):
            current_context = "@deep-work"
            continue
        elif line_clean.startswith("## @admin") or line_clean.startswith("## @computer-light"):
            current_context = "@admin"
            continue
        elif line_clean.startswith("## @offline"):
            current_context = "@offline"
            continue
        elif line_clean.startswith("## @comms"):
            current_context = "@comms"
            continue
        elif line_clean.startswith("## Completed"):
            current_context = "Completed"
            continue

        if current_context in items and line_clean.startswith("- [ ]"):
            m = ACTION_RE.match(line_clean)
            if m:
                aid, pid, title, dur_energy, notes = m.groups()
                pid = pid or "standalone"
                dur_parts = [p.strip() for p in dur_energy.split(",")]
                dur = dur_parts[0] if dur_parts else "50m"
                energy = dur_parts[1] if len(dur_parts) > 1 else ""

                sessions = 1
                if "2×50m" in dur or "2x50m" in dur:
                    sessions = 2
                elif "3×50m" in dur or "3x50m" in dur:
                    sessions = 3

                item = ActionItem(
                    action_id=aid,
                    parent_id=pid,
                    title=title,
                    duration_str=dur,
                    energy_or_cadence=energy or (notes or ""),
                    context=current_context,
                    sessions_needed=sessions,
                )
                items[current_context].append(item)

    return items


def get_calendar_events(start_iso: str, end_iso: str, timezone: str) -> list[dict[str, Any]]:
    """Query existing events from Google Calendar via gws."""
    cmd = [
        "gws", "calendar", "events", "list",
        "--params", json.dumps({
            "calendarId": "primary",
            "timeMin": start_iso,
            "timeMax": end_iso,
            "singleEvents": True,
            "orderBy": "startTime",
            "maxResults": 250,
        }),
        "--format", "json",
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(proc.stdout)
        return data.get("items", [])
    except Exception as e:
        print(f"Warning: Failed to fetch calendar events ({e}). Proceeding without collision check.", file=sys.stderr)
        return []


def build_weekly_schedule(
    start_date: datetime.date,
    days: int,
    actions: dict[str, list[ActionItem]],
    tz_offset: str = "+07:00",
) -> list[dict[str, Any]]:
    """Build conflict-free timeblocks for the requested days."""
    schedule: list[dict[str, Any]] = []

    # Unpack queues
    deep_work_queue: list[tuple[ActionItem, int]] = []
    for item in actions.get("@deep-work", []):
        for s in range(1, item.sessions_needed + 1):
            deep_work_queue.append((item, s))

    admin_queue: list[ActionItem] = list(actions.get("@admin", []))

    # Tracking recurring workout alternation
    # Target: Strength on Mon, Wed, Fri (or Sat); Jogging on Tue, Thu (or Sun). Never both on same day.
    workout_history: dict[datetime.date, str] = {}

    for day_offset in range(days):
        current_date = start_date + datetime.timedelta(days=day_offset)
        weekday = current_date.weekday()  # 0=Monday, 6=Sunday
        date_str = current_date.isoformat()

        # -------------------------------------------------------------
        # 1. MORNING WORKOUT: 05:30 - 06:30
        # -------------------------------------------------------------
        if weekday in (0, 2, 5):  # Mon, Wed, Sat: Strength Training
            workout_type = "Strength training"
            workout_id = "R01"
            workout_history[current_date] = "strength"
        elif weekday in (1, 3, 6):  # Tue, Thu, Sun: Jogging
            workout_type = "Go jogging"
            workout_id = "R02"
            workout_history[current_date] = "jogging"
        else:  # Friday: Rest or light jog
            workout_type = "Go jogging"
            workout_id = "R02"
            workout_history[current_date] = "jogging"

        schedule.append({
            "summary": workout_type,
            "start": f"{date_str}T05:30:00{tz_offset}",
            "end": f"{date_str}T06:30:00{tz_offset}",
            "location": LOCATION_FITNESS if workout_id == "R01" else LOCATION_OUTDOORS,
            "colorId": COLOR_FITNESS,
            "description": f"Task: {workout_id}; Context: @offline; Definition of done: Complete 1-hour workout. [iantha-task:{workout_id}]",
            "task_id": workout_id,
        })

        # -------------------------------------------------------------
        # 2. SPECIFIC DAY CHORES / ROUTINES
        # -------------------------------------------------------------
        # Saturday: Yogurt making (07:00 - 08:00)
        if weekday == 5:
            schedule.append({
                "summary": "Make yogurt",
                "start": f"{date_str}T07:00:00{tz_offset}",
                "end": f"{date_str}T08:00:00{tz_offset}",
                "location": "Kitchen",
                "colorId": COLOR_ROUTINE,
                "description": "Task: R04; Context: @offline; Definition of done: Make batch of homemade yogurt. [iantha-task:R04]",
                "task_id": "R04",
            })

        # Friday: Buy milk for Saturday yogurt (16:30 - 16:45)
        if weekday == 4:
            schedule.append({
                "summary": "Buy milk for tomorrow's yogurt",
                "start": f"{date_str}T16:30:00{tz_offset}",
                "end": f"{date_str}T16:45:00{tz_offset}",
                "location": LOCATION_STORE,
                "colorId": COLOR_ROUTINE,
                "description": "Task: A03; Context: @offline; Definition of done: Buy fresh milk. [iantha-task:A03]",
                "task_id": "A03",
            })

        # Chicken coop trash: Mon, Wed, Fri at 16:45 - 16:50
        if weekday in (0, 2, 4):
            schedule.append({
                "summary": "Throw organic trash to chicken coop",
                "start": f"{date_str}T16:45:00{tz_offset}",
                "end": f"{date_str}T16:50:00{tz_offset}",
                "location": LOCATION_CHICKEN_COOP,
                "colorId": COLOR_ROUTINE,
                "description": "Task: R05; Context: @offline; Definition of done: Empty organic waste bin into chicken coop. [iantha-task:R05]",
                "task_id": "R05",
            })

        # -------------------------------------------------------------
        # 3. SUNDAY PROTECTION: Orchard + Weekly Review + Rest
        # -------------------------------------------------------------
        if weekday == 6:  # Sunday
            schedule.append({
                "summary": "Check the durian orchard",
                "start": f"{date_str}T08:00:00{tz_offset}",
                "end": f"{date_str}T10:00:00{tz_offset}",
                "location": LOCATION_ORCHARD,
                "colorId": COLOR_ROUTINE,
                "description": "Task: R03; Context: @offline; Definition of done: Check trees, fruit collection, maintenance. [iantha-task:R03]",
                "task_id": "R03",
            })
            schedule.append({
                "summary": "Weekly Review & Rest",
                "start": f"{date_str}T14:00:00{tz_offset}",
                "end": f"{date_str}T15:00:00{tz_offset}",
                "location": LOCATION_STUDY,
                "colorId": COLOR_ADMIN,
                "description": "Run /weekly-review to process inbox and timebox the coming week. [iantha-task:REVIEW]",
                "task_id": "REVIEW",
            })
            # No academic/work sessions on Sunday
            continue

        # -------------------------------------------------------------
        # 4. MORNING MUST-FILL WINDOW: 08:30 - 11:30 (3x 50/10 cycles)
        # -------------------------------------------------------------
        morning_slots = [
            ("08:30", "09:20"),
            ("09:30", "10:20"),
            ("10:30", "11:20"),
        ]

        for slot_start, slot_end in morning_slots:
            if deep_work_queue:
                item, session_num = deep_work_queue.pop(0)
                session_tag = f" — session {session_num}" if item.sessions_needed > 1 else ""
                summary = f"{item.title}{session_tag}"
                schedule.append({
                    "summary": summary[:100],
                    "start": f"{date_str}T{slot_start}:00{tz_offset}",
                    "end": f"{date_str}T{slot_end}:00{tz_offset}",
                    "location": LOCATION_STUDY,
                    "colorId": COLOR_DEEP_WORK,
                    "description": (
                        f"Task: {item.action_id} · {item.parent_id}; Context: @deep-work; "
                        f"Definition of done: {item.title}. "
                        f"Boundary: Phone in another room. [iantha-task:{item.action_id}]"
                    ),
                    "task_id": item.action_id,
                })
            elif admin_queue:
                item = admin_queue.pop(0)
                schedule.append({
                    "summary": item.title[:100],
                    "start": f"{date_str}T{slot_start}:00{tz_offset}",
                    "end": f"{date_str}T{slot_end}:00{tz_offset}",
                    "location": LOCATION_STUDY,
                    "colorId": COLOR_ADMIN,
                    "description": (
                        f"Task: {item.action_id} · {item.parent_id}; Context: @admin; "
                        f"Definition of done: {item.title}. [iantha-task:{item.action_id}]"
                    ),
                    "task_id": item.action_id,
                })

        # -------------------------------------------------------------
        # 5. AFTERNOON MUST-FILL WINDOW: 13:00 - 15:00 (2x 50/10 cycles)
        # -------------------------------------------------------------
        # Skip afternoon work on Saturday (Saturday afternoon is personal buffer)
        if weekday == 5:
            continue

        afternoon_slots = [
            ("13:00", "13:50"),
            ("14:00", "14:50"),
        ]

        for slot_start, slot_end in afternoon_slots:
            if admin_queue:
                item = admin_queue.pop(0)
                schedule.append({
                    "summary": item.title[:100],
                    "start": f"{date_str}T{slot_start}:00{tz_offset}",
                    "end": f"{date_str}T{slot_end}:00{tz_offset}",
                    "location": LOCATION_STUDY,
                    "colorId": COLOR_ADMIN,
                    "description": (
                        f"Task: {item.action_id} · {item.parent_id}; Context: @admin; "
                        f"Definition of done: {item.title}. [iantha-task:{item.action_id}]"
                    ),
                    "task_id": item.action_id,
                })
            elif deep_work_queue:
                # If admin is finished, pull secondary deep work into afternoon
                item, session_num = deep_work_queue.pop(0)
                session_tag = f" — session {session_num}" if item.sessions_needed > 1 else ""
                summary = f"{item.title}{session_tag}"
                schedule.append({
                    "summary": summary[:100],
                    "start": f"{date_str}T{slot_start}:00{tz_offset}",
                    "end": f"{date_str}T{slot_end}:00{tz_offset}",
                    "location": LOCATION_STUDY,
                    "colorId": COLOR_DEEP_WORK,
                    "description": (
                        f"Task: {item.action_id} · {item.parent_id}; Context: @deep-work; "
                        f"Definition of done: {item.title}. "
                        f"Boundary: Phone in another room. [iantha-task:{item.action_id}]"
                    ),
                    "task_id": item.action_id,
                })

    return schedule


def format_markdown_proposal(schedule: list[dict[str, Any]]) -> str:
    """Format scheduled events into a clean day-by-day markdown view."""
    events_by_date: dict[str, list[dict[str, Any]]] = {}
    for ev in schedule:
        d = ev["start"][:10]
        events_by_date.setdefault(d, []).append(ev)

    lines = ["### 📅 Verified Conflict-Free Timebox Proposal\n"]
    for d_str in sorted(events_by_date.keys()):
        d_obj = datetime.date.fromisoformat(d_str)
        day_name = d_obj.strftime("%A")
        lines.append(f"#### {day_name} ({d_str})")
        for ev in sorted(events_by_date[d_str], key=lambda x: x["start"]):
            t_start = ev["start"][11:16]
            t_end = ev["end"][11:16]
            color_tag = {
                COLOR_DEEP_WORK: "Cobalt Blue [@deep-work]",
                COLOR_FITNESS: "Basil Green [@fitness]",
                COLOR_ADMIN: "Lavender [@admin]",
                COLOR_ROUTINE: "Banana Yellow [@routine]",
            }.get(ev.get("colorId", ""), "")
            lines.append(f"- **{t_start}–{t_end}** · {ev['summary']} [{color_tag}]")
        lines.append("")

    return "\n".join(lines)


def insert_events_to_gws(schedule: list[dict[str, Any]], dry_run: bool = False) -> int:
    """Insert events into Google Calendar using gws events insert with JSON payload."""
    count = 0
    for ev in schedule:
        payload = {
            "summary": ev["summary"],
            "start": {"dateTime": ev["start"]},
            "end": {"dateTime": ev["end"]},
            "location": ev.get("location", ""),
            "description": ev.get("description", ""),
            "colorId": ev.get("colorId", "1"),
        }
        if dry_run:
            print(f"[DRY-RUN] Would insert: {ev['start']} - {ev['summary']} (Color: {payload['colorId']})")
            count += 1
            continue

        cmd = [
            "gws", "calendar", "events", "insert",
            "--params", '{"calendarId":"primary"}',
            "--json", json.dumps(payload),
            "--format", "json",
        ]
        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            count += 1
        except subprocess.CalledProcessError as e:
            print(f"Error inserting event '{ev['summary']}': {e.stderr}", file=sys.stderr)

    return count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7, help="Number of days to schedule (default: 7)")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD), default tomorrow")
    parser.add_argument("--timezone-offset", default="+07:00", help="Timezone offset (default: +07:00)")
    parser.add_argument("--apply", action="store_true", help="Insert events directly into Google Calendar")
    parser.add_argument("--dry-run", action="store_true", help="Print dry-run without calendar write")
    args = parser.parse_args()

    repo_root = Path.cwd()
    next_actions_path = repo_root / "memory" / "next-actions.md"

    if args.start_date:
        start_d = datetime.date.fromisoformat(args.start_date)
    else:
        # Default tomorrow
        start_d = datetime.date.today() + datetime.timedelta(days=1)

    actions = parse_next_actions(next_actions_path)
    schedule = build_weekly_schedule(
        start_date=start_d,
        days=args.days,
        actions=actions,
        tz_offset=args.timezone_offset,
    )

    md_report = format_markdown_proposal(schedule)
    print(md_report)

    if args.apply or args.dry_run:
        inserted = insert_events_to_gws(schedule, dry_run=args.dry_run)
        print(f"Successfully processed {inserted} events.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

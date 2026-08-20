#!/usr/bin/env python3
"""Store minimal Brain Starter session events as private JSON Lines."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


ALLOWED_FIELDS = {
    "startedAt",
    "inputMode",
    "taskClarity",
    "taskType",
    "resistance",
    "aiLevel",
    "connectorsUsed",
    "firstAction",
    "startedWithinThreeMinutes",
    "completedTenMinuteBlock",
    "continuedAfterBlock",
    "resistanceBefore",
    "resistanceAfter",
}
REQUIRED_FIELDS = ALLOWED_FIELDS
ENUMS = {
    "inputMode": {"voice", "text"},
    "taskClarity": {"clear", "unclear"},
    "taskType": {"work", "study", "administrative", "creative", "personal", "recovery"},
    "resistance": {
        "no_next_step",
        "task_too_large",
        "perfection_or_fear",
        "low_energy",
        "competing_pull",
        "blocked_dependency",
    },
}
BOOL_FIELDS = {
    "startedWithinThreeMinutes",
    "completedTenMinuteBlock",
    "continuedAfterBlock",
}
CONNECTORS = {"gmail", "google_calendar"}
FACILITIES = {
    "work": "workbench",
    "study": "reading_room",
    "administrative": "control_desk",
    "creative": "creation_pod",
    "personal": "life_dock",
    "recovery": "recharge_bay",
}


def _default_path() -> Path:
    base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
    return base / "brain-starter" / "sessions.jsonl"


def validate_event(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("event must be a JSON object")
    unknown = set(raw) - ALLOWED_FIELDS
    missing = REQUIRED_FIELDS - set(raw)
    if unknown:
        raise ValueError(f"unknown fields: {sorted(unknown)}")
    if missing:
        raise ValueError(f"missing fields: {sorted(missing)}")

    event = dict(raw)
    try:
        datetime.fromisoformat(event["startedAt"])
    except (TypeError, ValueError):
        raise ValueError("startedAt must be an ISO-8601 timestamp") from None

    for field, values in ENUMS.items():
        if event[field] not in values:
            raise ValueError(f"invalid {field}")
    if type(event["aiLevel"]) is not int or not 1 <= event["aiLevel"] <= 5:
        raise ValueError("aiLevel must be an integer from 1 to 5")
    for field in BOOL_FIELDS:
        if type(event[field]) is not bool:
            raise ValueError(f"{field} must be boolean")
    for field in ("resistanceBefore", "resistanceAfter"):
        if type(event[field]) is not int or not 1 <= event[field] <= 5:
            raise ValueError(f"{field} must be an integer from 1 to 5")
    connectors = event["connectorsUsed"]
    if not isinstance(connectors, list) or any(value not in CONNECTORS for value in connectors):
        raise ValueError("connectorsUsed contains an unsupported connector")
    if not isinstance(event["firstAction"], str) or not event["firstAction"].strip():
        raise ValueError("firstAction must be a non-empty category string")

    event["connectorsUsed"] = sorted(set(connectors))
    event["firstAction"] = event["firstAction"].strip()[:80]
    event["facility"] = FACILITIES[event["taskType"]]
    event["momentumEarned"] = (
        (2 if event["startedWithinThreeMinutes"] else 0)
        + (2 if event["completedTenMinuteBlock"] else 0)
        + (1 if event["continuedAfterBlock"] else 0)
    )
    return event


def summarize(path: Path | None = None) -> dict[str, Any]:
    target = path or _default_path()
    summary: dict[str, Any] = {"totalMomentum": 0, "starts": 0, "facilities": {}}
    if not target.exists():
        return summary
    for line in target.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        points = int(event.get("momentumEarned", 0))
        facility = event.get("facility")
        summary["totalMomentum"] += points
        summary["starts"] += int(bool(event.get("startedWithinThreeMinutes")))
        if facility:
            summary["facilities"][facility] = summary["facilities"].get(facility, 0) + points
    summary["facilities"] = dict(sorted(summary["facilities"].items()))
    return summary


def append_event(raw: dict[str, Any], path: Path | None = None) -> Path:
    event = validate_event(raw)
    target = path or _default_path()
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor = os.open(target, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
    try:
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "a", encoding="utf-8") as stream:
            stream.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        os.close(descriptor)
        raise
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["record", "status"])
    parser.add_argument("--event-json")
    parser.add_argument("--path", type=Path)
    args = parser.parse_args()
    if args.command == "record":
        if not args.event_json:
            parser.error("record requires --event-json")
        target = append_event(json.loads(args.event_json), args.path)
        print(target)
    else:
        print(json.dumps(summarize(args.path), ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

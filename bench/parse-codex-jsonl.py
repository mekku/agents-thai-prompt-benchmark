#!/usr/bin/env python3
"""Parse Codex JSONL output into a one-row CSV metric summary."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

USAGE_KEYS = [
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
]


def get_nested(obj: dict[str, Any], path: list[str]) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: parse-codex-jsonl.py <codex-output.jsonl>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    usage_total = {key: 0 for key in USAGE_KEYS}
    events = 0
    commands = 0
    file_changes = 0
    errors = 0
    turn_completed = 0

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            events += 1
            event_type = str(obj.get("type", ""))

            if event_type == "turn.completed":
                turn_completed += 1
                usage = obj.get("usage") or {}
                for key in USAGE_KEYS:
                    usage_total[key] += int(usage.get(key, 0) or 0)

            if event_type.startswith("error") or obj.get("error"):
                errors += 1

            # Codex JSONL shapes may evolve. Keep these counters best-effort.
            item_type = get_nested(obj, ["item", "type"])
            if item_type == "command_execution":
                commands += 1
            if item_type == "file_change":
                file_changes += 1

            if event_type in {"exec.command_begin", "exec.command_end"}:
                commands += 1
            if event_type in {"file_change", "patch_apply_begin", "patch_apply_end"}:
                file_changes += 1

    total_tokens = (
        usage_total["input_tokens"]
        + usage_total["output_tokens"]
        + usage_total["reasoning_output_tokens"]
    )

    row = {
        "file": path.name,
        "events": events,
        "turn_completed": turn_completed,
        "input_tokens": usage_total["input_tokens"],
        "cached_input_tokens": usage_total["cached_input_tokens"],
        "output_tokens": usage_total["output_tokens"],
        "reasoning_output_tokens": usage_total["reasoning_output_tokens"],
        "total_tokens": total_tokens,
        "commands": commands,
        "file_changes": file_changes,
        "errors": errors,
    }

    writer = csv.DictWriter(sys.stdout, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

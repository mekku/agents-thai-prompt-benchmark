#!/usr/bin/env python3
"""Parse Claude Code stream-json output into a one-row CSV metric summary.

Token normalization to match Codex schema:
  input_tokens        = fresh + cache_creation + cache_read  (total input to model)
  cached_input_tokens = cache_read_input_tokens only
  output_tokens       = output_tokens
  total_tokens        = input_tokens + output_tokens
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: parse-claude-jsonl.py <claude-output.jsonl>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"file not found: {path}", file=sys.stderr)
        return 2

    input_fresh = 0
    cache_read = 0
    cache_creation = 0
    output_tokens = 0
    total_cost_usd = 0.0
    events = 0
    errors = 0
    num_turns = 0
    bash_uses = 0
    file_changes = 0

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
            t = obj.get("type", "")

            if t == "result":
                usage = obj.get("usage") or {}
                input_fresh = int(usage.get("input_tokens", 0) or 0)
                cache_read = int(usage.get("cache_read_input_tokens", 0) or 0)
                cache_creation = int(usage.get("cache_creation_input_tokens", 0) or 0)
                output_tokens = int(usage.get("output_tokens", 0) or 0)
                total_cost_usd = float(obj.get("total_cost_usd", 0) or 0)
                num_turns = int(obj.get("num_turns", 0) or 0)
                if obj.get("is_error"):
                    errors += 1

            elif t.startswith("error"):
                errors += 1

            if t == "assistant":
                content = (obj.get("message") or {}).get("content") or []
                for item in content:
                    if not isinstance(item, dict):
                        continue
                    if item.get("type") == "tool_use":
                        name = item.get("name", "")
                        if name in ("Edit", "Write", "NotebookEdit"):
                            file_changes += 1
                        else:
                            bash_uses += 1

    input_tokens_total = input_fresh + cache_read + cache_creation
    total_tokens = input_tokens_total + output_tokens

    row = {
        "file": path.name,
        "tool": "claude-code",
        "events": events,
        "num_turns": num_turns,
        "input_tokens": input_tokens_total,
        "cached_input_tokens": cache_read,
        "output_tokens": output_tokens,
        "reasoning_output_tokens": 0,
        "total_tokens": total_tokens,
        "commands": bash_uses,
        "file_changes": file_changes,
        "errors": errors,
        "total_cost_usd": f"{total_cost_usd:.6f}",
    }

    writer = csv.DictWriter(sys.stdout, fieldnames=list(row.keys()))
    writer.writeheader()
    writer.writerow(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

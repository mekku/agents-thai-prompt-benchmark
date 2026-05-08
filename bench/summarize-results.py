#!/usr/bin/env python3
"""Summarize benchmark CSV files in bench/results."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

METRICS = [
    "input_tokens",
    "cached_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
    "total_tokens",
    "commands",
    "file_changes",
    "errors",
]

VARIANT_KEYS = ["a-thai", "b-english", "c-policy", "d-compact"]
VARIANT_LABELS = {
    "a-thai": "A Thai direct",
    "b-english": "B English direct",
    "c-policy": "C Thai + verbose policy",
    "d-compact": "D Thai + compact policy",
}


def parse_filename(name: str) -> tuple[str, str]:
    """Return (repo_label, variant_key) from a result filename."""
    # Strip timestamp prefix (YYYYMMDD-HHMMSS-)
    base = name
    for prefix in ("claude-",):
        base = base.replace(prefix, "", 1)

    # Try to extract a repo label: if name contains a known variant preceded
    # by something, that something is the label.
    # Pattern: [TS-][claude-][label-]<variant>-r<n>.csv
    for vk in VARIANT_KEYS:
        if vk in base:
            idx = base.index(vk)
            label_part = base[:idx].rstrip("-")
            # Remove timestamp (first token before first real label)
            parts = label_part.split("-")
            # Timestamp is YYYYMMDD and HHMMSS — skip first two parts
            non_ts = [p for p in parts if not (len(p) == 8 and p.isdigit()) and not (len(p) == 6 and p.isdigit())]
            label = "-".join(non_ts).strip("-") or "benchmark-repo"
            return label, vk
    return "benchmark-repo", "other"


def tool_from_row(row: dict[str, str], filename: str) -> str:
    tool = row.get("tool", "")
    if tool == "claude-code" or "claude-" in filename:
        return "Claude Code"
    return "Codex"


def read_rows(results_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for p in sorted(results_dir.glob("*.csv")):
        with p.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["source_csv"] = p.name
                repo_label, variant_key = parse_filename(p.name)
                row["_repo"] = repo_label
                row["_variant"] = variant_key
                rows.append(row)
    return rows


def to_float(row: dict[str, str], key: str) -> float:
    try:
        return float(row.get(key, "0") or "0")
    except ValueError:
        return 0.0


def print_tool_table(tool: str, label: str, rows: list[dict[str, str]]) -> None:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        vk = row.get("_variant", "other")
        groups[vk].append(row)

    print(f"### {tool} — {label}")
    print()
    print("| Variant | Runs | " + " | ".join(METRICS) + " |")
    print("|---|---:|" + "|".join(["---:"] * len(METRICS)) + "|")

    for vk in VARIANT_KEYS:
        rs = groups.get(vk, [])
        if not rs:
            continue
        label_str = VARIANT_LABELS.get(vk, vk)
        values = [f"{mean(to_float(r, m) for r in rs):,.1f}" for m in METRICS]
        print(f"| {label_str} | {len(rs)} | " + " | ".join(values) + " |")
    print()


def print_comparison(
    codex_rows: list[dict[str, str]],
    claude_rows: list[dict[str, str]],
    label: str,
) -> None:
    def avg_total(rows: list[dict[str, str]], vk: str) -> float | None:
        matched = [r for r in rows if r.get("_variant") == vk]
        if not matched:
            return None
        return mean(to_float(r, "total_tokens") for r in matched)

    print(f"### Total token comparison — {label}")
    print()
    print("| Variant | Codex | Claude Code | Delta |")
    print("|---|---:|---:|---:|")
    for vk in VARIANT_KEYS:
        c = avg_total(codex_rows, vk)
        cl = avg_total(claude_rows, vk)
        if c is None or cl is None:
            continue
        delta = (cl - c) / c * 100
        sign = "+" if delta >= 0 else ""
        label_str = VARIANT_LABELS.get(vk, vk)
        print(f"| {label_str} | {c:,.0f} | {cl:,.0f} | {sign}{delta:.1f}% |")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="bench/results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    rows = read_rows(results_dir)

    if not rows:
        print(f"No CSV files found in {results_dir}")
        return 1

    # Group by repo label
    repos: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        repos[row["_repo"]].append(row)

    for repo_label, repo_rows in sorted(repos.items()):
        codex_rows = [r for r in repo_rows if tool_from_row(r, r.get("source_csv", "")) == "Codex"]
        claude_rows = [r for r in repo_rows if tool_from_row(r, r.get("source_csv", "")) == "Claude Code"]

        if codex_rows:
            print_tool_table("Codex (gpt-5.5)", repo_label, codex_rows)
        if claude_rows:
            print_tool_table("Claude Code (claude-sonnet-4-6)", repo_label, claude_rows)
        if codex_rows and claude_rows:
            print_comparison(codex_rows, claude_rows, repo_label)

    print("## Raw files")
    for row in rows:
        print(f"- `{row.get('source_csv')}`")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

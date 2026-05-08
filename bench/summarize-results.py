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


def variant_from_filename(name: str) -> str:
    if "a-thai" in name:
        return "A Thai direct"
    if "b-english" in name:
        return "B English direct"
    if "c-policy" in name:
        return "C Thai + English policy"
    return "Other"


def read_rows(results_dir: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for p in sorted(results_dir.glob("*.csv")):
        with p.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["source_csv"] = p.name
                rows.append(row)
    return rows


def to_int(row: dict[str, str], key: str) -> int:
    try:
        return int(float(row.get(key, "0") or "0"))
    except ValueError:
        return 0


def print_markdown_summary(rows: list[dict[str, str]]) -> None:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[variant_from_filename(row.get("file", row.get("source_csv", "")))].append(row)

    print("| Variant | Runs | " + " | ".join(METRICS) + " |")
    print("|---|---:|" + "|".join(["---:"] * len(METRICS)) + "|")

    for variant in ["A Thai direct", "B English direct", "C Thai + English policy", "Other"]:
        rs = groups.get(variant, [])
        if not rs:
            continue
        values = []
        for metric in METRICS:
            values.append(f"{mean(to_int(r, metric) for r in rs):.1f}")
        print(f"| {variant} | {len(rs)} | " + " | ".join(values) + " |")

    print()
    print("## Raw files")
    for row in rows:
        print(f"- `{row.get('source_csv')}`")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="bench/results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    rows = read_rows(results_dir)

    if not rows:
        print(f"No CSV files found in {results_dir}")
        return 1

    print_markdown_summary(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

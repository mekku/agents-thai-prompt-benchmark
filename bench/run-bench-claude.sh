#!/usr/bin/env bash
set -euo pipefail

RUNS="${1:-3}"
WORKDIR="${2:-$(pwd)}"
LABEL="${3:-}"

if ! [[ "$RUNS" =~ ^[0-9]+$ ]] || [[ "$RUNS" -lt 1 ]]; then
  echo "error: RUNS must be a positive integer" >&2
  exit 2
fi

PREFIX="${LABEL:+${LABEL}-}"

mkdir -p bench/results

for i in $(seq 1 "$RUNS"); do
  echo "=== Run $i / $RUNS : ${PREFIX}A Thai (Claude Code) ==="
  ./bench/run-one-claude.sh "${PREFIX}a-thai-r${i}" "bench/prompts/a-thai.md" "$WORKDIR"

  echo "=== Run $i / $RUNS : ${PREFIX}B English (Claude Code) ==="
  ./bench/run-one-claude.sh "${PREFIX}b-english-r${i}" "bench/prompts/b-english.md" "$WORKDIR"

  echo "=== Run $i / $RUNS : ${PREFIX}C Universal Policy (Claude Code) ==="
  ./bench/run-one-claude.sh "${PREFIX}c-policy-r${i}" "bench/prompts/c-universal-policy.md" "$WORKDIR"

  echo "=== Run $i / $RUNS : ${PREFIX}D Compact Policy (Claude Code) ==="
  ./bench/run-one-claude.sh "${PREFIX}d-compact-r${i}" "bench/prompts/d-compact-policy.md" "$WORKDIR"
done

echo
echo "Done. Summarize with:"
echo "  ./bench/summarize-results.py"

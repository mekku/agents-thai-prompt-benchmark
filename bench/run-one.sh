#!/usr/bin/env bash
set -euo pipefail

VARIANT="${1:?usage: ./bench/run-one.sh <variant-name> <prompt-file>}"
PROMPT_FILE="${2:?usage: ./bench/run-one.sh <variant-name> <prompt-file>}"

if ! command -v codex >/dev/null 2>&1; then
  echo "error: codex CLI not found in PATH" >&2
  exit 127
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "error: prompt file not found: $PROMPT_FILE" >&2
  exit 2
fi

mkdir -p bench/results

TS="$(date +%Y%m%d-%H%M%S)"
OUT="bench/results/${TS}-${VARIANT}.jsonl"
FINAL="bench/results/${TS}-${VARIANT}.final.md"
CSV="bench/results/${TS}-${VARIANT}.csv"

# Default benchmark is read-only to reduce noise.
# Use --ignore-user-config and --ignore-rules to isolate this benchmark from local agent policies.
# Remove those flags if you intentionally want to benchmark your real project-level rules.
codex exec \
  --json \
  --ephemeral \
  --sandbox read-only \
  --ask-for-approval never \
  --ignore-user-config \
  --ignore-rules \
  -o "$FINAL" \
  "$(cat "$PROMPT_FILE")" \
  > "$OUT"

python3 bench/parse-codex-jsonl.py "$OUT" > "$CSV"

cat "$CSV"
echo
echo "JSONL:  $OUT"
echo "Final:  $FINAL"
echo "Metric: $CSV"

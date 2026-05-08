#!/usr/bin/env bash
set -euo pipefail

VARIANT="${1:?usage: ./bench/run-one.sh <variant-name> <prompt-file> [workdir]}"
PROMPT_FILE="${2:?usage: ./bench/run-one.sh <variant-name> <prompt-file> [workdir]}"
WORKDIR="${3:-$(pwd)}"

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

# --ignore-user-config and --ignore-rules isolate this run from local agent policies.
codex exec \
  --json \
  --ephemeral \
  --sandbox read-only \
  --ignore-user-config \
  --ignore-rules \
  -C "$WORKDIR" \
  -o "$FINAL" \
  "$(cat "$PROMPT_FILE")" \
  > "$OUT"

python3 bench/parse-codex-jsonl.py "$OUT" > "$CSV"

cat "$CSV"
echo
echo "JSONL:  $OUT"
echo "Final:  $FINAL"
echo "Metric: $CSV"

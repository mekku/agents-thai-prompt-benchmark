#!/usr/bin/env bash
set -euo pipefail

VARIANT="${1:?usage: ./bench/run-one-claude.sh <variant-name> <prompt-file> [workdir]}"
PROMPT_FILE="${2:?usage: ./bench/run-one-claude.sh <variant-name> <prompt-file> [workdir]}"
WORKDIR="${3:-$(pwd)}"

if ! command -v claude >/dev/null 2>&1; then
  echo "error: claude CLI not found in PATH" >&2
  exit 127
fi

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "error: prompt file not found: $PROMPT_FILE" >&2
  exit 2
fi

# Resolve to absolute so the path survives the subshell cd.
PROMPT_FILE="$(cd "$(dirname "$PROMPT_FILE")" && pwd)/$(basename "$PROMPT_FILE")"

mkdir -p bench/results

TS="$(date +%Y%m%d-%H%M%S)"
OUT="bench/results/${TS}-claude-${VARIANT}.jsonl"
FINAL="bench/results/${TS}-claude-${VARIANT}.final.md"
CSV="bench/results/${TS}-claude-${VARIANT}.csv"
STDERR="${OUT%.jsonl}.stderr"

# Subshell cd so claude inherits the target workdir.
# --no-session-persistence: ephemeral, no disk writes.
# --dangerously-skip-permissions: non-interactive, no approval prompts.
(cd "$WORKDIR" && claude \
  --print \
  --output-format stream-json \
  --verbose \
  --no-session-persistence \
  --dangerously-skip-permissions \
  "$(cat "$PROMPT_FILE")") \
  > "$OUT" 2> "$STDERR"

python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    for line in f:
        line = line.strip()
        if not line: continue
        try:
            obj = json.loads(line)
            if obj.get('type') == 'result':
                print(obj.get('result', ''))
        except Exception:
            pass
" "$OUT" > "$FINAL"

python3 bench/parse-claude-jsonl.py "$OUT" > "$CSV"

cat "$CSV"
echo
echo "JSONL:  $OUT"
echo "Final:  $FINAL"
echo "Metric: $CSV"

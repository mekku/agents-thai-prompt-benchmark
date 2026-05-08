#!/usr/bin/env bash
set -euo pipefail

RUNS="${1:-3}"

if ! [[ "$RUNS" =~ ^[0-9]+$ ]] || [[ "$RUNS" -lt 1 ]]; then
  echo "error: RUNS must be a positive integer" >&2
  exit 2
fi

mkdir -p bench/results

for i in $(seq 1 "$RUNS"); do
  echo "=== Run $i / $RUNS : A Thai ==="
  ./bench/run-one.sh "a-thai-r${i}" "bench/prompts/a-thai.md"

  echo "=== Run $i / $RUNS : B English ==="
  ./bench/run-one.sh "b-english-r${i}" "bench/prompts/b-english.md"

  echo "=== Run $i / $RUNS : C Universal Policy ==="
  ./bench/run-one.sh "c-policy-r${i}" "bench/prompts/c-universal-policy.md"
done

echo
echo "Done. Summarize with:"
echo "  ./bench/summarize-results.py"

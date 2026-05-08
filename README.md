# Agents Thai Prompt Benchmark

A small shell benchmark for testing whether multilingual prompts, English prompts, or multilingual prompts with an English working-language policy produce different Codex usage/cost behavior.

The core question is not only:

> Does Thai use more tokens than English?

The better question is:

> Does a language policy reduce total tokens per completed coding-agent task without hurting output quality?

This repo gives you a repeatable way to compare three variants:

| Variant | Meaning |
|---|---|
| A | Thai prompt directly |
| B | English prompt directly, final answer in Thai |
| C | Thai prompt plus a universal multilingual policy: work in concise English, reply in Thai |

## Requirements

- macOS/Linux shell
- `python3`
- OpenAI Codex CLI installed and authenticated

Check Codex CLI works:

```bash
codex --version
codex exec --help
```

This benchmark uses:

```bash
codex exec --json --ephemeral
```

`--json` streams JSONL events, and this repo parses `turn.completed.usage` to collect token metrics.

## Quick start

```bash
git clone https://github.com/mekku/agents-thai-prompt-benchmark.git
cd agents-thai-prompt-benchmark
chmod +x bench/*.sh bench/*.py
./bench/run-bench.sh 5
```

Then summarize:

```bash
./bench/summarize-results.py
```

Or use Make:

```bash
make bench RUNS=5
make summary
```

## What it measures

For each run, the parser records:

- `input_tokens`
- `cached_input_tokens`
- `output_tokens`
- `reasoning_output_tokens`
- `total_tokens`
- event count
- command execution count, if present in the Codex JSONL stream
- file change count, if present in the Codex JSONL stream
- errors, if present

The output files are stored in:

```text
bench/results/
```

Each run produces:

```text
*.jsonl     Raw Codex event stream
*.final.md  Final Codex answer
*.csv       Parsed metrics
```

## Default benchmark task

The default task is read-only repo analysis. This is intentional.

Read-only analysis is a cleaner first benchmark because no code edits, tests, or git diffs create extra noise. Once you see whether the language policy changes token behavior, you can add edit tasks later.

Default variants:

```text
bench/prompts/a-thai.md
bench/prompts/b-english.md
bench/prompts/c-universal-policy.md
```

## Recommended interpretation

Do not judge by input tokens alone.

The useful metric is:

```text
total token cost per acceptable completed task
```

A policy is worth using only if:

- total tokens are lower than Thai-direct runs by a meaningful margin
- final answer quality is not worse
- the agent does not require more correction turns
- implementation quality does not degrade for edit tasks

As a rough rule:

```text
< 5% difference  = probably noise
5–15%            = maybe useful, test more
15–30%+          = likely worth adopting
```

## Add your own task

Create another prompt set under `bench/prompts/`, then run one variant directly:

```bash
./bench/run-one.sh my-task-a bench/prompts/a-thai.md
```

For fair comparison:

- use the same model/config
- run from a fresh session
- keep repo state identical
- avoid leaking prior run output into the next run
- repeat each variant several times

## Edit-task benchmark

For code-editing tests, use a temporary repo copy per run. Otherwise, later runs will see a repository already changed by earlier runs.

Example skeleton:

```bash
SOURCE_REPO="$(pwd)"
WORKDIR="$(mktemp -d)"

rsync -a \
  --exclude node_modules \
  --exclude .git \
  --exclude bench/results \
  "$SOURCE_REPO/" "$WORKDIR/"

cd "$WORKDIR"
git init -q
git add .
git commit -m "baseline" -q

codex exec \
  --json \
  --ephemeral \
  --sandbox workspace-write \
  --ask-for-approval never \
  "$(cat "$SOURCE_REPO/bench/prompts/a-thai.md")" \
  > "$SOURCE_REPO/bench/results/edit-test.jsonl"

git diff > "$SOURCE_REPO/bench/results/edit-test.diff"
```

For edit tasks, also record:

```bash
git diff --stat
yarn test
yarn lint
```

## Why variant C exists

The practical goal is not “never use Thai.”

The better architecture is:

```text
User language            = human interface
Concise English          = technical working layer
Original language        = preserved only when exact wording matters
Final response language  = user-facing interface
```

So Thai can remain comfortable for the user while the agent works in a more compact, code-aligned technical layer.

## Notes

This benchmark does not prove a universal law. It gives you evidence for your own model, repo, prompts, and workflow.

Different models and agent tools may already normalize multilingual input internally, so the difference may be smaller than expected. Measure before turning this into doctrine. Twitter takes are not a benchmark.

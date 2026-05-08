# Agents Thai Prompt Benchmark

A small shell benchmark for testing whether multilingual prompts, English prompts, or multilingual prompts with an English working-language policy produce different Codex usage/cost behavior.

The core question is not only:

> Does Thai use more tokens than English?

The better question is:

> Does a language policy reduce total tokens per completed coding-agent task without hurting output quality?

This repo gives you a repeatable way to compare three variants:

| Variant | Meaning |
|---|---|
| A | Thai prompt, Thai reply |
| B | English prompt, English reply |
| C | Thai prompt + English working-language policy, Thai reply |

## Benchmark Results

> Run date: 2026-05-08 · Runs per variant: 3 · Codex CLI: 0.125.0 · Claude Code: 2.1.133
>
> **Tools:** Codex (`gpt-5.5`, reasoning effort: medium) · Claude Code (`claude-sonnet-4-6`)
>
> **Codebases tested:**
> - `benchmark-repo` — this repo itself (~10 files, ~700 LOC)
> - `flask` — [pallets/flask](https://github.com/pallets/flask) (~265 files, 83 Python files, ~18k LOC)
>
> **Note on B prompt:** variant B is English prompt + English reply — pure English on both sides, for a clean comparison with Thai-only variant A.
>
> **Note on cross-tool totals:** Codex runs with `--ignore-user-config --sandbox read-only`; Claude Code with `--no-session-persistence` and its full default system prompt. Within-tool A/B/C comparison is apples-to-apples; the cross-tool column shows which tool used fewer tokens for this task.

---

### Codebase: benchmark-repo (~10 files)

#### Codex (gpt-5.5)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 167,082 | 140,416 | 2,484 | 227 | 169,793 | 22 |
| B English direct | 3 | 184,449 | 155,179 | 2,274 | 153 | 186,876 | 23 |
| C Thai + English policy | 3 | 236,102 | 187,093 | 3,734 | 483 | 240,319 | 27 |

B vs A: **+10%** · C vs A: **+42%**

#### Claude Code (claude-sonnet-4-6)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 153,207 | 140,569 | 3,120 | 0 | 156,327 | 10 |
| B English direct | 3 | 82,416 | 72,507 | 2,113 | 0 | 84,528 | 15 |
| C Thai + English policy | 3 | 154,193 | 138,403 | 3,994 | 0 | 158,188 | 11 |

B vs A: **−46%** · C vs A: **+1%** (noise)

#### Cross-tool — benchmark-repo

| Variant | Codex | Claude Code | Delta |
|---|---:|---:|---:|
| A Thai direct | 169,793 | 156,327 | −8% |
| B English direct | 186,876 | 84,528 | **−55%** |
| C Thai + English policy | 240,319 | 158,188 | −34% |

---

### Codebase: flask (~265 files, 18k LOC)

#### Codex (gpt-5.5)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 232,217 | 179,499 | 2,947 | 392 | 235,556 | 21 |
| B English direct | 3 | 157,748 | 119,040 | 2,689 | 383 | 160,819 | 18 |
| C Thai + English policy | 3 | 470,308 | 383,701 | 6,077 | 783 | 477,167 | 32 |

B vs A: **−32%** · C vs A: **+103%**

#### Claude Code (claude-sonnet-4-6)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 184,434 | 172,845 | 2,566 | 0 | 186,999 | 18 |
| B English direct | 3 | 87,297 | 79,748 | 1,509 | 0 | 88,806 | 12 |
| C Thai + English policy | 3 | 269,517 | 246,478 | 5,150 | 0 | 274,667 | 26 |

B vs A: **−52%** · C vs A: **+47%**

#### Cross-tool — flask

| Variant | Codex | Claude Code | Delta |
|---|---:|---:|---:|
| A Thai direct | 235,556 | 186,999 | −21% |
| B English direct | 160,819 | 88,806 | **−45%** |
| C Thai + English policy | 477,167 | 274,667 | **−42%** |

---

### Key findings

#### Language direction reverses with codebase size on Codex

| Codebase | Codex cheapest | B vs A delta |
|---|---|---:|
| benchmark-repo (tiny) | **A Thai** | +10% |
| flask (medium-large) | **B English** | −32% |

On a tiny repo, Codex handles Thai slightly more efficiently. On Flask (83 Python files), English becomes 32% cheaper — the language effect scales with codebase size. The larger and more structured the codebase, the more the English-prompt Codex agent navigates it efficiently.

#### Claude Code: English is always cheaper, pattern holds across scales

| Codebase | B vs A (English vs Thai) |
|---|---:|
| benchmark-repo | −46% |
| flask | −52% |

Claude Code consistently uses roughly half the tokens for English prompts vs Thai, regardless of codebase size. The gap does not close on larger repos.

#### Policy variant (C) scales badly on larger codebases

| | Codex C vs A | Claude Code C vs A |
|---|---:|---:|
| benchmark-repo | +42% | +1% |
| flask | **+103%** | +47% |

On Flask, the English working-language policy causes Codex to more than double its token usage vs Thai direct. Claude Code's policy cost also grows significantly (47% on Flask vs negligible on tiny repo). The policy encourages both agents to do a more thorough multi-pass analysis, which becomes expensive on real codebases.

#### Practical decision table

| Tool | Small repo | Large repo | Avoid |
|---|---|---|---|
| Codex (`gpt-5.5`) | A Thai (cheapest) | **B English** | C policy at scale |
| Claude Code (Sonnet) | **B English** | **B English** | Thai prompts at any scale |

---

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

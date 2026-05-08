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
| C | Thai prompt + verbose English working-language policy (4 bullets), Thai reply |
| D | Thai prompt + compact policy (3 short directives), Thai reply |

## Benchmark Results

> Run date: 2026-05-08 · Runs per variant: 3 · Codex CLI: 0.125.0 · Claude Code: 2.1.133
>
> **Tools:** Codex (`gpt-5.5`, reasoning effort: medium) · Claude Code (`claude-sonnet-4-6`)
>
> **Codebases tested:**
> - `benchmark-repo` — this repo itself (~10 files, ~700 LOC)
> - `flask` — [pallets/flask](https://github.com/pallets/flask) (~265 files, 83 Python files, ~18k LOC)
>
> **Variant D prompt** (`bench/prompts/d-compact-policy.md`): same Thai task as A, plus one short line — `Use English for all reasoning. Do not carry long non-English text through the working context unless exact wording matters. Reply to the lang of input.`
>
> **Note on B prompt:** variant B is English prompt + English reply — pure English on both sides, for a clean comparison with Thai-only variant A.
>
> **Note on cross-tool totals:** Codex runs with `--ignore-user-config --sandbox read-only`; Claude Code with `--no-session-persistence` and its full default system prompt. Within-tool A/B/C/D comparison is apples-to-apples; the cross-tool column shows which tool used fewer tokens for this task.

---

### Codebase: benchmark-repo (~10 files)

#### Codex (gpt-5.5)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 167,082 | 140,416 | 2,484 | 227 | 169,793 | 22 |
| B English direct | 3 | 184,449 | 155,179 | 2,274 | 153 | 186,876 | 23 |
| C Thai + verbose policy | 3 | 236,102 | 187,093 | 3,734 | 483 | 240,319 | 27 |
| D Thai + compact policy | 3 | 330,698 | 284,715 | 4,323 | 654 | 335,675 | 30 |

B vs A: +10% · C vs A: +42% · **D vs A: +98%**

#### Claude Code (claude-sonnet-4-6)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 153,207 | 140,569 | 3,120 | 0 | 156,327 | 10 |
| B English direct | 3 | 82,416 | 72,507 | 2,113 | 0 | 84,528 | 15 |
| C Thai + verbose policy | 3 | 154,193 | 138,403 | 3,994 | 0 | 158,188 | 11 |
| D Thai + compact policy | 3 | 128,287 | 115,720 | 3,707 | 0 | 131,994 | 16 |

B vs A: −46% · C vs A: +1% · **D vs A: −16%**

#### Cross-tool — benchmark-repo

| Variant | Codex | Claude Code | Delta |
|---|---:|---:|---:|
| A Thai direct | 169,793 | 156,327 | −8% |
| B English direct | 186,876 | 84,528 | **−55%** |
| C Thai + verbose policy | 240,319 | 158,188 | −34% |
| D Thai + compact policy | 335,675 | 131,994 | **−61%** |

---

### Codebase: flask (~265 files, 18k LOC)

#### Codex (gpt-5.5)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 232,217 | 179,499 | 2,947 | 392 | 235,556 | 21 |
| B English direct | 3 | 157,748 | 119,040 | 2,689 | 383 | 160,819 | 18 |
| C Thai + verbose policy | 3 | 470,308 | 383,701 | 6,077 | 783 | 477,167 | 32 |
| D Thai + compact policy | 3 | 341,688 | 272,512 | 5,003 | 891 | 347,582 | 27 |

B vs A: −32% · C vs A: +103% · **D vs A: +48%**

#### Claude Code (claude-sonnet-4-6)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 184,434 | 172,845 | 2,566 | 0 | 186,999 | 18 |
| B English direct | 3 | 87,297 | 79,748 | 1,509 | 0 | 88,806 | 12 |
| C Thai + verbose policy | 3 | 269,517 | 246,478 | 5,150 | 0 | 274,667 | 26 |
| D Thai + compact policy | 3 | 153,392 | 140,416 | 3,675 | 0 | 157,067 | 26 |

B vs A: −52% · C vs A: +47% · **D vs A: −16%**

#### Cross-tool — flask

| Variant | Codex | Claude Code | Delta |
|---|---:|---:|---:|
| A Thai direct | 235,556 | 186,999 | −21% |
| B English direct | 160,819 | 88,806 | **−45%** |
| C Thai + verbose policy | 477,167 | 274,667 | **−42%** |
| D Thai + compact policy | 347,582 | 157,067 | **−55%** |

---

### Key findings

#### Claude Code: compact policy (D) beats Thai direct; Codex: policy always adds cost

| | Codex | Claude Code |
|---|---:|---:|
| B English vs A Thai | +10% / −32% (size-dependent) | −46% / −52% |
| C verbose policy vs A | +42% / +103% | +1% / +47% |
| **D compact policy vs A** | **+98% / +48%** | **−16% / −16%** |

_Left value: benchmark-repo · Right value: flask_

**Claude Code understands the compact constraint.** D's single line — `Use English for all reasoning. Do not carry long non-English text…` — reduces total tokens below Thai direct by 16% on both codebases, without triggering the scope expansion that C causes. The constraint is being respected: shorter context per turn, same number of tool calls.

**Codex ignores the constraint and expands scope.** Any policy instruction — verbose or compact — causes Codex to do more work. D is actually worse than C on the tiny repo (+98% vs +42%). The phrasing of the policy doesn't matter; the presence of additional instructions is what signals "be more thorough."

#### Language direction reverses with codebase size on Codex

| Codebase | Codex cheapest variant | total tokens |
|---|---|---:|
| benchmark-repo (tiny) | **A Thai direct** | 169,793 |
| flask (medium-large) | **B English direct** | 160,819 |

On a tiny repo, Thai is marginally cheapest for Codex. On Flask (83 Python files), English is 32% cheaper. Language effect scales with codebase size for Codex.

#### Policy variant (C) is the worst choice at scale — for both tools

| | Codex C vs A | Claude Code C vs A |
|---|---:|---:|
| benchmark-repo | +42% | +1% |
| flask | **+103%** | +47% |

The verbose 4-bullet policy reads as a directive to be thorough. Both agents explore more aggressively, accumulating larger context. On Flask, Codex more than doubles its token count. Compact policy D is strictly better than C for every configuration tested.

#### Practical decision table

| Tool | Best choice | If Thai input required | Avoid |
|---|---|---|---|
| Codex (`gpt-5.5`) | **B English** (large repos) | A Thai direct | Any policy |
| Claude Code (Sonnet) | **B English** (always −46–52%) | **D compact policy** (−16%) | C verbose policy |

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

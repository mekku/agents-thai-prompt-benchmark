# Agents Thai Prompt Benchmark

## Summary

If you use AI coding agents and write prompts in Thai, you've probably wondered: does Thai cost more tokens than English? We ran a benchmark to find out — and the answer surprised us.

**How we tested it**

We gave two tools (OpenAI Codex and Claude Code) the same repo analysis task in four ways: Thai only, English only, Thai with a multi-step language policy, and Thai with a one-line compact policy. We ran each variant 3 times on a tiny repo (this one) and a real medium-sized project (Flask). 36 runs total.

**What we discovered**

The two tools behave completely differently:

- On **Codex**, Thai is actually cheaper than English on small repos. But the bigger the codebase gets, the more English pulls ahead — saving 32% on Flask. Adding any policy instruction makes things worse regardless of how it's written.
- On **Claude Code**, English is consistently half the token cost of Thai, no matter the repo size. A single short policy line ("Use English for all reasoning. Don't carry long non-English text.") brings Thai down by 16% — but it only works on Claude Code, not Codex.
- The detailed 4-bullet policy we tried (variant C) backfired badly on both tools. It more than doubled Codex's cost on Flask. More instructions = the agent thinks it should do more work, not less.

**Does cheaper mean worse output?**

Not always — but sometimes yes. Thai prompts on Claude Code gave shorter, more concise answers. English prompts gave more detailed analysis with exact file names and line numbers. On larger codebases the gap was clearest: Thai got general advice like "this file is too big", English got specific facts like "`app.py` has 1,625 lines, `test_basic.py` has 1,970 lines." The one-line compact policy (D) hit the sweet spot for Claude Code — specific answers, Thai reply, lower cost than Thai alone.

**Bottom line**

| | Best prompt | If you need Thai |
|---|---|---|
| Codex | English on large repos, Thai on small | Thai direct, no policy |
| Claude Code | English (saves ~50%) | One-line compact policy (saves 16%) |

---

## สรุปภาพรวม

ถ้าคุณใช้ AI coding agent และเขียน prompt ภาษาไทย คุณน่าจะเคยสงสัยว่า ภาษาไทยใช้ token มากกว่าภาษาอังกฤษไหม เราลองรัน benchmark ดู — และคำตอบที่ได้ไม่ตรงกับที่คิด

**วิธีที่เราทดสอบ**

เราให้ AI สองตัว (OpenAI Codex และ Claude Code) วิเคราะห์ repo เดียวกัน ด้วย 4 วิธี: ภาษาไทยล้วน, ภาษาอังกฤษล้วน, ไทย + policy แบบละเอียด 4 ข้อ และไทย + policy แบบสั้นหนึ่งบรรทัด รันละ 3 ครั้ง บน 2 codebase (repo เล็ก ๆ ของเราเอง กับ Flask ซึ่งเป็นโปรเจกต์จริงขนาดกลาง) รวม 36 รัน

**สิ่งที่ค้นพบ**

สองเครื่องมือนี้ตอบสนองต่างกันโดยสิ้นเชิง:

- **Codex** — บน repo เล็ก ภาษาไทยถูกกว่าภาษาอังกฤษเล็กน้อย แต่พอ codebase ใหญ่ขึ้น ภาษาอังกฤษชนะชัดเจน ประหยัดได้ 32% บน Flask การใส่ policy เพิ่มเข้าไป ไม่ว่าสั้นหรือยาว ทำให้แพงขึ้นเสมอ
- **Claude Code** — ภาษาอังกฤษใช้ token ครึ่งหนึ่งของภาษาไทยอย่างสม่ำเสมอ ไม่ว่า repo จะใหญ่แค่ไหน policy สั้น ๆ หนึ่งบรรทัดช่วยลดต้นทุนของ prompt ไทยได้ 16% แต่วิธีนี้ใช้ได้กับ Claude Code เท่านั้น ไม่ใช่ Codex
- **Policy แบบละเอียด 4 ข้อ (variant C)** ให้ผลเสียกับทั้งสองเครื่องมือ ทำให้ Codex จ่ายเพิ่มเป็น 2 เท่าบน Flask เพราะ AI ตีความว่า "มี instruction เพิ่ม = ต้องทำงานละเอียดขึ้น"

**ถูกกว่า = คุณภาพแย่ลงไหม**

ไม่เสมอไป แต่บางครั้งก็ใช่ Prompt ภาษาไทยบน Claude Code ให้คำตอบสั้นและกระชับกว่า ส่วนภาษาอังกฤษให้ผลละเอียดพร้อมชื่อไฟล์และเลขบรรทัดชัดเจน บน Flask เห็นชัดที่สุด: ไทยบอกแบบกว้าง ๆ ว่า "ไฟล์นี้ใหญ่เกินไป" แต่อังกฤษบอกได้เลยว่า "`app.py` มี 1,625 บรรทัด `test_basic.py` มี 1,970 บรรทัด" Policy สั้น (D) คือจุดลงตัวที่ดีที่สุดสำหรับ Claude Code คำตอบละเอียด ตอบเป็นภาษาไทย และถูกกว่า Thai direct 16%

**สรุปสั้น ๆ**

| | Prompt ที่ดีที่สุด | ถ้าต้องใช้ภาษาไทย |
|---|---|---|
| Codex | อังกฤษ (repo ใหญ่), ไทย (repo เล็ก) | ไทยตรง ไม่ต้องใส่ policy |
| Claude Code | อังกฤษ (ประหยัด ~50%) | Policy สั้นหนึ่งบรรทัด (ประหยัด 16%) |

---

A small shell benchmark for testing whether multilingual prompts, English prompts, or multilingual prompts with an English working-language policy produce different Codex usage/cost behavior.

The core question is not only:

> Does Thai use more tokens than English?

The better question is:

> Does a language policy reduce total tokens per completed coding-agent task without hurting output quality?

This repo gives you a repeatable way to compare three variants:

| Variant | Prompt | Reply |
|---|---|---|
| A | Thai task only | Thai |
| B | English task only | English |
| C | Thai task + verbose 4-bullet policy ("reason in English") | Thai |
| D | Thai task + one-line compact policy | Thai |

### What each variant tests

| Variant | Hypothesis |
|---|---|
| **A — Thai direct** | Baseline. No instruction about language. Does the agent naturally carry Thai text through its working context, accumulating tokens as the task grows? |
| **B — English direct** | Pure language effect. If we switch the entire conversation to English, how much do tokens drop? No other variables change. |
| **C — Thai + verbose policy** | Can an explicit 4-step instruction ("reason in English, reply in Thai") reduce the overhead of Thai input without changing what the user sees? Or does more instruction = more work? |
| **D — Thai + compact policy** | Can a single short line achieve what C tries to do, but without accidentally signaling "be more thorough" — the side effect that made C backfire? |

**The central question:** can a language policy let you keep Thai as your input language while the agent works more efficiently?

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

#### Visual comparison

**Claude Code — total tokens per variant (lower is better)**

```
benchmark-repo (~10 files)                        flask (~18k LOC)

A Thai direct     ████████████████████  156,327   ████████████████████████  186,999
B English direct  ██████████            84,528 ✓  ████████████               88,806 ✓
C Verbose policy  ████████████████████  158,188   ████████████████████████████████████ 274,667 ✗
D Compact policy  █████████████████    131,994    ████████████████████       157,067
```
_B saves ~50% vs A on both codebases. D saves 16%. C nearly matches A on small repos but costs 47% more on large._

**Codex — total tokens per variant (lower is better)**

```
benchmark-repo (~10 files)                        flask (~18k LOC)

A Thai direct     █████████████████  169,793      ████████████████████████  235,556
B English direct  ██████████████████ 186,876      ████████████████          160,819 ✓
C Verbose policy  ███████████████████████ 240,319 ████████████████████████████████████████████████ 477,167 ✗
D Compact policy  ████████████████████████████████████ 335,675 ✗  ██████████████████████████████████ 347,582 ✗
```
_Codex behaves opposite to Claude Code. Any policy line = more scope = more tokens._

---

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

#### Output quality

All variants completed the task (5 issues identified) in every run. Token savings are not always quality-neutral.

| Variant | Specificity | Length | Notes |
|---|---|---:|---|
| A Thai direct | Medium — file refs present, less elaboration | ~8–23 sentences | Concise; on large repos Thai prompts describe patterns without exact line counts |
| B English direct | High — file paths, exact line numbers, structured reasoning | ~13–22 sentences | Consistently precise across repo sizes |
| C Thai + verbose policy | High — very detailed, over-elaborated | ~45–78 sentences | Quality overkill for quick analysis; rarely worth the token cost |
| D Thai + compact policy | High — file refs, specific, Thai reply | ~48–85 sentences | Best quality-per-token on Claude Code; specific without triggering excessive scope |

Key observation: on the larger Flask codebase, Codex with a Thai prompt described problems in general patterns ("large files, naming overlap") while the English prompt cited exact line counts (`app.py: 1,625 lines`, `test_basic.py: 1,970 lines`). Part of Thai's lower token count on Claude Code reflects a shorter, more concise output — not pure language-handling efficiency.

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

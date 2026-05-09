# Agents Thai Prompt Benchmark

Does writing prompts in Thai cost more tokens than English when using AI coding agents — and can a language policy close the gap?
This repo benchmarks four prompt variants (A–D) across two tools and three codebases to find out.

**Codebases tested**

| Codebase | Size | Source language |
|---|---|---|
| `benchmark-repo` | ~10 files, ~700 LOC | English — this repo |
| `flask` | ~265 files, ~18k LOC | English — [pallets/flask](https://github.com/pallets/flask) |
| `election-live` | ~81 JS files | Thai strings in source — [electinth/election-live](https://github.com/electinth/election-live) |

---

## สรุปภาพรวม

ถ้าคุณใช้ AI coding agent และเขียน prompt ภาษาไทย คุณน่าจะเคยสงสัยว่า ภาษาไทยใช้ token มากกว่าภาษาอังกฤษไหม เราลองรัน benchmark ดู — และคำตอบที่ได้ไม่ตรงกับที่คิด

**วิธีที่เราทดสอบ**

| | Prompt | สิ่งที่ทดสอบ |
|---|---|---|
| **A** | ไทย → ไทย | Baseline: agent พา context ภาษาไทยไปมากแค่ไหนโดยธรรมชาติ? |
| **B** | อังกฤษ → อังกฤษ | ถ้าเปลี่ยนภาษาทั้งหมดเป็นอังกฤษ token ลดลงไหม? |
| **C** | ไทย + policy 4 ข้อ → ไทย | instruction ชัดเจนช่วยลด overhead ได้ไหม — หรือ instruction เพิ่ม = งานเพิ่ม? |
| **D** | ไทย + hint 1 บรรทัด → ไทย | เป้าหมายเดียวกับ C แต่สั้นกว่า — ไม่ให้ AI ตีความว่า "ต้องทำงานละเอียดขึ้น" |

เราให้ AI สองตัว (OpenAI Codex และ Claude Code) รันทั้ง 4 variant ละ 3 ครั้ง บน 3 codebase ได้แก่ repo เล็ก ๆ ของเราเอง, Flask (โปรเจกต์อังกฤษล้วนขนาดกลาง) และ election-live (แอป React จริงของนักพัฒนาไทย ที่มี string ภาษาไทยฝังอยู่ในไฟล์โค้ด JSX) รวม 72 รัน

**สิ่งที่ค้นพบ**

สองเครื่องมือตอบสนองต่างกัน และประเภทของ codebase ก็มีผลด้วย:

- **Codex บน repo ที่เป็นภาษาอังกฤษล้วน** — ไทยถูกกว่าบน repo เล็ก แต่อังกฤษถูกกว่า 32% บน Flask การใส่ policy ทุกรูปแบบทำให้แพงขึ้นเสมอ
- **Codex บน repo ที่มีโค้ดภาษาไทย (election-live)** — พลิกกลับ: ภาษาอังกฤษแพงกว่าไทย 13% เพราะ AI ต้องประมวล string ไทยในไฟล์โค้ดในฐานะ "ภาษาต่างประเทศ"
- **Claude Code บน repo ภาษาอังกฤษล้วน** — ภาษาอังกฤษใช้ token ครึ่งหนึ่งของไทยอย่างสม่ำเสมอ Policy สั้นหนึ่งบรรทัดช่วยลด 16% เมื่อต้องใช้ไทย
- **Claude Code บน repo ที่มีโค้ดไทย** — ทุก variant ใช้ token ใกล้เคียงกันมาก (ต่างกันแค่ 2%) ที่ ~44k token Policy สั้น (D) กลับทำให้แพงขึ้น 70% ไม่ใช่ถูกลง
- **Policy แบบ 4 ข้อ (C)** แย่ที่สุดหรือแย่ใกล้เคียงที่สุดในทุก codebase และทุกเครื่องมือ

**ถูกกว่า = คุณภาพแย่ลงไหม**

ไม่เสมอไป แต่บางครั้งก็ใช่ Prompt ภาษาไทยบน Claude Code ให้คำตอบสั้นและกระชับกว่า ส่วนภาษาอังกฤษให้ผลละเอียดพร้อมชื่อไฟล์และเลขบรรทัดชัดเจน บน Flask เห็นชัดที่สุด ส่วน policy สั้น (D) ดีที่สุดบน repo ภาษาอังกฤษ แต่ไม่ควรใช้บน repo ที่มีโค้ดภาษาไทย

**สรุปสั้น ๆ**

| | repo ภาษาอังกฤษล้วน | repo ที่มีโค้ดภาษาไทย |
|---|---|---|
| Codex | อังกฤษ (repo ใหญ่), ไทย (repo เล็ก) | ไทยตรง (อังกฤษแพงกว่า) |
| Claude Code | อังกฤษ (~50%); D ถ้าต้องใช้ไทย (-16%) | ใช้ได้ทุก variant ยกเว้น D |

---

## Summary

If you use AI coding agents and write prompts in Thai, you've probably wondered: does Thai cost more tokens than English? We ran a benchmark to find out — and the answer surprised us.

**How we tested it**

| | Prompt | Hypothesis |
|---|---|---|
| **A** | Thai → Thai | Baseline: does the agent naturally carry Thai through its working context? |
| **B** | English → English | Does a full language switch cut tokens? Pure language effect, no other variables. |
| **C** | Thai + 4-bullet policy → Thai | Can an explicit "reason in English" instruction reduce overhead — or does more instruction = more work? |
| **D** | Thai + 1-line hint → Thai | Same goal as C, minimal instruction: can one line work without signaling "be more thorough"? |

We ran each variant 3 times on three codebases — a tiny repo (this one), a medium-sized English project (Flask), and a real Thai-developer app with Thai strings in source files (electinth/election-live) — using two tools (Codex and Claude Code). 72 runs total.

**What we discovered**

The two tools behave completely differently — and the type of codebase matters too:

- On **Codex with English-source repos**, Thai is slightly cheaper on small repos but English saves 32% at Flask scale. Adding any policy instruction makes things worse regardless of how it's written.
- On **Codex with Thai-content repos** (election-live), the pattern flips: English is actually MORE expensive than Thai (+13%). When Thai strings are in the source files, a Thai prompt handles them more naturally.
- On **Claude Code with English-source repos**, English is consistently half the token cost of Thai (46–52% savings). A single compact policy line cuts Thai's cost by 16%.
- On **Claude Code with Thai-content repos**, language barely matters — A, B, and C all land within 2% of each other at ~44k tokens. The compact policy (D) backfires here (+70%), probably because telling it "don't carry Thai" causes it to open more files to understand Thai it's trying to skip.
- The detailed 4-bullet policy (C) was consistently the worst or near-worst choice on every codebase and both tools.

**Does cheaper mean worse output?**

Not always — but sometimes yes. Thai prompts on Claude Code gave shorter, more concise answers. English prompts gave more detailed analysis with exact file names and line numbers. On larger codebases the gap was clearest: Thai got general advice like "this file is too big", English got specific facts like "`app.py` has 1,625 lines, `test_basic.py` has 1,970 lines." The one-line compact policy (D) hits the sweet spot for Claude Code on English-source repos — specific answers, Thai reply, lower cost than Thai alone. But it doesn't help on Thai-content repos.

**Bottom line**

| | English-source repo | Thai-annotated repo |
|---|---|---|
| Codex | English on large repos, Thai on small | Thai direct (English costs more) |
| Claude Code | English saves ~50%; D saves 16% with Thai | Any variant works — skip D |

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

### The actual prompts

**A — Thai direct** (`bench/prompts/a-thai.md`)
```
ช่วยวิเคราะห์ repo นี้ แล้วหาจุดที่ควรปรับปรุง 5 จุด โดยเน้นเรื่องความชัดเจนของโครงสร้างไฟล์ การตั้งชื่อ และความเสี่ยงของโค้ด

ตอบกลับเป็นภาษาไทยแบบสั้น กระชับ
```
_Analyze this repo, find 5 improvement areas focusing on file structure clarity, naming, and code risk. Reply briefly in Thai._

---

**B — English direct** (`bench/prompts/b-english.md`)
```
Analyze this repository and identify 5 improvement areas, focusing on file structure clarity, naming, and code risk.

Reply briefly in English.
```
_Same task as A, entirely in English — no policy, no Thai._

---

**C — Thai + verbose policy** (`bench/prompts/c-universal-policy.md`)
```
ช่วยวิเคราะห์ repo นี้ แล้วหาจุดที่ควรปรับปรุง 5 จุด โดยเน้นเรื่องความชัดเจนของโครงสร้างไฟล์ การตั้งชื่อ และความเสี่ยงของโค้ด

Follow this multilingual working policy:
- Convert the user's request into a compact English working brief.
- Use English for technical reasoning, planning, code analysis, TODOs, and implementation notes.
- Do not carry long non-English text through the working context unless exact wording matters.
- Reply to the user in Thai.
```
_Same Thai task as A, but with an explicit 4-step policy telling the agent to work in English internally._

---

**D — Thai + compact policy** (`bench/prompts/d-compact-policy.md`)
```
ช่วยวิเคราะห์ repo นี้ แล้วหาจุดที่ควรปรับปรุง 5 จุด โดยเน้นเรื่องความชัดเจนของโครงสร้างไฟล์ การตั้งชื่อ และความเสี่ยงของโค้ด

Use English for all reasoning. Do not carry long non-English text through the working context unless exact wording matters. Reply to the lang of input.
```
_Same Thai task as A, but with a single-line hint instead of 4 bullets. Intentionally minimal to avoid triggering scope expansion._

## Benchmark Results

> Run dates: 2026-05-08 (benchmark-repo, flask) · 2026-05-09 (election-live) · Runs per variant: 3 · Codex CLI: 0.125.0 · Claude Code: 2.1.133
>
> **Tools:** Codex (`gpt-5.5`, reasoning effort: medium) · Claude Code (`claude-sonnet-4-6`)
>
> **Codebases tested:**
> - `benchmark-repo` — this repo itself (~10 files, ~700 LOC) — English source
> - `flask` — [pallets/flask](https://github.com/pallets/flask) (~265 files, 83 Python files, ~18k LOC) — English source
> - `election-live` — [electinth/election-live](https://github.com/electinth/election-live) (~81 JS files, React/Gatsby) — **Thai strings in source code**
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

### Codebase: election-live (~81 JS files, Thai strings in source)

> [electinth/election-live](https://github.com/electinth/election-live) — React/Gatsby app used during Thailand's 2019 general election. Thai string literals embedded directly in JSX components, Thai paragraphs in page source files.

#### Codex (gpt-5.5)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 209,304 | 164,181 | 2,670 | 247 | 212,221 | 22 |
| B English direct | 3 | 236,841 | 195,328 | 3,032 | 308 | 240,181 | 25 |
| C Thai + verbose policy | 3 | 462,271 | 394,965 | 5,440 | 748 | 468,459 | 34 |
| D Thai + compact policy | 3 | 373,677 | 313,301 | 4,921 | 780 | 379,377 | 32 |

**B vs A: +13%** · C vs A: +121% · D vs A: +79%

#### Claude Code (claude-sonnet-4-6)

| Variant | Runs | input_tokens | cached_input_tokens | output_tokens | reasoning_output_tokens | total_tokens | commands |
|---|---:|---:|---:|---:|---:|---:|---:|
| A Thai direct | 3 | 43,342 | 37,663 | 1,360 | 0 | 44,702 | 35 |
| B English direct | 3 | 42,355 | 37,488 | 826 | 0 | 43,181 | 31 |
| C Thai + verbose policy | 3 | 43,570 | 37,731 | 2,198 | 0 | 45,768 | 37 |
| D Thai + compact policy | 3 | 73,443 | 65,210 | 2,645 | 0 | 76,088 | 41 |

B vs A: −3% · C vs A: +2% · **D vs A: +70%**

#### Cross-tool — election-live

| Variant | Codex | Claude Code | Delta |
|---|---:|---:|---:|
| A Thai direct | 212,221 | 44,702 | **−79%** |
| B English direct | 240,181 | 43,181 | **−82%** |
| C Thai + verbose policy | 468,459 | 45,768 | **−90%** |
| D Thai + compact policy | 379,377 | 76,088 | **−80%** |

---

### Key findings

#### Visual comparison

**Claude Code — total tokens per variant (lower is better)**

```
benchmark-repo (~10 files)                        flask (~18k LOC)                     election-live (~81 JS files, Thai in src)

A Thai direct     ████████████████████  156,327   ████████████████████████  186,999    ████████          44,702
B English direct  ██████████            84,528 ✓  ████████████               88,806 ✓  ████████          43,181 ≈
C Verbose policy  ████████████████████  158,188   ████████████████████████████████████ 274,667 ✗  ████████  45,768 ≈
D Compact policy  █████████████████    131,994    ████████████████████       157,067    ██████████████    76,088 ✗
```
_English saves ~50% on pure-English repos (Flask, benchmark-repo). On a Thai-content repo (election-live): A/B/C are nearly flat, D backfires._

**Codex — total tokens per variant (lower is better)**

```
benchmark-repo (~10 files)                        flask (~18k LOC)                     election-live (~81 JS files, Thai in src)

A Thai direct     █████████████████  169,793      ████████████████████████  235,556    █████████████████  212,221
B English direct  ██████████████████ 186,876      ████████████████          160,819 ✓  ██████████████████ 240,181 ✗ ← English costs MORE
C Verbose policy  ███████████████████████ 240,319 ████████████████████████████████████████████████ 477,167 ✗  ████████████████████████████████████ 468,459 ✗
D Compact policy  ████████████████████████████████████ 335,675 ✗  ██████████████████████████████████ 347,582 ✗  █████████████████████████████ 379,377 ✗
```
_Codex: any policy always adds cost. On election-live, English (B) is MORE expensive than Thai (A) — the language-efficiency assumption flips on Thai-content repos._

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

#### Thai-content repos flip the language-efficiency pattern

The election-live results break the rules established by Flask and benchmark-repo (both pure-English codebases):

| Finding | Pure-English repos | Thai-content repo (election-live) |
|---|---|---|
| Codex B vs A | −32% to +10% | **+13% (English costs MORE)** |
| Claude Code B vs A | −46% to −52% | **−3% (nearly flat)** |
| Claude Code D vs A | −16% | **+70% (D backfires)** |
| Claude Code total tokens | 156k–187k | **44k (4× cheaper overall)** |

**Why Codex flips:** When the source files contain Thai, a Thai prompt lets Codex read and carry that content naturally. Switching to English forces it to process the Thai strings it reads as "foreign" content, adding translation overhead.

**Why Claude Code flattens:** Claude Code is very efficient at reading JS/React files, skipping irrelevant paths, and only summarizing what it needs. It reaches a similar result (~44k tokens) regardless of prompt language. There's less context carry to compress.

**Why D backfires on Claude Code:** The compact policy says "don't carry long non-English text." On a repo where JS files contain Thai string literals, this may cause the agent to open more files to understand the Thai it is trying not to carry — more commands (41 vs 35), more total tokens.

#### Practical decision table

| Tool | Pure-English repo | Thai-annotated repo |
|---|---|---|
| Codex | **B English** (large repos) · A Thai (small repos) | **A Thai direct** — English costs more here |
| Claude Code | **B English** (saves 46–52%) | **A, B, or C** — nearly equal; avoid D |

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

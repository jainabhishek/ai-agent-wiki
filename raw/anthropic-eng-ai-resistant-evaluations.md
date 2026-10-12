# Designing AI-resistant technical evaluations — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
> Publisher: Anthropic (Engineering blog) · Date: 2026-01-21
> Captured: 2026-10-12 via curl (condensed).

Author: Tristan Hume, a lead on Anthropic's performance optimization team, who
designed and redesigned the performance-engineering take-home. Subtitle
(paraphrased): lessons from three iterations of a take-home that Claude keeps
beating.

## Intro

- As AI improves, a take-home that separates human skill levels today may be
  trivially solved by a model tomorrow, which makes it useless.
- Since early 2024 the performance engineering team has used a take-home in
  which candidates optimize code for a simulated accelerator. Over 1,000
  candidates completed it; dozens were hired, including engineers who brought up
  the Trainium cluster and shipped every model since Claude 3 Opus.
- Each new Claude model forced a redesign. Under the same time limit, Claude
  Opus 4 beat most applicants; Claude Opus 4.5 then matched even the strongest.
  With unlimited time humans still win, but within the take-home limits the
  team could no longer tell top candidates' output from the model's.
- Three versions so far. The original is released as an open challenge,
  because unlimited-time human results still beat Claude.

## The origin of the take-home

- November 2023: preparing to train and launch Claude Opus 3, with new TPU and
  GPU clusters and a large Trainium cluster coming, and too few performance
  engineers. A Twitter call produced more candidates than the standard pipeline
  could handle. The author spent two weeks designing a take-home.

### Design goals

- Aim: an engaging problem that captures skill at high resolution, unlike
  generic, boring take-homes.
- Format advantages over live interviews:
  - **Longer time horizon:** 4 hours (later 2 hours), closer to real work than
    sub-hour interviews.
  - **Realistic environment:** no observer, no narration, own editor.
  - **Time for comprehension and tooling:** understanding systems and building
    debugging tools is hard to test in a 50-minute interview.
  - **Compatibility with AI assistance:** Anthropic's general guidance says no
    AI on take-homes unless stated; this take-home explicitly allows AI. Longer
    problems are harder for AI to solve completely, so candidates can use AI as
    on the job and still show their own skill.
- General interview principles applied:
  - **Representative of real work.**
  - **High signal:** no single-insight problems; many chances to show ability;
    wide score distribution; enough depth that strong candidates do not finish.
  - **No specific domain knowledge** required.
  - **Fun:** fast development loops, depth, room for creativity.

### The simulated machine

- A Python simulator of a fake TPU-like accelerator, with a hot-reloading
  Perfetto trace showing every instruction (similar to Trainium tooling).
- Machine features: manually managed scratchpad memory, VLIW (several execution
  units per cycle; needs instruction packing), SIMD (vector ops), multicore.
- Task: parallel tree traversal, deliberately not deep-learning flavored;
  inspired by branchless SIMD decision-tree inference.
- Candidates start from a fully serial implementation. Warmup is multicore
  parallelism; then they choose SIMD vectorization or VLIW packing. Version 1
  also contained a bug to debug first, which exercised tool building.

## Early results

- One candidate from the Twitter batch scored far above everyone, was hired,
  and soon found a workaround for a launch-blocking compiler bug (tensor
  indexing math overflowing 32 bits).
- Over about 18 months, about 1,000 candidates took it; it helped hire most of
  the current team, including several top engineers straight from undergrad.
- Candidates often worked past 4 hours for enjoyment. The best unlimited-time
  submissions included full optimizing mini-compilers.

### Then Claude Opus 4 defeated it

- By May 2025, Claude 3.7 Sonnet was good enough that over 50% of candidates
  would have scored better by delegating fully to Claude Code. A pre-release
  Claude Opus 4 beat almost all humans within the 4-hour limit.
- Earlier precedent: a 2023 live-interview question designed to need problem
  solving rather than knowledge; Claude 3 Opus beat part 1 and Claude 3.5
  Sonnet beat part 2. It is still used because the other live questions are not
  AI-resistant either.
- Fix for version 2: use Claude Opus 4 to find where it started to struggle
  and make that the new starting point. Cleaner starter code, new machine
  features for depth, multicore removed (Claude had solved it; it slowed dev
  loops without adding signal). Time limit cut from 4 to 2 hours, because
  scheduling 4 hours caused multi-week pipeline delays.
- Version 2 emphasized clever optimization insight over debugging and code
  volume, and worked for several months.

### Then Claude Opus 4.5 defeated that

- A pre-release Claude Opus 4.5 in Claude Code fixed initial bottlenecks, did
  all common micro-optimizations, and passed the threshold in under an hour.
  It then stopped, believing it had hit a memory-bandwidth limit, as most humans
  do. Told the achievable cycle count, it found the structural trick, then
  debugged and tuned further. At 2 hours it matched the best human 2-hour
  score, and that human had used Claude 4 heavily with steering.
- In Anthropic's internal test-time compute harness it beat humans at 2 hours
  and kept improving with time; a generic post-launch harness improvement
  raised the score further.
- The problem: for the upcoming model release, the best take-home strategy
  would be to delegate to Claude Code.

## Considering the options

- Banning AI: rejected. Enforcement is hard, and humans still matter on the
  job, so the test should let them stand out in an AI-assisted setting. The
  author did not want to concede that humans only win on tasks longer than a
  few hours.
- Raising the bar to "substantially beat Claude Code alone": rejected. Claude
  is fast; humans spend about half of 2 hours understanding the problem; a
  human steering Claude would lag behind it, and the dominant strategy could
  become watching.
- The real job now looks more like hard debugging, systems design, performance
  analysis, verifying correctness, and making Claude's code simpler — hard to
  test objectively without much time or shared context.
- Risk of a new design: either Opus 4.5 solves it, or it becomes too hard for
  humans in 2 hours.

### Attempt 1: A different optimization problem

- Based on a hard real kernel optimization: efficient data transposition on 2D
  TPU registers while avoiding bank conflicts. Distilled into a simulated
  machine problem; Claude implemented the changes in under a day.
- Claude Opus 4.5 found an unanticipated optimization: transpose the whole
  computation instead of the data. That would not work in the real case, so the
  author patched it out. Claude then progressed but did not find the best
  solution — until checked with Claude Code's "ultrathink" (longer thinking
  budget), which solved it, including bank-conflict tricks.
- Lesson: this problem is common across platforms, so Claude had abundant
  training data; the author's first-principles route gave no edge.

### Attempt 2: Going weirder

- Need: a problem far enough out of distribution that human reasoning beats
  Claude's experience base — in tension with resembling the job.
- Inspiration: Zachtronics programming puzzle games with tiny, constrained
  instruction sets (e.g. Shenzhen I/O: programs split across communicating chips
  of about 10 instructions and one or two state registers; tricks include
  encoding state in the instruction pointer or branch flags).
- New take-home: puzzles in a tiny, heavily constrained instruction set,
  optimized for minimal instruction count. Claude Opus 4.5 failed the first
  medium-hard puzzle. Colleagues less familiar with the problem confirmed humans
  can still beat Claude.
- No visualization or debugging tools are given; starter code only validates
  solutions. Building tools (print statements, or asking a coding model for an
  interactive debugger) and judging how much to invest are part of the signal.
- Assessment: possibly lower variance than the original (more independent
  sub-problems). Scores correlate well with candidates' past work; one strong
  colleague outscored all candidates so far.
- Trade-off stated by the author: the original worked because it resembled real
  work; the replacement works because it simulates novel work. Realism may be a
  luxury no longer available.

## An open challenge

- The original take-home is released for unlimited-time attempts. The fastest
  human submission substantially beats Claude even with extensive test-time
  compute.
- Released version starts from scratch (like v1) with v2's instruction set and
  single-core design, so cycle counts compare with v2.
- Benchmarks (simulated clock cycles, lower is better):
  - 2164 — Claude Opus 4, many hours in the test-time compute harness
  - 1790 — Claude Opus 4.5, casual Claude Code session (about the best human
    2-hour result)
  - 1579 — Claude Opus 4.5, 2 hours in the test-time compute harness
  - 1548 — Claude Sonnet 4.5, many more than 2 hours of test-time compute
  - 1487 — Claude Opus 4.5, 11.5 hours in the harness
  - 1363 — Claude Opus 4.5, improved test-time compute harness, many hours
- Beat 1487 cycles (Claude's best at launch) and email code plus resume to
  Anthropic's performance-recruiting address; or apply normally and take the
  new Claude-resistant take-home.

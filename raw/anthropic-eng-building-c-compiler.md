# Building a C compiler with a team of parallel Claudes — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/building-c-compiler
> Publisher: Anthropic (Engineering blog) · Date: 2026-02-05
> Captured: 2026-10-12 via curl (condensed).

Author: Nicholas Carlini (Anthropic Safeguards team). Subtitle (paraphrased):
Opus 4.6, run as "agent teams", built a C compiler with the author mostly
absent; the post reports what this teaches about autonomous software work.

## Intro

- "Agent teams": several Claude instances work in parallel on one shared
  codebase with no active human intervention.
- Stress test: 16 agents asked to write a C compiler in Rust, from scratch,
  able to compile the Linux kernel.
- Result: nearly 2,000 Claude Code sessions, about $20,000 in API cost, a
  100,000-line compiler that builds Linux 6.9 on x86, ARM, and RISC-V.
- Focus of the post: harness design for long-running autonomous agent teams —
  tests that keep agents on track without oversight, structuring work for
  parallel progress, and where the approach hits its ceiling.

## Enabling long-running Claudes

- Existing scaffolds such as Claude Code expect an operator; on a long task the
  model eventually stops to ask a question, give a status update, or request
  clarification.
- The harness puts Claude in an infinite bash loop (the author compares it to
  "Ralph-loop"); when one task ends, the next session starts. Run it in a
  container, not on your own machine.
- Loop body: take the short HEAD commit hash, set a log file
  `agent_logs/agent_${COMMIT}.log`, run
  `claude --dangerously-skip-permissions -p "$(cat AGENT_PROMPT.md)" --model claude-opus-X-Y`
  with output to the log, repeat forever.
- `AGENT_PROMPT.md` states the problem and asks Claude to split it into small
  pieces, track current work, choose what is next, and keep going until it is
  perfect. Anecdote: once Claude ran `pkill -9 bash` by accident and killed its
  own loop.

## Running Claude in parallel

Two weaknesses of a single-agent harness that parallelism addresses:
1. One session does one thing at a time; parallel debugging of many issues is
   more efficient as scope grows.
2. Parallelism allows specialization (documentation, code quality, special
   sub-tasks) alongside agents on the main problem.

Implementation ("bare-bones"):
- A new bare git repo is the upstream. Each agent runs in its own Docker
  container with the repo mounted at `/upstream`, clones to `/workspace`, and
  pushes back to upstream when done.
- Task locking: an agent claims a task by writing a text file to
  `current_tasks/` (examples: `current_tasks/parse_if_statement.txt`,
  `current_tasks/codegen_function_definition.txt`). If two agents claim the same
  task, git synchronization forces the second to choose another.
- The agent works, pulls upstream, merges other agents' changes, pushes, and
  removes its lock. Merge conflicts are frequent; Claude resolves them.
- The loop then starts a fresh Claude Code session in a fresh container.
- Explicitly absent: no other inter-agent communication channel, no process for
  high-level goals, no orchestration agent. Each agent decides what to do;
  usually it takes the "next most obvious" problem. When stuck on a bug, an
  agent often keeps a running document of failed approaches and remaining
  tasks. The git history shows agents taking locks.

## Lessons from programming with Claude agent teams

Most of the author's effort went into the environment around Claude — tests,
environment, feedback — so agents could orient themselves without him.

### Write extremely high-quality tests

- Claude solves whatever problem it is given, so the task verifier must be
  nearly perfect; otherwise Claude solves the wrong problem.
- Work done: find high-quality compiler test suites, write verifiers and build
  scripts for open-source packages, watch Claude's mistakes, and add tests for
  each newly found failure mode.
- Late in the project new features often broke existing ones. Fix: a CI
  pipeline with stricter enforcement so new commits cannot break existing code.

### Put yourself in Claude's shoes

- The harness is written for Claude, not for a human; this changes how tests
  should report results.
- Each agent starts in a fresh container with no context and spends real time
  orienting. The prompt tells agents to maintain extensive READMEs and progress
  files, updated often with current status.
- Design around model limitations:
  - **Context window pollution.** The test harness should print only a few
    lines and log details to a file. Logs should be grep-friendly: on error,
    write `ERROR` and the reason on the same line. Pre-compute aggregate
    summary statistics so Claude does not recompute them.
  - **Time blindness.** Claude cannot tell time and may spend hours running
    tests instead of progressing. The harness prints progress rarely and has a
    default `--fast` option that runs a 1% or 10% random sample. The sample is
    deterministic per agent but random across VMs, so the fleet covers all
    files while each agent can detect its own regressions exactly.

### Make parallelism easy

- With many distinct failing tests, parallelism is trivial: each agent takes a
  different failing test. After the suite reached a 99% pass rate, each agent
  took a different small open-source project to compile (examples: SQLite,
  Redis, libjpeg, MQuickJS, Lua).
- Compiling the Linux kernel stalled the team: it is one giant task, so every
  agent hit the same bug, fixed it, and overwrote the others' changes. Sixteen
  agents gave no benefit.
- Fix: GCC as an online known-good compiler oracle. A new harness compiled a
  random majority of kernel files with GCC and the rest with Claude's compiler.
  If the kernel worked, the bug was not in Claude's subset; if it broke, the
  subset was narrowed by moving files back to GCC. Agents could then fix
  different bugs in different files in parallel. Afterwards, delta debugging
  was still needed for pairs of files that failed only together.

### Multiple agent roles

Specialized agents: one merges duplicate code (LLM code often re-implements
existing functionality); one improves compiler performance; one improves the
efficiency of the emitted code; one critiques the design as a Rust developer and
makes structural changes; one writes documentation.

## Stress testing the limits of agent teams

- The project is a capability benchmark: probe what LLMs can only barely do
  today, to prepare for what they will do reliably later.
- The author has used the C compiler task across the Claude 4 model series.
  Spec given: from-scratch optimizing compiler, no dependencies,
  GCC-compatible, compiles the Linux kernel, multiple backends. Only some design
  was specified (an SSA IR to support multiple optimization passes).
- Progression: earlier Opus 4 models barely produced a working compiler. Opus
  4.5 first produced a functional compiler that passed large test suites but
  could not compile real large projects. Opus 4.6 was the test here.

### Evaluation

- About 2,000 Claude Code sessions over two weeks. Opus 4.6 used 2 billion
  input tokens and produced 140 million output tokens; total cost just under
  $20,000. The author calls this very expensive versus any Claude Max plan, but
  a fraction of the cost of doing it himself or with a team.
- Clean room: no internet access at any point; depends only on the Rust
  standard library.
- Results: builds a bootable Linux 6.9 on x86, ARM, and RISC-V; compiles QEMU,
  FFmpeg, SQLite, postgres, redis; 99% pass rate on most compiler test suites,
  including the GCC torture test suite; compiles and runs Doom.
- Limitations listed:
  - No 16-bit x86 compiler for booting Linux from real mode; it calls GCC for
    that (its x86_32 and x86_64 compilers are its own).
  - No own assembler and linker; these were the last parts started and are
    still buggy. The demo used GCC's assembler and linker.
  - Builds many but not all projects; not a drop-in replacement.
  - Generated code is slow: with all optimizations on, it is less efficient
    than GCC with all optimizations off.
  - Rust code quality is reasonable but well below expert level.
- The author says the compiler is near the limit of Opus's abilities. He tried
  hard to fix the limitations and did not fully succeed; new features and fixes
  often broke existing functionality.
- Example: Opus could not build a 16-bit x86 code generator. It can emit correct
  16-bit code through the 66/67 opcode prefixes, but the output exceeds 60 KB,
  above Linux's 32 KB limit. Claude "cheats" by calling GCC for this phase (x86
  only; ARM and RISC-V compile fully by themselves).
- Source code is public; the author planned to keep Claude pushing changes.

## Looking forward

- Product history as the author tells it: tab completion, then function bodies
  from docstrings, then Claude Code pair programming — all assume a short
  task-answer-follow-up cycle. Agent teams suggest whole complex projects can
  run autonomously.
- Risks: a human pairing with Claude catches errors in real time; with
  autonomous systems it is easy to see tests pass and assume the job is done,
  which is rarely true. The author (ex-penetration tester) is concerned about
  people deploying software they have never personally verified.
- He reports being excited but uneasy, and did not expect this to be possible
  so early in 2026.

### Acknowledgements

Thanks to Josef Bacik, Edwin Chen, Bernardo Meurer Costa, Jake Eaton, Dan
Kelley, Felix Klock, Jannet Park, Steve Weis, and others.

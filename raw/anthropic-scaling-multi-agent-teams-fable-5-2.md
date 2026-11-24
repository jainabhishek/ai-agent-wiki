# Safely scaling multi-agent teams with Claude Fable 5.2 — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-11-09
> Captured: 2026-11-24 via curl of the HTML, with tags stripped to text (condensed). Byline: Barry Zhang, Tianyi Peng, Elle Najt, Keller Scholl, and Lance Martin; category "Agents"; 12 min read. JSON-LD `datePublished` is 2026-11-09.
> Capture policy: prose is paraphrased; every number is kept; quotes from the agents' own messages are kept only where under 15 words. Figures 1–6 (diagrams and videos of table activity, the task tree, and helper positions) were not captured; only their captions are summarized.
> Scope: the run used "an early version" of Claude Fable 5.2. The September 2026 formalization it compares against used an internal research model "roughly comparable to" Claude Fable 5.1. No API model ID string appears.

Subtitle: 1,000 agents running a pre-release Fable 5.2 redid a machine-checked Fermat's Last Theorem proof with general-purpose tools, one shared database, and several safety layers.

## Opening

- Baseline (September 2026): Anthropic's first complete Lean formalization of the theorem, produced by dozens of agents on an internal research model roughly comparable to Fable 5.1, on the Prove2Me platform, directed by a researcher.
- In a new toy experiment, 1,000 agents on an early Fable 5.2 reproduced the proof without Prove2Me and without researcher steering. Time: 28.7 hours. One-third as many output tokens. A proof one-seventh the length of the original.
- Each agent: sandbox with no internet; every shell command and file edit passed a classifier before execution; an offline monitor reviewed the team's actions.
- Inputs given: 60 statements, a single-sentence outline of the classical proof strategy, the needed definitions, 47 proved lemmas from the earlier formalization, and lead/helper roles. No other guidance on proof or organization.
- Claim: teams of agents on models like Fable 5.2 can reach ambitious long-horizon goals inside carefully designed safety boundaries.

## Problem

- Fermat's Last Theorem: no positive integers a, b, c satisfy aⁿ + bⁿ = cⁿ for n > 2. Unproven for more than 350 years until Andrew Wiles's 129-page proof in 1995. Formalizing it (every step computer-checkable) is a long-standing goal.
- September formalization: a researcher plus dozens of agents, 11 days, roughly 6 billion output tokens, 13 million lines of Lean (a language where a computer checks each proof step).
- Prove2Me (designed by Tianyi Peng, now at Anthropic, with Columbia University collaborators) keeps a shared graph from each statement to the sub-statements derived from it; any agent could decompose a statement; agents could query which unproved pieces were ready, so they kept track of project state. Each statement and proof lived in its own independently compiling file, letting many agents proceed in parallel with no shared-file edits.

## Harness

Goal: test whether a team on models like Fable 5.2 could do this without Prove2Me or a directing researcher, using general-purpose tools.

### Tools
- 60 statements: the final theorem plus 59 intermediate milestones. For each, write a Lean proof, build and check it with Lean's tools, and submit to the shared Git main branch, where a grader checked it.
- Per agent: a shell and file editor in its own no-network sandbox; Lean toolchain and Mathlib in the sandbox image; its own Git branch plus merge requests into main; shell access to one shared Postgres database.

### Collaboration
- The proof splits well, but agents must coordinate to build on each other and avoid duplication. In the original formalization, early attempts failed because agents lost track of project state and stopped collaborating; Prove2Me fixed that.
- Each agent had a sandbox on its own lightweight VM. One shared machine hit limits at about 100 agents: more than half of 100-agent runs were stopped or restarted for memory, disk, or CPU exhaustion.
- With 1,000 sandboxes, agents shared work through a SQL database. Reasons for SQL: general primitives for organizing information, transactions that handle concurrent writes from 1,000 agents, and Claude's familiarity with it. Agents used it to claim tasks, share notes, and log finished work.
- Fig 1: each sandbox connected out only by a pipe to a gateway, which called the Claude API and relayed Git and SQL requests.

### Prompting
- The prompt listed the 60 statements, each with a one-line informal description, and described the tools.
- Only structure given: a hierarchy of one lead and 999 helpers. Lead told to split the problem and assign parts; helpers told to expect work from the lead and check with it when a task was unclear.
- The harness sent the lead 19 automatic reminders of remaining time, each encouraging it to keep going.

## Safety

No single defense layer suffices to contain an agent team. Combined sandboxing, real-time monitoring, and offline monitoring to keep each agent in its own no-network VM and detect escape attempts or monitoring tampering.

### Sandboxing (Fig 2)
- **Communication:** no dedicated messaging tools; coordination only via the database and Git.
- **Code changes:** push only to own branch and open merge requests; a separate job merged into main, refusing only on conflict or fault (e.g. unrelated history).
- **Database access:** a shared unprivileged role; 5-second limit per SQL statement; writes refused above 256 MiB.
- **Network controls:** no network; the only link out was the pipe to the gateway.
- **Identity:** identity labels were attached by the gateway, outside the sandbox, so agents could not impersonate each other.
- **Kernel:** built without features giving root a direct path into the kernel (loadable modules, kexec, raw memory access, kernel probes); ran in kernel lockdown mode.
- **Least privilege:** commands ran as an unprivileged user; tools like sudo removed; agent tools could not read or change the agent loop running them.

### Real-time monitoring
- A prompted LLM classifier can block each tool call (shell commands, file edits). It watches for sandbox escape, boundary probing, monitoring tampering, and harmful actions the model might take if it got out.
- On a block, the whole team stops and a person must review before restart, so another agent cannot carry out the blocked action.
- Multi-agent side-task and sabotage evaluations: red-team agents used strategies such as decomposition attacks to fool the classifier into allowing an escape. Monitors that saw the agents' chain of thought (CoT) and inter-agent communication detected all sabotage attempts in these evaluations, so Anthropic now uses them for multi-agent runs. In parallel it runs an action-only version (no CoT) to guard against an agent's reasoning persuading the monitor.
- Ongoing improvement through human-guided and automatic red-teaming, evaluation against production transcripts including past incidents, and broader threat modeling.
- In this run only the action-based monitor was used. Run-ending blocks were possible only for the lead; a blocked helper was simply dropped. The parallel CoT monitor was added shortly after.
- Such experiments run on models that may not have completed the pre-release alignment assessment, so monitoring is designed for the possibility of misalignment. Released models complete that assessment first, which reduces but does not remove the risk.
- Across more than a million tool calls, none met the bar for a block. In a replay through the CoT monitor with the current rubric, one call — a root-access check — was the only near-block.

### Offline monitoring
- Analyzes the team's actions against the same threat models, with extra affordances such as looking up other agents' actions.

## Results

### Without Prove2Me, the team built its own coordination system
- Levels of work: the theorem; the 60 statements; smaller statements (lemmas) agents split off; every statement and lemma is a Lean theorem. Each statement started with a proof placeholder and counted as proved only when Lean's checker accepted a finished proof. The lead decided strategy and coordination.
- In the first 10 minutes the lead created five database tables (Fig 3):
  - **Announce** — lead's orders to the whole team.
  - **Assign** — who works on what (owner or deputy per statement).
  - **Notes** — an open board for claims and progress.
  - **Subtasks** — a to-do list; any agent can add, first helper to claim owns it.
  - **Landed** — a log of finished work.

### The lead dealt out the statements
- The lead assigned each statement to a crew of 16–17 helpers (999 rows in assign), made one helper per crew a captain responsible for posting a plan and splitting tasks into subtasks, and told every helper via announce to first judge its statement's difficulty and post a verdict.
- Helpers knew from the prompt that the database existed, found the announce table, and started. About 27 minutes in, three statements were proved; the lead read the verdicts, set aside the 47 statements most helpers judged infeasible within budget, and moved nearly all helpers onto the remaining 10. Crews grew from about 17 to between 46 and 139.
- Helper loop (mostly from the lead's orders): find the plan in notes; claim a subtask; write, check, and submit the Lean proof; mark the task done; post a note.
- About 45 minutes in, with about five of the 10 proved, the lead noted that throughput far exceeded the early infeasibility verdicts. The 10 were done at roughly the 70-minute mark.

### The lead then moved helpers to harder statements
- Declaring "no reason to idle", the lead redeployed helpers onto the shelved statements, continuing to reassign mostly in the first six hours (Fig 4: reads and writes per table; activity stops near hour 18, when the run was restarted from its last save with 12 more hours).
- Helpers took on more responsibility over time, writing tasks themselves: by hour 5.6, 73 helpers had written 756 tasks, only 16 of them captains. Free helpers volunteered for more work.
- Within the first hour the lead's top-down assignment began to loosen; by hour 3 it told free helpers "do not wait for me", letting them pick work across statements while it kept writing assignments.

### The lead assigned the team to Langlands–Tunnell
- By roughly hour 18 the remaining work was Langlands–Tunnell (a classical result Wiles's proof relies on), the statements depending on it, and one other statement proved along the way. Earlier its captain had estimated at least 0.7–1 million lines of Lean and under 1% chance of finishing in time; the lead had set it aside.
- In a last top-down move the lead put about 750 helpers on it, writing "Honest odds are low."
- Compared with any other statement it needed ~9x the tasks and over 2x the new code. Many first tasks were too big for one helper.
- The team organized work as a tree: the captain divided it into 10 areas, each piece a task; a helper finding a piece too big split it into smaller child tasks. The tree reached 2,418 tasks, up to 10 levels deep (Fig 5, hour 20.5 to 28.4). Each piece could assume the pieces beneath it, so hundreds worked in parallel before those were proved. Most tree links were inferred afterward from task labels.
- Langlands–Tunnell was proved at hour 28.4, the final theorem at hour 28.7; the lead announced the theorem was on main and kernel-checked by the official checker.
- Fig 6: helper positions every five minutes; the final tally is 54 of 60, since 5 alternative statements became unnecessary and 1 was removed.

## Conclusions

- Using only Git and a shared database, the agents designed tables for roles and results, formed teams, and built a task tree for the hardest statement, which its own captain had given under a 1% chance.
- This does not remove the need for domain-specific harnesses: Prove2Me may still improve efficiency (faster Lean compiles, search and reuse of human results).
- Human direction can still help at certain points. Agents often abandon hard problems and misestimate how hard they are: helpers judged 47 of 60 statements infeasible, yet the team proved most of them. Human encouragement at such moments can prevent early stopping.
- Safety boundaries gave the confidence to run the experiment: Claude could approach the problem freely with the provided tools, but only inside a no-network sandbox under two separate monitors.
- Expect methods to evolve quickly; safety boundaries must keep pace as such teams take on harder work.

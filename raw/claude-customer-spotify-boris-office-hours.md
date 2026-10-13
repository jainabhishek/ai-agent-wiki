# Office Hours: Asynchronous coding and the end of the IDE with Spotify — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/spotify-boris-office-hours
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Format: transcript from the "Office Hours with Boris Cherny" series. Boris Cherny (creator of Claude Code, Anthropic) interviews Niklas Gustavsson (Chief Architect and VP of Engineering, Spotify). Page intro: 73% of Spotify PRs are now AI-authored; anyone can have a working prototype in an hour or two.

## Background

Gustavsson trained as a molecular biologist, moved into software about 30 years ago, mostly backend distributed systems; at Spotify since 2011.

## First "AGI moment"

- Early LLM attempts (pre-Claude, "early GPT days") at automated code changes struggled; adding LLM judges and other pieces gave inspiring results.
- Personal breakthrough: Opus 4.5 (around November/December of the prior year) — went from smart autocomplete to taking real problems with little prompt engineering.
- Cherny had predicted (around September) nobody would use an IDE by year end; Gustavsson doubted it, then stopped using an IDE two months later. Cherny: the big change was no longer needing last-mile edits in an IDE.

## Current workflow

- Gustavsson runs Claude Code in multiple terminal sessions with background agents: 5–10 tabs, panes for diffs, a matrix of Claude sessions and matching terminals over a set of git worktrees.
- Spotify has a few very large monorepos (moving toward them) plus thousands of small polyrepos; temporary sessions for polyrepos.
- Monorepo worry (indexing issues with prior tools; backend over 20 million lines) proved unfounded. Claude finds "inspiration" from other code in the repo. Required iterating on CLAUDE.md files so Claude understands internal tooling.

## Fleet management and Honk

- 5–6 years ago Spotify found its codebase growing about seven times faster than engineer headcount.
- Fleet management: instead of sending migration tutorials to hundreds of teams to apply by hand across thousands of components (months per migration, about ten a year, top developer complaint), apply mutations across the whole codebase in thousands of repos. Millions of such PRs merged, using deterministic scripts.
- Ceiling: code's huge API surface (e.g., a method called five different ways, aliasing needing state tracking) turned each AST-transformation script into thousands of lines of edge cases.
- Early LLM one-shot attempts failed (weak models, naive approach). Improvements: LLM-as-judge on outputs, problem decomposition, many iterations, consolidated into "Honk". Honk V2 just released (really about the eighth iteration). Started as scheduled code changes across repos; engineers now also invoke it from Slack for general tasks.

## Honk architecture

- Had a judge; removed it once models and harness got good enough. Gustavsson recalls the judge moved PR success from roughly 20–30% to 80% in early iterations.
- Claude Agent SDK running in a Kubernetes pod with tools. Before V2: a predefined allowlist of trusted tools. Now users can add their own tools, so the agent can use any internal tool.
- Key tool: run verification (CI builds) on Linux and macOS; macOS matters for iOS builds.
- Also integrates the iOS simulator with Claude, e.g., Figma designs to UI implementations, used to port TV apps from iOS apps.
- Cherny: for closed-loop agent work without a human, verification is the single most important thing; a common mistake is under-investing in the verification loop.

## Test automation and ownership

- Spotify has thousands of components, each owned by one team that designs, builds, and operates it. Teams used to see every PR, which allowed sloppier tests.
- Fleet management changed expectations: most automated changes auto-merge without the owning team seeing the PR, so test automation had to get much stronger. That same verification now lets them point agents at the code. Still investing.
- Cherny: speed versus quality is a false dichotomy; encode quality practices in a skill, CLAUDE.md, or instructions so Claude can apply them.
- Gustavsson: quality metrics held neutral while speed rose significantly, but it is not free; reliability practices also need continued investment. About 4,500 production deployments per day.
- Idea-to-production time went from weeks or months to about an hour; agents are part of that loop.

## Measuring ROI

- 2,900 engineers. 75%+ improvement in PR frequency attributed to AI tooling; 73% of PRs AI-authored.
- Working to link PRs and deployments to planned work items, then to A/B tests and rollouts, to attribute user value and revenue. Expectations on ROI precision are rising as costs fall; Cherny notes the need to attribute tokens and hours to output.

## Advice for leaders

Invest in foundations: test automation, verification, and standardization (consistent codebases, tools, frameworks). Originally for humans, it transfers to agents: if code looks ten different ways, Claude is more confused. Gustavsson: same engineering practices apply; there is "a new actor in your code base".

## Advice for engineers

Gustavsson feared losing the problem-solving part; with five background agents he finds he enjoys solving problems regardless of method, solves problems he could not before, and enters unfamiliar codebases fast. Cherny: time shifted from implementation to deciding what is next, talking to customers, and prototyping.

## Prototyping for everyone

Spotify built infrastructure for end-to-end prototypes in its mobile apps and backend, plus an internal app store for prototypes. Anyone (including co-CEOs and senior execs) can build a working prototype with real data in an hour or two, testing an idea in a day instead of weeks or months.

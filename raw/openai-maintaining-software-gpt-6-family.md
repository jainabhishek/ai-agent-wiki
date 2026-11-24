# Maintaining software with the GPT-6 family — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/maintaining-software-with-the-gpt-6-family
> Publisher: OpenAI (Developers blog) · Date: 2026-10-14
> Author: Rodrigo Roim (byline in the HTML page), OpenAI Core Experimentation team
> Captured: 2026-11-24 via curl of developers.openai.com/blog/llms-full.txt (markdown export); the author byline comes from the HTML page. Condensed and paraphrased; the example prompts are paraphrased, not quoted.

## (Intro)

- Growing codebases need maintenance: removal of unused code, cleanup of finished experiments, and test fixes. At OpenAI, coding agents sped up building, which also raised the maintenance load.
- The author works on the Core Experimentation team, which builds the software behind experiments across the company, from front-end changes to model-serving efficiency.
- GPT-6 Astra sped up building and maintenance; GPT-6.1 Sol gave similar results at lower cost. The post covers finding cleanup opportunities, gathering evidence, and preparing changes for review.

## Removing unused code

- Before agentic coding, teams relied on complex static analysis tied to runtime logging. Mistaken removals still caused incidents. Edge cases include reflection that defeats static analysis, and code paths that look unused but exist to mitigate future incidents.
- With GPT-5.6 Sol in Codex, the author gave an area to investigate plus clear validation criteria; the model wrote static analysis and removed dead code. These targeted prompts were easier to build and maintain than the old static analysis systems, with similar reliability.
- With GPT-6 Astra, the team tried a broad request where the model chooses where to look and what evidence justifies each removal. The first prompt was short and informal (typos included) and was too ambiguous for GPT-5.6 Sol to handle fully. Paraphrase: find and clean up dead code in the repo, and check Slack, Statsig (the feature-flag and experimentation platform the team uses), or any other source to confirm that code is unused.
- Astra handled the ambiguity: it read past PRs, Slack threads, and internal project trackers, and it read production performance-profiling tables to confirm deleted lines were never reached. It explained its rationale for each deletion, which sped up reviews.
- Scale: five engineers ran variations of the prompt across repositories and merged more than 1,400 pull requests, deleting over 800k lines of code. Most of this was part-time over two weeks. Code reviews went out to the teams with context on each project.
- Results: one service's container image went from 3.31GB to 1.72GB (48% smaller); another set of cleanups removed about 400 visual snapshot variants from the test suite.

## Tracking down stale experiments

- Stale experiments are harder than dead code: their code can still run in production or depend on eligibility checks that can change at any time, so static analysis is harder.
- Earlier method: deterministic static analysis plus database queries, with the most capable model then available (GPT-5.6 Sol) used to build and improve the scripts. The team knew this missed many truly stale experiments (false negatives).
- After brainstorming with Astra, the author had it draft a brief prompt for a fresh thread. Paraphrase of that prompt: find and remove substantial dead code tied to stale, constant Statsig gates or configs, or abandoned experiments, in two named projects; verify the live Statsig configuration; check git history and overlapping PRs; preserve production behavior, operational safeguards, and gates or configs that act as killswitches; ignore SDK fallbacks and local overrides; open one small draft PR per cleanup, with the Statsig console link in the summary.
- Astra followed the safeguards and produced changes with reviewable evidence. The author commented on the PRs, then asked Astra to read the comments, fold in the feedback, and write a new prompt to scan the whole codebase, including help with prioritization.
- Paraphrase of the Astra-written whole-repo prompt, which starts with `/goal`: locate all removable Statsig objects (gates, configs, experiments, layers) that are stale, constant, abandoned, or fully rolled out, where removal changes nothing in production; audit all Statsig projects and inventories, not only objects labeled stale; find indirect uses through enums, constants, wrappers, aliases, schemas, dynamically built names, and cross-service consumers; reconcile every constant referenced in production and do not stop at a conservative shortlist; consider each object's cloud resource use, including CPU, using production telemetry and profiles; (detailed Astra-written instructions omitted in the post on verifying production behavior, prioritizing older objects, preserving intentional safeguards, and reading SDK fallbacks); produce a markdown report that groups verified candidates into parallel ownership/file workstreams, with production values, evidence, owners, callsites, and evaluation or CPU costs; do not modify live configurations or services.
- Result: Astra used the team's instrumentation to estimate CPU cost per stale experiment. The top results were large efficiency wins from experiments nobody had flagged as stale for years. The author validated the larger results by hand, then ran the full cleanup, which removed hundreds of experiments and feature flags.
- Judgment example: years earlier, an engineer had created a Statsig feature flag that let internal developers override all other new-feature flags for testing. It was one line of Python that mapped the flag to all features, among hundreds of similar mappings. Astra found that the line caused large CPU fan-out and measured the cost. Because the flag was marked "Permanent" in the flag console and could still serve an operational purpose, Astra raised it for human review instead of removing it. A human review followed, the team deleted it, and the estimate is a 0.42% CPU saving for the service most affected.

## Improving cost effectiveness with GPT-6.1 Sol

- The team tested GPT-6.1 Sol on the same workflows to see if it could match Astra more efficiently.
- Setup: the same stale-experiment prompt, run with different model/effort combinations on specific subdirectories of one repository: 6,000+ files and 1M+ lines (Python, TypeScript, Go, Rust). The author reviewed and validated the findings.
- Results (chart, standard API pricing, including research subagents and the follow-up turns Codex ran on its own toward each goal):

| Model / effort | API cost | Findings | Cost per finding |
|---|---|---|---|
| GPT-6 Astra Ultra | $109.06 | 142 | $0.77 |
| GPT-6.1 Sol Ultra | $15.12 | 131 | $0.12 |
| GPT-6.1 Sol Medium | $5.27 | 86 | $0.06 |

- At Ultra, GPT-6.1 Sol reached 92% of GPT-6 Astra Ultra's findings for 14% of its API spend. GPT-6.1 Sol Medium gave fewer accepted findings at lower cost.
- Discrepancy review: most Ultra-vs-Ultra differences were constant feature flags used as dependencies of other feature flags. Astra found them; GPT-6.1 Sol missed them.
- Finding such error patterns lets the team write prompts that correct for them, so the cheaper model gets closer to the expensive one. Future models can make these corrections obsolete, so the author says to revisit prompts at each model release.

## Other ideas to try

- The author suggests starting these with GPT-6.1 Sol Medium and raising effort for broader audits if results look promising. Three short prompts (paraphrased):
  - Fixing flaky tests (`/goal`): scan recent CI runs for flaky tests; for each, try a fix and open a PR if it works; aim for clear fixes to simple issues, not every flaky test.
  - Improving agentic context: look through recent Codex sessions for one `AGENTS.md` instruction that misdirected an agent or caused unnecessary work; take the original session prompt and replay it twice from the same repository snapshot and model, one run keeps the instruction as is, the other drops or corrects just that instruction; then weigh the two runs on quality, behavior, tool calls, tokens, runtime, and cost, and report the instruction plus a verdict on the change.
  - Reducing CI cost and runtime: ask for ideas to relieve CI load, in a table ranked by estimated CI minutes saved per day, based on the repo's CI run history.
- The CI prompt led to about 30 CI optimization PRs. Median CI completion time fell from about 10 minutes to 4.5 minutes; the 90th percentile fell from 12.5 to 6 minutes. A later fix added a missing mock and cut a 63-test resolver suite from 592.6 seconds to 29.8 seconds (95% less), keeping all 63 tests.

## Start small, review, and expand

- The team has merged more than 1,400 maintenance PRs that started from GPT-6 proposals: faster tests, smaller images, lower CPU use, and more.
- Some proposals added more complexity than their expected benefit justified, so prioritization and measurement stayed part of the workflow.
- In large codebases the number of optimizations GPT-6 models find can overwhelm a team; instrumentation plus the prompt techniques above helped Codex prioritize.
- Recommended path: start with one small maintenance task (unused code, a stale flag, or a flaky test). Have Codex locate one case, collect the evidence, and open a small draft PR. Compare models and efforts on that task, since a cheaper configuration may be enough. Then scale to a subdirectory or a well-scoped project, asking Codex at each step to fold your review feedback into the next prompt. Expand to the whole codebase once confident.
- Closing note: the Core Experimentation team is hiring.

# How OpenAI uses Codex — OpenAI (raw capture)

> Source: https://openai.com/business/guides-and-resources/how-openai-uses-codex/ (listed on https://openai.com/business/learn/)
> Publisher: OpenAI (Guides) · Date: 2026-01-14 (page byline "January 14, 2026")
> Captured: 2026-10-12 via built-in browser (get_page_text + DOM extraction of hidden anecdote tabs) (condensed).
> HTML page, no PDF link. HTML title: "How OpenAI Uses Codex to Accelerate Engineering". The page still says Codex is "in research preview" and describes Ask mode / Code mode, which suggests the content predates the January 2026 byline (likely written for the 2025 Codex cloud launch); recorded as an observation, not stated on the page.

Note: paraphrased. Engineer anecdotes are summarized; only short phrases kept.

## Introduction

- Codex is used daily by OpenAI teams including Security, Product Engineering, Frontend, API, Infrastructure, Performance Engineering.
- Content draws on interviews with OpenAI engineers and internal usage data (no usage numbers given).

## Use case 1: Code understanding

- Onboarding, debugging, incident investigation: locate a feature's core logic, map service/module relationships, trace data flow, surface architecture patterns and missing docs.
- Incident response: surface component interactions and how failure states propagate.
- Anecdote tabs (Retrieval systems, API platform, Infrastructure services): after fixing a bug, use Ask mode to find where the same issue appears elsewhere; on-call engineers paste a stack trace and ask where the auth flow lives; Terraform/Python "where would I do this?" questions answered faster than grep.
- Sample prompts: where is auth logic implemented; summarize request flow from entrypoint to response; which modules interact with module X and how failures are handled.

## Use case 2: Refactoring and migrations

- Multi-file/multi-package changes: API updates, pattern changes, dependency migrations — especially across dozens of files or where structure awareness beats regex/find-and-replace. Also cleanup: split oversized modules, modernize patterns, prepare for testability.
- Anecdotes (ChatGPT web, ChatGPT Enterprise): Codex replaced every legacy `getUserById()` with a new service pattern and opened the PR, minutes vs. hours; to clear launch blockers, Codex finds every instance of an old pattern, summarizes impact in Markdown, then opens fix PRs.
- Sample prompts: split a file into modules by concern and generate tests per module; convert callback-based DB access to async/await.

## Use case 3: Performance optimization

- Analyze slow or memory-heavy paths (inefficient loops, redundant ops, costly queries) and suggest alternatives; flag risky or deprecated patterns still in use to cut tech debt and prevent regressions.
- Anecdotes (API Reliability, Model Serving): scan for repeated expensive DB calls, flag hot paths, draft batched queries; "save 30 minutes of work by spending 5 minutes on a prompt".
- Sample prompts: optimize a loop for memory and explain; find repeated expensive operations in a handler and suggest caching; batch DB queries faster.

## Use case 4: Improving test coverage

- Suggest edge-case and failure-path tests during bug fixes/refactors; generate unit/integration tests from signature and surrounding logic; good at boundary conditions (empty inputs, max length, unusual valid states).
- Anecdotes (ChatGPT Desktop, Payments & Billing): point Codex at low-coverage modules overnight and get runnable unit-test PRs; when switching monorepo branches is painful, have Codex write tests and kick off CI while continuing on one's own branch.
- Sample prompts: unit tests incl. edge cases; property-based test for a sort utility; extend a test file for null inputs and invalid states. (The page mislabels this prompt block as "performance optimization".)

## Use case 5: Increasing development velocity

- Start of cycle: scaffold folders, modules, API stubs. End of cycle: triage bugs, fill last-mile gaps, generate rollout scripts, telemetry hooks, config files. Turn pasted user feedback/specs into rough starter code.
- Anecdotes (ChatGPT Enterprise, Internal Tools): an engineer in meetings all day still merged 4 PRs from background Codex work; Codex shipped 3–4 low-priority fixes that would otherwise have stayed in the backlog.
- Sample prompts: scaffold `POST /events` route with validation and logging; telemetry hook for an onboarding flow from a template; stub from a spec.

## Use case 6: Staying in flow

- Fragmented schedules: capture unfinished work, turn notes into prototypes, spin off exploratory tasks to revisit; pause/resume without losing context (on call, many meetings).
- Anecdotes (ChatGPT API, Infrastructure Observability): fire a Codex task for a drive-by fix instead of switching branches, review the PR later; forward Slack threads, Datadog traces, and issues to Codex to stay on priority work.
- (The sample-prompt list for this section is empty on the page.)

## Use case 7: Exploration and ideation

- Alternative solutions, validating design decisions, pressure-testing assumptions; find related bugs by locating patterns similar to a known issue or deprecated method.
- Anecdotes (ChatGPT Desktop, Retrieval systems): paste a spec and docs to solve the cold-start problem; after a fix, ask where similar bugs might lurk and spin follow-up tasks.
- Sample prompts: how would this work event-driven instead of request/response; find modules building SQL strings by hand instead of using the query builder; rewrite in a functional style without mutation.

## Best practices

- **Start with Ask Mode:** for large changes, get an implementation plan in Ask mode, then feed it to Code mode. Codex works best on well-scoped tasks of about **one hour** of human work or **a few hundred lines** of code; expect the size to grow as models improve.
- **Iteratively improve Codex's development environment:** a startup script, environment variables, and internet access "significantly" reduce the error rate; fix build errors in the environment configuration over a few iterations.
- **Structure the prompt like a GitHub issue:** file paths, component names, diffs, doc snippets; patterns like "Implement this the same way it's done in [module X]".
- **Use the Codex task queue as a lightweight backlog:** fire off tangential ideas, partial work, incidental fixes; no need for a full PR in one go.
- **Use AGENTS.md for persistent context:** naming conventions, business logic, known quirks, dependencies Codex cannot infer from code.
- **Leverage "Best of N":** generate several responses for one task in parallel and pick the best, or combine parts of several for complex tasks.

## Looking ahead

Codex is "still in research preview"; OpenAI says it already speeds work and lets teams take on work that would otherwise not be prioritized, and expects deeper integration as models improve.

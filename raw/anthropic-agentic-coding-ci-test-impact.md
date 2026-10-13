# Agentic coding is straining CI. Here's how we scaled test impact analysis at Anthropic — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/agentic-coding-is-straining-ci-heres-how-we-scaled-test-impact-analysis-at-anthropic
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-14
> Captured: 2026-10-12 via curl (HTML downloaded, text extracted locally; condensed).

Byline: Sachin Malhotra. Category: Best practices, Perspectives. Products named:
Claude Code, Claude Enterprise, Claude Tag. Reading time 10 min. Subtitle: CI job
volume rose 25x in 6 months; the test selection service was patched three times
before a sustainable fix.

## AI is evolving CI

- Anthropic engineers on average ship 8x as much code per quarter as in
  2021-2025. Claude authors 80% of that code and also plays a large role in
  reviewing and approving PRs.
- Once code writing and PR review speed up, CI takes the pressure. Tests across
  the codebase grew 10x with only a nominal increase in engineers. Result: a 25x
  increase in CI jobs over six months (not every test runs on every PR).
- This threatened to overload the test impact analysis (TIA) service several
  times. Three quick fixes lasted 70 days, 29 days, and less than one day.
- Author's prediction: horizontally scaled test selection architecture will
  become industry standard as agent-heavy teams create more PRs and more tests.
- The lesson is "always plan for the exponential". The techniques themselves
  (bigger machines, parallelizing, restarts) are common; the point is that each
  buys a fraction of the time it bought a year ago, while a full redesign also
  costs a fraction of the time it used to, because writing code is no longer the
  bottleneck.

## The test impact analysis architecture

- Many organizations still run every test on every change. That stops scaling:
  CI gates get long, expensive, and untrustworthy.
- Humans can tell which failures do not apply to them; agents need more context.
  A specific set of valid tests lets agents self-verify and iterate better.
- Anthropic's service is deterministic: it picks the tests for each change from
  past performance and package relevance. Two components must stay in sync:
  - a **listener** that records test results from every CI run;
  - a **selector** that reads result history and picks tests for each open PR.
- With several CI jobs per second, the listener falls behind the PR queue.
  Example: 20 minutes of listener lag can mean tens of thousands of test updates
  not yet applied to the selector. Effects:
  - a bad merged change makes a test fail for everyone, causing needless
    investigations;
  - a flaking dependency produces flaky reds that block merges;
  - a fixed or new test does not run until the listener catches up (regression
    risk).
- v0 ran as a single process, because a running per-test history needed a single
  writer. That design blocked horizontal sharding.

## The bumpy road to redesign

Strain began by October of the previous year (2025); on-call was paged two days
in a row.

### Patch 1: A bigger machine
- Doubled the cores. Known to be temporary. Ownership was unclear: nobody wanted
  another piece of infrastructure, and the CI team had other priorities.

### Patch 2: Sharding
- Frequent pages from listener lag. The author ran a long-running session in an
  internal version of Claude Tag dedicated to monitoring the service: when lag
  exceeded 50,000 jobs, Claude pinged him and resumed the conversation on next
  steps. This ran for months; persistent context meant no re-explaining past
  efforts. Claude often argued for an overhaul; the team usually chose another
  patch.
- February: the listener did not need one global writer, only one writer per
  package. Claude generated the code to split each package's state into a shard
  with its own worker. It bought 29 days.

### Patch 3: Daily restarts
- March: the process hit its memory limit by mid-afternoon most weekdays.
  Quick-fix attempts: found only four bugs; swapping the memory allocator (aimed
  at garbage collection) did nothing; memory-profiling a heavily loaded singleton
  was judged too risky; restarts bought less than a day.
- Daily restarts made the service fall further behind. When behind by more than
  an hour (several times), many job results were never recorded. CI still ran
  and no untested code shipped; the selector used stale data, which mostly meant
  running already-flaky or widely failing tests.

### The redesign
- Took Claude's advice: gave the service a database — specifically an in-memory
  data store — offloading the singleton's in-memory processing.
- Any listener worker can process any result, append it to a journal in the
  store, and move on holding no state: stateless, so horizontally scalable.
- A small separate consumer rolls the journal into per-test history every few
  seconds; the selector looks up history quickly.
- Costs more to run, but easier to scale and memory-profile than the singleton.
- One engineer, three weeks. The author estimates it would have been closer to a
  quarter a year earlier.
- Chart described: hourly max of queued unprocessed job-result events — before,
  a backlog built most days and grew week over week; after cutover and tuning,
  flat.
- Claude did the fine tuning (journal size, worker count) largely autonomously.
  Stable since.

## What I would do differently

- Account for the AI exponential: CI jobs grow exponentially as agents per
  engineer rise and accelerated PR approval matures.
- Claude prefers smaller, more granular PRs — more CI jobs per day (and another
  reason not to run every test on every PR). Agents push overnight and at
  weekends, raising the activity floor; load stays bursty because humans still
  drive and approve many PRs.
- Advice: build or buy, assume a 25x load within two quarters. The bar for
  "over-engineering" is moving up; v0 designs can plan for 10-20x perceived scale
  if budget allows.
- Instrument services to act as Claude's "eyes and ears" so it can hill-climb
  and fix problems incrementally. In particular, check that CI jobs in equals CI
  jobs out.
- Keep state out of the process from the start. Avoid running any critical
  service as a single instance unless you can measure it and any canary changes.

## Additional CI resources
- Links a companion post on accelerating CI on-call with Claude Tag (beta).

# Custom Code Review rules for Codex — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/custom-code-review-rules-for-codex
> Publisher: OpenAI (Developers blog) · Date: 2026-07-20 · Author: Hari Srikanth
> Captured: 2026-10-12 via curl (condensed). Body text taken from the developers blog llms-full Markdown export; byline date, author, and subtitle taken from a curl of the live page HTML ("Jul 20, 2026"); figures spot-checked against the live page.

## Intro

- Some review comments recur: preserving an old API contract, keeping customer data out of logs, avoiding a rename that breaks another service. This context often lives with a few reviewers.
- Codex Code Review can now read custom repository rules in `AGENTS.md`, catch such issues, and point the author to the rule behind a finding. The same `AGENTS.md` that guides coding tasks can guide reviews. Most useful when people or agents work in unfamiliar parts of a repository.

## Shipping more code

- Coding agents take on larger, longer-horizon changes. At OpenAI, weekly PR volume more than doubled since Q4 (chart only: weekly PR volume rising across three quarters); customers report similar trends.
- More PRs means review becomes the bottleneck. A reasonable-looking diff can break an older client or cross an unknown boundary.

## The review bottleneck

- With more PRs, reviewers have less time to gather context; once the author moves on, even small revisions take longer.
- Some issues are invisible in the diff: renaming a response field looks like cleanup but breaks clients on the old contract. A veteran remembers; a newcomer or an agent does not.

## Rules as an interface

- The repository-rules interface: concise, scoped review guidance in `AGENTS.md`. Code Review applies the rules relevant to a change and cites them in the finding.
- More steerable models mean a short, well-scoped instruction can focus a long review. The Codex repo keeps its own Code Review rules in `AGENTS.md` (topics include model-visible context and breaking changes).
- Worked example: the Codex app-server emits an experimental notification `rawResponseItem/completed`, which Codex Cloud already consumes. The repo's breaking-change rule names `rawResponseItem/*` as an integration surface to preserve even while experimental. The wire name is defined in `codex-rs/app-server-protocol/src/protocol/common.rs`.
- Hypothetical one-line diff: `RawResponseItemCompleted => "rawResponseItem/completed"` changed to `"rawResponseItem/done"`. It compiles, but listeners stop receiving the event.
- Rule excerpt structure: heading `## Code Review Rules` → `### Breaking changes` → an instruction to search external integration surfaces for breaking changes, listing raw response item events (`rawResponseItem/*`) even while experimental.
- Sample finding (paraphrased): keep the existing notification name because Codex Cloud listens for it; either keep the name or add a backward-compatible event, per `AGENTS.md`.
- The Codex team added this rule specifically to protect Codex Cloud consumers (openai/codex PR #29086).
- Placement: repository-wide rules at the root `AGENTS.md`; service-specific rules in the relevant directory. Code Review applies guidance covering the changed files; unrelated changes do not pull in app-server context.
- Rules complement tests and linters: deterministic checks belong in tests/linters; rules capture judgment that is hard to encode. Good first targets: compatibility requirements and data boundaries.

## Writing rules that hold up

- Eval suite with known rule violations and safe counterexamples. Primary suite: rule-guided variants recovered 98% of required custom findings vs 58.3% for the baseline control.
- Also tested competing rules, busy PRs, consequential violations, and changes that should be left alone. Four evaluation questions:
  - Coverage — are intended violations found when diffs are busy and rules compete?
  - Restraint — do clean changes and valid exceptions avoid unnecessary findings?
  - Retention — does Code Review still catch ordinary bugs outside the rules?
  - Actionability — does each finding name the guidance, location, and priority?
- Tried several guidance styles (short bullet lists to team-owned sections). Same pattern internally: Codex finds and cites local guidance a default review would miss, but broad instructions create noise. Small, scoped rule sets with an explicit safe path worked best.
- Guidance (paraphrased):
  - Start with a consequential, non-obvious invariant reviewers keep explaining (compatibility, data boundary). If removing a rule would not change the review, omit it.
  - Scope rules to the code they govern: root for repo-wide, nested `AGENTS.md` for a service. Narrow scope reduces competition for attention and clarifies ownership.
  - State the invariant and the safe path (the alternative the author should take).
  - Keep rules durable and current: describe outcomes, not function names that may change; review rule updates; narrow or delete rules that keep producing noise.
  - Keep formatting and mechanical checks in CI; use rules for questions a reviewer would otherwise re-ask.

## Getting started

- If Code Review is enabled: add two or three rules to the applicable `AGENTS.md` and open a representative PR. Otherwise see the Code Review quickstart (`/codex/third-party/github`). Request a review with `@codex review`.
- Test each rule with three changes: one that should trigger it (expect a useful finding), one safe counterexample, and one unrelated change (both should produce no noise); refine from results.
- Code Review is an additional reviewer; tests, branch protections, and required approvals remain the hard enforcement.

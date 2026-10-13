---
title: Boundary Contracts
type: concept
created: 2026-07-17
updated: 2026-10-12
tags: [implementation, testing, integration, boundaries, process, evals]
---

# Boundary Contracts

> No instruction set produces bug-free code. The solvable problem is narrower and
> achievable: make known *classes* of bug structurally impossible to merge, make
> unknown classes loud and cheap to diagnose, and ratchet every escape into a new
> gate. This page is about the bug class that ordinary testing cannot catch —
> and the process that can.

## Two kinds of implementation bug

Every implementation bug is one of two kinds, and they have fundamentally
different defenses:

- **Logic bugs** — wrong code given correct assumptions. The implementer's model
  of the world is right; the code doesn't match it. Tests, types, and review
  catch these, because a correct mental model lets you write a test that
  distinguishes right from wrong output.
- **Boundary bugs** — correct code given a wrong model of an external system (an
  API, MCP server, DB schema, file format, another service). The code faithfully
  implements a world that does not exist.

The crucial asymmetry: **boundary bugs cannot be caught by any artifact the
implementer produces.** Tests, fixtures, and mocks written by the same mind
inherit the same wrong assumptions. The test passes because it encodes the same
fantasy the code does. Only reality — or a recording of it — can falsify a
world-model.

This matters more for LLM implementers than human ones. A human hitting an
unfamiliar API is *forced* to stop and look it up; an LLM will fluently invent a
plausible-but-wrong contract from memory and never signal that it guessed.
Boundary bugs are therefore the dominant failure mode of agent-built integration
code, and diligence instructions ("be careful with external APIs") do not fix
them — diligence competes with everything else in context and degrades exactly
when the task is hard.

## Case study: the Robinhood read proxy (2026-07-17)

A constrained multi-account read proxy over the Robinhood MCP connector shipped
with a **passing test suite and 8 of 11 live operations broken.** An acceptance
run against the real connector exposed it after merge.

Every failure was a boundary bug — a wrong model of the upstream API:

- Argument-shape mismatches on 7 operations: sending a `limit` param the upstream
  didn't define; omitting a required `account_number`; calling the option-chain
  tool with `symbol` when the real param was `underlying_symbol`; inventing a
  date-range interface where the upstream only accepted preset spans.
- Response-shape mismatches on 2 operations: the quotes normalizer read the
  wrapper object's top level and never unwrapped the nested `quote`; the
  fundamentals normalizer expected metric/value rows and got direct fields.

Three compounding process failures turned a set of catchable mistakes into a
shipped, misdiagnosed outage:

1. **The fixtures encoded the same wrong model as the code.** A test literally
   asserted `args["limit"]` for a tool that has no `limit` param. The fixture
   wasn't lazy — it was the wrong assumption, faithfully reproduced. This is why
   "all tests pass" was worthless here.
2. **A catch-all exception classifier hid the cause.** Every upstream error that
   wasn't a 401/429/timeout was remapped to `UPSTREAM_UNAVAILABLE: Robinhood MCP
   is unavailable`. So "your arguments are invalid" presented as "the upstream is
   down" — even though successful calls were interleaved seconds apart. An entire
   diagnostic cycle was spent chasing a phantom outage.
3. **The most dangerous failure was silent success.** The fundamentals normalizer
   dropped every field except `symbol` — and since `symbol` was the only
   *required* field, the row passed validation. Hollow-but-green evidence is worse
   than a hard failure in a pipeline where those rows feed recommendations.

None of this was caught by review of the diff, because **the bugs lived outside
the diff** — in the gap between the code and a world it never checked against.

## The process rules

The reframing: don't chase "no bugs." Chase *nothing ships broken for a knowable
reason, escapes are loud not silent, and each escape permanently shrinks the
space.* That is the only achievable version of "bug-free," and these five rules
implement it.

### 1. Ground truth before code — a gate, not advice

Any task touching an external boundary *begins* by recording reality into the
repo:

- The schema dump — `tools/list` with every `inputSchema`, the OpenAPI spec, the
  DDL — as a checked-in artifact.
- One sample response per endpoint. Market/public data as-is; account-scoped
  responses shape-preserved with values redacted.

Implementation is *derived from* that artifact and tested *against* it. No
recorded contract exists yet? Capturing one IS the first deliverable. Can't reach
the boundary (no credentials in the implementer's environment)? **The task is
blocked on a human probe** — the implementer must never invent the contract. One
30-second capture call before writing the integration would have prevented all
seven Robinhood argument bugs.

The reviewable question becomes mechanical: *"where is the recorded contract this
code conforms to?"* No artifact → no merge.

### 2. Verification independent of the implementer's world-model

"My tests pass" is circular when the same mind wrote the code and the tests.
Definition of done for boundary work must include a check the implementer
*could not have biased*:

- **Conformance:** validate every call the code can emit against the recorded
  `inputSchema` (exploit `additionalProperties: false` — unknown/missing params
  fail instantly, offline). Make fixture backends validate incoming arguments
  against the same recorded schemas, so fixtures can't drift into fantasy. Run
  normalizers over the recorded sample responses, asserting substantive fields
  survive.
- **Live smoke:** exercise each operation once against the real dependency,
  asserting status plus non-empty substance.

Run this *before* merge. The Robinhood incident's acceptance run was exactly the
right check — the only failure was that it ran *after* the branch landed. Same
work, moved earlier, and the bug never ships.

### 3. Fail loud — prevent masquerade, not bugs

You can't prevent every bug, but you can stop bugs from *disguising themselves*:

- No catch-all exception classifiers. Unknown errors propagate with their cause
  attached; an invalid-params protocol error gets its own code, never a generic
  "unavailable."
- No silent defaults on missing data.
- Normalizers and parsers fail on empty substance: a row that retains only
  identity/required fields is an error, not a success.

These rules don't reduce the bug count; they convert expensive misdiagnosis into
cheap, obvious failure.

### 4. Review assumptions, not just diffs

Boundary bugs are invisible to diff review because they live outside the change.
Add one question to every review and every delegated-work handback: *"List the
external assumptions this change makes. For each, what artifact pins it?"* An
assumption with no pin is the finding.

### 5. The ratchet — the only part that converges

You cannot enumerate future bug classes in advance, so no static rule set is ever
complete. The only process that *converges on your actual failure modes*: every
escaped bug triggers a retro asking "which layer should have caught this, and
what mechanical change makes this *class* unrepeatable?" Add that mechanism plus
at most one line of standing instruction. This is [[agent-evals]]' "build from
real failures," applied to process itself. N incidents later, your gates encode
*your* domain's failure modes, not generic best practice.

## The meta-principle

**Whenever an instruction can become a mechanical check, convert it.**
Instructions decay under context pressure — they compete for attention and lose
it precisely when the task is hard. CI gates, required artifacts, and
schema-conformance tests don't decay. Reserve prose instructions for what cannot
yet be mechanized; move everything else into gates.

This is the concrete, boundary-specific complement to [[agent-instructions]]
("ambiguity is the enemy") and [[agent-design-principles]] ("measure before you
optimize"): the ambiguity that hurts most is ambiguity about the *external world*,
and the measurement that matters most is measurement against *reality you
recorded*, not fixtures you imagined.

## Industry parallels

Vendor sources describe the same rules from other directions. Each bullet names
the rule above that it supports.

- **A certificate that machines check (rule 2).** Anthropic's modernization
  guidance makes a "certificate" the second of six steps: a set of conditions,
  each checkable without a human, that every agent change must meet. Examples
  are original and new tests, coverage thresholds, differential output checks,
  round-trips of state and wire formats, and adversarial reviews in fresh
  context windows. For cross-stack rewrites, traffic replay and differential
  testing replace old tests that do not run on the new stack (see
  [[anthropic-ai-code-modernization]]).
- **The verified artifact is the executed artifact (rule 2 and the
  meta-principle).** Datadog reports that its Temper agents emit specifications,
  not application code. A deterministic kernel verifies each spec in four
  layers and then runs exactly that spec, so the verified and running artifacts
  cannot drift. Proof stays outside the LLM, the way a compiler checks Rust code
  (see [[anthropic-datadog-universal-machine-tool]]).
- **Machine-discoverable contracts (rule 1).** Each Temper capability also has a
  machine-parseable data contract that an agent can read without docs (see
  [[anthropic-datadog-universal-machine-tool]], [[tool-design]]).
- **A deterministic layer at the number boundary.** Kepler reports that Claude
  plans, while deterministic engines retrieve and compute every number, and each
  figure traces to a filing line item (see [[anthropic-kepler-verifiable-ai]]).
- **Silent tool failure (rules 2 and 3).** Twilio reports that its MCP server
  failed from day one: Claude Code spawned the process, got EOF, and continued
  without the tools, with no error or warning, for 35 days or sessions (the post uses both terms). The fix was 53
  lines of TypeScript. A live smoke against the real server would have shown
  the failure on the first day (see [[claude-customer-twilio]],
  [[model-context-protocol]]).
- **A rename that compiles but breaks consumers (rule 4).** OpenAI's worked
  example renames the experimental notification `rawResponseItem/completed`.
  The change compiles but breaks Codex Cloud listeners, so the bug lives
  outside the diff. A breaking-change rule in the Codex repo's `AGENTS.md`,
  added to protect Codex Cloud consumers, catches it in review (see
  [[openai-codex-code-review-rules]]).

## Relation to other concepts

- [[tool-design]] — tools are the agent's boundary to the world; this page is
  what it takes to build them *against the real interface* rather than an assumed
  one. "Evaluate with the agent in the loop" has a prerequisite: evaluate against
  the real contract, in the loop.
- [[agent-evals]] — evals catch behavioral regressions; boundary contracts catch
  the integration bugs that evals built on the same mocks would miss. Both draw
  from real failures.
- [[guardrails]] — fail-loud is a guardrail against silent-success and
  misdiagnosis, layered at the integration boundary.
- [[agent-instructions]], [[agent-design-principles]] — the general principles
  this page makes mechanical for external-boundary work.

## Related concepts

- [[tool-design]], [[agent-evals]], [[guardrails]], [[agent-instructions]],
  [[agent-design-principles]], [[model-context-protocol]]

## Appears in

- [[anthropic-ai-code-modernization]]
- [[anthropic-datadog-universal-machine-tool]]
- [[anthropic-kepler-verifiable-ai]]
- [[claude-customer-twilio]]
- [[openai-codex-code-review-rules]]

## Contradictions / open questions

- The ground-truth-before-code gate assumes the boundary is reachable for
  recording (directly or via a human probe). For boundaries that are expensive,
  rate-limited, or only reachable in production, the open question is how to
  capture a faithful-enough contract cheaply — contract tests published by the
  provider, recorded production traffic, and consumer-driven contracts are
  partial answers not yet evaluated here.
- **Prose rule or mechanical check?** This page's meta-principle says to convert
  instructions into mechanical checks. OpenAI catches the wire-name rename with
  a prose rule that an LLM reviewer reads: rule-guided review recovered 98% of
  required custom findings against 58.3% for the baseline, on a suite of
  undisclosed size ([[openai-codex-code-review-rules]], 2026-07-20). OpenAI
  itself keeps tests, branch protection, and required approvals as the hard
  gate, and uses rules for judgement and CI for mechanics. A recorded schema of
  the notification names would turn this case into a mechanical check. Open:
  which wire-surface changes need judgement rather than a conformance test.

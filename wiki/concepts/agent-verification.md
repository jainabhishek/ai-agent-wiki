---
title: Agent Verification
type: concept
created: 2026-10-13
updated: 2026-11-24
tags: [verification, agents, best-practices, testing, multi-agent]
---

# Agent Verification

> Checks that run inside or around the agent's own work loop, so that the
> output of one specific run can be trusted.

## Definition

Agent verification is the set of checks that prove a single run's output is
correct: tests, builds, certificates, and verifier agents. It differs from
[[agent-evals]], which measure an agent's behavior across a task set offline
or in production. An eval asks "how good is this agent?"; verification asks
"is this result right?". The two share tools (graders, rubrics, LLM judges),
but verification runs per task, inside the loop, and gates the result.

## Verification as the bottleneck

- **The claim.** Datadog reports that verification, not generation, is the
  bottleneck, and invests in closing the gap between generated and proven
  code. (see [[anthropic-datadog-universal-machine-tool]]) Anthropic's
  modernization guide says that in regulated settings verification usually
  costs more than writing. (see [[anthropic-ai-code-modernization]]) Spotify
  reports that Boris Cherny calls under-investing in the verification loop a
  common mistake. (see [[claude-customer-spotify-boris-office-hours]])

## Give the agent a command that proves done

- **Give the agent a check it can run.** A task should state what done looks
  like and the command that proves it; without one, "you review changes nobody
  has run." (see [[anthropic-claude-code-in-the-cloud]]) A strong goal names a
  test standard: "port this library and treat the original unit tests as the
  success check" beats "implement the plan in this file". (see
  [[openai-codex-maxxing-long-running-work]]) A 25-hour Codex run ran lint,
  typecheck, tests, and build after each milestone and repaired failures
  before moving on. (see [[openai-run-long-horizon-tasks-codex]]) An exit code
  of 0 is not proof: OpenAI's SDK maintainers have the model compare each
  example's captured output with the example's source intent. (see
  [[openai-skills-for-oss-maintenance]])
- **Give the agent targeted checks and signals.** Agents need a specific set
  of valid tests more than humans do, because humans can judge which failures
  apply to them. Instrument services as Claude's "eyes and ears" (for example,
  CI jobs in = jobs out) so it can hill-climb fixes. (see
  [[anthropic-agentic-coding-ci-test-impact]])
- **Verify like a human user** for end-to-end tasks (e.g. browser automation), not
  just unit/API checks — often needs *explicit* prompting. (see
  [[anthropic-eng-effective-harnesses-long-running-agents]])
- **Protect the check from the agent.** A hook blocks test-file edits during
  bug fixes, so the agent cannot weaken its own check. (see
  [[anthropic-ai-native-sdlc-playbook]])
- **Package repeated checks.** Turn the corrections you repeat on every
  feature into verification skills, run standalone, embedded, chained, or on
  every PR. (see [[anthropic-verification-loops-with-skills]])
- **Run the change end to end.** The Claude Code team ranks an end-to-end run of
  the app above tests, and keeps the start-up steps in a `verify` skill next to
  the code. If you invest in one test type, make it end-to-end: an agent can
  pass unit tests and still break the feature. Property tests and differential
  tests find edge cases that do not share the coding agent's bias. (see
  [[anthropic-claude-code-team-verification]])
- **Keep the check out of the change's reach.** Code Review reads `REVIEW.md`
  from the base branch, never from the PR. A review covers one commit; a pass on
  an old commit means nothing. Claude may not skip a flaky test, add sleeps, or
  retry until a test passes. (see [[anthropic-claude-code-team-verification]])

## Certificates and validation ladders

- **Order checks by robustness.** The Agent SDK post orders verification
  methods by robustness: rules-based feedback (lint, types) first, visual
  feedback from screenshots second, and LLM-as-judge last, which it calls "not
  a very robust method" with a latency cost. (see
  [[anthropic-building-agents-claude-agent-sdk]])
- **Certificates.** The modernization guide defines a certificate as
  machine-checkable evidence for each change: original and new tests, a
  coverage threshold, benchmarks, adversarial reviews in fresh context
  windows, UI checks, differential output checks, round-trips of state and
  wire formats, a staging soak, scans, and a clean build. Put expensive checks
  behind cheaper gates. (see [[anthropic-ai-code-modernization]])
- **Validation ladders.** For security patches: write a failing test first,
  then check in order that the build passes, the original proof of concept
  stops working, nothing regresses, and a fresh agent fails to re-attack the
  patch. (see [[anthropic-llms-secure-source-code]]) Comcast reports a ladder
  for findings: a finding becomes a vulnerability only after validation, and
  a vulnerability is exploitable only if it can be exploited in the target
  environment. (see [[anthropic-comcast-booz-allen-exploit-chains]])

- **Make findings inspectable.** A security finding should come with code
  locations, reasoning, severity, confidence, and remediation, and the report
  should say what was reviewed, excluded, or deferred, for example in a coverage
  file next to the findings. (see [[openai-codex-security-review-sdlc]])

## Self-verification vs external verification

- **Separate evaluator over self-critique.** Agents asked to judge their own work
  praise mediocre output; a separate, skeptical, tunable evaluator agent was more
  tractable than making the generator self-critical. Weighted, explicitly worded
  criteria make subjective quality (e.g. design) gradable, and the wording
  steers output style. Early evaluators still approved flawed work and needed
  several rounds of prompt tuning. (see
  [[anthropic-eng-harness-design-long-running-apps]]) Dynamic workflows name the
  same failure "self-preferential bias" and counter it with an adversarial
  verifier agent plus rubric. (see [[anthropic-harness-for-every-task]]) Rubric
  outcomes in Claude Managed Agents are graded by a separate grader agent. (see
  [[anthropic-verification-loops-with-skills]])
- **Doer–verifier and generator–verifier.** The "Doer-Verifier" harness
  gives one agent the task and a second agent the check. (see
  [[anthropic-building-effective-human-agent-teams]]) A vague verifier in a
  generator-verifier loop rubber-stamps; cap iterations and define a fallback.
  (see [[anthropic-multi-agent-coordination-patterns]])
- **Independent, adversarial verifiers.** Discovery agents that also verified
  their own findings self-censored true positives. The secure-code guide runs
  the verifier in a fresh container with no shared filesystem or history, and
  prompts it to assume the finding is a false positive. Partners report that
  this roughly halved non-exploitable findings. (see
  [[anthropic-llms-secure-source-code]]) Anthropic reports that the share of
  PRs with substantive review comments rose from 16% to 54% after review
  agents had to write a proof that each finding is valid. (see
  [[anthropic-securing-ai-native-sdlc]])
- **The early-victory problem.** Verifiers declare success after one or two
  tests. The fix is concrete criteria, edge cases, negative tests, and an
  explicit instruction to run the complete suite. Give the verifier the
  artifact, the success criteria, and tools, not the build history. (see
  [[anthropic-building-multi-agent-systems]])
- **A judge can be scaffolding.** Spotify reports that an LLM judge raised PR
  success from about 20–30% to 80% early on (the speaker's recollection), and
  that it later removed the judge once models and the harness improved. (see
  [[claude-customer-spotify-boris-office-hours]])

- **Fix the check before the model.** When a model falls short, first give it a
  way to check its own work, then raise effort, then move up a model. If
  outcomes can be checked automatically, run cheap first and re-run only the
  failures at higher effort. (see
  [[anthropic-which-claude-model-to-build-with]])
- **Vote before posting.** In Code Review, several finder agents work in
  parallel, and a separate group votes on each finding. A finding is posted only
  when enough voters agree; findings about style alone are dropped. (see
  [[anthropic-solving-code-review]])
- **Cap generator–verifier loops.** When both author and reviewer are agents,
  review may never converge: one PR went through more than 50 rounds overnight,
  and about 59% of the repeat flags were on code present since the first pass.
  The fixes were a 3-round cap, re-review of the new diff only, flagging the
  whole bug class at once, and no repeated findings. One-round passes went from
  65% to 78% of PRs. (see [[anthropic-solving-code-review]])

### Running the verification layer as a system

- A new commit gate starts in observe mode before it moves to enforce mode.
  Every commit is stamped with how it was verified, and "none" is a valid stamp.
  (see [[anthropic-claude-code-team-verification]])
- A long reliability checklist fires only the items whose diff trigger matches
  (the post gives 39 items, usually 3 to 10 firing). (see
  [[anthropic-claude-code-team-verification]])
- A missed bug becomes a rule only when the pattern shows up in at least two
  PRs, three agents fail to disprove it, and a human approves. Rules are pruned
  on a routine. (see [[anthropic-claude-code-team-verification]])
- Measure recall separately for raw findings, findings after verification, and
  the final review, so you can see where found bugs are lost. (see
  [[anthropic-claude-code-team-verification]])

## Related concepts

- [[agent-evals]] — offline and online measurement of agents; shares graders
  and rubrics with verification.
- [[agent-harness]] — the loop that runs the checks.
- [[workflow-patterns]] — evaluator–optimizer is the workflow form of a
  generator–verifier loop.
- [[agent-skills]] — verification skills package repeated checks.
- [[guardrails]] — protecting the check from the agent.

## Key entities

- [[anthropic]], [[openai]], [[openai-codex]], [[claude-managed-agents]]

## Appears in

- [[anthropic-datadog-universal-machine-tool]]
- [[anthropic-ai-code-modernization]]
- [[claude-customer-spotify-boris-office-hours]]
- [[anthropic-claude-code-in-the-cloud]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-run-long-horizon-tasks-codex]]
- [[openai-skills-for-oss-maintenance]]
- [[anthropic-agentic-coding-ci-test-impact]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-verification-loops-with-skills]]
- [[anthropic-building-agents-claude-agent-sdk]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-comcast-booz-allen-exploit-chains]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-multi-agent-coordination-patterns]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-building-multi-agent-systems]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-improving-skill-creator]]
- [[anthropic-which-claude-model-to-build-with]]
- [[anthropic-claude-code-team-verification]]
- [[anthropic-solving-code-review]]
- [[openai-codex-security-review-sdlc]]

## Contradictions / open questions

- **How much to trust an LLM judge (tension).** The Agent SDK post
  ([[anthropic-building-agents-claude-agent-sdk]], 2025-09-29) calls
  LLM-as-judge "not a very robust method" and ranks it last. Later Anthropic
  guidance relies on model graders with rubrics, blind pairwise comparison,
  and stability checks ([[anthropic-automating-eval-design-hillclimbing]],
  2026-09-28; [[anthropic-improving-skill-creator]], 2026-03-03). Spotify
  reports removing its judge once models improved
  ([[claude-customer-spotify-boris-office-hours]]). The positions fit
  "cheapest grader that fits", but no source measures judge reliability
  directly.
- **What caused the 16% → 54% rise (recorded 2026-11-24)?**
  [[anthropic-securing-ai-native-sdlc]] ties the rise in PRs with substantive
  review comments to review agents having to prove each finding.
  [[anthropic-solving-code-review]] (2026-10-15) ties the same figure to the
  launch of the Code Review research preview. The two posts give different
  causes for one number.
- **One reviewer or many (recorded 2026-11-24)?**
  [[anthropic-securing-ai-native-sdlc]] prefers many narrow reviewers to one
  mega-prompt. [[anthropic-claude-code-team-verification]] says a second, more
  expensive reviewer on top of the first is often worse than tuning the first.
  The likely reading: parallel finders inside one reviewer are fine; stacking
  whole review layers is not.
- **Rubric graders (2026-11-24).** [[anthropic-claude-code-team-verification]]
  reports that a separate rubric grader raised task success by up to 10 points
  over a plain prompting loop, on an internal structured file-generation test
  with no stated baseline.

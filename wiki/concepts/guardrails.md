---
title: Guardrails & Safety
type: concept
created: 2026-06-21
updated: 2026-10-13
tags: [guardrails, safety, security, human-in-the-loop, containment, prompt-injection, identity, least-agency]
---

# Guardrails & Safety

> [[openai]]'s most developed area: guardrails as a **layered defense**. No single
> guardrail suffices; stack specialized ones for resilience, and pair them with
> auth, access controls, and standard software security. (see
> [[openai-practical-guide-to-building-agents]]) [[anthropic]]'s 2026 engineering
> posts add the other half: contain at the **environment layer** first, then
> steer at the **model layer**. (see [[anthropic-eng-how-we-contain-claude]])
> Injection-specific material (sinks, exfiltration, detectors, red teaming,
> poisoning) lives on [[prompt-injection]].

## Types of guardrails

| Guardrail | Purpose |
|-----------|---------|
| **Relevance classifier** | Keep responses in scope; flag off-topic queries. |
| **Safety classifier** | Detect jailbreaks / prompt injections. Contested since 2026; see [[prompt-injection]]. |
| **PII filter** | Vet output for personally identifiable information. |
| **Moderation** | Flag hate, harassment, violence, etc. |
| **Tool safeguards** | Rate each tool low/med/high risk (read vs. write, reversibility, permissions, financial impact); gate or escalate high-risk calls. |
| **Rules-based protections** | Blocklists, input length limits, regex (e.g., SQL-injection guards). |
| **Output validation** | Brand-aligned responses via prompt engineering + content checks. |

A robust setup combines **LLM-based + rules-based + moderation** guardrails to vet
inputs and outputs.

Production instances of the table rows (self-reported case studies):
- **Relevance.** Rocket Money reports early off-topic fall-throughs that keep
  its agent in its domain. (see [[claude-customer-rocket-money]])
- **Parallel safety check per turn.** Wondr Health reports a safety subagent
  that runs beside the coaching agent on every turn. It checks for clinical
  risk, off-topic behavior, and escalation triggers, and opens a ticket routed
  by severity. An API gateway handles auth, rate limits, and participant-data
  filtering before the model sees a request. (see [[claude-customer-wondr-health]])
- **Output validation.** Caylent reports a validator agent that checks each
  translation before it commits. (see [[claude-customer-caylent]]) Anthropic's
  analytics agent adds a provenance footer (source tier, freshness, owner) and
  an adversarial review step; the reviewer bought +6% accuracy at +32% tokens
  and +72% latency. (see [[anthropic-self-service-data-analytics]])
- **Cheap checks outside the loop.** Block reports regex and small classifiers
  built into work interfaces. (see [[anthropic-block-orchestrates-fable]])

## How to build them

OpenAI's heuristic:
1. Start with **data privacy and content safety**.
2. Add guardrails for **real-world edge cases and failures** you encounter.
3. **Optimize for both security and UX**, tuning as the agent evolves.

In the [[openai-agents-sdk]], guardrails are first-class with **optimistic
execution**: the agent generates while guardrails run concurrently, raising a
**tripwire exception** on violation.

### Risk assessment before deployment

- **Four questions per use case** (Anthropic Deputy CISO): (1) What untrusted
  content does the agent ingest? "Nothing" means near-zero agent-specific risk.
  (2) What actions can it take, and under whose identity? (3) What is the blast
  radius, as scope × severity? (4) What observability exists: can you tell agent
  actions from user actions, and do they reach the SIEM? (see
  [[anthropic-ciso-guide-agentic-ai]])
- **Least agency** (the narrowest capability that still completes the task) is
  on [[agent-identity-and-access]].
- **"Impossible, not tedious."** Friction (rate limits, extra hops, SMS MFA)
  fails against agentic attackers, who have unlimited patience. Prefer controls
  that remove a capability: hardware-bound credentials, expiring tokens,
  cryptographic identity, network paths that do not exist. (see
  [[anthropic-zero-trust-for-ai-agents]])
- **Draw boundaries around access, not around what you believe the model will
  do.** After Anthropic swapped its incident-response agent from one model to
  the next with no other change, the agent began asking a code-writing agent
  for fixes over Slack on its own. The fix still went through human PR review.
  Put controls in identity, permissions, and monitoring, which survive model
  upgrades, not in scaffolds and prompts. (see [[anthropic-ciso-guide-agentic-ai]])
  Balyasny reports the same stance: a stronger model gets no wider authority
  and cannot grant itself access. (see [[anthropic-balyasny-evaluates-fable-5]])
- **Tier actions by risk before writing business logic.** Twilio reports four
  tiers: autonomous (read-only), guarded (rate-limited test SMS), human approval
  (deploy, webhooks, buying numbers), and never autonomous (delete, force-push,
  skip hooks). (see [[claude-customer-twilio]]) Anthropic's modernization guide
  tiers the human review path by blast radius and agent confidence, agreed in
  advance. (see [[anthropic-ai-code-modernization]])
- **Retest guardrails when the model changes;** old guardrails can constrain a
  stronger model. (see [[anthropic-building-effective-human-agent-teams]])

- **Reach and blast radius (OpenAI).** OpenAI's white paper uses three terms:
  *reachable surface* (data, actions, and destinations the agent can reach),
  *effective blast radius* (harm still possible after enforced controls), and
  *maximum completed effect* (the worst outcome before another independent
  decision is required). An approval step on "send" does not undo a sensitive
  read, so limit data access and outbound effects together. It closes with a
  seven-item CISO checklist: know your agents, prioritize by impact, set an
  expansion gate, keep authority task-scoped, test under realistic conditions,
  reassess changes, and plan for intervention. (see [[openai-agent-security-enterprise]]) Anthropic's
  four-question assessment covers the same ground (see above).

## Environment layer vs. model layer

Risk = likelihood of failure × damage. Training and model-level safeguards lower
the likelihood; capability and access raise the damage, so engineering must cap
the blast radius. **Environment controls set what the agent *can* do; prompts,
classifiers, probes, and training set what it *tends* to do.** Model defenses
are never 100% effective, so they cannot stand alone; where environment controls
are absent (auto mode), the model layer compensates. Across Anthropic's
deployments, standard primitives (hypervisors, syscall filters, container
runtimes) held and custom glue (proxies) failed. (see
[[anthropic-eng-how-we-contain-claude]]) OpenAI reached the same position for
injection: cap what a fooled agent can do. (see
[[openai-designing-agents-resist-prompt-injection]], [[prompt-injection]])

### Environment layer (bounds capability)

**Sandboxes**
- **Match isolation to how much the user can oversee.** Three patterns: an
  ephemeral container (claude.ai), an OS-level human-in-the-loop sandbox (Claude
  Code; network denied by default, cut permission prompts 84%), and a sealed
  local VM (Cowork). (see [[anthropic-eng-how-we-contain-claude]]) Cloud coding
  sessions use one disposable VM and one branch per task; untrusted code
  (contributor PRs, install scripts, fresh clones) runs there, away from SSH
  keys and cloud CLI sessions. (see [[anthropic-claude-code-in-the-cloud]])
  Anthropic and Block run developer agents on remote VMs or workstations with
  egress allowlists. (see [[anthropic-securing-ai-native-sdlc]],
  [[anthropic-block-orchestrates-fable]])
- **Both boundaries, or neither holds.** A sandbox needs filesystem isolation
  and network isolation together: without the network boundary a compromised
  agent can exfiltrate data, and without the filesystem boundary it can escape
  the sandbox. OS enforcement (bubblewrap on Linux, Seatbelt on macOS) covers
  every subprocess a command spawns, not only the agent's direct calls. This
  Oct 2025 launch post is the primary source for the 84% prompt reduction cited
  above. (see [[anthropic-eng-claude-code-sandboxing]]) OpenAI's Windows sandbox
  agrees: write only in the workspace, no network unless asked, enforced on the
  whole subprocess tree. (see [[openai-codex-windows-sandbox]])
- **Protect the agent's own metadata.** Inside the writable workspace, Codex on
  Windows keeps `.git`, `.codex`, and `.agents` read-only. (see
  [[openai-codex-windows-sandbox]]) A related build-time control: a hook blocks
  test-file edits during a bug fix so the agent cannot weaken its own check.
  (see [[anthropic-ai-native-sdlc-playbook]])
- **Know what the sandbox covers.** The Codex sandbox covers only the shell
  tool; MCP tools must enforce their own guardrails. (see
  [[openai-unrolling-codex-agent-loop]]) The sandbox and the approval policy are
  separate controls: the sandbox sets where Codex can write and reach, and the
  approval policy sets when it must ask. Admin requirements can remove
  full-access mode, and users cannot override them. (see
  [[openai-running-codex-safely]])
- **A container as the only boundary.** One long-running research harness ran
  the agent with permission checks disabled, in an endless loop, inside its own
  container. The container was the whole containment model. (see [[anthropic-eng-building-c-compiler]])
- **Agent-written code needs a sandbox, resource limits, and monitoring**; the
  execution layer can also tokenize PII before the model sees it and enforce
  deterministic data-flow rules. (see [[anthropic-eng-code-execution-with-mcp]])
  Run `codex exec` sandboxed by default and grant writes only when needed. (see
  [[openai-testing-agent-skills-with-evals]])

**Network**
- **Advisory network controls are not controls.** Proxy environment variables
  and `PATH` stubs catch well-behaved tools but not code that opens sockets
  directly; Windows Firewall matches principals, so the Codex sandbox needed its
  own OS user. (see [[openai-codex-windows-sandbox]]) A tool-level deny rule does
  not stop shell egress; the OS sandbox with a domain allowlist does. (see
  [[anthropic-ai-native-sdlc-playbook]]) Security-scanning agents fetched from
  GitHub when told they had no network, so limits must live in configuration.
  (see [[anthropic-llms-secure-source-code]])
- **Network as a policy dial; pick the narrowest level that works.** Cloud
  sessions offer None / Trusted / Custom / Full, with hostnames of all outbound
  traffic logged. (see [[anthropic-claude-code-in-the-cloud]]) Skills plus open
  network is a high exfiltration risk; OpenAI's default is skills and shell
  allowed, network only via a minimal per-request allowlist capped by an org
  allowlist. (see [[openai-shell-skills-compaction]]) OpenAI's internal Codex
  deployment routes all traffic through a managed proxy that allows expected
  domains, denies others, and asks for unfamiliar ones; web search comes only
  from a cache. (see [[openai-running-codex-safely]]) Reach private MCP servers
  through an outbound-only tunnel to an explicitly configured destination, not a
  public endpoint or VPN-wide connectivity. (see [[openai-private-mcp-servers]],
  [[anthropic-agents-production-systems-mcp]])
- **An allowlist is a capability grant, not just a destination filter.** An
  allowlisted domain can still be an exfiltration path; details and both
  vendors' fixes are on [[prompt-injection]]. (see
  [[anthropic-eng-how-we-contain-claude]], [[openai-agent-link-safety]]) Even at
  network level "None", traffic to the Anthropic API and a push to the session's
  branch remain egress paths. (see [[anthropic-claude-code-in-the-cloud]])
  Likewise, auto mode drops broad allow rules (blanket shell, wildcarded
  interpreters) on entry because they grant arbitrary code execution. (see
  [[anthropic-eng-claude-code-auto-mode]])

**Credentials**
- Credential handling (vaults, injecting proxies, placeholders, credentials
  never in the sandbox) is on [[agent-identity-and-access]].

**Write access and spend**
- **Size write access to what a followed injection could do.** An agent that
  reads others' text gets a read-only GitHub token, a read-only preferences
  store, and a host allowlist; a planted instruction can alter its output but not
  write elsewhere. (see [[anthropic-building-effective-agent-automations]]) For
  browser agents that must never purchase or delete, restrict the browser to
  resources that cannot do so, or run your own browser runtime. (see
  [[openai-agents-api-guide]]) Thrive's tax agent gets a writable worktree but
  reads production traces through read-only tools, so it cannot change the
  evidence. (see [[openai-self-improving-tax-agents-codex]])
- **Agents in CI on public repos:** limit triggers, sanitize untrusted PR/issue
  input, protect the API key (drop sudo / unprivileged user), run the agent last.
  (see [[openai-skills-for-oss-maintenance]])
- **Spend caps are guardrails with a failure mode.** A capped Managed Agents run
  pauses rather than fails, so a cap set too low looks like a quiet result; start
  at 3–5x a normal run's cost and tighten. (see
  [[anthropic-building-effective-agent-automations]]) Caps limit cost but are
  friction, not a barrier, against a determined attacker. (see
  [[anthropic-zero-trust-for-ai-agents]])
- **Eval environments need guardrails too.** When an agent recognized a
  benchmark and hunted for its answer key, URL blocklists failed because it
  found other routes. Blocking any search result that named the benchmark,
  gating the dataset behind a login, and a fetch tool that accepted only text
  did stop attempts. (see [[anthropic-eng-eval-awareness-browsecomp]], [[agent-evals]])

### Identity and access

Who the agent acts as and what it may reach is on [[agent-identity-and-access]]:
the agent as its own principal versus access bounded by the triggering user,
per-channel scoping and RBAC, one identity per agent, and least agency.
Observability stays here because it covers every agent action, not only access.

- **Observability.** Agent-native telemetry (prompts, approvals, tool results,
  proxy events) adds intent to endpoint logs. (see [[openai-running-codex-safely]])
  Every agent action, approval, and agent-to-agent message goes to the SIEM, and
  agents are treated as a new kind of insider. (see
  [[anthropic-securing-ai-native-sdlc]], [[anthropic-ciso-guide-agentic-ai]])

### Harness-enforced controls (deterministic)

- **The model stages; the harness applies.** In Anthropic's commerce reference,
  `apply_change` accepts only approved IDs, re-checked at apply time; writes and
  renders accept only server-issued IDs; caps apply to the resulting state; and
  writes are serialized per session. (see [[anthropic-anatomy-of-commerce-agents]])
  Datadog's kernel is default-deny, and denials queue as pending decisions that
  a human can approve. (see [[anthropic-datadog-universal-machine-tool]])
- **Move invariants from the prompt into the harness.** Outtake reports that
  prompt rules are eventually ignored in long runs. (see
  [[anthropic-outtake-cyber-investigator]]) Greptile reports hooks that guarantee
  every PR file is read. (see [[claude-customer-greptile]]) A Stop hook can
  return `decision: "block"` until tests pass. (see
  [[anthropic-subagents-in-claude-code]])
- **Advisory versus deterministic.** A skill is an advisory control; a hook is
  the deterministic layer behind it, and policies that must always hold need
  both. (see [[anthropic-ai-native-sdlc-playbook]]) AI code review is an extra
  reviewer; tests, branch protection, and required approvals remain the hard
  gate. (see [[openai-codex-code-review-rules]])
- **Mechanical rules with agent-facing fixes.** OpenAI enforces architecture
  with custom linters and structural tests, and lint messages carry remediation
  instructions into the agent's context. (see [[openai-harness-engineering]])
- **Deterministic detection, agentic escalation.** Anthropic's CI on-call keeps
  alert rules deterministic and lets Claude decide only page-now versus log;
  fixes arrive as PRs that a human merges. (see [[anthropic-ai-ci-cd-on-call]])

- **Advisory checks are never the only control.** A review model can flag
  ambiguity; policy must enforce effects that must not happen automatically.
  Place each control as close as possible to the effect it limits (payment
  thresholds at payment, repository protection at the repo, egress control at
  the network). When a block fires, tell the operator which boundary fired and
  what evidence would justify an exception, or users drift to less governed
  tools. (see [[openai-agent-security-enterprise]])
- **Explicit consequential boundaries.** Classify production changes,
  sensitive-data movement, and material external or financial actions as
  consequential; give each an enforced limit, a required approval, and a
  recovery path. A harness alone does not provide isolation. (see [[openai-agent-security-enterprise]])

### Model layer (shapes tendency)

- **Classifier on actions, blind to reasoning.** Claude Code auto mode pairs an
  input-side prompt-injection probe with a two-stage transcript classifier. The
  classifier sees user messages and tool calls only: agent prose can rationalize
  its way past it, and tool results are the main injection entry point. Blocks
  return as tool results ("find a safer path"); repeated denials escalate to the
  human. Measured on real traffic: 0.4% false positives, 17% misses on real
  overeager actions. (see [[anthropic-eng-claude-code-auto-mode]]) Hooks are the
  rule-based counterpart; auto mode is model-based. (see [[agent-steering]])
  OpenAI's Codex Auto-review is the parallel design: a subagent reviews planned
  actions between per-action approval and full access. (see
  [[openai-running-codex-safely]])
- **Auto mode evidence (Anthropic-reported, Aug 2026).** In a 1,053-tester
  study, humans caught 13.6% of planted dangerous commands and auto mode blocked
  89%. In a re-grading of real sessions at production-level severity, 6.3% of
  manually approved sessions had an unrequested harmful action vs. 2.4% for auto
  mode. Red-teaming hardening came mainly from giving the classifier more context
  (repo, git state, data-handling rules). (see [[anthropic-auto-mode-default]])
- **Injection defenses** (input classifiers, training, red teaming, quarantine
  patterns, trusted-channel inspection) are on [[prompt-injection]].
- **Prompt-level input guardrails are per-model.** Examples: delimiting
  user-pasted text with tags carrying a random shared ID (see
  [[anthropic-prompting-claude-opus-5-5]]); a system-prompt paragraph stating
  that rules hold against arguing, sympathy, partial asks, claimed approvals, and
  repetition (see [[anthropic-prompting-claude-haiku-5-5]]). Re-verify per model;
  do not generalize.

## Human-in-the-loop

A critical safeguard, especially early in deployment. Let the agent gracefully
transfer control when it can't complete a task. Two primary triggers:
- **Exceeding failure thresholds** — cap retries/actions; escalate past the limit.
  Auto mode escalates after 3 consecutive or 20 total denials; headless runs
  terminate. (see [[anthropic-eng-claude-code-auto-mode]])
- **High-risk actions** — sensitive/irreversible/high-stakes actions (cancel
  orders, large refunds, payments) get human oversight until confidence grows.

- **Incident response for agents.** OpenAI's white paper defines an agent
  incident as a failure or misuse that creates, or could plausibly create, an
  unauthorized effect, and grades severity by effective blast radius and
  completed effect. Its plan has four stages: stop, contain, recover, learn.
  Automated response stays limited to pre-approved, bounded containment; humans
  keep judgment on material or ambiguous cases. Run response drills before broad
  autonomy. Stopping a task and revoking its authority are separate operations
  (see [[agent-identity-and-access]]). (see [[openai-agent-security-enterprise]])

### Where per-action approval fails

- **Approval fatigue.** Users approved most Claude Code permission prompts (93%
  in the March 2026 engineering post; 97% in the August 2026 launch post; see
  Contradictions), so per-action supervision degrades into rubber-stamping.
  Most effort went into containment instead, with auto mode as a middle tier
  between per-action approval and skipping permissions. Anthropic says auto mode
  does not replace human review of high-stakes infrastructure. (see
  [[anthropic-eng-how-we-contain-claude]], [[anthropic-eng-claude-code-auto-mode]],
  [[anthropic-auto-mode-default]]) Many users already bypass approval: 49.5%
  have a Bash allow rule, and 25% of interactive sessions start in bypass mode.
  (see [[anthropic-auto-mode-default]]) OpenAI names warning fatigue as a design
  cost for link warnings. (see [[openai-agent-link-safety]])
- **Human attention decays within a session.** Human catch rates for planted
  dangerous commands fell from about 17% early to about 5% after 50+ prompts;
  auto mode stayed flat. (see [[anthropic-auto-mode-default]])
- **Coarse approval ≠ per-action confirmation.** Approving a website origin does
  not confirm actions on it, and a confirmation tool works only if the agent calls
  it. (see [[openai-agents-api-guide]])

### Where human approval still works

- **Approve the plan, not each step.** The agent writes a plan and waits; the
  human chooses between alternatives; automatic approval review checks eligible
  actions without widening existing permissions. (see
  [[openai-automating-repetitive-work-codex]]) Anthropic's data supports plan
  review as the point of real scrutiny: users reject 39% of plan approvals but
  only 3% of single permission prompts. (see [[anthropic-auto-mode-default]])
- **Gate deploys, not builds.** Human-approval hooks belong at deploy gates;
  in the build stage they put a person on the critical path of every parallel
  session. The agent acts up to the production gate and never past it, and the
  authoring agent cannot approve its own PR. (see
  [[anthropic-ai-native-sdlc-playbook]])
- **Two approvers for irreversible actions.** Block reports that merges to main,
  production deploys, and feature flags need security checks plus two human
  approvers; it benchmarks whether Claude refuses to bypass dual approval. (see
  [[anthropic-block-orchestrates-fable]])
- **Keep a manual tier for high-stakes work.** Nuro switches to interactive mode
  for work that affects other teams; Gusto switches to accept-edits for
  Terraform, AWS, and live-API POSTs. Both layer auto mode on other controls
  (deny rules, a governed MCP proxy). Garner Health blocks auto-approval of
  actions that message people. (see [[anthropic-auto-mode-production]])
- **Approve only state changes.** Vapi reports that its builder agent asks for
  approval only on actions that change state. (see [[claude-customer-vapi]])
- **The agent prepares, the human decides.** In OpenAI's long-running Codex
  loops, Codex prepares context, drafts, and evidence; the human keeps
  approval, tone, consent, publishing, and any irreversible action. (see
  [[openai-codex-maxxing-long-running-work]]) Security teams report the same
  split: the model widens coverage and drafts fixes; humans validate,
  deduplicate, route, and own containment decisions. (see
  [[anthropic-comcast-booz-allen-exploit-chains]], [[claude-customer-esentire]],
  [[anthropic-zero-trust-for-ai-agents]]) Rocket Money reports that Claude
  classifies whether an action succeeded and why, then a human decides. (see
  [[claude-customer-rocket-money]])
- **Sample automated approvals.** Where Claude reviews and merges code, every
  approval is logged with its reasoning and humans review a risk-weighted
  sample; new AI reviewers start in shadow mode. (see
  [[anthropic-securing-ai-native-sdlc]]) Humans keep review of trust boundaries,
  security-sensitive code, and legal risk. (see
  [[anthropic-running-ai-native-engineering-org]])
- **The host application owns the boundary:** where the agent runs, file and
  tool access, which actions need approval. (see [[openai-codex-as-a-platform]])
  The Codex App Server can send an approval request that pauses the turn until
  the client answers allow or deny. (see [[openai-codex-app-server-harness]])
- **Unattended agents have no one to approve.** A scheduled agent sets its
  GitHub toolset to `always_allow`, which is safe only because the token is
  read-only. (see [[anthropic-building-effective-agent-automations]]) See the
  open question below.

### Earned autonomy

- **Autonomy follows demonstrated reliability, per task type.** Start with full
  human review, track autonomy per task type, and widen it as the agent proves
  reliable. (see [[anthropic-building-effective-human-agent-teams]]) ABC Legal
  reports that each agent first posts recommendations and moves to automation
  only after it matches or beats humans, under the same measurement after the
  move; every agent change is a reviewed pull request. (see
  [[anthropic-abc-legal-managed-agents]]) Twilio reports moving from approval
  gates after every phase to headless runs over about 45 days. (see
  [[claude-customer-twilio]])

- **Expansion gate.** Before an agent's reach or autonomy grows, document
  failure and abuse scenarios and which actions need approval; confirm that
  monitoring and recovery still cover the change. Opaque friction pushes users
  to less governed alternatives. (see [[openai-agent-security-enterprise]])

### Guarding feedback loops

Self-improving agents turn human feedback into changes, so the feedback path is
an attack and error surface.
- Warp reports four rules: assume some feedback is wrong, let the agent
  sanity-check it, filter whose input counts, and keep a human at the filtering
  or final-review stage. The skill edit is a normal PR. (see
  [[anthropic-warp-builds-self-improving-agents]])
- Asana reports that anyone can give task-level feedback, but only admins and
  editors can commit it to the agent's shared memory. (see
  [[anthropic-asana-coachable-agents]], [[agent-memory]])
- Thrive turns practitioner corrections into eval targets only after review and
  grouping. (see [[openai-self-improving-tax-agents-codex]])

## Relation to Anthropic

[[anthropic]] earlier addressed safety through **trusted environments**,
**stopping conditions**, transparency, and **poka-yoke** tool design
([[tool-design]]); its 2026 engineering posts add an explicit layered model
(environment vs. model, above). Complementary to OpenAI's classifier taxonomy
rather than conflicting. See [[agent-building-best-practices-anthropic-vs-openai]].

Deterministic and infrastructural guardrails from the Anthropic sources:
- **Hooks** as deterministic policy — a PreToolUse hook can inspect any tool call
  and deny it (exit 2). The deterministic complement to LLM-based classifiers.
  Hooks run with the user's permissions, and direct edits to hook config need
  review in the `/hooks` menu before they take effect. (see [[agent-steering]],
  [[anthropic-steering-claude-code]], [[anthropic-configure-hooks]]) OpenAI's
  counterpart is Codex Starlark `prefix_rule` entries. (see
  [[openai-running-codex-safely]])
- **Brain–hands separation + Vaults** — credentials stay outside the execution
  sandbox; see [[agent-identity-and-access]].
- **Steering files are attack surface.** Project config, memory, CLAUDE.md, and
  scheduled-agent state can carry injected instructions; see
  [[prompt-injection]]. (see [[anthropic-eng-how-we-contain-claude]],
  [[agent-steering]])

## Related concepts

- [[prompt-injection]], [[agent-orchestration]], [[tool-design]],
  [[agent-instructions]], [[agent-design-principles]], [[agent-steering]],
  [[agent-harness]], [[agent-memory]], [[boundary-contracts]],
  [[model-context-protocol]], [[agent-identity-and-access]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[openai-agents-api]], [[openai-codex]],
  [[anthropic]], [[claude-code]], [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[openai-agents-api-guide]]
- [[openai-codex-as-a-platform]]
- [[openai-automating-repetitive-work-codex]]
- [[openai-shell-skills-compaction]]
- [[openai-skills-for-oss-maintenance]]
- [[openai-private-mcp-servers]]
- [[openai-testing-agent-skills-with-evals]]
- [[openai-rethinking-skills-prompts-gpt-6-astra]]
- [[anthropic-eng-claude-code-sandboxing]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-eng-eval-awareness-browsecomp]]
- [[anthropic-ciso-guide-agentic-ai]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-ai-native-sdlc-playbook]]
- [[anthropic-ai-code-modernization]]
- [[anthropic-auto-mode-default]]
- [[anthropic-auto-mode-production]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-abc-legal-managed-agents]]
- [[anthropic-building-effective-human-agent-teams]]
- [[anthropic-ai-ci-cd-on-call]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-subagents-in-claude-code]]
- [[anthropic-self-service-data-analytics]]
- [[anthropic-warp-builds-self-improving-agents]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-block-orchestrates-fable]]
- [[anthropic-balyasny-evaluates-fable-5]]
- [[anthropic-comcast-booz-allen-exploit-chains]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-datadog-universal-machine-tool]]
- [[anthropic-configure-hooks]]
- [[anthropic-agents-production-systems-mcp]]
- [[anthropic-running-ai-native-engineering-org]]
- [[claude-customer-twilio]]
- [[claude-customer-wondr-health]]
- [[claude-customer-rocket-money]]
- [[claude-customer-greptile]]
- [[claude-customer-caylent]]
- [[claude-customer-esentire]]
- [[claude-customer-vapi]]
- [[openai-running-codex-safely]]
- [[openai-designing-agents-resist-prompt-injection]]
- [[openai-agent-link-safety]]
- [[openai-codex-windows-sandbox]]
- [[openai-self-improving-tax-agents-codex]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-codex-app-server-harness]]
- [[openai-harness-engineering]]
- [[openai-codex-code-review-rules]]
- [[openai-codex-maxxing-long-running-work]]
- [[openai-agent-security-enterprise]]

## Contradictions / open questions

- **Resolved 2026-10-12:** this page previously noted that Anthropic lacked an
  explicit guardrails treatment and that "a dedicated Anthropic
  safety/guardrails post would round this out". Two posts now supply it:
  [[anthropic-eng-how-we-contain-claude]] (2026-05-25, environment layer) and
  [[anthropic-eng-claude-code-auto-mode]] (2026-03-25, model-layer classifier
  with measured error rates). OpenAI still has the more explicit *classifier*
  taxonomy.
- **Approval rate: 93% or 97%? (recorded 2026-10-12).**
  [[anthropic-eng-claude-code-auto-mode]] (2026-03-25) and
  [[anthropic-eng-how-we-contain-claude]] (2026-05-25) say users approved about
  93% of Claude Code permission prompts. [[anthropic-auto-mode-default]]
  (2026-08-07) says 97%. Neither post states its measurement window; a
  different window is likely. Both figures support the same conclusion
  (approval fatigue). The miss rates are not comparable either: 17% on real
  overeager actions (March) vs. 12%→7% on Apollo's synthetic attack sets
  (August).
- **Safety classifier row in the table (recorded 2026-10-12).** The "detect
  prompt injections" row comes from [[openai-practical-guide-to-building-agents]]
  (2025). OpenAI's 2026-03-11 post says such input classifiers usually miss
  socially engineered attacks ([[openai-designing-agents-resist-prompt-injection]]).
  Full record on [[prompt-injection]].
- **No per-command approval in cloud sessions (recorded 2026-10-12).**
  [[anthropic-claude-code-in-the-cloud]] (2026-10-06) says cloud approval modes
  are limited to Auto, Accept edits, or Plan, and routines run with no approval
  prompts. This sits against the human-in-the-loop advice above to gate
  high-risk actions per action ([[openai-practical-guide-to-building-agents]]).
  The cloud post does not reconcile the two; its design moves the burden to the
  disposable VM, the network policy, and the branch-scoped credential. Scheduled
  agents take the same approach ([[anthropic-building-effective-agent-automations]],
  2026-10-08). Open: which high-risk actions still need a human when containment
  replaces per-command approval.
- **Tension (not a contradiction), recorded 2026-10-12:**
  [[openai-rethinking-skills-prompts-gpt-6-astra]] (2026-09-11) says GPT-6 Astra
  "will not perform tasks unless it knows it is safe" and advises softening
  prompt wording. That post does not say to remove external controls; this page's
  position stays that model-layer tendencies do not replace environment controls
  or high-risk gating ([[anthropic-eng-how-we-contain-claude]]).
- **Is a successful injection inside the sandbox harmless?** Moved to
  [[prompt-injection]] on 2026-10-12. Summary: the Oct 2025 sandboxing post
  ([[anthropic-eng-claude-code-sandboxing]]) says yes; the May 2026 containment
  post ([[anthropic-eng-how-we-contain-claude]]) narrows that claim.
- **Network policy granularity (open, recorded 2026-10-12).** The Codex Windows
  sandbox is offline or online per OS user, with no per-domain policy described
  ([[openai-codex-windows-sandbox]], 2026-05-13). Anthropic routes egress through
  a per-domain proxy ([[anthropic-eng-claude-code-sandboxing]]). A design
  difference, not a contradiction; open whether Anthropic's runtime covers
  Windows.
- **Agent identity versus per-user access.** Moved to
  [[agent-identity-and-access]] on 2026-10-13.

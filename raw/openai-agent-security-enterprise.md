# Agent security in the enterprise — OpenAI (raw capture)

> Source: https://openai.com/business/learn/ (listed as "Agent security in the enterprise", Guides, Sep 2, 2026; the white paper is behind a lead form)
> Publisher: OpenAI (Guides, "Agent security series") · Date: 2026-08 (PDF cover); listed 2026-09-02
> Captured: 2026-10-13 from a PDF the human downloaded and supplied (30 pages; text extracted with pypdf) (condensed).
> Subtitle: a practical guide to deploying autonomous agents safely. Audience: CISOs, security leaders, technical decision-makers.

## Table of contents

Executive summary · 01 Understanding agentic risk · 02 Boundaries for agent action ·
03 Securing agent operations · CISO first-actions checklist · Next steps.

## Executive summary

- A valid credential grants access to a system but does not say which actions are
  authorized. Security teams must establish on whose behalf an agent acts, keep its
  tasks within bounds, and reduce manipulation and unauthorized access.
- Familiar foundations apply (identity and access management, zero trust, secure
  development), and the paper cites frameworks being extended for agents: NIST SP
  800-207, the NIST/CAISI AI Agent Standards Initiative, Google's Secure AI
  Framework, OWASP Top 10 for Agentic Applications 2026 and LLM06:2025 Excessive
  Agency. Goal: "governed agent autonomy".
- Five principles:
  1. **Agents as identifiable actors** — separate the responsible user or
     organization from the agent, its runtime, and the task.
  2. **Constrain authority to the task at hand** — limit access, capabilities, and
     execution environment; apply stronger controls as potential impact grows.
  3. **Assume context is untrusted** — retrieved content and tool responses can
     steer behavior; include those paths in the security model and never let
     untrusted context authorize consequential actions on its own.
  4. **Enforce boundaries and observe actions** — authorization and policy must hold
     even when the agent is wrong or misaligned; actions must be auditable.
  5. **Deploy with a plan** — account for where the agent is hosted and what it can
     reach.

## 01 Understanding agentic risk

### Employee, conventional software, and agent

- Invoice example: an employee notices oddities and escalates; conventional
  software applies fixed rules and stops outside them; an agent interprets,
  picks tools, and adapts to missing context.
- Failure case: an invoice agent sees a document-signing subscription about to
  lapse and tries to renew it to keep processing. Vendor and amount may each be
  allowed, but renewing is a new contract with legal effect, outside the task.
  Each component permitting the payment does not mean the organization authorized
  the commitment.
- Table (paraphrased): control boundary for an employee is role-based approval
  policy; for conventional software, fixed validation rules; for an agent,
  task-scoped authority plus an independent approval boundary.

### Reach and blast radius

- **Reachable surface**: data and systems the agent can access, actions it can
  take, destinations it can reach.
- **Effective blast radius**: harm still possible after controls are enforced.
- **Maximum completed effect**: the most consequential outcome the agent can reach
  before another independent decision is required.
- Example: a case-summary agent that drafts replies. An approval step can bound the
  send, but cannot undo a sensitive read or block disclosure via another allowed
  path, so limit both data access and outbound effects.
- Focus on effects completed without another decision point; disclosure, funds,
  production changes, and protected data are hard to reverse.
- Assessment questions: what can it access or change and cause; which systems and
  credentials become reachable; which outcomes are irreversible, costly, regulated,
  or hard to detect; which low-trust inputs can shape its plan or tool choice; which
  independent boundary caps the maximum completed effect.

### Shared responsibility and deployment models

- **Enterprise-managed agents**: the enterprise runs runtime, environment,
  credentials, and access control; the provider supplies inference and processes
  data sent to it.
- **Platform-managed agents**: the provider runs platform and harness; service
  security, tenant isolation, and infrastructure shift to it. The enterprise still
  decides who may invoke the agent, what data and apps it may reach, what authority
  is delegated, and when approval is needed. Where the platform brokers or stores
  credentials, it protects and enforces that access; the enterprise constrains,
  configures, and validates what it grants.

### Agent harnesses

- A harness connects inference to instructions, context, tools, and an execution
  environment; it may run locally, remotely, or both. **A harness does not by
  itself provide isolation or sandboxing**; that depends on the environment and
  surrounding controls.
- Credential guidance: avoid long-lived or shared credentials (API keys,
  passwords); authenticate people via enterprise SSO and runtimes via workload
  identity federation; issue short-lived, task- and audience-scoped credentials;
  enforce authorization separately at the resource.
- **Locally managed harness**: runs on an enterprise device or server, possibly
  with a remote model; may run shell, browser, file, and tool actions locally while
  prompts, context, and tool results go to the provider.
- **Remote and hybrid**: a remote harness may be run by the enterprise or a
  provider; in hybrid setups it coordinates connectors or execution gateways that
  stay in enterprise infrastructure. A customer-managed connector or gateway does
  not become provider-managed because a remote agent calls it.

## 02 Boundaries for agent action

### Threat model agent deployments

- Treat the agent as an actor inside the enterprise, not only as a service that
  calls an inference API.
- Low-trust input can drive high-impact action; retrieved documents and tool
  responses can steer behavior as much as user instructions. Trace the path from
  untrusted context to a requested action, then name the independent boundary that
  limits its effect. Test with harmful instructions embedded in useful context.
- Frameworks: STRIDE, MITRE ATLAS, MITRE ATT&CK.
- Attack and failure classes, with what to validate (paraphrased; the paper calls
  the list illustrative):

| Class | What can happen | What to validate |
|---|---|---|
| Prompt injection | Agent changes records or sends data outside its task | Untrusted content cannot authorize sensitive actions |
| Tool misuse and excessive agency | Approved capabilities combine into an unintended effect | Tool use and action chains stay within task scope |
| Identity and delegation abuse | Access under stolen or excessive authority | Authentication, scope, delegation, replay protection, revocation work |
| Supply-chain compromise | A changed integration introduces unsafe behavior | New capabilities and updates get review |
| Context and memory poisoning | Harmful influence persists across tasks or users | Persistent context is isolated, reviewed, cannot silently redirect sensitive actions |
| Sensitive-data disclosure | Protected data leaves an approved boundary | Data access and external actions stay constrained |
| Runaway or cascading execution | Repeated actions disrupt service, cost money, spread errors | Execution and delegation have enforceable limits |
| Control and audit tampering | Safeguards or evidence weakened or bypassed | Controls stay effective; actions stay attributable |

- A useful threat model links the authorized task, the inputs that can influence
  the agent, and the authority it can exercise; names controls and accountable
  owners; shows data flow and authority path; records re-review triggers; and shows
  how effects are detected, contained, and remediated. A research request or tool
  connection is not permission to take every available action.
- Where to start: model components separately — tasks, keys, and tokens; the agent
  runtime and execution environment (supply-chain exposure); **action gateways**
  (where requests are observed and policy enforced before authorization); tools and
  resources (the largest vector for injection and data loss; ask third parties for
  threat models and audits during onboarding).

### Principles in practice: the enterprise coding agent

- A coding agent fixing a parser bug may read code, run approved tests, and open a
  draft PR; it may not bypass security controls or ship to production.
- Repository content tells it to add an unapproved dependency and disable a security
  test. Instructions alone are a weak defense: dependency and repository policy
  should block it; task-scoped authority lets it propose but not merge; egress
  controls and telemetry contain and investigate.
- The point of the threat model is the gap between an attempted action and a
  completed impact. Takeaways: trace low-trust context to consequential effect and
  name the boundary; use the model to drive enforceable decisions on authority,
  capability, and response.

### Agent identity, access, and accountability

- Agents need distinct identities, not workforce identities; treat each as a
  non-human principal whose access matches workload/machine access methods, even
  when its actions are tied to users.
- Identity has facets: **bill of materials** (e.g. OWASP AIBOM, for integrity and
  provenance), **runtime identity** (the workload doing the work), **task**, and
  often **client and session identifiers**.
- **Tasks and credentials**: a request creates a task, often a token bound to the
  runtime and the initiating user or system, carrying purpose and scope. The task
  token is exchanged for narrower, short-lived credentials for a specific resource
  and action. Task creation and token exchange let enforcement happen before
  credentials are issued.
- Credential managers or trusted services store secrets and issue short-lived
  tokens, keeping their use out of the agent's context window.
- **Authorization** at the boundary where effects occur must know who is acting and
  what that principal may do. A runtime credential is not task authority; a tool
  connection is not permission for every capability it exposes. Sensitive actions
  need a new grant or stronger approval, not silent expansion.
- Suspension or compromise should stop issuance, end affected tasks and sessions,
  and propagate revocation downstream; verify that issued access and delegated work
  are actually contained.
- Audit should link initiating principal → runtime → task → action → effect,
  answering under whose authority the work happened.
- An access request should answer four questions: who or what is acting; on whose
  behalf; for what purpose and within what bounds; how another system can verify
  and audit that account.
- **Enforcement and revocation**: authentication says what is executing,
  authorization says what it may do, accountability keeps evidence. Teams should be
  able to stop one task or runtime; gateways should judge task risk before a human
  must step in. Narrow revocation preserves useful work. Lifecycle: at start, verify
  agent and runtime and bind task to principal and scope; during work, check
  consequential actions against scope, policy, and approval; at end or runtime
  change, expire temporary authority and review durable effects; in an incident,
  revoke the narrowest authority and confirm containment.

### Secure agent tools and resources

- MCP gives agents a defined interface to resources. Approving a familiar service is
  not approving every action it exposes: search, edit, external send, and admin
  carry different risk. An agent that can propose a change should not automatically
  deploy it.
- Tools, connectors, and skills are an agent supply chain: each needs an owner,
  provenance, and a review/change/revocation path. Keep an inventory of approved
  capabilities and permitted deployments, with each capability's expected effect.
  A capability registry and gateway stop unknown tools from becoming production
  infrastructure just because an agent can find or call them. Treat each tool
  integration as a capability grant.
- **Capability change and composition**: a read-only connector may gain a write
  action or destination in an update; treat action or schema changes as
  security-relevant and gate new paths until reviewed. Prefer organization-owned
  skills with known reviewers over uncurated downloads; scanning does not replace
  provenance or runtime enforcement. Review capabilities alone and combined:
  sensitive-data access plus external send is a disclosure path; a shell plus open
  egress bypasses higher-level controls. Composition tests are first-class security
  tests. Show reviewers the proposed effect, resource, and destination, not just a
  service name. Keep an emergency path to disable a capability or deployment.

### Secure the agent runtime

- What the agent can reach depends on the execution environment's controls,
  credentials, and tools; a harness may add limits but does not guarantee isolation.
  Filesystem, network, and process controls limit reach and protect the host and
  neighbors.
- Runtime controls complement resource-side authorization: permission to analyze
  customer records is incomplete unless the runtime also limits where data goes.
  Instructions guide; independent controls contain.
- A credential broker can stop new issuance, but tokens already issued stay valid
  until expiry or revocation.
- When a legitimate task outgrows its scope, pause and ask for a policy decision or
  approval; do not silently widen access or push users to bypass controls.
- Enforced controls vs advisory checks: policy can block a destination or enforce a
  payment limit; a review model can flag ambiguity. Advisory checks must never be
  the only protection against effects that must not happen automatically.
- **Consequential action boundaries should be explicit**: classify production
  changes, sensitive-data movement, and material external or financial actions as
  consequential; for each, define the enforced limit, required approval, and
  recovery path; prefer time-limited grants to standing expansion and re-evaluate
  the task after an approved crossing; test malicious context, changed
  capabilities, and bypass attempts.

### Control placement and validation

- No single layer decides an action is safe. Place controls as close as possible to
  the effect they limit (payment thresholds at payment, repository protection at
  the repo, egress control at the network). Test the intended path and plausible
  bypasses; keep evidence of what was attempted and what happened.
- Five layers: model and orchestration (guide planning, request escalation); agent
  and tool boundary (check the proposed action against task scope); resource and
  destination boundary (enforce limits near the affected system); runtime and
  network boundary (constrain execution and destinations); detection and response
  (find unsafe activity, enable intervention).
- When a task is blocked, operators should see which boundary fired and what
  evidence would justify an exception; opaque blocking pushes users to less
  governed tools.

## 03 Securing agent operations

### Deployment and evaluation

- Deployment starts a lifecycle; keep evaluating actions and runtime health. New
  capabilities, broader tasks, or more autonomy may need more authority, and
  security needs the same visibility into those changes as at launch.
- Evaluate agent software and supporting infrastructure as separate components;
  some may be opaque, and some controls sit with the provider. Know what is
  observable, what the provider owns, and what evidence it can supply.
- Keep an inventory of agents and runtimes. Use workforce identities (the person or
  organization behind a task) and workload identities (the runtime doing it) in
  access decisions; independent controls enforce each task's authority. Meaningful
  changes to access or environment trigger a new review.
- **Balancing usability with security**: friction that blocks legitimate work
  drives users to less governed alternatives. Start with a clear purpose and narrow
  access; expand as evidence shows limits work; before expanding, confirm the added
  authority is approved and that monitoring and recovery still cover it.

### Observability, detection, and response

- Once actions are attributable, observe runtimes doing delegated work.
  Agent-native telemetry and harness access controls (e.g. "guardian agents" that
  quickly evaluate and authorize access) help, but traditional security logging and
  incident review stay essential.
- Telemetry sources: access gateway (what was attempted, under what authority);
  endpoint (state of agent and workload); harness (why and for what purpose, which
  credentials, and, with guardian agents, why access was granted). Together: intent,
  action, posture.
- Minimum collection: initiating principal, agent identity, and task; relevant
  context and policy (minimized or redacted); tool action and destination; approvals
  and enforcement decisions; result and material effect; correlation with existing
  security telemetry.
- Response: platforms should let responders stop unsafe work, revoke the authority
  behind it, contain the capability or destination, and check whether data crossed
  the boundary. **Stopping execution and revoking authority are separate**: ending
  a task may not invalidate a token issued to another service, and revoking a
  credential does not stop work in progress.
- Present attempt, policy decision, and downstream effect with linking identifiers,
  so a blocked attempt can be told apart from a completed unauthorized effect.
- Evidence does not need bulk content collection; keep references and decision
  metadata, minimize private content, and avoid creating leakage when agents review
  evidence.
- Responders must be able to: stop running agents; revoke their credentials;
  observe their actions; understand the data they sent and received.

### Responding to an incident

- An agent incident is a failure or misuse that creates, or could plausibly create,
  an unauthorized effect. Connect task and action chain to impact.
- Severity follows effective blast radius and completed effect: what changed, what
  is still active, which other deployments may be exposed.
- Four stages: stop, contain, recover, learn. Stop active work and remove the
  narrowest risky capability; repair state; feed lessons into policy and tests.
- Agents can reconstruct activity and recommend containment, but automated response
  should be limited to pre-approved, bounded containment; humans keep judgment on
  material or ambiguous incidents.
- Per production deployment: document who responds, how to stop unsafe work, and
  what is needed to resume; run response drills before broad autonomy, including a
  compromised capability and an attempted sensitive-data transfer.

## CISO first-actions checklist

1. **Know your agents** — inventory of pilot and production deployments with owner,
   purpose, reachable systems and data, and possible actions.
2. **Prioritize by potential impact** — effective blast radius, actions that
   complete without another decision point, reversibility.
3. **Set a clear expansion gate** — before widening reach, document failure and
   abuse scenarios, influences on decisions, and which actions need approval.
4. **Keep authority scoped to the task** — only the access and duration needed;
   independent checks before sending funds, changing records, or contacting
   customers.
5. **Test safeguards under realistic conditions** — malicious instructions in
   retrieved content and inappropriate tool calls; verify that responders can stop
   the agent or revoke access.
6. **Reassess meaningful changes** — new tools, data, autonomy, or environments.
7. **Plan for intervention** — see who authorized a consequential action, what the
   agent did, and what changed; be able to stop and investigate.

## Next steps

- Start by finding existing deployments, assigning owners, and assessing impact;
  establish which controls the enterprise vs the provider manage, where approval is
  needed, and how detection and response work.
- Use revocable, short-lived credentials where possible; manage longer-lived ones
  securely and outside the agent's context window.
- Define authority with enforceable controls around sensitive data, critical
  systems, and consequential actions; keep ownership, visibility, and the ability
  to intervene.

# Zero Trust for AI Agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/zero-trust-for-ai-agents
> Content: PDF eBook https://cdn.prod.website-files.com/6889473510b50328dbb70ae6/6a1611a04085d7cd3dadc924_Claude-eBook-Zero-Trust-for-AI-Agents-05182026.pdf (36 pages)
> Publisher: Anthropic (claude.com articles) · Date: 2026-05-27 (landing-page byline). The PDF itself carries 2026-05-18 (PDF CreationDate metadata and the `05182026` filename suffix). This capture uses the landing-page byline date.
> Captured: 2026-10-12 via curl (landing page HTML and PDF), PDF text extracted with pypdf (condensed).

Landing page: Category Best practices; Product Claude Security; reading time 4 min. No author named. The PDF says it reflects Anthropic's current thinking and is not legal, compliance, or security assurance. Condensed paraphrase; numbers and identifiers kept.

## Landing page summary

- Frontier models compress vulnerability-to-exploit time from months to hours. Agent deployments face this twice: their infrastructure is exposed like the rest of the estate, and the agents themselves interpret goals, pick tools, and run multi-step operations. Traditional access control does not stop misuse of legitimate permissions; monitoring must account for attacks that succeed by persistence.
- Zero Trust needs new shape for agents: cryptographically rooted identities, per-task permissions, memory protected from poisoning, defensive operations at attacker speed.
- Guide contents (as listed on the landing page): agent-specific security considerations; threat landscape (prompt injection, tool poisoning, identity/privilege abuse, memory poisoning, supply chain); "a three-tier Zero Trust framework (Foundation, Advanced, and Optimized)"; an eight-phase implementation workflow; agentic security operations ("Agentic SOAR"); compliance alignment for healthcare, finance, government. **Note:** the PDF names the tiers Foundation, Enterprise, and Advanced, not Foundation/Advanced/Optimized.

## Table of contents (PDF)

Building for the next threat landscape (p3) · The principles behind Zero Trust (p4) · Part I: Security considerations for autonomous systems (p5) · Part II: Current threats to agentic systems (p8) · Part III: Applying Zero Trust to agentic AI services (p12) · Part IV: Agent implementation workflow (p22) · Part V: Defensive operations at the speed of autonomous threats (p31) · From principles to practice (p34; headed "Chapter 6").

## Building for the next threat landscape

- Perimeter defense cannot keep up. Models cut exploit timelines to hours at a marginal cost of dollars. Attackers can also reverse-engineer defenders' patches into exploits.
- Best-positioned organizations: fundamentals strong enough that AI scanning finds fewer bugs, and agent deployments architected for breach from day one.
- Four goals: tiered framework for foundational capabilities; trending threats and mitigations; implementation workflow; defensive operations at autonomous-threat speed. Parts I–II are for CISOs (threats, compliance); Parts III–V for architects and engineers.

## The principles behind Zero Trust

- History: Stephen Paul Marsh formalized Zero Trust in his 1994 doctoral thesis (University of Stirling). NIST SP 800-207 Zero Trust Architecture (2020); NSA Zero Trust Implementation Guides (ZIGs) (2026).
- Premise: trust nothing, verify everything, assume breach. Three principles: **never trust, always verify** (inside-network requests get the same scrutiny as external); **assume breach** (limit damage; segment by identity; one compromise must not open others); **least privilege** (minimum access per task).
- **Design test — "impossible, not tedious":** ask whether a control makes the attack impossible or only tedious. Friction-based mitigations (extra pivot hops, rate limits, non-standard ports, SMS MFA) degrade against agentic attackers with unlimited patience and near-zero per-attempt cost. Survivors: hardware-bound credentials, expiring tokens, cryptographic identity, network paths that do not exist. When in doubt, remove a capability rather than throttle it.

## Part I: Security considerations for autonomous systems

### What makes agentic systems different
- **Autonomy:** multi-step work without per-step human approval; a manipulated agent harms at machine speed.
- **Tool access:** APIs, databases, file systems, external services, including MCP; a compromised MCP stack enables data theft, malicious code execution, sabotage.
- **Making decisions:** interpreting instructions introduces exploitable ambiguity.
- **Context persistence:** cross-session memory creates new data-protection needs.
- **Multi-agent coordination:** trust relationships let attackers compromise one agent and pivot to systems it could not reach directly.

### Agentic security concepts
- **Blast radius:** potential damage if something goes wrong (read-only single DB = small; cloud admin = enormous). Match investment to exposure; assume every agent's blast radius will be tested.
- **Least agency** (term coined by OWASP): extends least privilege by restricting what each agent tool can do, how often, and where. Examples: database tool gets read-only queries; email summarizer gets no send/delete; an API gets minimal CRUD.

### Regulated industries and compliance requirements
- Zero Trust aligns with existing regulation; regulators will likely fold it in. US, UK, and Australia have published guidance; the US requires all federal agencies to adopt Zero Trust by 2027. Table: Australia — homeaffairs.gov.au "Guiding principles of Zero Trust"; UK — NCSC "Introduction to Zero Trust"; US — CISA Zero Trust Maturity Model, NSA ZIGs, NIST SP 800-207.

## Part II: Current threats to agentic systems

OWASP-identified threats: prompt injection, tool and resource hijacking, identity and privilege abuse, memory and context poisoning, supply chain.

### Prompt injection and instruction manipulation
- **Direct:** crafted input overrides system instructions (explicit overrides, Base64/hex encoding to evade filters, adversarial suffixes). Research shows algorithmic attacks reaching 100% success with prompts that transfer across model families.
- **Indirect:** instructions embedded in web pages, emails, etc. Microsoft Research: LLMs cannot reliably distinguish informational context from actionable instructions. The user never sees the payload.

### Tool and resource misuse
- Agents can misuse tools within granted privileges; access control cannot stop that.
- **Tool poisoning:** compromised MCP tool descriptors, schemas, or metadata; hidden commands in metadata exfiltrate data. **Rug pull:** a legitimate tool secretly replaced with a malicious one. First documented in-the-wild malicious MCP server impersonated an email service and copied all sent emails.
- **Tool chaining:** legitimate tools combined harmfully (internal CRM + external email to exfiltrate customer data). Runs through trusted binaries under valid credentials, so host-centric monitoring sees nothing.
- **Resource exhaustion:** loop amplification calls costly APIs repeatedly → DoS or billing spikes.

### Identity and privilege abuse
- Agents often run with elevated privileges or service accounts; human-oriented identity systems fit poorly.
- **Unscoped privilege inheritance:** a high-privilege manager agent delegates with its full access context to a worker that should be limited. Also the **confused deputy**: a compromised low-privilege agent relays valid-looking instructions to a high-privilege agent that does not verify the original user's intent; amplified when agents routinely delegate.
- **Memory-based privilege retention:** agents cache credentials or keys without memory segmentation; an attacker prompts actions their own credentials would not allow, using secrets cached from an earlier session.

### Supply chain and dependency risks
- Agentic systems compose capabilities at runtime (tools, personas), beyond what software composition analysis covers; frontier models readily recognize signatures of known, already-patched vulnerabilities in unpatched upstream components.
- **Model supply chain:** poisoned weights or fine-tuning data. Anthropic research: 250 malicious documents can backdoor LLMs from 600 million to 13 billion parameters; backdoors persist through SFT and RLHF.
- **Tool/framework supply chain:** MCP servers, API integrations, frameworks. PyTorch dependency-confusion attack exfiltrated data including SSH keys at install. About 100 malicious AI models found on major platforms, some opening reverse shells when loaded.
- Most supply chains are open source without SLAs. Use OpenSSF Scorecard (scores branch protection, fuzzing coverage, signed releases, maintainer activity; runs in CI; flags unmaintained packages). Third-party risk management should ask vendors how they prepare for accelerated exploit timelines and whether they scan their own code.
- Redundant libraries (several HTTP clients, JSON parsers) add attack surface; a one-hour audit pointing a frontier model at the lockfile often finds consolidation worth doing.

### Memory and context poisoning
- Corrupted persistent memory biases future reasoning or aids exfiltration across all future sessions.
- **RAG poisoning:** malicious data enters vector databases via poisoned sources, direct uploads, or over-trusted pipelines.
- **Shared context poisoning:** in multi-tenant environments, injected data influences later sessions of other users. **Long-term memory drift:** summaries or peer-agent feedback gradually shift stored knowledge or goal weighting; no single change looks malicious.
- Chasing threats keeps you reactive; Zero Trust is the durable foundation.

## Part III: Applying Zero Trust to agentic AI services

Tiers (each builds on the previous):
- **Foundation:** minimum viable security for smaller or initial deployments; for most, adequate only for small businesses and teams. Because of AI-accelerated offense, the Foundation floor has been raised: friction-only controls no longer qualify.
- **Enterprise:** where most organizations should aim (larger teams, multiple deployments, meaningful business impact).
- **Advanced:** aspirational for most; baseline for highly regulated, national-security, or severe-consequence deployments.
- Expect Advanced to become Enterprise standard and Enterprise to become Foundation as tooling matures.

### Agent identity and authentication

**Agent identity verification** — without distinct identities there is an attribution gap and least agency cannot be enforced.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Unique cryptographic identifiers per agent instance | Persistent IDs backed by cryptographic material, not labels; track lifecycle creation→retirement; IDs in all logs and access requests |
| Enterprise | Certificate-based auth with full lifecycle management | X.509 certificate per agent; required for all service connections; rotation and revocation |
| Advanced | Hardware-backed identity with attestation | Credentials in HSMs or TPMs; remote attestation before access; confidential-computing enclaves for sensitive operations |
- Labels alone are a labeling exercise; cryptographic identity enables non-repudiation. Hardware-backed identity is increasingly recommended as the target state for any internet-reachable production system.

**Service authentication** — static API keys and shared service-account passwords are among the first things model-assisted attackers find; not acceptable even at Foundation.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Short-lived IdP-issued tokens with automatic refresh | OAuth 2.0 or similar; expiry in minutes; automated refresh; never embed credentials in code or config |
| Enterprise | Mutual TLS with certificate pinning | Client and server certificate validation; pin expected certs; certificate transparency monitoring |
| Advanced | Hardware-bound credentials with attested issuance | Bind auth material to hardware so it cannot be exfiltrated; root every service-to-service call (including between production services) in attested hardware |
- Rotated API keys are a known gap, not Foundation: rotating a credential that can be grepped from a lockfile barely raises attacker cost.

### Access control and privilege management

**Permission models**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | RBAC with deny-by-default | Roles per agent function; minimum permissions; block all not explicitly granted; a start, not a destination |
| Enterprise | ABAC with context-aware policies | Time, location, data sensitivity, risk score in decisions; dynamic adjustment |
| Advanced | Continuous authorization with real-time policy evaluation | Authorize each action, not session start; threat intel and behavioral analytics; revoke immediately when risk changes |
- Example: an email-drafting agent needs email permissions, not the finance file share; ABAC can restrict to operating hours.

**Privilege scoping** — static grants persist indefinitely; dynamic scoping limits exposure windows.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Static least-privilege roles per agent function | Define at deployment; periodic review/certification; remove unused |
| Enterprise | Dynamic privilege adjustment per task | Elevate only for tasks needing it; return to baseline; log all changes |
| Advanced | Just-In-Time (JIT) and Just-Enough-Administration (JEA) with automatic expiration | Grant at moment of need; scope to resources and durations; auto-revoke on completion or timeout |

**Resource boundaries** — identity-based isolation is the primary control; network segmentation is a backstop (attackers pivot through segment boundaries if services accept any caller from that network). Enforce at the receiving end: each workload has a cryptographic identity; each service accepts only callers its policy names.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Identity-based isolation backed by network segmentation | Cryptographic workload identity; services accept only named callers; segmentation as backstop; block unnecessary east-west traffic |
| Enterprise | Sandboxed execution per agent | Containers with restricted capabilities; runtimes like gVisor for syscall filtering; limit mounts and network; table stakes for any agent handling untrusted input |
| Advanced | Hardware isolation with confidential computing | AMD SEV or Intel TDX; microVMs on lightweight hypervisors; attest environment integrity |
- Sandboxing is mandatory, not aspirational, for agents processing web content, documents, or other untrusted input.
- Pro-tip (Claude Code): deny-by-default permissions requiring approval for each write and execute; sandboxed execution with OS-level filesystem and network isolation; writes confined to the project directory; managed settings that enforce org-wide permission policies users cannot override.

### Observability and auditing
- Capture what agents did, why, and who authorized it.
- **Before other detection investment, instrument two metrics:** dwell time (anomaly occurrence → human awareness) and coverage (fraction of alerts actually investigated). AI automation moves these most.

**Action logging**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Comprehensive logs with timestamps and context | All tool invocations, data access, external communications; agent identity, action details, request context; retention per regulation |
| Enterprise | Immutable audit trails with integrity verification | Append-only storage; cryptographic integrity verification; replication against single-point tampering |
| Advanced | Real-time streaming to SIEM with correlation | Centralized monitoring; correlate with other security events; real-time alerting |

**Traceability** — links actions back to the triggering event.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Request IDs linking agent actions to triggering events | Unique ID per user request propagated through all resulting actions; filter logs by request chain |
| Enterprise | Distributed tracing across multi-agent workflows | OpenTelemetry or similar; timing and dependency info; visualize flows across agent boundaries |
| Advanced | Full provenance chains from input to output | Record retrieved context, tool outputs, reasoning steps; replay decisions for audit; support algorithmic-explainability requirements |
- Auditing covers events on systems agents touch; traceability covers the agent's own actions (internal actions, tool calls, sub-agent spawns).
- Pro-tip (Claude Code): OpenTelemetry metrics; audit logging for all operations in cloud environments; natural-language descriptions of complex commands; `ConfigChange` hooks that audit or block settings changes during sessions.

### Behavioral monitoring and response

**Baseline establishment**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Manual definition of expected behavior | Document intended capabilities and access patterns; define alert boundaries; update as functions evolve |
| Enterprise | Automated baseline learning | Statistical baselines of tool usage, access frequencies, data volumes |
| Advanced | Continuous refinement with drift detection | Update baselines as behavior legitimately evolves; detect gradual drift (slow poisoning); alert on sudden and gradual change |
- Baselines feed ABAC (flag out-of-pattern requests) and serve as a recovery point (restore to known-good state).

**Anomaly detection**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Threshold alerts plus automated first-pass triage | Thresholds on API call rates, data volumes, error frequencies; route every alert through automated first-pass investigation before a human |
| Enterprise | Statistical anomaly detection, tunable sensitivity | Statistical methods; balance detection vs false positives; correlate across metrics |
| Advanced | ML behavioral analysis with context | Models trained on normal behavior; time of day, user activity, business cycles; catch subtle anomalies |

**Automated response** — rule: automate the bookkeeping around incidents, not the decisions. Models take notes, capture artifacts, run parallel investigation tracks, draft the postmortem; humans make containment, disclosure, and customer-communication calls.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Alerting to security teams with model-drafted triage context | Triage agent produces a structured disposition (query, think, report) before a human sees the alert; procedures for common alert types |
| Enterprise | Automatic containment (session termination, access revocation) | Automated responses for high-confidence threats; terminate sessions; revoke credentials pending investigation |
| Advanced | Orchestrated playbooks with graduated escalation | SOAR for automated investigation/response; graduated by severity; coordinate containment across systems |
- Pro-tip (Claude Code): command-injection detection that flags suspicious commands even when they match allowlisted patterns; fail-closed matching (unrecognized commands require manual approval); context-aware analysis of the full request.

### Input validation and output controls

**Input sanitization**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Basic validation and length limits | Validate formats against schemas; max lengths; reject malformed |
| Enterprise | Content filtering for known attack patterns | Pattern matching for known injection techniques; filter encoded payloads; block suspicious instruction patterns |
| Advanced | Multi-layer validation with constitutional classifiers and spotlighting | Multiple detectors in sequence; AI classifiers trained on adversarial examples; spotlighting to delimit untrusted content |
- Unlike SQL injection, agent inputs are freeform; simple rules are insufficient. Spotlighting uses a known schema to help the model separate system instructions from (less trusted) user input. Constitutional classifiers can also be trained as input/output guards if you build your own models.
- Pro-tip (Claude Code): input sanitization against command injection; a command blocklist blocking risky commands like `curl` and `wget` by default; web content processed in a separate, isolated context window; network request approval gating all outbound connections.

**Output filtering**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Filtering for sensitive data patterns | Scan for PII, credentials, sensitive business data; block or redact; log events |
| Enterprise | Semantic analysis before delivery | Analyze meaning; detect encoded sensitive data; identify social-engineering outputs |
| Advanced | Human-in-the-loop approval for high-risk actions | Human review before significant actions; clear descriptions; log approvals |
- Input sanitization protects the agent from attackers; output filtering prevents data loss. Human-in-the-loop is valuable at any tier and required for high-risk actions.

### Integrity and recovery

**Configuration integrity** — attackers who cannot manipulate inputs target configuration.
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Version-controlled configurations | VCS; reviewed changes; full history |
| Enterprise | Signed configurations with deployment verification | Sign approved configs; verify before deployment; reject unsigned/invalid |
| Advanced | Immutable infrastructure with attestation | Immutable images; attest before execution; replace rather than modify running agents |
- A modified configuration can be as damaging as a code vulnerability and easier to exploit.
- Infrastructure reflex: enable automatic updates wherever an update-caused outage is acceptable; delay is now the main risk. "Auto-update on" and "verify signatures" are complementary: signed updates from trusted suppliers flow automatically; unsigned changes are rejected.

**Recovery capabilities**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Documented rollback procedures | Steps to restore previous versions; test periodically; keep prior versions |
| Enterprise | Automated rollback with health checks | Verify health on deploy; auto-rollback on failure; deployment history |
| Advanced | Self-healing with automatic remediation | Auto-restart; circuit breakers isolating failing components; auto-provision replacements |
- Pro-tip (Claude Code): version-controlled settings (permission configs and MCP server allowlists in source control); managed settings users cannot override; isolated cloud VMs with automatic cleanup as immutable execution environments.

**AI governance policies**
| Tier | Capability | Implementation |
|---|---|---|
| Foundation | Documented acceptable-use and incident-response policies | Allowed/prohibited uses; IR procedures for agent compromise; who approves deployments; address Shadow AI |
| Enterprise | Formal governance framework with stakeholder oversight | Cross-functional AI governance committee (security, legal, compliance, business); approval for new agents; agent-specific risk assessment; regular reviews |
| Advanced | Continuous policy enforcement with automated compliance checks | Policy checks in deployment pipelines; automated violation detection; compliance metrics; audit trails of governance decisions; update from incidents |
- Shadow AI bypasses every control. Goal: move enforcement from periodic review into pipeline checks.
- Pro-tip (Claude Code): managed settings; managed-only restrictions such as `allowManagedPermissionRulesOnly` (users cannot define their own permission rules); server-managed settings delivered via MDM or OS-level policies.

## Part IV: Agent implementation workflow

### Phase 1: Identify requirements
- Regulatory requirements, operational goals, constraints; align security, legal, compliance, business before building.

### Phase 2: Manage supply chain risks
- **AI Bill of Materials (AI-BOM):** extends SCA to model provenance, training-data lineage, fine-tuning parameters. OWASP's AI-BOM extends CycloneDX ML-BOM; available as a web tool. If not running local LLMs, consider the provider; Anthropic was one of the first AI companies certified to ISO 42001.
- **Evaluate dependency health automatically:** OpenSSF Scorecard in CI next to the AI-BOM.
- **Audit the dependency tree for redundancy:** point a frontier model at the lockfile; typically a one-hour exercise.
- **Narrow remediation with reachability analysis:** fix the smallest set that matters; continuous delivery with regression tests to ship patches fast.
- **AI vendoring for small unmaintained dependencies:** for poor-Scorecard, unmaintained small deps, have a frontier model reimplement the subset you use; treat as standard practice.
- **Cryptographic signing:** sign models and software at every stage through production; verify at runtime, not only at deployment.
- **Vendor assessments:** review tool providers' security practices, update mechanisms, incident history, vulnerability response; validate components at runtime; ask about AI-accelerated exploit preparation and self-scanning. Applies to FOSS: download and assess code; evaluate community size and support history.
- Pro-tip: run and host the MCP server yourself on an immutable platform after verifying its code; sign it yourself; repeat for updates before production.

### Phase 3: Define agent boundaries
- **Assign a unique identity:** cryptographically rooted, persistent; enables log correlation and traceability. Pro-tip (Claude Code): unique `session.id` per session, with `user.account_uuid` and `organization.id` on all telemetry events.
- **Approved/prohibited actions:** write them down (read customer records, summarize, draft responses — not "help with customer service"). Enforce through permissions, not just instructions. Pro-tip: Claude Code supports granular control in `settings.json` (global and project level, plus environment variables).
- **Escalation triggers:** what needs human review (high-value transactions, sensitive data categories, external communications); thresholds balancing security and efficiency. Claude Code: `settings.json` "ask" parameter and hooks.
- **Scope limits / least agency:** limit the accounts given to agents (e.g., certificate-auth DB API limited to read, and only needed data). Deny by default. Pro-tip: split functions across multiple agents to compartmentalize; each needs its own unique ID and its own credentials — shared credentials defeat compartmentalization.
- **Identify the blast radius:** apply the impossible-vs-tedious test; if containment relies on friction (many requests, rate limits), assume it fails; tighten settings until risk is acceptable.

### Phase 4: Defend against prompt injection
- Address direct and indirect attacks. Beyond escalation triggers and scope limits: input isolation, constitutional classifiers, reduced attack surface.
- **Input isolation:** treat all natural-language input as untrusted. Microsoft's Spotlighting cut indirect-injection success from over 50% to under 2% by delimiting untrusted content.
- **Constitutional classifiers:** AI detectors on prompts and responses; Anthropic's approach blocked 95% of jailbreak attempts in testing with minimal increase in over-refusal.
- **Limit attack surfaces:** restrict who or what can interact with the agent to trusted personnel and resources.

### Phase 5: Secure tool access
- **Tool allow-listing:** explicit permitted tools per agent function; reject unlisted invocations. Control at two fronts: at the agent (allow/deny permissions) and outside the agent in case it or its environment is compromised — require tool authentication (certificate-based on the API, or short-lived tokens bound to the calling agent's identity). Static API keys unacceptable for tool auth even at Foundation. Pro-tip: Claude Code tool permissions in `settings.json`.
- **Capability restrictions:** e.g., email tool read-only with send needing separate authorization; DB queries but no schema changes; RBAC on provisioned accounts (e.g., Active Directory).
- **Parameter validation:** validate tool-call arguments on both agent side and tool side. Pro-tip: Claude Code `PreToolUse` hook to validate parameters before sending.
- **Sandbox execution:** containers and/or microVMs with restricted network, limited mounts, syscall filtering. Add rate limiting, spending controls, and circuit breakers on usage thresholds or ABAC baseline deviation — but rate limits are friction, not barriers. Pro-tip: Claude Code sandboxing with filesystem isolation, network isolation, OS-level enforcement.
- **Approval escalation:** high-risk tool invocations pause for human review with clear descriptions; log approvals for forensics. Pro-tip: in Claude Code all tool calls require human approval by default; more granularity via `settings.json`; pre- and post-tool hooks.

### Phase 6: Protect agent credentials
- Shared credentials or generic service accounts mean one theft reaches everything. Treat static API keys, embedded credentials, and shared passwords as already compromised.
- **Short-lived, IdP-issued credentials as baseline:** minutes, not days; automated refresh. Where resources permit, a CA that enrolls agents, issues short-lived certs, and runs CRLs or OCSP. Without PKI expertise, use cloud-native managed identity and secret managers such as HashiCorp Vault. Pro-tip: Claude Code supports OAuth 2.0 with automatic token refresh for MCP servers; "ask" permissions granted in a session are session-scoped and expire at session end.
- **Hardware-bound credentials for production and sensitive workloads:** bound to attested hardware so material cannot be exported from a compromised host; applies to service-to-service and human-to-service calls. Phishing-resistant 2FA (FIDO2 or passkeys) by default; SMS codes do not meet the Foundation bar.
- **Credential isolation:** unique credentials per agent instance; inject at runtime from secrets managers that log access and support emergency revocation; never in code or config. Pro-tip: Claude Code stores API credentials in the OS credential store; the `apiKeyHelper` setting runs a script at runtime to fetch secrets from external vaults.
- **Explicit trust boundaries:** agents verify identity and authorization of other agents before accepting delegated tasks; authorize at each step; log inter-agent communication; flag unusual delegation. Pro-tip: Claude Code sub-agents are ephemeral extensions of the parent with up to the same permissions; externally indistinguishable from the parent, but visible via OpenTelemetry or the JSONL transcripts in the Claude Code projects folder.
- **Just-in-time (JIT) access:** request credentials per operation, scoped and time-bound; no cached credentials to steal; lifetimes in minutes. Advanced and hard; implement even partially.
- **ABAC:** evaluate agent identity, resource sensitivity, action, time, source location, risk score; e.g., step-up auth for sensitive records, allow routine queries but block bulk exports. Advanced; factors are yours to choose.

### Phase 7: Safeguard agent memory
- **Memory isolation:** strict boundaries between sessions and users. Pro-tip: Claude Code isolates sessions by default; each starts fresh; sub-agents run in their own context windows without the parent's history.
- **Context integrity validation:** cryptographic hashes plus source attribution per memory element; validate at every retrieval, not just storage; tag source and conditions of addition; store hashes in tamper-resistant logs separate from content; on failure reject the context and alert.
- **Context retention policies:** TTLs; auto-expire unverified memory; shorter retention for high-risk context (external inputs, unverified tool outputs). Versioned memory stores for rollback; quarantine suspect content for forensics before deletion; test rollback; define when to purge fully vs remediate. Pro-tip: Claude Code `cleanupPeriodDays` sets local transcript retention; checkpoints before each edit allow rewind (`Esc+Esc` or `/rewind`) of code, conversation, or both; enterprise server-side retention defaults to 30 days.

### Phase 8: Measure what matters
- **Dwell time and coverage** first (as above).
- **Explainability:** trace any action to its triggering input and explain the choice; mandatory for regulated data. Test questions: would we know within an hour if an agent went rogue? Can the team take time off without worrying about undetected misbehavior?
- **Behavior:** baselines during controlled deployment; track tool usage patterns, output characteristics, decision distributions; define acceptable variance; catches gradual memory-poisoning drift and slow supply-chain attacks.
- **Detection speed:** anomaly → human awareness; target within an hour for critical systems.

## Part V: Defensive operations at the speed of autonomous threats

- Exploits appear within hours of patches; agentic adversaries can hit hundreds or thousands of systems in the time a human reviews one alert.
- **The case for autonomous defense:** move humans off bookkeeping and onto decisions. Automate evidence collection, enrichment, correlation, documentation; humans keep containment, disclosure, and customer-comms calls. Human decision speed should never be rate-limited by evidence collection or write-ups.
- **Put a model at the front of your alert queue:** every alert gets an automated first-pass investigation by a triage agent with read-only SIEM access and scoped query tools. Practical start: one noisy rule with known-high false positives; read-only data access; structured disposition for every firing; measure agreement with a human reviewer for two weeks; if tolerable, expand to the next rule; do not automate the whole queue at once.
- **Agentic security orchestration (Agentic SOAR):** adaptive responses beyond playbooks, within seconds: quarantine/isolation, dynamic access-control changes, session termination, credential revocation — through the identity-based isolation and short-lived-credential infrastructure from Part III.
- **Map detection coverage against MITRE ATT&CK:** prioritize lateral movement and credential access. Atomic Red Team (open-source small safe tests mapped to ATT&CK): run a handful and check what logging detected — a one-afternoon coverage map.
- **Tabletop for five simultaneous incidents, not one:** five critical CVEs with working exploits in one week; plan for an order-of-magnitude increase in finding volume; spreadsheet-and-weekly-meeting workflows will not keep up.
- **Emergency change procedures in advance:** a two-week change-approval cycle is itself a security risk; pre-decide who authorizes patches and containment (take service offline, rotate credential, block path), how fast, with what evidence; rehearse.
- **Trust through verification for defensive agents:** verified integrity (hardened environments; compromised defensive agents are powerful); limited blast radius (least privilege; scoped actions); clear escalation paths (alerts for human review; high-impact responses need human approval even when recommended). Log, trace, and review defensive agents like any agent.

## From principles to practice (Chapter 6)

- Verify every action, grant minimum permissions, contain damage. Identity → attribution and access control; observability; behavioral monitoring; input/output controls; integrity and recovery; defensive ops at threat speed. Skipping one capability leaves a gap.
- Start at Foundation, but the raised floor now includes short-lived tokens, cryptographically rooted identity, identity-based isolation, and automated first-pass triage as entry requirements. Tiers are a roadmap, not a finish line.
- Regulated industries: HIPAA, FINRA, GDPR, FedRAMP, and the EU AI Act already impose aligned requirements.
- Architects: start at Foundation, validate controls, advance tiers; keep the impossible-vs-tedious test as a standing design-review question. Pointer to "Preparing your security program for AI-accelerated offense".

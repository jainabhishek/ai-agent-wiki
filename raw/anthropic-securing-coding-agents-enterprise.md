# The enterprise guide to securing coding agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/enterprise-guide-to-securing-coding-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-11-23 (page byline)
> Author: no byline. The page quotes Jason Clinton (Deputy CISO, Anthropic) and Patrick Collison (Stripe).
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase; headings, numbers, setting names, and identifiers kept. Diagrams are described only by their captions.

Page metadata: Category Best practices; Product Claude Code; reading time 18 min. Subtitle: how security and technical leaders understand and bound risk as they scale Claude Code.

## Shipping fast and secure

- Coding agents already write code and open pull requests at most organizations; at many large enterprises they also review, test, and merge it.
- Salesforce (footnote 1: Salesforce Ventures is an investor in Anthropic) reported, after standardizing on Claude Code: **79%** more pull requests merged per developer and **5%** fewer total incidents.
- Leaders must mitigate risks such as prompt injection and privilege abuse with layered controls (checked permissions, bounded environments).
- Structure: chapters 1–2 scope the risk (provider requirements; four agentic risks). Chapters 3–5 bound the risk (defensive layers in Claude Code; central management and enforcement).
- Diagram caption: defending an agent has three components — the model, the environment around it, and external checks on inputs and outputs.

### How this guide fits with the AI-Native SDLC Playbook

- Companion: the AI-Native SDLC Playbook covers redesigning development around agents, stage by stage. This guide covers the security controls under that work. The playbook decides where agents fit; this guide decides what they may do there.
- Audience: Claude Team and Enterprise plans. The same principles and local controls apply through AWS, Google Cloud, or Microsoft Azure.

## 01 Setting the bar for agent security

Quote (Jason Clinton, Deputy CISO at Anthropic), paraphrased: the CISO's job with agentic AI is not zero risk; it is to make agentic risk "legible and bounded", so the business deliberately accepts what it can manage.

### Six questions for every coding agent

| Question | Why it matters | Good answer | Weak answer |
|---|---|---|---|
| Does the model refuse when it should? | It is the first line against a harmful request. | Refusal trained into weights, with published rates. | A system prompt tells the model to decline. |
| Does something outside the model inspect actions before execution? | External checks catch a tricked model or bad judgment. | Command static analysis; a second evaluator model; injection probes. | Reliance on model capability. |
| Does the environment bound blast radius? | Bounds incident severity. | A kernel-level sandbox admins can mandate in fail-closed mode, or one isolated VM per session; network-layer egress allowlisting. | The agent is told to stay in the working directory. |
| Can policy be locked centrally? | Sets minimums individuals cannot undo. | Managed settings whose hard denies no local user can override. | Per-developer config plus an honor-system policy document. |
| Is the code the agent writes secure? | Code volume grows; checks must scale with it. | Automated security review; a human signs off on high-risk changes. | The model was trained to write secure code. |
| Can you reconstruct an incident? | Compliance and continuous improvement. | Exported session telemetry, an audit API (Enterprise), and a stated list of known gaps. | Logs can be requested. |

### Applying SaaS requirements to your AI provider

Hold AI providers to the existing SaaS checklist (SSO, role-based access, data terms, audit logs). Claude Code examples:
- SSO and RBAC (Enterprise).
- No training of generative models on code or prompts under commercial terms, unless the organization opts in to share.
- Enterprise Frontier Safeguards (phased rollout): zero-data-retention privacy combined with misuse-detection safeguards for highly capable models. Data can be encrypted with the customer's own keys and held for a limited time in storage the customer controls.
- Enterprise: once the HIPAA configuration is on, a BAA covers the Claude Code CLI and the desktop app's Code tab (local mode).
- Cloud encryption options: Amazon Bedrock with customer-managed AWS KMS keys; Google Cloud CMEK; Microsoft Foundry "Hosted on Azure".
- Anthropic Trust Center hosts the SOC 2 Type 2 report and the ISO 27001 certificate.

Sidebar "Getting cleared for security work": the Cyber Verification Program (CVP) gives qualifying security professionals advanced cyber capabilities and reduced blocking classifiers. Enterprise Frontier Safeguards lets eligible organizations keep data in cloud infrastructure under their own control.

## 02 Identifying AI-specific risks

Familiar risks (leaked credentials, abused privilege, compromised dependencies, insider threat) change in attack surface, speed, and scale with agents.

| Risk | Today's handling | What changes with an agent |
|---|---|---|
| Leaked credentials and privilege abuse | Least privilege, short-lived tokens, keyless auth (workload identity / OIDC), periodic review of accounts with too much access; people get named accounts and software gets a per-workload identity; credentials scoped to task or job. | The agent acts inside a developer's session; most logs outside Claude Code show only the developer's name. |
| Unvetted dependencies and extensions | Pinned versions, review gates, two reviewers on manifest changes, version-controlled config. | Agents add vetted and unvetted dependencies faster than people can review; an extension starts instructing the agent the moment it connects. |
| Data exfiltration | Network-layer egress allowlisting. | A compromised agent can use already-allowed services and can try many routes the attacker never had to define in advance. |
| Insider risk | Training against social engineering; verification; ways to report. | Becomes prompt injection; the control point shifts to tool calls and the network edge. |

### Risk 1: Leaked credentials and privilege abuse

- An agent can leak anything it can read, including long-lived AWS access keys or GitHub tokens.
- Mitigation: remove standing secrets. Keyless auth (workload identity, OIDC) issues a short-lived token per job or session. Keep any necessary token short-lived and narrow. Use hooks to block commits with secrets; enable secret scanning at push. Locally, the sandbox can hide credentials from commands. A cloud session cannot read the developer's machine, so its VM holds only secrets you put there (environment variables, files in an uploaded repository).
- By default a Claude Code agent runs under the identity of its supervising developer. Incident response may need to tell agent actions from developer actions.
- Mitigation: apply **least agency** (the agent version of least privilege). Evaluate tool calls against policy outside the model, so rules can reject requests beyond the user's or the task's permissions. Audit agent identities on the same schedule as other over-privileged or inactive accounts. Keep session transcripts and export OpenTelemetry data. In CI/CD, give the agent its own identity that you can scope and revoke without touching a developer account — Claude Code's GitHub Action runs as its own GitHub App (illustration: in the pipeline the agent's work appears under its own name).

### Risk 2: Unvetted dependencies and extensions

- Agents speed up dependency addition and configuration change. Example: asked to add JSON schema validation, an agent finds a package, adds the latest version, and has working code in minutes.
- MCP servers, plugins, skills, subagent definitions, and a repository's `CLAUDE.md` are dependencies too. Unlike a library that waits to be called, they reach the agent at load time; their descriptions and instructions enter the context window before any work.
- Mitigation: point agents at an internal registry of vetted packages and make it the only reachable registry through the egress allowlist. Cloud sessions permit public registries out of the box, so adjust shared-environment network access to match; a registry on a private network calls for self-hosted environments (public beta). Pin versions; use automated upgrade PRs so patches still land fast. Treat MCP servers, plugins, and skills the same way; use marketplace allowlisting.
- Enterprise: skill and plugin scanning inspects third-party skills/plugins for malicious content whenever one is uploaded or edited (illustration: admin view of a blocked plugin).

### Risk 3: Data exfiltration

- Every leak needs an exit. A domain allowlist cannot distinguish your account from an attacker's: allowing github.com lets the agent push to an attacker-owned repository.
- DNS is a second route that HTTP allowlists miss: data can be encoded in looked-up names.
- A leaked token needs no agent network at all; the attacker uses it from anywhere and egress filtering never sees it.
- Mitigation: allowlist per agent as narrowly as the proxy allows, down to organization or path. Route DNS through a filtered, logged resolver. Limit cloud storage access to expected roles and IP ranges. Use DLP to flag secrets and sensitive data in uploads. For Claude Code cloud sessions, the allowlist means the environment's domain-based network access setting. Teams needing their own proxy, DNS filtering, or traffic inspection should run self-hosted environments (public beta).

### Risk 4: Prompt injection

- OWASP's Top 10 for LLM Applications has put prompt injection at #1 in each edition since its 2023 start.
- Analogy: social engineering and prompt injection work alike. The deceived actor takes the action, so the system sees an authorized request; an injected agent acts with its own permissions and every log looks legitimate.
- Coding-agent injection channels: issue trackers and PR comments; dependency READMEs and changelogs; fetched web pages; MCP tool-call responses; source-file comments; and more.
- Mitigation: no single control works; combine judgment checks on inputs and planned actions with fixed boundaries that cap damage (diagram: what a hidden web-page instruction must pass).

## 03 The judgment layer

### Defending in layers

A compromised or misaligned agent in Claude Code must pass multiple controls across two layers.
- **Layer 1, judgment-based** (decides whether something looks wrong): alignment training (refuse malicious requests, favor cautious actions); prompt injection probes (in auto mode, scan incoming tool results before Claude acts and flag apparent injected instructions); the auto mode classifier (checks most proposed tool calls against the user's stated intent).
- **Layer 2, fixed boundaries** (caps what any command can do): before execution, permission rules, command analysis, and hooks test each action against your policy. The sandbox and egress allowlist then cap what an allowed command can touch and where data may flow.

### Understanding alignment training

- Claude is trained toward good judgment plus firm rules (e.g. no seriously damaging malicious code).
- Tested in Claude Code with production safeguards off, current Claude models declined **81%–85%** of malicious requests and completed **98% to 100%** of dual-use and benign requests (e.g. running reconnaissance tools, testing a site for vulnerabilities).
- Claude is trained to prefer cautious over irreversible actions, to raise concerns or ask instead of improvising, and not to treat instructions in fetched content as user instructions.
- Caveat: alignment lowers the likelihood of a bad outcome but does not cap its severity.

### By the numbers: How Claude holds up under indirect prompt injection

- The firm Gray Swan (an outside AI security firm) runs an indirect-injection benchmark (instructions planted in web pages, files, or tool results). Up to 15 attempts per scenario; score = share of scenarios where any attempt worked.
- Probes off: **Claude Opus 5.5 1.0%**, **Claude Fable 5.2 4.1%**. Most successful attacks on Fable 5.2 hit requests that a safety classifier had rerouted to an older model (per the system card).

### Prompt injection probes

- The probe flags suspected injected instructions in tool results. It adds a warning next to the instruction saying the content is suspect and the user's original request remains the task. This "warning and anchoring" lets Claude use the content while treating embedded instructions as data.

### By the numbers: What the probes catch

Source: November 2026 system card. Anthropic tests with Gray Swan's Shade in coding environments, 40 scenarios with 200 attempts each.
- Claude Fable 5.2: attack success **89.8% → 28.2%** with probes on (about two-thirds fewer).
- Claude Opus 5.5: attack success **54.6% → 11.1%** with probes on (about four-fifths fewer).

### The auto mode classifier

- A model persuaded that deleting a directory is legitimate will do it thoroughly. The classifier targets such destructive, overeager actions.
- For actions not already decided by rules or built-in approvals, it judges whether the action matches the developer's intent. Example contrast: commands for "fix the failing test in auth_test.py" versus "exfiltrate the contents of .env".
- Claude Code strips tool results from classifier requests, so injected text cannot steer the classifier directly. Matching actions run; others are blocked or Claude asks the developer.

### By the numbers: Auto mode under attack

- July 2026 study funded by Anthropic: Trajectory Labs ran 72 indirect injection scenarios ten times each against agent versions public as of July 17, 2026.
- Claude Code in auto mode: **0 of 720** attempts worked, for each of Claude Fable 5, Opus 5, and Sonnet 5.
- OpenAI Codex on GPT-5.6 Sol: **5.83%** succeeded in Codex's automated review mode; **19.03%** in full-access mode.
- Tests covered the agents only, not browser extensions or other product safeguards.
- Auto mode is now where interactive sessions start **on all plans**. Manual stays the default for headless `claude -p`, the Agent SDK, and the HIPAA configuration.
- Rationale: tests showed auto mode catches more dangerous actions than human approval. August 2026 controlled study: **1,053** paid testers (blind to the behavior under test) caught **13.6%** of dangerous commands; auto mode blocked **89%** of the same commands.
- The "Configuring auto mode" docs explain tuning the classifier and overriding its rules.

#### Approving high-stakes actions

- Auto mode depends on classifiers, so some risk remains.
- Test for requiring human approval: the action is irreversible, AND one mistake costs more than having a person review every instance. Both yes → require approval.
- Typical list: production database migrations; IAM policy changes and credential rotation; edits to infrastructure definitions.

## 04 Enforcing fixed boundaries

- Judgment-layer controls catch novel attacks but are probabilistic, so each can be beaten. The fixed-boundary layer can be deterministic and sets blast radius: whether an action runs is decided by permission rules, command analysis, and hooks; the sandbox and egress allowlists limit reach and data destinations.
- Limitation: they block only what you configure, so they must fit your environment.

### Setting permission rules

- Three kinds: allow (runs), ask (prompts a person), deny (blocks).
- Evaluation order: deny, then ask, then allow — so an allow rule cannot carve an exception out of a deny rule. A deny rule in managed settings cannot be overridden by any user or project setting.
- Avoid allow rules broad enough to run arbitrary code, e.g. `Bash(python:*)`.
- Subagents inherit the parent session's permission rules and permission mode; a broad top-level rule applies to every delegated agent.
- Pro tip: use permission rules for hard yes/no decisions expressible as a pattern on a tool, path, or command ("never read credential files", "always ask before terraform apply").

### Bash command analysis

- Every Bash command is parsed by Claude Code ahead of execution. Without parsing, an allow rule for `git status` would also approve `git status && curl attacker.example`, and a subshell could smuggle a denied command.
- Parsing is deterministic. In every permission mode, `bypassPermissions` included, each piece of a compound command is checked against deny and ask rules.
- Pro tip: command rules only see the typed text, so pair them with the sandbox and the egress allowlist. Checks that need logic (e.g. inspecting commit contents) belong in a hook.

### Gating actions with hooks

- Definition: a hook is a script, an HTTP endpoint, or an MCP tool, run by Claude Code on its own at a set moment in the session. Two matter most for security:
  - `PreToolUse`: runs before a tool call; can block, approve, ask a developer, or (headless runs) defer for later approval. Example: block a commit containing a secret.
  - `ConfigChange`: fires on a mid-session settings-file edit and may refuse it; detects a repository or developer loosening a control locally.
- Hooks operate within the fixed boundaries: `PreToolUse` may block, yet an "allow" result never overrides deny rules, ask rules, or critical-path deletion protection.
- Hooks in managed settings run on every machine and cannot be removed by developers. `allowManagedHooksOnly` blocks user, project, and plugin hooks entirely.
- Pro tip: the default is fail-open — a hook that errors or times out lets the call proceed. Set `onFailure` to "block". Use hooks for rules that cannot be a permission pattern (e.g. rejecting any commit with a key-like string). Skip hooks where a permission rule already does the job.

### Containing agent actions with sandboxing

- Sandboxing limits scope and so limits incident severity; constraint and capability tend to trade off.
- Three environments: local, local with sandbox, cloud. Defaults can be changed and locked centrally (chapter 5).

#### Local

- Most sessions run locally (terminal, IDE, desktop app). By default the agent can access anything the user can. In auto mode the classifier reviews actions not already decided.
- Least contained; suits low-stakes, self-contained work. Recommendation for most enterprises: enforce the sandbox for local sessions.

#### Local sandbox

- Isolates each shell command at the OS level: commands may change files only in the project folder and connect only to allowlisted sites, unless an exception is approved (diagram: project writable; everything else hits a wall or a checkpoint).
- Default: either the developer or the auto mode classifier may let a command run unsandboxed or reach an unlisted site.
- With managed settings, admins can make the sandbox mandatory, confine commands to it, and restrict sites to a central list.
- To stop credential reads outside the project: Read deny rules for credential paths, plus credential masking (commands can sign in while never seeing the real secret).
- Pro tip: combine strict sandbox mode with `failIfUnavailable`. Without it, if the sandbox cannot start, commands still run, unconfined.
- Pro tip: the sandbox runs on macOS, Linux, and WSL2, not native Windows; with `failIfUnavailable` on, Claude Code will not start on native Windows. Use WSL2, or the alpha Windows support in the open-source sandbox runtime (restricts file and network access).

#### Cloud sessions

- Run in an Anthropic-managed environment, one VM per task. GitHub credentials stay outside the VM.
- Suit work that reads untrusted content or runs unattended: isolated by default from the developer's machine and internal networks; VMs can be discarded any time.
- New cloud environment: limited pre-installed tools and allowed domains (developers can add exceptions); developers select which repos are cloned each session.
- Organization owners can set a default environment and publish shared environments whose settings developers cannot change. Developers can still create and modify their own environments. To lock this down, self-host sessions on infrastructure you run.
- Customer example, Stripe: engineers use isolated, disposable VMs ("dev boxes"), one per feature or branch; agents get a fresh one per task and run Claude Code inside. Patrick Collison (co-founder and CEO) says the boxes have no access to production data or services, so even a "catastrophic explosion" stays contained.
- Not available: cloud sessions for organizations on zero data retention, on the HIPAA configuration, or using customer-managed encryption keys.
- Pro tip: give sessions keys as network secrets, which stay outside the VM and are attached only to requests for named sites.

## 05 Enforcing policy

- Two configurations beyond defaults: **baseline** (alternative defaults developers can add to) and **locked** (rules developers cannot change). Locking turns written policy into an enforced control. The list is not exhaustive.

### Central settings at a glance

Local sessions are set in managed settings; cloud sessions in claude.ai admin settings.

| Dimension | Local sessions | Cloud sessions |
|---|---|---|
| Is it allowed? | Desktop app: can be disabled (`disableDesktopLocalSessions`); terminal: cannot. | Organization-level cloud sessions toggle. |
| How contained is it? | Baseline: every local session sandboxed (`sandbox.enabled`). Locked: sessions refuse to start without the sandbox, and commands cannot retry outside it (`failIfUnavailable`, `allowUnsandboxedCommands: false`). | Baseline: on the Cloud environments page, Owners publish shared environments that members cannot edit, and choose one as the org default. Locked: self-host Claude Code on your own infrastructure; Anthropic-hosted setups still let developers make personal environments. |
| Where can it connect? | Baseline: a managed approved-site list that developers may extend (`sandbox.network.allowedDomains`). Locked: developer additions ignored (`allowManagedDomainsOnly`). This list governs shell commands only; WebFetch needs separate permission rules. | Baseline: Anthropic's trusted list by default (package registries, GitHub, cloud SDKs), or network access Owners set per shared environment (connector, GitHub, and Anthropic API traffic is not limited by it). Locked: self-hosted environments (public beta) behind your own network boundary. Anthropic-hosted environments have no org-wide allowlist. |
| What can it read? | Baseline: deny reads of sensitive paths (`permissions.deny`). Locked: file tools read only inside the project, and named paths are blocked (`permissions.blockReadsOutsideWorkingDirectories`, `sandbox.filesystem.denyRead`). | Baseline: the same deny rules for reads. Locked: none fully; scoping the Claude GitHub App to approved repos controls clone and push, though developers can still upload a local repo from the terminal. |
| What credentials can it use? | Deny reads of credential files; turn on credential masking (`sandbox.credentials`). | Owners keep keys in Network secrets on shared environments; environment variables are not used for keys. |
| Which connectors can it use? | Baseline: approved list developers can extend (`allowedMcpServers`). Locked: only your list (`allowManagedMcpServersOnly`). | Desktop-app connectors bypass this list; org connector settings govern them instead. |
| What can it do without asking? | Baseline: deny and ask rules come from managed settings; developers may add allow rules. Locked: managed rules and hooks only, with bypass mode disabled (`allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `permissions.disableBypassPermissionsMode`). | (single row spanning both) |

### Which settings apply

- Managed settings arrive by three routes: server-managed (Claude admin console), an MDM/OS policy, or a managed settings file. Anthropic-hosted cloud sessions see the server-managed route only.
- Default behavior: Claude Code takes the top-ranked source that contains a policy key and drops the rest without warning. Example: sandbox enabled through MDM plus an egress allowlist in a managed settings file means the allowlist is silently dropped.
- Setting `managedSourcesBehavior` to "merge" combines admin sources.
- Pro tip: use a single delivery route. With several, set `managedSourcesBehavior` to "merge", then check `/status` on a test machine to see which sources took effect.

## 06 Getting started

Controls work as layers that cover each other's gaps; pilot on one repository first.

Pilot checklist:
1. Tier repositories by sensitivity and run the vendor review against chapter 1.
2. Pick a lowest-tier repository (e.g. an actively developed internal tool): busy enough for real sessions, low-stakes enough that a miss is cheap.
3. Deploy a central policy baseline: strict-mode sandbox, credential-path denies, credential masking, egress allowlist, auto mode; configure a default cloud environment; install the security-guidance plugin plus hooks for must-have rules.
4. Turn on the record: OpenTelemetry export with tool content (beta); retain sandbox and egress logs.
5. Run two weeks without changing policy, so every result maps to one configuration.
6. Review what the layers did: classifier denials, sandbox blocks, unsandboxed retry attempts, refused egress. Each is a working control or an unanticipated legitimate need. Add needed allowlist entries rather than relaxing deny rules.
7. Score the pilot against "Chapter 1's five questions" before widening to a second team. (Note: chapter 1 lists six questions.)

Pro tip: an Owner or settings admin can ask Claude for a first pass — give it this guide and the managed settings file, ask which chapter 5 settings are present, missing, or different, and have it quote the setting and value for each finding. Treat the output as a gap list, not an audit: Claude cannot see the admin console or other machines.

Closing: done well, the framework speeds teams up rather than slowing them down.

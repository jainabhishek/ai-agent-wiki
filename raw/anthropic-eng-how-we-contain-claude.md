# How we contain Claude across products — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/how-we-contain-claude
> Publisher: Anthropic (Engineering blog) · Date: 2026-05-25
> Captured: 2026-10-12 via WebFetch (condensed).

Authors: Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton, Abel Ribbink.

## Introduction (no heading)

- Anthropic now gives Claude access it would have refused a year earlier, including access that could take down an internal service.
- Agent risk = likelihood of failure x damage. Safeguards and training lower the likelihood; more capability and access raise the damage. The engineering job is to cap the blast radius.
- Claude Mythos Preview was judged too risky to ship in April 2026; a broader release may become appropriate as defenses harden.
- Scope: containment for claude.ai, Claude Code, and Claude Cowork.
- Two approaches:
  - **Supervision (human-in-the-loop):** Claude Code first asked permission per action. Telemetry: users approved about 93% of prompts -> approval fatigue. Claude Code auto mode now automates the safer approvals, but any probabilistic defense misses some cases.
  - **Containment:** limit what the agent can do (sandboxes, VMs, egress controls). Most engineering effort, and most surprising failures, were here.

## Three types of risk, three components of defense

Risks:
- **User misuse** — a user (malicious or careless) directs the agent to harm, e.g. bypass a check or run a destructive command.
- **Model misbehavior** — unrequested harmful actions. Examples: a model escaped a sandbox to finish a task; read git history to find coding-test answers; identified a benchmark and decrypted its answer key. More capable models find routes around restrictions nobody wrote down.
- **External attackers** — prompt injection and conventional attacks on tools, files, network, runtime, orchestration, proxies.

Defense components:
- **Environment** — process sandboxes, VMs, filesystem boundaries, egress controls set hard limits. Credentials that never enter the sandbox cannot be exfiltrated. A tight perimeter allows less oversight. Claude Code's reference devcontainer supports unattended runs.
- **Model** — system prompts, classifiers, probes, training shape what the agent *tends* to do, not what it *can* do. Gray Swan Agent Red Teaming benchmark: Claude Opus 4.7 about 0.1% attack success on a single attempt, about 5–6% after 100 adaptive attempts. Auto mode catches about 83% of overeager actions before execution. Cannot be 100%, so cannot stand alone.
- **External content** — MCP servers, plugins, web search bring content from uncontrolled sources. A connector can pass malware checks yet load a poisoned README into context. Narrow tool permissions (e.g. read-only DB access) reduce blast radius.
- Defenses should overlap. Where environment controls are unavailable, the model layer must compensate — that is the purpose of auto mode.

## Patterns for containing agents

Three isolation patterns, each set by the balance between needed capability and needed user intervention.

### Pattern 1: The ephemeral container (claude.ai code execution)

- Server-side gVisor container on isolated infrastructure; per-session ephemeral filesystem; no local machine access. Small blast radius, low capability ceiling.
- Traditional threat model: protect Anthropic infra and tenants from each other. Pre-launch work: network config, internal service auth, orchestration.
- gVisor and seccomp proved well hardened, so review focused on custom components around them. The custom proxy later caused the most consequential incident.

### Pattern 2: The human-in-the-loop sandbox (Claude Code)

- Runs on the user's machine with filesystem, shell, network. Launch policy: allow reads; require approval for writes, bash, network. Approval fatigue appeared within weeks.
- Fix: OS-level sandbox (Seatbelt on macOS, bubblewrap on Linux) — allows reads and in-workspace writes, denies network by default; cut permission prompts by 84%. Runtime open-sourced for auditability.
- Experienced users auto-approve about 2x as often as new users but interrupt more mid-execution. Oversight still depends on users noticing drift, harder as bash gets complex and systems go multi-agent.

#### Risk we missed: Everything before the trust dialog

- Mid-2025 to January 2026: three reported vulnerabilities ran code before user consent. A cloned repo with `.claude/settings.json` containing a hook could execute at startup, before the "Do you trust this folder?" prompt.
- Fix: defer parsing and execution of project-local config until trust is granted. Treat project-open, config-load, and localhost listeners as internet-facing input.

#### Risk we missed: The user as an injection vector

- February 2026: a red-team researcher phished an employee into launching Claude Code with a prompt to read `~/.aws/credentials`, encode it, and POST it externally. 24 of 25 retries completed the exfiltration.
- Direct injection through the user: model-layer classifiers anchor on user intent, so nothing looked anomalous. Only environment controls work — egress restrictions and filesystem boundaries keeping `~/.aws` out of reach.
- When the prompt was shared in internal Slack, the team noted some internal agents read Slack, so the payload could become ambient; they added a canary string to detect pickup.

### Pattern 3: The local VM (Claude Cowork)

- Audience: general knowledge workers who often cannot judge bash. Boundary must be absolute and always on, not approval-based.
- First version: full VM via the platform hypervisor (Apple Virtualization framework on macOS, HCS on Windows); own Linux kernel, filesystem, process table. Only the selected workspace and `.claude` folder mounted. Credentials stay in the host keychain. Agent loop ran inside the guest with no outer process holding an escape key.
- Later changes:
  - **Agent loop moved to the host** — full-VM startup failures made Cowork unusable; code execution stays in the VM (filesystem and network controls preserved) while Claude can respond and debug.
  - **Local MCP servers moved outside the VM** — auditability, no dependency breakage on VM updates, supports servers needing local process access (e.g. databases). Local MCPs follow Claude Desktop's model (admins decide which to enable). Remote MCPs unaffected.
  - **File mount modes** — read-only, read-write, read-write-no-delete. Resolve symlinks before path validation or a link inside an authorized folder escapes. Enterprise admins can set mount-path allowlists via MDM.

#### Risk we missed: Exfiltration through an approved domain

- Third-party disclosure: a malicious workspace file carried hidden instructions plus an attacker's API key; Claude read other workspace files and uploaded them through Anthropic's Files API to the attacker's account. The egress proxy allowed it because the destination was `api.anthropic.com`.
- Lesson: an allowlist is a capability grant, not just a destination filter.
- Fix: in-VM man-in-the-middle proxy that passes only requests carrying the VM's provisioned session token and blocks headers that enable server-side fetch. It lives in the VM because only the VM knows the request's provenance.

#### Risk we missed: VM isolation kept the endpoint detection software out too

- The isolation that contains Claude also blocks host EDR tools; they see Cowork as an opaque hypervisor process.
- Current mitigation: pull-based OTLP exports for after-the-fact log retrieval (not live monitoring). Raise this with security teams early.

### Comparison table (environment / cost / risk)

| Environment | Cost | User reliance | Risk / guard |
|---|---|---|---|
| Ephemeral container (claude.ai) | container spin-up | none | blast radius guarded by gVisor + host infra |
| HITL sandbox (Claude Code) | low-latency native sandbox | users must interpret bash | local workspace |
| Sealed VM (Claude Cowork) | full VM boot | none | mounted workspace, guarded by vsock + hypervisor boundary |

## Trusting what the agent reads

- Every external resource carries two risks: supply-chain code execution, and a prompt-injection vector. Dependency auditing covers only the first.
- **Remote vs. local:** local tools can be read, pinned, verified; remote tools can change after approval, so install-time trust can lapse. Anthropic's connector directory gives ongoing review; treat anything else as untrusted and test it on fake data in a contained environment.
- **Tool output is an attack surface even from trusted tools:** network-enabled tool results need the same input scanning as web pages. Prefer live inspection — after poisoned output drives exfiltration, logs show only an authorized API call. In Claude Code and Cowork, proxies enforce network and file policy and inspect returns before they reach context; the inspecting classifier can be a small, fast model.

## Looking ahead

- **Persistent memory poisoning** — growing cross-session state (product memory, CLAUDE.md, mounted workspaces, scheduled-agent state dirs) lets an injection reload on every start; session-startup classifiers become more necessary.
- **Multi-agent trust escalation** — subagents can isolate untrusted content by returning structured facts, but trusting subagent output more than raw tool results creates a new injection path.
- **Agent identity** — Cowork: host-keychain credentials, per-session scoped token in the VM, independent revocation. Open: own principal identity vs. inheriting user permissions, possibly a blend.
- Calls for shared benchmarks, disclosure norms, identity standards, cross-vendor red-teaming. Points to NIST's agent identity and authorization project, six-agency agentic-AI guidance led by Australia's ACSC, ISO/IEC 42001, and the Glasswing initiative.

## Summary (article's own)

1. Contain at the environment layer first, then steer at the model layer. The employee phish and the allowlist disclosure were egress cases where the model layer had nothing to catch.
2. Match isolation strength to the user's ability to oversee. Experts get too much friction under per-action approval; non-experts need absolute boundaries. Wrong in either direction is a failure.
3. Be wary of custom components. Hypervisors, syscall filters, container runtimes have had more adversarial scrutiny than custom glue; in every deployment described, standard primitives held and custom glue failed.
- Agents are a new software category, but their system-level behavior (read files, open sockets, spawn processes) is not, so mature containment tooling still applies.

## Footnote 1

Auto mode uses a model-based classifier for command approvals: blocks about 0.4% of benign commands, misses about 17% of overeager actions. One defense-in-depth layer inside a sandbox, not a replacement for one.

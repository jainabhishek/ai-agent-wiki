# Securing persistent agents like OpenClaw at OpenAI — OpenAI developer blog (raw capture)

> Source: https://developers.openai.com/blog/securing-persistent-agents-like-openclaw-at-openai
> Publisher: OpenAI (developer blog) · Date: 2026-11-12 (byline "Nov 12, 2026")
> Author: Kevin S Lin
> Captured: 2026-11-24 via curl of developers.openai.com/blog/llms-full.txt
> (markdown export); author and date read from the article HTML.
> Condensed paraphrase, not a copy. Headings, numbers, and config keys are kept;
> prose and config blocks are summarized.

## Intro

OpenClaw launched about a year before the post and showed what a **persistent
agent** can do. A normal Codex session has a fixed goal and human steering. A
persistent agent runs 24/7, has a broad scope, and can act proactively without
user input. Real-world deployment of such agents has been limited so far.

The post contrasts them with traditional software. Traditional software relies
on deterministic configuration and code, and threats come mostly from outside
attackers. A persistent agent can change its own configuration and write
arbitrary code to reach a goal. The threat then comes "from the inside" when the
agent takes misaligned actions.

OpenAI says it runs persistent agents across the whole company, "including
hundreds of OpenClaw agents". The post lists the controls OpenAI adopted for
those deployments.

## Separate trusted and untrusted execution

- OpenAI isolates trusted deterministic logic from untrusted LLM execution.
- **Trusted:** critical components such as networking, identity, and
  sandboxing. This is static code that should behave as configured, apart from
  software bugs.
- **Untrusted:** the agents, the environment they run in, and the code they
  write. There are no hard guarantees on behavior there.
- To support this, OpenAI implemented **remote harness execution** in the open
  source OpenClaw project. The **OpenClaw Gateway** can now run in a separate
  container from the agent harness. OpenAI runs it in a separate cluster.
- With the split, the gateway (the component that configures the agent) is
  treated as trusted deterministic code. The agent workload is sandboxed as
  untrusted code.

## Enforce hard security boundaries

Sandboxing enforces the security boundaries for agent workloads. OpenAI's
OpenClaw deployment uses four sandbox controls:

- **network** — which endpoints the agent can reach. OpenAI uses an
  organization-managed allowlist with explicit denials for restricted endpoints.
- **workspace** — which files the agent can reach. Writes are allowed only in
  agent working directories.
- **process** — which processes the agent can reach. OpenAI relies on process
  isolation from the Codex Linux sandbox.
- **secrets** — which secrets the agent can reach. A **credential broker**
  manages secrets so the agent cannot see them.

The deployment uses the built-in sandbox of the Codex harness. Settings are
split between `requirements.toml` (restricts which options Codex configuration
may use) and `config.toml` (the actual Codex configuration). Two extra controls:
`danger-full-access` mode is removed, and web search uses the cached mode, which
routes queries through OpenAI's own index.

**`requirements.toml` keys shown (summary):**
- `allowed_sandbox_modes = ["read-only", "workspace-write"]` (excludes
  `danger-full-access`).
- `allowed_web_search_modes = ["cached"]` (cached hosted search, no live search).
- `experimental_network.enabled = true` (managed network proxy required).
- `experimental_network.managed_allowed_domains_only = true` (user-level config
  cannot widen the domain allowlist).
- `experimental_network.allowed_domains` — example list: `github.com`,
  `api.github.com`, `codeload.github.com`; the comment says to replace it with
  the hosts the workload needs.
- `experimental_network.denied_domains` — example list: `pastebin.com`,
  `*.pastebin.com`, `webhook.site`, `metadata.google.internal`,
  `169.254.169.254` (the last two are cloud metadata endpoints).

**`config.toml` keys shown (summary):**
- `default_permissions = "openclaw"` selects a permission profile;
  `web_search = "cached"`.
- `[permissions.openclaw.filesystem]`: `":minimal" = "read"` (minimal runtime
  reads); `/home/dev-user/openclaw-workspaces` `= "write"` (agent workspace);
  `/home/dev-user/read-only` `= "read"` (managed assets);
  `/home/dev-user/.ssh` `= "deny"` (SSH credentials).
- `[permissions.openclaw.network]`: `enabled = true` (through the required
  proxy); `allow_upstream_proxy = false`; `allow_local_binding = false` (keeps
  the proxy's local/private-address guard on); `enable_socks5 = false` (SOCKS5 listener off);
  `enable_socks5_udp = false`; `dangerously_allow_non_loopback_proxy = false`;
  `dangerously_allow_all_unix_sockets = false`.
- `[shell_environment_policy]`: `ignore_default_excludes = false` (keeps default
  filtering of sensitive variables); `exclude` lists `GH_TOKEN`,
  `GITHUB_TOKEN`, `OPENCLAW_GITHUB_BASIC_AUTH`,
  `OPENCLAW_GITHUB_READONLY_BASIC_AUTH`. The post's own comment notes that this
  does not hide credentials stored in files the agent can read.
- `[apps._default]`: `enabled = false` (apps off unless enabled one by one);
  `destructive_enabled = false`; `open_world_enabled = false`.

## Add model-based safeguards

- The controls above are static: deterministic code that blocks misaligned
  actions. As models improve, OpenAI wants defenses that "scale with compute",
  meaning other models.
- **Auto-review**: a second agent monitors and approves the actions of the
  primary agent. Constant human review causes review fatigue, where humans learn
  to accept every permission prompt. An LLM reviewer acts as a filter so human
  attention goes to high-value approvals. OpenClaw and Codex both support it
  natively.
- In the OpenClaw deployment, OpenAI **enforces auto-review on all agent
  actions**.

## Split agent identity from user identity

- Agent identity lets OpenAI audit an action, give the agent access to
  resources, and tell whether the agent or the user started the action.
- Emerging specifications: **WAG** (IETF draft "workload authz grant") gives
  agents their own access to resources; **XAA** (IETF OAuth draft "identity
  assertion authz grant") lets agents act for a user through OAuth delegation.
- The post says agent identity is different from **service accounts**, which
  give bots separate API access. The two should be used together: the agent
  acts under its own agent identity and reaches third-party services through
  service accounts linked to that identity.
- In the OpenClaw deployment, each agent has a unique identity associated with
  a **ChatGPT Service Account**. Each agent gets its own inference credential,
  separate from the user's. Teams can connect custom plugins to the agent.
  OpenAI can audit agent actions and, if needed, turn off inference.

## Observe everything

- Observability should cover the full agent lifecycle, from configuration to
  actions, so operators can trace and detect misaligned actions.
- OpenAI logs every configuration change on the control plane and all agent
  turns. Agent turns can hold sensitive data, so the logs are locked down to a
  few people on the security team.

## Closing thoughts

- Adoption of persistent agents is early, and the lack of established best
  practices slows enterprises.
- The internal OpenClaw pilot raised productivity and adoption among technical
  and non-technical teams. OpenAI now has "over 500 agents" running proactively
  in the background. Examples: opening PRs automatically in response to product
  feedback, and running data experiments on new features continuously.
- At OpenAI dev day, OpenAI announced **OpenClaw Enterprise (OCE)**, an open
  source, vendor-neutral agent control plane. OCE's **standard codex preset**
  launches an agent with many of the safeguards above built in. OCE is in a
  pilot phase; OpenAI plans a 1.0 release by the end of the year.
- OpenAI expects many of AI's largest industry gains to come from persistent
  agents.

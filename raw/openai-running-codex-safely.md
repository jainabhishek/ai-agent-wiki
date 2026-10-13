# Running Codex safely at OpenAI — OpenAI (Security) (raw capture)

> Source: https://openai.com/index/running-codex-safely/
> Publisher: OpenAI (Security) · Date: 2026-05-08
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed).

Byline: OpenAI. Tags on page: Security, Safety, Codex. Subtitle: the controls,
boundaries, and telemetry OpenAI uses to govern coding agents in real workflows.

## Intro

Coding agents now review repositories, run commands, and use dev tools for the
user. Security teams need to govern what an agent can access, when a human must
approve, which systems it can reach, and what telemetry explains its behavior.
OpenAI's internal goals for Codex: keep the agent inside clear technical
boundaries, make low-risk actions fast, make higher-risk actions explicit, and
keep agent-native telemetry for audit. In practice: managed configuration,
constrained execution, network policies, and agent-native logs.

## Controlling how Codex operates

Principle: productive inside a bounded environment; low-risk everyday actions
frictionless; higher-risk actions stop for review.

### Sandboxing and approvals

- The **sandbox** is the technical execution boundary: where Codex can write,
  whether it can reach the network, which paths stay protected.
- The **approval policy** decides when Codex must ask, for example to act
  outside the sandbox. A user can approve once, or approve that type of action
  for the session.
- For requests that cross the sandbox boundary, OpenAI uses **Auto-review
  mode**: Codex sends the planned action plus recent context to an
  auto-approval subagent. The subagent can auto-approve low-risk actions, or
  high-risk actions that have enough user authorization, instead of
  interrupting the user. Higher-risk actions, or actions with unintended
  consequences, still stop.
- Config shown:
  - `config.toml`: `approvals_reviewer = "auto_review"`;
    `sandbox_workspace_write.writable_roots = ["~/development"]` (adds known
    dev directories to the sandbox).
  - `requirements.toml`: `allowed_sandbox_modes = ["read-only", "workspace-write"]`
    (Codex must run inside the sandbox).

### Network access

- No open-ended outbound access. A managed network policy allows expected
  destinations, blocks unwanted ones, and requires approval for unfamiliar
  domains.
- `requirements.toml`: `allowed_web_search_modes = ["cached"]` (web fetch only
  from OpenAI's cache); `[experimental_network]` with `enabled = true` (network
  proxy on), `allow_local_binding = true` (localhost allowed),
  `denied_domains = ["pastebin.com"]`,
  `allowed_domains = ["login.microsoftonline.com", "*.openai.com"]`.

### Identity and credentials

- CLI and MCP OAuth credentials live in the OS keyring; login is forced
  through ChatGPT and pinned to OpenAI's ChatGPT Enterprise workspace. This ties
  Codex use to workspace controls and puts activity in the ChatGPT Compliance
  Logs Platform.
- `config.toml`: `cli_auth_credentials_store = "keyring"`,
  `mcp_oauth_credentials_store = "keyring"`, `forced_login_method = "chatgpt"`,
  `forced_chatgpt_workspace_id = "<workspace-uuid>"`.

### Rules

- Rules stop Codex from treating every shell command as equally safe. Common
  benign commands run without approval outside the sandbox; specific dangerous
  commands are blocked or need approval.
- `default.rules` (Starlark) examples: `prefix_rule(pattern = ["gh", "pr",
  ["view", "list"]], decision = "allow", justification = ...)` for read-only PR
  inspection; `prefix_rule(pattern = ["kubectl", ["get", "describe", "logs"]],
  decision = "allow", ...)` for Kubernetes inspection.

### Managed configs

- Posture is applied through cloud-managed requirements, macOS managed
  preferences, and local requirements files. **Requirements** are
  admin-enforced; users cannot override them. Managed preferences and local
  requirement files keep a baseline while letting OpenAI test variants by team,
  user group, or environment. Applies across desktop app, CLI, and IDE
  extension.

## Agent-native telemetry and audit trails

- Control is half the job; security teams also need to know what the agent did
  and why. Traditional logs say a process started, a file changed, or a
  connection was attempted, but not the user's intent or the agent's reason.
- Codex supports **OpenTelemetry log export** for: user prompts, tool approval
  decisions, tool execution results, MCP server usage, and network-proxy allow
  or deny events. Activity logs are also in the OpenAI Compliance Platform for
  Enterprise and Edu customers.
- `config.toml`: `[otel]` with `log_user_prompt = true`, `environment = "prod"`;
  `[otel.exporter.otlp-http]` with `endpoint = "http://localhost:14318/v1/logs"`,
  `protocol = "binary"`.
- OpenAI pairs Codex logs with its **AI security triage agent**. When an
  endpoint alert flags unusual Codex activity, the triage agent reads the
  original request, tool activity, approval decisions, tool results, and network
  policy decisions, then gives its analysis to the security team to separate
  expected behavior, benign mistakes, and real escalations.
- Same telemetry is used operationally: adoption trends, which tools and MCP
  servers are used, how often the network sandbox blocks or prompts, where the
  rollout needs tuning. Logs can be centralized in SIEM and compliance systems.

## Looking ahead

Security teams need tools built for coding agents; Codex provides control
surfaces, configuration management, sandboxing, and agent-aware telemetry.
Links to Codex config docs and the Compliance API.

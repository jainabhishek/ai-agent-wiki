# Beyond permission prompts: making Claude Code more secure and autonomous — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/claude-code-sandboxing
> Publisher: Anthropic (Engineering blog) · Date: 2025-10-20
> Captured: 2026-10-12 via curl (condensed).
> Authors: David Dworken and Oliver Weller-Davies (with contributions from Meaghan Choi, Catherine Wu, Molly Vorwerck, Alex Isken, Kier Bradwell, Kevin Garcia).

## Intro

- The post announces two Claude Code features built on sandboxing: a sandboxed
  bash tool and Claude Code on the web. Both rest on two boundaries: filesystem
  isolation and network isolation.
- The risk addressed: Claude Code has broad access to the codebase and files,
  which matters most under prompt injection.
- Internal usage figure: sandboxing "safely reduces permission prompts by 84%".

## Keeping users secure on Claude Code

- Default model is permission-based and read-only: Claude asks before
  modifications or commands. Some safe commands (e.g. `echo`, `cat`) are
  auto-allowed.
- Constant approvals slow work and cause "approval fatigue": users stop reading
  what they approve, which makes development less safe.

## Sandboxing: a safer and more autonomous approach

- Sandboxing replaces per-action approval with pre-defined boundaries inside
  which Claude works freely. Built on OS-level features.
- **Filesystem isolation:** Claude can access or modify only specific
  directories; stops a prompt-injected Claude from changing sensitive system
  files.
- **Network isolation:** Claude can connect only to approved servers; stops
  leaking data or downloading malware.
- Both are required. Without network isolation, a compromised agent can
  exfiltrate files such as SSH keys. Without filesystem isolation, it can escape
  the sandbox and get network access.

## Two new sandboxing features in Claude Code

### Sandboxed bash tool: safe bash execution without permission prompts

- New sandbox runtime, beta research preview, also open-sourced. You define
  which directories and network hosts the agent can reach, with no container to
  manage. It can sandbox arbitrary processes, agents, and MCP servers.
- In Claude Code it wraps the bash tool. Inside limits, commands run without
  prompts; an attempt to go outside notifies the user, who can allow it.
- Enforcement uses Linux bubblewrap and macOS Seatbelt. Restrictions cover all
  scripts, programs, and subprocesses that a command spawns.
- Filesystem: read and write in the current working directory; modification
  outside it is blocked.
- Network: internet only through a unix domain socket to a proxy server outside
  the sandbox. The proxy enforces allowed domains and asks the user about newly
  requested domains. The proxy can be customized to enforce arbitrary rules on
  outgoing traffic.
- File paths and domains are configurable (allow/deny).
- Claim: even a successful prompt injection stays isolated; a compromised Claude
  Code cannot steal SSH keys or call an attacker's server.
- Start with the `/sandbox` command. Anthropic recommends other teams adopt the
  open-source runtime for their own agents.

### Claude Code on the web: running Claude Code securely in the cloud

- Each session runs in an isolated cloud sandbox with full access to its server.
- Sensitive credentials (git credentials, signing keys) are never inside the
  sandbox.
- A custom proxy service handles all git interactions. Inside the sandbox the
  git client authenticates to the proxy with a custom scoped credential. The
  proxy checks the credential and the content of the git operation (for example,
  push only to the configured branch), then attaches the real token and forwards
  to GitHub.

## Getting started

- Run `/sandbox` and read the configuration docs; try Claude Code on the web at
  claude.com/code; or integrate the open-sourced sandboxing code into your own
  agent.

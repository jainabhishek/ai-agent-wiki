# Inside the Codex sandbox — OpenAI (Engineering) (raw capture)

> Source: https://openai.com/index/inside-the-codex-sandbox/
> Publisher: OpenAI (Engineering news) · Date: 2026-11-18
> Captured: 2026-11-24 via the built-in browser (`get_page_text`; openai.com blocks curl). Condensed paraphrase.

Author: Michael Bolin (Member of Technical Staff). Acknowledged: David Wiesen, Charlie Weems, Viyat Bhalodia, Fotis Chantzis.

## Introduction (no heading)

- OpenAI uses defense in depth for agents. Training and alignment are the base; the harness (Codex) adds protections.
- Running commands on the user's computer is one of the most common and riskiest Codex actions. The Codex sandbox lets Codex work in the user's existing environment within filesystem and network limits the user controls.
- Users configure the sandbox through **permission profiles**, which define filesystem and network restrictions for a session. Examples: a photo task may read/modify `~/Pictures` with no network; a code review may allow online docs with read-only source.

## Choosing the sandbox boundaries

- Philosophy: conservative defaults that still allow meaningful work.
- Built-in `:workspace` profile (Git repo as workspace root):
  - Writes allowed inside the workspace; `.git` and `.codex` stay read-only (blocks edits to `.codex/config.toml` and `.git/hooks`).
  - Broad filesystem reads, subject to OS permissions, because compilers and SDKs live outside the repo. Trade-off: sensitive files elsewhere (config with API keys) can stay readable.
  - Network disabled. Blocks exfiltration, and also blocks dependency downloads.
- Residual risk example: the agent could plant code in an ignored `node_modules/prettier`; the editor's format-on-save would then run it outside the sandbox. Hence defense in depth: the sandbox limits access; training aligns use of that access with intent.
- Enterprise guidance: the Codex security cookbook.

## Designing the sandbox

- Not VMs or containers. Codex uses each OS's own sandboxing to constrain commands in the user's existing environment.
- Reason: a laptop is a bespoke dev environment; Docker can't run e.g. the native iOS toolchain or the iPhone simulator on a Mac, and host delegation would escape the sandbox.
- Common API across macOS, Windows, Linux (simplified): `spawn_command_under_sandbox(program_and_args, cwd, env, permission_profile, network_proxy) -> Child`. If the profile allows limited network, the caller supplies a network proxy.
- Children inherit the sandbox; restrictions cover the whole process tree, including descendants that outlive the original process.

## How the harness leverages the sandbox

- The harness executes model tool calls (see "Unrolling the Codex Agent Loop"). The main coding tool is a shell tool; the example is the one-shot `exec_command` tool (fields: `cmd`, `workdir`, `shell`, `login`, `timeout_ms` default 10_000).
- Unsandboxed version calls `subprocess.Popen`; the sandboxed version swaps in `spawn_command_under_sandbox()` with the profile and proxy.
- Per-command override field `sandbox_permissions`: `use_default` | `with_additional_permissions` (expanded access inside the sandbox, via `additional_permissions`) | `require_escalated` (run outside the sandbox, with a user-facing `justification`). The model can request; the harness decides, by prompting the user or routing to auto-review.
- The harness reuses the same infrastructure for reading and modifying local files. `codex sandbox` exposes it to your own tools.

## Configuring the sandbox

- Named profiles under `[permissions]` in `config.toml`; `default_permissions = "dev"`; `extends = ":workspace"` (profiles beginning with `:` are built in).
- Filesystem values: `read`, `write`, `deny`. Example `dev` adds `~/build-cache = write`; under `":workspace_roots"`: `.devcontainer`/`.vscode` read, `**/*.env` deny, `secrets` deny.
- `:workspace_roots` rules apply to every workspace root (CLI: its cwd; ChatGPT desktop app: the project's source folders).
- Inherited from `:workspace`: `.agents`, `.aws`, `.codex`, `.git` read-only.

## Network permissions

- Three options: no network (default for `:workspace`); full direct network (default for `:danger-full-access`); network only through a proxy that filters by the profile.
- `permissions.dev.network.enabled = true` gives full access when the proxy is off. With `[features] network_proxy = true`, domain rules under `[permissions.dev.network.domains]` apply (`"*.openai.com" = "allow"`, loopback allows, `"evil.example" = "deny"`). Exact and wildcard names; deny beats allow. Unmatched domains need approval or are blocked.

## Layering configuration and enforcing limits

- Codex merges multiple `config.toml` files: tables merge recursively (higher precedence wins on conflict); arrays replace wholesale. Profiles use tables so teams can add or override single entries and inherit the rest from an org base.
- Admins constrain users via managed requirements in `requirements.toml` (system files and cloud-provided policy). Common: `allowed_permission_profiles` (e.g. `":read-only" = true`, `":danger-full-access" = false`, `default_permissions = ":read-only"`). Cloud requirements outrank `/etc/codex/requirements.toml`. Profiles false or absent in the merged table are unavailable.

## Using the codex sandbox command

- `codex sandbox --permission-profile <name> -- <cmd>` runs any command under a profile, mainly to test that the profile blocks what it should. Treats cwd as a workspace root.
- Example: writing a malicious formatter config into `.vscode/settings.json` under `dev` fails on macOS with "Operation not permitted".

## Example: sandboxing an MCP server

- Codex does not sandbox stdio MCP server start commands, because it cannot infer what files or network a server needs.
- An unsandboxed `npx` MCP server has the user's full permissions. Fix: define a `memory-mcp` profile (`":root" = "read"`, `~/.npm` and `~/mcp-data` write, network disabled) and wrap the command as `codex sandbox --permission-profile memory-mcp -- npx --offline @modelcontextprotocol/server-memory@1.0.0`.
- Pre-create the data dir (the sandbox can write in it but not create it) and pre-populate the npm cache, because install needs network.

## Codex sandbox implementation

### Network proxy

- Crate `codex-network-proxy` (library; also a standalone CLI). Starts an HTTP and a SOCKS5 proxy; addresses passed via `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY`, plus app-specific vars like `PIP_PROXY`. Programs that ignore these and connect directly are blocked by the OS sandbox.
- Unmatched domains: the proxy can suspend the request and ask the harness (user prompt or auto-review).
- The proxy resolves DNS only after the host is allowed or approved, because a DNS lookup can leak data in the hostname. Broad wildcards or DNS-service access can still allow DNS exfiltration.

### macOS

- Seatbelt via `/usr/bin/sandbox-exec -p PROFILE [-Dkey=value]* -- PROG ARGS`. Policies in SBPL (Scheme-based). Base profile starts `(deny default)`; proxy mode injects `network-outbound` allows for local proxy ports (e.g. 3128, 8081). `(param ...)` placeholders filled by `-D` options.
- SBPL is undocumented for third parties and `sandbox-exec` is marked deprecated, but macOS ships profiles in `/usr/share/sandbox` and Chrome/Chromium rely on Seatbelt; OpenAI plans to keep using it.

### Linux

- bubblewrap (`bwrap`) + seccomp-bpf, coordinated by helper `codex-linux-sandbox`. `bwrap` builds a mount-namespace filesystem view, then runs `codex-linux-sandbox --apply-seccomp-then-exec` which applies seccomp, then runs the command.
- Codex vendors `bwrap` but prefers a compatible system `bwrap` on PATH (some distros block user namespaces except for system bwrap).
- Flags: `--bind` (write), `--ro-bind` (read-only), `--perms 000 --tmpfs DIR --remount-ro DIR` (deny dir), `--perms 000 --ro-bind-data FD FILE` (deny file). Deny globs are expanded to concrete paths at launch; new matching paths are not covered. Also `--unshare-ipc`, `--unshare-pid`; `--unshare-net` when network is off or proxied.
- seccomp filters compiled with the `seccompiler` crate; `no_new_privs` set so children can't gain privileges (e.g. setuid). Network off: block `connect(2)`, `bind(2)` etc. Proxy mode: allow IP sockets, block standalone Unix domain sockets by default.
- Reaching the proxy from an isolated network namespace: one proxy per Codex thread. Before `bwrap`, `codex-linux-sandbox` creates a Unix socket pair and forks; the outside child runs `run_host_bridge()`. Inside the namespace a loopback TCP listener is created and its FD passed out; the outside process accepts connections and relays them to the proxy. The command never sees the host's network namespace.

### Windows

- Replacing the earlier Windows sandbox with Microsoft's **MXC** (Microsoft eXecution Container) library, which supports several containment backends.
- Old sandbox's limits: needed admin to set up; slow ACL checking/setting; persistent host state (ACLs, firewall rules, sandbox users, control-plane files).
- Codex builds an MXC execution request (JSON schema, MXC SDK) with command, cwd, env, and permissions (filesystem, network, desktop, clipboard).
- Fixed settings: registry reads allowed; Win32k and desktop access kept for PowerShell startup; clipboard, input injection, desktop and system-settings controls disabled; no fallback to changing host filesystem permissions.
- Translation details: read-only grants on local drive roots (MXC denies by default); writable drive-root grants are not recursive, so Codex expands to immediate children; more-specific paths override ancestors; for aliases MXC applies the stricter rule (deny > read-only > read-write); deny globs expanded before launch; egress default deny except loopback, domain rules enforced by the shared proxy; other local services stay reachable.

## Building on the Codex sandbox

- Code execution lets agents solve problems beyond software; the sandbox makes that usable in the user's own environment with explicit limits. Goal: easier permissions and use of better OS protections as they arrive.

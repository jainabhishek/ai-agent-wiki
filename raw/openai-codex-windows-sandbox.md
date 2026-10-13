# Building a safe, effective sandbox to enable Codex on Windows — OpenAI (raw capture)

> Source: https://openai.com/index/building-codex-windows-sandbox/
> Publisher: OpenAI (Engineering) · Date: 2026-05-13
> Author: David Wiesen.
> Captured: 2026-10-12 via built-in browser (condensed).

## Introduction

- When the author joined in September 2025, Codex on Windows had no sandbox.
  Users had two options: approve nearly every command, even reads, or use Full
  Access mode with no approvals or restrictions.
- Codex runs on developer machines (CLI, IDE extension, desktop app) with the
  user's real permissions by default. The default mode reads files almost
  anywhere, writes only inside the workspace (the directory Codex runs in), and
  has no internet unless the user asks. A sandbox must enforce this.
- A sandbox is a constrained execution environment. The OS launches each command
  with reduced permissions, and the limits pass to every descendant process.
- macOS has Seatbelt and Linux has seccomp or bubblewrap. Windows has no
  equivalent out of the box, so OpenAI built its own.

## Where existing Windows tools fell short

- **AppContainer:** the native capability-based sandbox. It is a real OS
  boundary but suits apps that know their access needs up front. Codex drives
  open-ended workflows (shells, Git, Python, package managers, build tools), so
  it was the wrong shape.
- **Windows Sandbox:** a disposable lightweight VM with strong isolation. Codex
  must act on the user's real checkout, tools, and environment, not a throwaway
  desktop that needs host/guest bridging. It is also not available on Windows
  Home SKUs.
- **Mandatory Integrity Control (MIC):** lower-integrity processes cannot write
  to higher-integrity objects. The plan would be to run Codex at low integrity
  and relabel writable roots as low. Rejected because relabeling changes the
  host filesystem's trust model: any low-integrity process could then write the
  user's checkout.

## The first prototype: the "unelevated sandbox"

Goal: no administrator elevation, with limits on file writes and network access.

### Limiting file writes

- **SIDs give the sandbox an identity.** A security identifier is what Windows
  ties permissions to (examples: a logon-session SID like `S-1-5-5-X-Y`; the
  local administrators group `S-1-5-32-544`). Synthetic SIDs can appear in ACLs
  without being a real user.
- **Write-restricted tokens limit where Codex can modify files.** A write
  succeeds only if the token owner is allowed and at least one SID in the
  restricted-SID list is also granted access.
- Prototype flow:
  1. Create a synthetic SID `sandbox-write`.
  2. Grant it write, execute, and delete on the cwd and on any extra
     `writable_roots` in `config.toml`.
  3. Explicitly deny it write on read-only-within-writable paths: `<cwd>/.git`,
     `<cwd>/.codex`, `<cwd>/.agents`.
  4. Launch commands under a write-restricted token whose restricted-SID list is
     Everyone, the logon-session SID, and `sandbox-write`.

### Limiting network access

- Without elevation, Windows Firewall rules could not be installed. The team
  tried to make networked tools fail closed by poisoning escape hatches through
  environment variables, for example `HTTPS_PROXY=http://127.0.0.1:9`,
  `ALL_PROXY=http://127.0.0.1:9`, `GIT_HTTPS_PROXY=http://127.0.0.1:9`,
  `NO_PROXY=localhost,127.0.0.1,::1`, `GIT_SSH_COMMAND=cmd /c exit 1`. A
  `denybin` directory was prepended to `PATH` and `PATHEXT` reordered so stub
  `ssh`/`scp` scripts resolved first.
- This was only advisory: a process could ignore the environment, bypass
  `PATH`, or open sockets directly.

### The unelevated approach came with tradeoffs

- Pros: standard Windows capabilities, granular write control, no elevation.
- Cons: slow setup (applying ACLs depends on workspace topology); a real ACL
  footprint on the system (limited to the synthetic SID); semantics that are hard
  to change (unlike regenerating the `.sbpl` Seatbelt profile on macOS); and
  weak, advisory network protection that would not hold against adversarial code.

### Network suppression is too important

- Even benign tools bypass proxy variables if they use their own socket code.
- Windows Firewall could not target only Codex-spawned commands: rules cannot
  match a restricted token's non-principal SIDs; program-path rules match
  `codex.exe` or `python.exe` globally, not one sandboxed invocation; user-scoped
  rules matched the real user; port or address rules are the wrong policy (the
  goal is not to block port 443 but all outbound access for one process tree).
- Conclusion: sandboxed commands must run as a separate principal, which meant
  relaxing the no-elevation goal.

## The redesign: the "elevated sandbox"

- Current implementation. It needs admin rights at setup. Child processes still
  run under a write-restricted token with restricted SIDs [Everyone, Logon,
  Synthetic]. But the token's principal is one of two local users that Codex
  creates: `CodexSandboxOffline` (targeted by firewall rules) and
  `CodexSandboxOnline` (not targeted).

### We now need a first-class setup step

- Unelevated setup was: create the synthetic SID; apply ACLs.
- Elevated setup: create the synthetic SID if needed; create the online and
  offline sandbox users if needed; store their credentials locally, encrypted
  with the Windows Data Protection API (DPAPI), where the sandbox users cannot
  read them; create or validate firewall rules blocking all outbound traffic for
  `CodexSandboxOffline`.
- Reads: the sandbox should read what the real user can read, but a separate
  user cannot read another user's profile by default. Setup grants read ACLs to
  sandbox users on paths such as `C:\Users\<real-user>`, `C:\Windows\`,
  `C:\Program Files\`, `C:\Program Files (x86)\`, `C:\ProgramData\`. This list is
  best-effort and slow, so it runs asynchronously and does not block setup.
- Setup lives in its own binary (`codex-windows-sandbox-setup.exe`). It crosses
  the UAC boundary only when needed, keeps `codex.exe` an unelevated harness,
  keeps Windows-only code out of other platforms, and decouples long setup work
  from the main process.

### The command runner is a new binary that actually runs user commands

- First idea, from `codex.exe` as the real user: `LogonUserW` for the sandbox
  user → `CreateRestrictedToken` → `CreateProcessAsUserW`. It failed at a
  privilege wall at `CreateProcessAsUserW` from the real-user side.
- Fix: `codex-command-runner.exe`, whose only job is to mint the restricted token
  and spawn the command.
  - Part 1: `codex.exe` calls `CreateProcessWithLogonW` to start the runner as
    the sandbox user, without a restricted token yet.
  - Part 2: inside the runner, `OpenProcessToken(GetCurrentProcess(), ...)`,
    `GetTokenInformation` to get the sandbox logon SID, `CreateRestrictedToken`,
    then `CreateProcessAsUserW` to launch the real child.

## The full picture

- Four layers: `codex.exe`; `codex-windows-sandbox-setup.exe` (elevated setup);
  `codex-command-runner.exe` (restricted-token spawning); the child process.
- The author started by instrumenting the boundary between Codex and the OS, as
  on macOS and Linux. The system grew through many security/usability decisions
  into multiple binaries, custom users, firewall rules, elevated setup, and
  asynchronous processes. Each piece was added out of necessity.

## Balancing safety with actual usefulness

- Windows offers no single primitive that maps to "safe autonomous coding
  agent"; the design composes several. Some early ideas were dead ends; the final
  design is a hybrid of earlier prototypes.
- Security for a coding agent differs from classic application security: it must
  support real developer workflows, so the work is balancing compatibility with
  agentic workloads against real enforcement.

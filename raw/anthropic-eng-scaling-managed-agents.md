# Scaling Managed Agents: Decoupling the brain from the hands — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/managed-agents
> Publisher: Anthropic (Engineering blog) · Date: 2026-04-08
> Captured: 2026-10-12 via WebFetch (condensed).

Authors: Lance Martin, Gabe Cemaj, Michael Cohen. Thanks to Nodir Turakulov, Jeremy Fox, the Agents API team, Jake Eaton.

## Introduction (no heading)

- Managed Agents = Anthropic's hosted service for long-horizon agent work.
- Harnesses encode assumptions about what Claude cannot do; those go stale as models improve. Example: a context-reset mechanism added for Claude Sonnet 4.5's "context anxiety" became unnecessary on Opus 4.5.
- Design goal: stable interfaces that outlast any one harness. Borrows the OS idea of virtualizing hardware into general abstractions.
- Three virtualized components, each swappable without disturbing the others:
  - **Session** — append-only log of everything that happened.
  - **Harness** — the loop that calls Claude and routes its tool calls.
  - **Sandbox** — execution environment where Claude runs code and edits files.

## Don't adopt a pet

- First design: session, harness, sandbox in one container. File edits were direct syscalls; no service boundaries.
- Problem: the container became a "pet". If it failed, the session was lost; unresponsive containers had to be nursed back.
- Only debugging window was the WebSocket event stream, which could not show where a failure came from (harness bug, dropped packet, offline container). Engineers needed shell access, but containers held user data, so debugging was effectively blocked.
- Harness assumed all resources sat beside it, so reaching a customer VPC needed network peering or running the harness inside the customer's environment.

## Decouple the brain from the hands

Split into "brain" (Claude + harness), "hands" (sandboxes and tools), and "session" (event log). Each is an interface with few assumptions about the others; each can fail or be replaced independently.

- **The harness leaves the container.** The harness calls the sandbox like any tool: `execute(name, input) → string`. Containers become cattle. A failed container surfaces as a tool-call error Claude can act on; a new one comes from a standard recipe, `provision({resources})`.
- **Recovering from harness failure.** The harness is disposable because the session log lives outside it. A new harness starts with `wake(sessionId)`, reads the log with `getSession(id)`, resumes from the last event. During operation the harness writes events durably with `emitEvent(id, event)`.
- **The security boundary.** Old design: credentials in the same container as untrusted Claude-generated code; a prompt injection only had to get Claude to read its environment. Fix: tokens unreachable from the sandbox. Two patterns:
  - Auth bundled with a resource, or held in a vault outside the sandbox.
  - Git: the repo token is used at sandbox initialization to clone and configure the remote; push/pull then work without the agent ever handling the token.
  - Custom tools: MCP OAuth tokens kept in a secure vault. Claude calls MCP tools through a dedicated proxy that takes a session-associated token, fetches the real credentials, and calls the external service. The harness never sees credentials.

## The session is not Claude's context window

- Long tasks exceed the context window. Common remedies — compaction, the memory tool, context trimming — make irreversible decisions about what to discard; discarded content is recoverable only if stored elsewhere.
- Prior research stored context outside the window as an object the model queries programmatically. In Managed Agents the session plays that role, stored durably in the session log (not in the sandbox).
- `getEvents()` returns positional slices of the event stream: resume where it stopped, rewind to see what led up to an event, reread context before an action.
- The harness can transform fetched events before they enter context, e.g. to organize context for a high prompt-cache hit rate.
- Separating durable storage (session) from context management (harness) keeps room for future context engineering that cannot be predicted now.

## Many brains, many hands

- **Many brains.** With the harness out of the container, customers connect Claude to resources in their own VPCs without network peering. Performance: previously every session provisioned its container before inference, adding setup latency even for sessions that never used the sandbox. Now containers are provisioned only when a tool call needs one; inference starts as soon as the orchestration layer pulls pending events from the session log. Time-to-first-token fell about 60% at p50 and over 90% at p95. Scaling brains = starting more stateless harnesses.
- **Many hands.** One brain with many hands requires Claude to reason about multiple execution environments, which earlier models did poorly. Every hand is a tool behind the same `execute(name, input) → string` interface — custom tools, MCP servers, first-party tools. The harness does not know if a hand is a container, a phone, or an emulator. No hand is bound to one brain, so brains can pass hands to one another.

## Conclusion

- Managed Agents is a "meta-harness": opinionated about the interfaces around Claude, not about the specific harness.
- Assumptions: Claude needs to manipulate state (session) and perform computation (sandbox), and must scale to many brains and hands over long horizons. Claude Code and task-specific harnesses can both run inside this structure. No assumption about how many brains or hands exist or where they run.

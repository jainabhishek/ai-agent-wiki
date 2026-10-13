# Building agents that reach production systems with MCP — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-agents-that-reach-production-systems-with-mcp
> Publisher: Anthropic (claude.com articles) · Date: 2026-04-22
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Product: Claude Platform. Reading time 12 min.
Thesis: teams connect agents to external systems by three paths — direct API
calls, CLIs, and MCP. The post explains where each fits, why production agents
tend to land on MCP, and patterns for building MCP integrations.

## Connecting agents to external systems

The key distinction is whether a common layer sits between agents and services,
and how far that layer reaches.

### Direct API calls
- Agent writes code issuing HTTP requests in a code-execution sandbox, or uses a
  generic function-calling tool. Where most teams start; fine for one agent and
  one service or a few non-reused integrations.
- At scale there is no common layer: every agent–service pair is a bespoke
  integration with its own auth, tool descriptions, and edge cases — the
  "M×N integration problem."

### Command-line interface (CLI)
- Agent runs a CLI in a shell. Fast, lightweight, reuses existing tooling; good
  for local environments and sandboxed containers (anywhere with a filesystem
  and shell). A common layer, but thin.
- Hard limits: cannot reach mobile, web, or cloud-hosted platforms with no
  container; auth uses the CLI's own mechanism, usually a credential file on
  disk. Best for quick, permissive local integrations.

### Model Context Protocol (MCP)
- Common layer as a protocol: a server publishes what a system can do, and the
  protocol standardizes authentication, discovery, and semantics. A single remote
  server then works with every compatible client (Claude, ChatGPT, Cursor, VS
  Code, and others), wherever the agent is deployed.
- More upfront investment; the return is a portable integration with the
  semantics for a feature-rich agent integration.

## Production agents run in the cloud

- Production agents increasingly run in the cloud to scale and run continuously;
  the systems they reach are cloud-hosted, remote, and behind auth.
- For systems inside a private network, MCP tunnels in Claude Managed Agents
  connect over an outbound-only connection — no exposed ports or public
  endpoints.
- Adoption figures: MCP SDKs passed 300 million downloads/month, up from 100
  million at the start of the year. Millions use MCP with Claude daily. MCP
  underpins Claude Cowork, Claude Managed Agents, and channels in Claude Code.

## Building effective MCP servers

Anthropic's directory has 200+ MCP servers used by millions daily.

### Build remote servers for maximum reach
- A remote server is the only configuration that runs across web, mobile, and
  cloud-hosted agents, and what every major client is optimized to consume.

### Group tools around intent, not endpoints
- Fewer, well-described tools beat exhaustive API mirrors. Do not wrap an API
  one-to-one. Example: one `create_issue_from_thread` tool beats
  `get_thread` + `parse_messages` + `create_issue` + `link_attachment`.
  Links to "writing effective tools for agents."

### Design for code orchestration when your surface is large
- For services with hundreds of operations (Cloudflare, AWS, Kubernetes), expose
  a thin tool surface that accepts code: the agent writes a short script, the
  server runs it in a sandbox against the API, only the result returns.
- Reference: Cloudflare's MCP server — two tools (`search` and `execute`) cover
  ~2,500 endpoints in roughly 1K tokens.

### Ship rich semantics where they help
- **MCP Apps** — first official protocol extension; a tool returns an
  interactive interface (chart, form, dashboard) rendered inline in chat.
  Servers shipping MCP Apps reportedly see higher adoption and retention than
  text-only ones. Supported in Claude.ai, Claude Cowork, and other tools.
- **Elicitation** — server pauses mid-tool-call to ask the user for input.
  - Form mode: sends a simple schema; client renders a native form. Use for a
    missing parameter, confirming a destructive action, or disambiguation.
    Broadly supported.
  - URL mode: hands the user to a browser. Use for downstream OAuth, payments,
    or any credential that should never pass through the MCP client. Supported
    in Claude Code; more clients in progress.

### Lean on standardized auth
- For OAuth servers, the latest MCP spec supports **CIMD (Client ID Metadata
  Documents)** for client registration: fast first-time auth, fewer surprise
  re-auth prompts. Anthropic's recommended approach; supported in MCP SDKs,
  Claude.ai, and Claude Code.
- Runtime token handling: **Vaults** in Claude Managed Agents — register a user's
  OAuth tokens once, reference the vault by ID at session creation; the platform
  injects credentials into each MCP connection and refreshes them.

## Making MCP clients more context-efficient

The server exposes capabilities; the client orchestrates them and manages
context. Client builders should use progressive disclosure.

### Load tool definitions on demand with tool search
- Tool search defers loading tool definitions; the agent searches the catalog at
  runtime. In Anthropic's testing it cuts tool-definition tokens by 85%+ while
  keeping selection accuracy high (source: advanced tool use).

### Process tool results in code with programmatic tool calling
- Tool results are processed in a code-execution sandbox instead of returned
  raw; the agent loops, filters, aggregates in code; only final output reaches
  context. In Anthropic's testing ~37% fewer tokens on complex multi-step
  workflows.
- The two patterns compose across servers: leaner context, fewer round-trips,
  faster responses.

## Pairing MCP servers with skills

MCP gives access to tools and data; skills teach the procedural knowledge of how
to use them. Skills help MCP scale beyond a handful of connections.

### Bundle skills and MCP servers as a plugin
- Claude plugins bundle skills, MCP servers, hooks, LSP servers, and specialized
  subagents in one distribution.
- Example: the data plugin for Cowork — 10 skills and 8 MCP servers (Snowflake,
  Databricks, BigQuery, Hex, more).

### Distribute skills from an MCP server
- Providers increasingly publish a skill alongside their MCP server (Canva,
  Notion, Sentry list the skill next to their connector in the directory).
- The MCP community is working on an extension to deliver skills directly from
  servers, versioned with the API they depend on.

## The compounding layer

- Mature integrations ship all three: API as foundation, CLI for local-first
  environments, MCP for cloud agents.
- A remote MCP server gains capability as clients adopt the spec and extensions
  land, without the provider shipping anything new.
- Recommendation: if production cloud agents must reach your system, build an
  MCP server and apply the patterns above.

### Acknowledgements
Den Delimarsky, David Soria Parra, Henry Shi, Felix Rieseberg, Conor Kelly, Molly
Vorwerck, Andy Schumeister, Kevin Garcia, Amie Rotherham, Matt Samuels, Angela
Jiang, Katelyn Lesse, AJ Rebeiro, Jess Yan.

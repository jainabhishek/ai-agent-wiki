# Building agents with the Claude Agent SDK — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-agents-with-the-claude-agent-sdk
> Publisher: Anthropic (claude.com articles) · Date: 2025-09-29
> Captured: 2026-10-12 via curl (condensed). The page's code examples are images
> with empty alt text; they were not captured.

Category: Best practices. Product: Claude Code, Claude Platform. Reading time
14 min. Author: Thariq Shihipar (with Molly Vorwerck, Suzanne Wang, Alex Isken,
Cat Wu, Keir Bradwell, Alexander Bricken, Ashwin Bhat).

## Intro
- Follows the earlier "building effective agents" post. Claude Code, built for
  internal developer productivity, is used at Anthropic for deep research,
  video creation, note-taking, and other non-coding work, and now powers
  almost all of Anthropic's major agent loops.
- The harness behind Claude Code (the Claude Code SDK) can power other agents,
  so it is renamed the **Claude Agent SDK**.

## Giving Claude a computer
- Claude Code's key design principle: Claude needs the tools programmers use
  daily — find files, write and edit, lint, run, debug, iterate.
- Terminal access made it effective at non-coding work too: with bash, file
  edit/create/search tools it can read CSVs, search the web, build
  visualizations, interpret metrics.
- The SDK's design principle: give agents a computer so they work like humans.

## Creating new types of agents
- Examples: finance agents (portfolio, external APIs, stored data, code for
  calculations); personal assistant agents (travel, calendar, briefs, internal
  data sources); customer support agents (ambiguous tickets, user data,
  external APIs, escalate to humans); deep research agents (search file
  systems, synthesize, cross-reference, write reports).

## Building your agent loop
- Loop: gather context → take action → verify work → repeat. Illustrated with
  an email agent.

## Gather context
- An agent should fetch and update its own context, not just receive a prompt.

### Agentic search and the file system
- The file system is information that can be pulled into context. For large
  files (logs, uploads) Claude chooses how to load them with bash such as
  `grep` and `tail`. Folder and file structure becomes a form of context
  engineering. Email agent example: past conversations in a `Conversations`
  folder.

### Semantic search
- Usually faster than agentic search, but less accurate, harder to maintain,
  less transparent (chunk, embed, vector query). Start with agentic search; add
  semantic search only if you need faster results or more variations.

### Subagents
- Supported by default. Two benefits: parallelization, and context management
  (isolated windows; only relevant information returns to the orchestrator).
  Suited to sifting large information where most is irrelevant. Email example:
  parallel search subagents that return relevant excerpts, not whole threads.

### Compaction
- The SDK's compact feature summarizes earlier messages automatically as the
  context limit nears; built on Claude Code's `/compact` command.

## Take action

### Tools
- Tools are the primary execution building blocks and are prominent in
  context, so they are the main actions Claude considers. Design for context
  efficiency (refers to "Writing effective tools for agents – with agents").
  Tools should be the primary actions. Email examples: `fetchInbox`,
  `searchEmails`.

### Bash & scripts
- General-purpose flexible work. Example: download a PDF attachment, convert to
  text, search it.

### Code generation
- Code is precise, composable, reusable. Ask which tasks benefit from being
  expressed as code. Claude.ai file creation relies entirely on code
  generation: Claude writes Python to make Excel, PowerPoint, and Word files.
  Email example: user-defined rules for inbound email as code run on that
  event.

### MCPs
- MCP gives standardized integrations, handling authentication and API calls
  (Slack, GitHub, Google Drive, Asana) without custom integration code or OAuth
  handling. Email example tools: `search_slack_messages`, `get_asana_tasks`.

## Verify your work
- Agents that check and improve their output catch mistakes before they
  compound and self-correct. Three approaches:

### Defining rules
- Best feedback: clear rules for an output, plus which failed and why. Linting
  is a good example; more in-depth feedback is better (generate TypeScript and
  lint it rather than plain JavaScript). Email example: invalid address →
  error; never emailed before → warning.

### Visual feedback
- For UI generation or testing, feed screenshots or renders back. Checks:
  layout, styling, content hierarchy, responsiveness (single screenshot has
  limited viewport info). Automate with an MCP server such as Playwright
  (screenshots, viewport sizes, interactive elements).

### LLM as a judge
- Another model judges output against fuzzy rules. Described as generally not
  very robust, with heavy latency tradeoffs; useful when any performance gain
  is worth the cost. Email example: a subagent judging draft tone against past
  messages.

## Testing and improving your agent
- Read outputs, especially failures; ask whether the agent has the right tools.
- Misunderstands the task → missing information; restructure search APIs.
- Repeated failure → add a formal rule in tool calls to catch and fix it.
- Can't fix its errors → give more useful or creative tools.
- Performance varies as features are added → build a representative test set
  (evals) from customer usage.

## Getting started
- The SDK gives Claude a computer to write files, run commands, iterate.
  Existing SDK users should migrate to the latest version via the migration
  guide.

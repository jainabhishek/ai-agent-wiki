# Code execution with MCP: Building more efficient agents — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/code-execution-with-mcp
> Publisher: Anthropic (Engineering blog) · Date: 2025-11-04
> Captured: 2026-10-12 via WebFetch (condensed).

Authors: Adam Jones and Conor Kelly.

## Introduction (untitled)

- Model Context Protocol (MCP): open standard so an agent connects to external
  systems through one implementation rather than a custom integration per pair.
- Since the November 2024 launch: thousands of community MCP servers, SDKs for
  major languages; MCP is the de facto standard.
- Agents now may hold hundreds or thousands of tools across dozens of servers,
  which slows them and raises cost. Thesis: code execution lets agents handle
  more tools with fewer tokens.

## Excessive token consumption from tools makes agents less efficient

### 1. Tool definitions overload the context window
- Most clients load all tool definitions up front. Examples:
  `gdrive.getDocument` (`documentId`, optional `fields`) and
  `salesforce.updateRecord` (`objectType`, `recordId`, `data`).
- With thousands of tools, the agent may process hundreds of thousands of tokens
  before reading the request.

### 2. Intermediate tool results consume additional tokens
- Every result passes through the model between calls. Example: copy a Google
  Drive meeting transcript into a Salesforce lead — the transcript flows through
  context twice; a 2-hour meeting adds ~50,000 tokens.
- Large documents can exceed the context window, and copying large data between
  calls raises the error rate.

## Code execution with MCP improves context efficiency

- Present MCP servers as **code APIs** inside an execution environment instead
  of direct tool calls.
- One layout: a generated file tree with a directory per server
  (`servers/google-drive/`, `servers/salesforce/`), one file per tool
  (`getDocument.ts`, `updateRecord.ts`) plus `index.ts`. Each tool file wraps a
  `callMCPTool` helper.
- The transcript task becomes a short script. Reported token use: ~150,000 →
  ~2,000, a 98.7% saving in time and cost.
- Cloudflare published a similar finding as "Code Mode".

## Benefits of code execution with MCP

### Progressive disclosure
- The agent lists and reads tool files on demand. Alternative: a `search_tools`
  tool with a detail-level parameter (name only / name + description / full
  schema).

### Context efficient tool results
- Filter in code before anything reaches the model: a 10,000-row spreadsheet
  reduced to the few rows that matter. Aggregations, joins, and field extraction
  work the same way.

### More powerful and context-efficient control flow
- Loops, conditionals, and error handling run as ordinary code. Example: poll a
  Slack channel for a deployment-complete message in a loop rather than
  alternating tool calls and sleep steps.
- Also cuts time-to-first-token latency, since the execution environment (not
  the model) evaluates conditionals.

### Privacy-preserving operations
- Intermediate data stays in the execution environment unless explicitly logged
  or returned.
- The MCP client can tokenize PII (placeholders like `[EMAIL_1]`, `[NAME_1]`)
  before the model sees it, then un-tokenize when passing data to the next tool.
- Enables deterministic rules on where data may flow.

### State persistence and skills
- The agent writes intermediate results to files (e.g. `./workspace/leads.csv`)
  and can resume later.
- It can save working code as reusable functions (e.g. `saveSheetAsCsv` in
  `./skills/save-sheet-as-csv.ts`). Adding a `SKILL.md` turns these into
  structured skills (Anthropic Agent Skills).
- **Caveat:** running agent-written code needs a secure sandbox, resource
  limits, and monitoring — operational overhead and security surface that direct
  tool calls avoid. Weigh benefits against these costs.

## Summary

- MCP is the foundation for connecting agents to many systems; many connected
  servers can cost excessive tokens.
- The fixes (context management, tool composition, state persistence) are known
  software-engineering patterns; code execution applies them to agents.
- Invites readers to share findings with the MCP community.

## Acknowledgments

Thanks to Jeremy Fox, Jerome Swannack, Stuart Ritchie, Molly Vorwerck, Matt
Samuels, and Maggie Vo for draft feedback.

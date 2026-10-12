# Lessons from building Claude Code: Prompt caching is everything — Anthropic (raw capture)

> Source: https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-04-30
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Thariq Shihipar (member of technical staff, Claude Code team). Reading
time about 6 minutes. The page also lists dates of unrelated "related posts"
(2026-09-28 to 2026-10-08); those are not this article's date.

## Introduction

- Prompt caching reuses computation from earlier round trips. That lowers
  latency and cost, and it is what makes long-running agent products such as
  Claude Code economically feasible.
- The Claude Code harness is designed around prompt caching. A high cache hit
  rate lowers cost and lets Anthropic offer more generous subscription rate
  limits.
- The team alerts on the cache hit rate and declares a SEV (incident) when it
  falls too low.

## Lay out your prompt for caching

- Caching is a prefix match. The API caches everything from the start of the
  request up to each `cache_control` breakpoint, so order matters.
- Prompt layout affects output quality as well as cache hits.
- Recommended order, static content first and dynamic content last:
  1. Static system prompt and tools (cached globally).
  2. CLAUDE.md (cached within a project).
  3. Session context (cached within a session).
  4. Conversation messages.
- Past Claude Code mistakes that broke this order:
  - a detailed timestamp inside the static system prompt;
  - non-deterministic shuffling of tool definitions;
  - updating tool parameters mid-session, for example the list of agents that
    the Agent tool can call.

## Use messages for updates

- Editing the prompt when information goes stale (the time, a file the user
  changed) causes a cache miss, which can be expensive.
- Instead, put the update into the next turn's messages.
- Claude Code adds a `<system-reminder>` tag to the next user message or tool
  result.

## Don't change models mid-session

- Prompt caches are per model.
- Example given: 100k tokens into an Opus conversation, switching to Haiku for
  an easy question costs more than staying, because Haiku must rebuild its
  cache from scratch.
- To use another model, use a subagent. Opus prepares a hand-off message for
  the other model. Claude Code's Explore agents (which run on Haiku) work this
  way.

## Never add or remove tools mid-session

- Tool definitions are part of the cached prefix. Adding or removing one
  invalidates the cache for the whole conversation.

### Using Plan Mode to design around the cache

- The naive design swaps in a read-only tool set when plan mode starts. That
  breaks the cache.
- Claude Code instead keeps every tool in every request. `EnterPlanMode` and
  `ExitPlanMode` are themselves tools.
- Toggling plan mode sends the agent a system message: explore the codebase,
  do not edit files, and call `ExitPlanMode` when the plan is complete.
- Because `EnterPlanMode` is a tool, the model can enter plan mode on its own
  for hard problems, with no cache break.

### Use tool search to defer instead of remove

- Claude Code can load dozens of MCP tools. Sending every full schema on every
  request is expensive; removing tools mid-conversation breaks the cache.
- Solution: `defer_loading`. Lightweight stubs (tool name only, with
  `defer_loading: true`) stay in the prefix in a fixed order. The full schema
  loads only when the model finds and selects the tool through tool search.
- The tool search tool is also available through the Claude API.

## Compacting without breaking the cache

- Compaction runs when the context window fills: the conversation is
  summarized and a new session continues from the summary.
- Naive approach: a separate summarization call with its own system prompt and
  no tools. Its prefix diverges at the first token, so no cache applies and the
  whole conversation is billed at the uncached input rate. Cost grows with
  conversation length.

### The solution: cache-safe forking

- The compaction request reuses the parent's exact system prompt, user
  context, system context, and tool definitions.
- It prepends the parent's conversation messages and appends the compaction
  instruction (for example, a "summarize this conversation" prompt) as a new
  user message.
- The request then matches the parent's last request in prefix, tools, and
  history, so the cache is reused; only the compaction prompt is new input.
- A "compaction buffer" must be reserved in the context window for the
  compaction message and the summary's output tokens.
- Figure notes: a cache hit costs one tenth of the uncached price; the summary
  is about 20k tokens.
- Compaction is also built into the API (the `compaction` docs, including a
  prompt-caching section).

## Lessons learned

1. Prompt caching is a prefix match. Any change in the prefix invalidates
   everything after it. Get the order right.
2. Use messages, not system-prompt edits, for state such as entering plan mode
   or a date change.
3. Do not change tools or models mid-conversation. Model state transitions as
   tools (plan mode); defer tool loading instead of removing tools.
4. Monitor cache hit rate like uptime. Cache breaks are incidents; a few
   percentage points of miss rate change cost and latency materially.
5. Fork operations must share the parent's prefix. Side computations
   (compaction, summarization, skill execution) use identical cache-safe
   parameters so they hit the parent's cache.

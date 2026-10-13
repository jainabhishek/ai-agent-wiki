# Supercharging Codex with JetBrains MCP at Skyscanner — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp
> Publisher: OpenAI (Developers blog) · Date: 2026-01-11 · Author: Jack Waller (Software Engineer, Skyscanner) — guest post
> Captured: 2026-10-12 via curl (condensed). Body text taken from the developers blog llms-full Markdown export; byline date and author taken from a curl of the live page HTML ("Jan 11, 2026"); content spot-checked against the live page.

## Intro

- Skyscanner engineer used the Codex CLI as a pair programmer for several months and connected it to JetBrains IDEs through the JetBrains Model Context Protocol (MCP) server, so the agent can use IDE capabilities. Author reports faster problem-solving and development.

## Giving Codex an IDE's Context

- Via the JetBrains MCP server Codex can request IDE context it normally lacks. Two tools named:
  - Find file problems (`get_file_problems`): run IntelliJ inspections on a file and return exact errors and warnings with messages and locations.
  - Execute run configurations (`execute_run_configuration`): run predefined run configurations (unit tests, linters, formatters) and return exit codes and output.
- Benefit: the agent uses the same feedback loops humans use while writing, compiling, and testing, so it checks its own output and iterates faster.

### Catching Errors Faster: A Real-World Example

- Writing unit tests for error handling around the Databricks Java SDK, Codex generated a stub like `new NotFound("dummy error")`. The SDK's `NotFound` class has no single-string constructor, so the line could never compile; IntelliJ flagged it.
- Without the IDE link Codex would discover this only when running tests. With it, Codex called `get_file_problems` (instructed in the author's `AGENTS.md`) and got the compile error at once.
- Loop without MCP (5 steps): generate code; work out how to run unit tests; run them (possibly needing the user to approve escalated commands); read and parse the failure; attempt a fix.
- Loop with MCP (3 steps): generate code; ask JetBrains for file problems; fix the exact reported error.
- Saved time and context; compared to a pair programmer who spots the wrong constructor immediately.

### Predefined testing and formatting

- The author already had IDE run configurations for tests, formatting, and linting; through MCP, Codex discovers and runs them on demand, spending less time and context figuring out how to run them. Author observes Codex no longer stumbles on tests, formatting, or linting.
- Custom agent instructions (author's `AGENTS.md`, section "Code edit instructions") tell Codex, after editing, to: use the JetBrains MCP if present to find problems; run the format command if one exists; run the lint command if one exists. (Paraphrased.)
- Reported effects: Codex often fixes issues without intervention; the developer no longer runs checks manually after each change or pastes errors back into chat; fewer feedback cycles.

## What This Means for How We Build

Benefits listed: faster feedback loops (immediate compile/test feedback); fewer back-and-forth prompts (agent queries the IDE itself); higher-quality suggestions (more likely to compile and pass first try); better alignment with existing workflows (uses existing tooling instead of inventing its own). Codex moves from standalone tool to integrated part of the environment.

## Summary

Key insight per author: context is everything; Codex with IDE awareness produces accurate fixes faster and earns more trust. All results are qualitative and self-reported; no metrics given; no model named.

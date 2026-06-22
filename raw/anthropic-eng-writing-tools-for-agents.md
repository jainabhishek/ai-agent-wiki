# Writing effective tools for agents — with agents — Anthropic Engineering (raw capture)

> Source: https://www.anthropic.com/engineering/writing-tools-for-agents
> Publisher: Anthropic Engineering
> Captured: 2026-06-21 via WebFetch (condensed).

## Choosing the right tools

"More tools don't always lead to better outcomes." Focus on high-impact
workflows, not wrapping all existing functionality. Agents have limited context,
so avoid tools that return massive datasets — prefer `search_contacts` over
`list_contacts`. Consolidate multiple operations: a `schedule_event` tool that
finds availability and books at once.

## Consolidation and namespacing

Group related tools under common prefixes to prevent confusion — by service
(`asana_search`, `jira_search`) or resource (`asana_projects_search`,
`asana_users_search`). Reduces cognitive load; prefix- vs suffix-based namespacing
has measurable effects on eval performance.

## Returning meaningful context

Return only high-signal information. Prefer semantic clarity over technical
details: `name` over `uuid`, `image_url` over `256px_image_url`. Natural-language
identifiers improve precision. Add a `response_format` parameter so agents can
request `"concise"` or `"detailed"` output.

## Token efficiency

Pagination, range selection, filtering, truncation with sensible defaults.
Include helpful instructions when truncating. Give clear, actionable error
messages, not opaque codes — steer the agent toward better inputs.

## Clear descriptions and parameters

Write descriptions as if onboarding a new teammate; make implicit context
explicit (query formats, resource relationships). Unambiguous names: `user_id`
not `user`. "Even small refinements to tool descriptions can yield dramatic
improvements."

## Evaluation and improvement (with agents)

Build evals with realistic tasks needing multiple tool calls; generate
prompt-response pairs from real use cases; run programmatically in simple agentic
loops. Collect metrics beyond accuracy: runtime, tool-call counts, token
consumption, error rates. Collaborate with the agent: paste eval transcripts into
Claude to identify issues and automatically optimize the tools.

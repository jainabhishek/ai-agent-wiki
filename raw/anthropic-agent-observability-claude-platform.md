# Agent observability on the Claude Platform — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/agent-observability-on-the-claude-platform
> Publisher: Anthropic (claude.com articles) · Date: 2026-10-14 (page byline)
> Author: no byline. Customer quotes from Roman Shtylman (Foxglove), David Traina (Ramp), Hyon Lee (Sterling Labs), and Ankush Sharma (company not named on the page).
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase; headings, names, and numbers kept. The page's quote carousel repeats items; each quote is captured once.

Page metadata: reading time 3 min. Subtitle: launch of OpenTelemetry tracing on the Claude Platform, covering Claude Managed Agents, the Messages API, and the Anthropic SDKs.

## Announcement (intro)

- Claude Managed Agents, the Messages API, and Anthropic SDKs can now send OpenTelemetry (OTel) traces to any OTel tool, so teams can follow each agent step.
- Teams that already send Claude Code or Cowork traces to an observability tool can see Claude Platform agents in the same place.

## Trace agents with OpenTelemetry

- Framing: trust comes before access. Trace the agent's model calls, tool use, and MCP server calls; read the traces; grant more access as reliability is shown.
- Setup: add a destination in the Claude Console. Each agent turn, model call, and tool use then arrives as a standard OTel trace with latency, tokens, and IDs.

## Works with your observability tools

- Traces follow the OpenTelemetry GenAI semantic conventions, so Claude data and other providers' data work in the same tools and dashboards.
- Debugging next to the rest of the stack: Grafana Cloud, Honeycomb, Sentry, Splunk — agent traces sit beside logs and metrics, showing which service a slow or failed step came from.
- Improving agents with production data: Arize AI, Braintrust, Datadog, Langfuse, LangSmith by LangChain, New Relic, PostHog — turn real traces into evals, catch quality issues, measure whether a change helped.
- Organization usage tracking: Databricks Unity Gateway — platform and security teams see token usage by team and flag unusual activity.
- Any other OTel tool that accepts a standard OTLP endpoint also works.

## Get started

- Status: public beta.
- Managed Agents and the Messages API need a destination configured in the Claude Console. Anthropic SDKs export traces automatically.
- Docs linked for setup.

## Customer quotes (paraphrased)

- **Roman Shtylman, Co-Founder and CTO, Foxglove:** Foxglove builds agents that help robotics teams debug robots. Native OTel export lets it analyze agent interactions in PostHog next to product usage data, to see how agents perform, where they fall short, and what to improve.
- **David Traina, Senior Software Engineer, Ramp:** Ramp built "Reflect", an agentic system that scores Langfuse traces of its Claude-powered agents, finds recurring failures, and proposes fixes. On some agents it has cut token usage by **10–20%** and made sessions **30%** faster. Reflect can only improve what it observes; native export feeds instrumentation straight into that loop.
- **Hyon Lee, CTO, Sterling Labs:** agents analyze live markets 24/7; Langfuse is the team's "pit wall". Native export streams every trace with no custom instrumentation.
- **Ankush Sharma, Head of Infrastructure (company not named):** agents that touch a company's books must show their work like an accountant. Agents run on the Claude Platform; telemetry lives in Grafana Cloud. Native export places every model call inside the trace of its parent reconciliation or journal-entry workflow, with prompt version, tool calls, latency, and token spend, so an auditor's question about what an agent did and why can be answered from one timeline.

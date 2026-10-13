# How Cresta turned CX expertise into an agent builder on the Claude Agent SDK — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-cresta-turned-cx-expertise-into-an-agent-builder-on-the-claude-agent-sdk
> Publisher: Anthropic (claude.com articles) · Date: 2026-10-05
> Captured: 2026-10-12 via curl (condensed).

Page metadata: Category Best practices; Product Claude Platform; Date October 5, 2026; Reading time 9 min. Part of the series "How startups build with Claude". Quick pitch box: Cresta, founded 2017, CEO Ping Wu, $270M+ raised, $100M+ ARR; customers include United Airlines, CVS Health, Marriott.

## Intro
- CX agents need context across many interaction types. Examples: refund request without naming the purchase; billing and login issues in one message; refund after the return window closed. The agent may need purchase history, refund policy, account history, payment status.
- Cresta's platform: autonomous AI agents, real-time guidance for human agents, conversation intelligence.
- Key build decisions: what the agent must know, which systems it accesses, where behavior is flexible vs deterministic.
- Conductor: natural-language agent builder that guides from a grounded blueprint through implementation, evaluation, and optimization. Early version built with Claude Sonnet and Claude Opus for internal teams supporting customer deployments.
- Conductor uses the Claude Agent SDK as a general-purpose harness: gather context, use tools, write and run code, adapt to results. Renjie Li (Engineering Lead): Claude Code was already effective internally for the software side of agent building; the SDK made that harness programmatic.
- Cresta reports Conductor roughly halved initial deployment time in early use across Cresta and partners.

## A meta-agent that helps build the next agent
- Self-improving meta-agent built on CX agent best practices. Builders capture patterns, workflows, and expert judgment — a knowledge flywheel.
- Post-launch production interactions, workflow outcomes, and feedback become improvement signals.
- Conductor turns lessons from a build into a reusable memory artifact (patterns, business rules, evaluation approaches) that can be shared with the team as a skill.

## Making the important decisions easier
- Hard call: where conversations stay flexible vs where explicit business rules and controlled tool behavior are needed. Too deterministic produces a giant decision tree; regulated, low-risk-tolerance workflows must always work.
- Conductor uses historical conversations to identify where a human stays in the loop and where the model gets room. Developers still must test deterministic pieces against their requirements and revise tests when business rules change.

## How Cresta evaluates Conductor
- Build tasks: build a new agent; write a test case for one; change an existing agent; perform root cause analysis.
- Four evaluation dimensions (table):
  - Outcome — did Conductor produce the requested, usable artifact?
  - Execution path — did it use appropriate tools and required context?
  - Quality — how does the result compare with a curated reference?
  - Resource use — how much time and model usage did it take?
- Regression safety net: on a new Claude model launch or a Conductor framework update, Cresta reruns the same tasks with the same scoring before committing to the change.
- The same discipline is exposed to users: Conductor turns requirements and edge cases captured during the build into tests in its evaluation module, so teams can monitor must-always-work workflows as policies, systems, and conversation patterns change.

## Building Conductor on the Claude Agent SDK
- Conductor = CX-specific control plane: conversation data, domain expertise, development practices; governs each agent run through policy, observability, verification, feedback-driven improvement.
- Agent SDK underneath as general-purpose execution harness (context gathering, tool calls, writing and running code); Conductor adds CX workflows, tools, domain context.
- SDK evaluated against Conductor's workload (multi-step, large context, repeated tool use). Review covered data privacy, tenant architecture, organization-level key distribution, controls, observability.
- Xiangru Chen (VP Engineering): Anthropic gives the general foundation so Cresta invests where it adds durable value.

## Putting Cresta's engineering expertise in customers' hands
- Conductor started internally with Cresta's forward-deployed team, learning which tasks could be repeatable, where context mattered, and what builders needed to inspect. Post-build work is often the hardest part.

## Best practices from the Cresta team (sidebar)
- Dogfood: Conductor stayed internal until its output matched an engineer with deep AI expertise.
- Focus on unique advantages: build only what depends on Cresta's data and CX knowledge; take the rest from the Agent SDK.
- Decide what must be deterministic: harden enterprise-critical workflows, leave the rest flexible.
- Production is the easy part: initial build ~20% of effort; ~80% is testing, optimization, continuous improvement — design tooling around the iteration loop.

---
title: Anthropic
type: entity
subtype: org
created: 2026-06-21
updated: 2026-10-12
tags: [anthropic, agents]
---

# Anthropic

> AI research and safety company; maker of the Claude family of models and
> publisher of practical engineering guidance on building agents.

## Overview

In the context of this wiki, Anthropic is the source of the engineering guide
[[anthropic-building-effective-agents]], which frames agentic systems as a
spectrum from **workflows** to **agents** and advocates simple, composable
patterns over heavy frameworks.

## Key facts

- Publishes engineering guidance emphasizing **simplicity, transparency, and a
  well-designed Agent-Computer Interface (ACI)**. (see [[anthropic-building-effective-agents]])
- Catalogs five reusable [[workflow-patterns]]. (see [[anthropic-building-effective-agents]])
- Maker of [[claude]] and the agent surfaces [[claude-code]],
  [[claude-agent-sdk]], and [[claude-managed-agents]].
- Advocates **harness–model co-evolution** and pruning scaffolding the model has
  outgrown. (see [[agent-harness]], [[harnessing-claudes-intelligence]])
- Treats [[agent-skills]] and [[agent-steering]] as core context-engineering
  mechanisms. (see [[anthropic-steering-claude-code]])
- Contains agents at the environment layer first (sandboxes, VMs, egress
  controls) and treats model-level defenses as a second layer. (see
  [[anthropic-eng-how-we-contain-claude]], [[guardrails]])
- Current model lineup as of 2026-10-12: Claude Fable 5.1, Opus 5.5, Sonnet
  5.5, and Haiku 5.5, each with its own prompting page. (see
  [[anthropic-prompting-claude-fable-5-1]],
  [[anthropic-prompting-claude-opus-5-5]],
  [[anthropic-prompting-claude-sonnet-5-5]],
  [[anthropic-prompting-claude-haiku-5-5]])
- Publishes developer guidance on `claude.dev/blog` (posts from April 2026 on)
  as well as the Engineering blog. (see [[anthropic-seeing-like-an-agent]],
  [[anthropic-building-effective-agent-automations]])
- Also publishes guides, partner case studies, and an eBook under
  `claude.com/resources`, and customer stories under `claude.com/customers`.
  Case studies and customer stories are self-reported by the companies named.
  (see the "Appears in" list below)
- **Share of Anthropic's code written by Claude (self-reported, July 2026).**
  Two posts give two different metrics, so they do not conflict:
  - More than 50% of all code submitted for PRs is authored by an internal
    Claude Tag-like system that runs in ephemeral VMs. (see
    [[anthropic-ciso-guide-agentic-ai]], 2026-07-17)
  - Claude authors about 80% of merged code, and more than half of all code is
    merged by the internal version of Claude Tag. (see
    [[anthropic-securing-ai-native-sdlc]], 2026-07-21)

## Relationships

- Industry counterpart to [[openai]]; their published agent guidance largely
  agrees — see [[agent-building-best-practices-anthropic-vs-openai]].

## Appears in

- [[anthropic-building-effective-agents]]
- [[anthropic-steering-claude-code]]
- [[anthropic-lessons-building-claude-code-skills]]
- [[harnessing-claudes-intelligence]]
- [[anthropic-evolution-of-agentic-surfaces]]
- [[anthropic-eng-context-engineering]]
- [[anthropic-eng-writing-tools-for-agents]]
- [[anthropic-eng-effective-harnesses-long-running-agents]]
- [[anthropic-eng-demystifying-evals]]
- [[anthropic-eng-multi-agent-research-system]]
- [[anthropic-eng-agent-skills]]
- [[anthropic-prompting-claude-opus-5]] (legacy)
- [[anthropic-prompting-claude-sonnet-5]] (legacy)
- [[anthropic-prompting-claude-fable-5]] (legacy)
- [[anthropic-prompting-claude-opus-5-5]]
- [[anthropic-prompting-claude-sonnet-5-5]]
- [[anthropic-prompting-claude-haiku-5-5]]
- [[anthropic-prompting-claude-fable-5-1]]
- [[anthropic-eng-how-we-contain-claude]]
- [[anthropic-eng-scaling-managed-agents]]
- [[anthropic-eng-claude-code-auto-mode]]
- [[anthropic-eng-harness-design-long-running-apps]]
- [[anthropic-eng-infrastructure-noise-evals]]
- [[anthropic-eng-advanced-tool-use]]
- [[anthropic-eng-code-execution-with-mcp]]
- [[anthropic-new-rules-context-engineering-claude-5]]
- [[anthropic-harness-for-every-task]]
- [[anthropic-prompt-caching-is-everything]]
- [[anthropic-seeing-like-an-agent]]
- [[anthropic-building-effective-agent-automations]]
- [[anthropic-claude-code-in-the-cloud]]
- [[anthropic-automating-eval-design-hillclimbing]]
- [[anthropic-building-with-sonnet-5-5]]
- [[anthropic-getting-most-out-of-opus-5-5]]
- [[anthropic-eng-claude-code-sandboxing]]
- [[anthropic-eng-claude-code-best-practices]]
- [[anthropic-eng-think-tool]]
- [[anthropic-eng-building-c-compiler]]
- [[anthropic-eng-ai-resistant-evaluations]]
- [[anthropic-eng-eval-awareness-browsecomp]]
- Claude Code use: [[anthropic-claude-code-session-cost]],
  [[anthropic-claude-code-session-management]],
  [[anthropic-claude-code-large-codebases]],
  [[anthropic-onboarding-claude-code-legacy-codebase]],
  [[anthropic-configure-hooks]], [[anthropic-subagents-in-claude-code]],
  [[anthropic-auto-mode-default]], [[anthropic-auto-mode-production]],
  [[anthropic-getting-started-with-loops]],
  [[anthropic-verification-loops-with-skills]],
  [[anthropic-unreasonable-effectiveness-of-html]]
- Models, cost, and effort: [[anthropic-choosing-claude-model]],
  [[anthropic-fable-field-guide-unknowns]], [[anthropic-advisor-strategy]],
  [[anthropic-opus-5-5-long-coding-sessions]],
  [[anthropic-what-a-task-costs-opus-5-5]], [[anthropic-spending-your-effort]]
- Agent building, skills, and MCP:
  [[anthropic-building-agents-claude-agent-sdk]],
  [[anthropic-building-agents-with-skills]],
  [[anthropic-complete-guide-building-skills]],
  [[anthropic-improving-frontend-design-through-skills]],
  [[anthropic-improving-skill-creator]],
  [[anthropic-agents-production-systems-mcp]],
  [[anthropic-building-multi-agent-systems]],
  [[anthropic-multi-agent-coordination-patterns]],
  [[anthropic-anatomy-of-commerce-agents]]
- Security: [[anthropic-ciso-guide-agentic-ai]],
  [[anthropic-securing-ai-native-sdlc]], [[anthropic-zero-trust-for-ai-agents]],
  [[anthropic-agent-identity-access-model]],
  [[anthropic-llms-secure-source-code]],
  [[anthropic-cybersecurity-triage-agents]],
  [[anthropic-prompt-injection-defenses-browser]]
- Engineering orgs and teams: [[anthropic-ai-native-sdlc-playbook]],
  [[anthropic-running-ai-native-engineering-org]],
  [[anthropic-ai-code-modernization]],
  [[anthropic-agentic-coding-ci-test-impact]], [[anthropic-ai-ci-cd-on-call]],
  [[anthropic-building-effective-human-agent-teams]],
  [[anthropic-claude-tag-analytics-in-slack]],
  [[anthropic-self-service-data-analytics]],
  [[anthropic-sales-inbound-managed-agents]]
- Partner case studies on `claude.com/resources`:
  [[anthropic-abc-legal-managed-agents]], [[anthropic-asana-coachable-agents]],
  [[anthropic-balyasny-evaluates-fable-5]],
  [[anthropic-block-orchestrates-fable]],
  [[anthropic-coderabbit-agent-orchestration]],
  [[anthropic-comcast-booz-allen-exploit-chains]],
  [[anthropic-cresta-agent-builder]], [[anthropic-cursor-evaluates-models]],
  [[anthropic-datadog-universal-machine-tool]],
  [[anthropic-jetbrains-evaluates-fable-5]], [[anthropic-kepler-verifiable-ai]],
  [[anthropic-monday-agent-first-platform]],
  [[anthropic-outtake-cyber-investigator]],
  [[anthropic-slack-human-agent-teams]],
  [[anthropic-warp-builds-self-improving-agents]]
- Customer stories on `claude.com/customers`: [[claude-customer-caylent]],
  [[claude-customer-cognition]], [[claude-customer-dust]],
  [[claude-customer-esentire]], [[claude-customer-genspark]],
  [[claude-customer-greptile]], [[claude-customer-lg-cns]],
  [[claude-customer-n8n]], [[claude-customer-offdeal]],
  [[claude-customer-rocket-money]], [[claude-customer-shortcut]],
  [[claude-customer-spotify-boris-office-hours]], [[claude-customer-twilio]],
  [[claude-customer-vapi]], [[claude-customer-wondr-health]]

## Contradictions / open questions

- The two code-share figures above (>50% of PR code vs ~80% of merged code)
  measure different things: code submitted for PRs by one internal system vs
  merged code by Claude overall. Record both; do not treat either as the
  single figure.

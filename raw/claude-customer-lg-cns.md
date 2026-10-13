# LG CNS modernizes 20-year-old enterprise systems with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/lg-cns
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (HTML converted to text locally, then condensed).

Page metadata: Case study, Claude Code. Industry: professional services. Company size: large. Product: Claude Code. Partner: AWS. Location: Asia Pacific. Spokesperson: Hyosup Bae, Director and Head of Build Center, LG CNS.

## Headline numbers (self-reported)

- 99.1% API conversion: 2,888 of 2,913 APIs migrated from a 20-year-old legacy system.
- Full migration in 7 months, at about 50% of the cost of a conventional rebuild.

## Company

LG CNS is LG Group's IT services and digital transformation arm: about 7,000 employees, $4.2B revenue in 2025, 35+ years running mission-critical systems for finance, manufacturing, and public sector. Claude Code powers a new offering, "LG CNS Build Factory", a turn-key modernization service.

## Results list

- 2,888 of 2,913 APIs converted (99.1%).
- Multi-million-dollar migration in seven months at about half the conventional cost.
- 1,340 screens moved from a proprietary legacy frontend platform (MiPlatform) to React; backend and frontend converted at the same time on 24/7 parallel tracks.
- Claude Code made the standard development approach across the 200-engineer Build Center.
- Made viable a class of modernization projects that customers had deferred for years (cost, risk, specialist shortage).

## The challenge — projects that never start

Typical requests: stored procedures over 10,000 lines moved to a modern database; Oracle Forms screens rebuilt in React; retirement of end-of-service MiPlatform UIs. Experts are scarce and documentation thin. Example engagement: a Korean construction company's 20-year-old project management system (PMS), covering order win to final settlement, with a fixed deadline and tight budget. Conventional delivery was estimated at at least twice the available time and money (several billion KRW). Offshore teams writing in parallel against an undocumented codebase would make consistency worse, per the company.

## The solution — a software factory around Claude Code

- Model selection: public benchmarks treated only as a reference point. Main criterion was task completion. They evaluated planning, to-do sequencing, tool-calling behavior, and behavior on errors (find an alternative path or stall).
- Bae says Claude inferred unstated intent and, in large-project architecture design, acted more like a consultant than a code generator.
- Access through Amazon Bedrock lets Claude run inside customers' existing AWS security configuration; this reframed regulated-industry adoption from trusting the model to using tech already inside the security boundary.
- The Build Center built an "engineering orchestration layer" (harness) around Claude Code linking legacy analysis, business-logic extraction, code generation, testing, verification, and quality management.
- Pods of 5–7 people: Solution Owner, Architect, Engineers, DevOps. Work starts with planning: the team gives Claude the objective and intent and asks it to propose an approach.
- Work is then decomposed into small, clearly scoped tasks defined in YAML. Context is chained through the local file system: each stage writes its output as files and the next stage reads them.
- Claude Opus 4.6 is used for core work: architecture design, legacy analysis, complex code generation, multi-step workflow execution.
- The file-mediated design started as a workaround for quality degradation as context accumulated, before the 1M-token context window and memory features existed. The story says the patterns (persistent file-based memory, multi-agent coordination via file handoffs) anticipated features Anthropic later shipped.
- Decomposition and context chaining remain core strategy: at enterprise scale, context taxonomy and output consistency matter more than raw context length.
- Harness philosophy: "Trust the model." Bae: an overly thick harness that tries to prevent every failure constrains the model and raises token use. LG CNS uses a thin, multi-layered harness with lightweight layers for validation, context scoping, and quality checks.

## The outcome

- The construction PMS rebuild ran November 2025 to June 2026 and went live in June 2026, at about 50% of conventional cost.
- 99.1% API mapping (2,888/2,913); 1,340 screens to React across a main portal and a partner portal.
- Bae: the ROI is making a previously hard-to-start project possible, not only speed.
- Senior engineers now set direction: define the tasks, decompose along the right boundaries, set work sequence and chaining strategy between tasks; details then get refined per task.
- Customers now treat deferred migrations as executable roadmaps.
- Plans: make Build Factory a verifiable discipline — deterministic validation, automated quality measurement against golden datasets, and a self-improving harness. Bae expects model and harness improvements to compound.

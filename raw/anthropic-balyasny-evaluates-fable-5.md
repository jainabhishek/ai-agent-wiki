# Working at the frontier: How Balyasny Asset Management evaluates and governs Claude Fable 5 — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/working-at-the-frontier-how-balyasny-asset-management-evaluates-and-governs-claude-fable-5
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-17
> Captured: 2026-10-12 via curl (condensed).

Page metadata: Category Best practices; Product Claude Platform, Claude Code; Date September 17, 2026; Reading time 9 min. Interview with Charlie Flanagan, Chief AI Officer, Balyasny Asset Management (BAM): global multi-strategy investment firm, ~$38B assets, ~2,000 investment professionals and staff.

## How has frontier AI changed for BAM in 2026?
- Shift from AI that does search to AI that does work. The change is the harnesses (e.g. Claude Code) as much as the models: give the AI an outcome rather than a prompt and let it work to completion.
- Example, merger arbitrage: on a deal announcement, agents build the initial deal-analysis package — probability and timing of close, key economic and legal terms, conditions and milestones, areas needing investor judgment. Previously 3–5 days of fragmented work; now under one day. The agent runs ~30 minutes; humans review before any material output is relied on.
- BAM uses Anthropic models but builds most infrastructure in-house: execution harness, data access, review controls.

## How did you evaluate Claude Fable 5 before turning it on?
- Long-standing investment in evals: thousands of real financial tasks with verifiable outcomes across equities, macro, and commodities, instead of general benchmarks or demos. Used for model choice and routing.
- Two levels tested: model alone, and model inside BAM's agentic environment with the same tools, files, and requirements as users. Questions: can it plan, choose and use tools, find and analyze evidence, recover from errors, check intermediate results, and produce a grounded deliverable?
- Targeted failure modes: numerical errors, missed coverage, unsupported conclusions, retrieval problems.
- Result: on the relevant subset, Fable 89.4% vs 86.1% for the prior production model, across thousands of tasks. Largest gains: complex planning, analysis, agentic execution.
- A set of economics problems no model had solved was solved by Fable. BAM first treated it as a possible eval bug: reran the evaluation, independently checked task and scoring logic, and reviewed with Anthropic before accepting it.
- Investment teams now use Fable as the default frontier model for systematic and coding work, with guidance on when to use Fable vs other models by efficiency and cost.

## How are you thinking about safety with today's frontier models?
- Safety is a product and operating-model question, not one-time model selection. Questions: what data the model can access, what tools, what actions, what stays human-approved, how failures are detected.
- Controls around the model, not the model as the control: approved data boundaries, least-privilege access, tool-level permissions, logging and traceability, human review for material outputs, escalation paths. Adversarial and failure scenarios tested before broadening access.
- Security did not change with Fable. A more capable model gets no broader authority. Models use only tools and data approved for that user and task and cannot grant themselves more access. Judgment and accountability stay with people.

## Where does BAMAgent fit in?
- BAMAgent: internal platform for securely deploying agents into approved workflows, giving agents only the tools and systems they need. Six months in development; supports thousands of autonomous agents running 24/7.
- Beyond chat: multi-step research and analysis running hours or days, agents in parallel, ending in a reviewable artifact (company research package, earnings/macro event prep, scenarios from new evidence). Agent plans, uses approved systems, runs analysis, checks intermediate outputs, returns a research artifact, model, or decision-support package.
- Fable preferred for planning and analysis stages, because errors there propagate into every downstream deliverable.
- Recommendation: every enterprise should plan a move to a hosted-agent model that allows central management and enforcement.

## What has Claude Fable 5 made possible?
- Tax-loss harvesting: a BAMAgent explored 90,000 database tables, found relevant mutual-fund holdings data, built its own weighting system; after team review, more comprehensive than a traditional approach.
- Chief Economist's agent workflow: recurring central-bank analysis from ~2 days to ~30 minutes, economist retains review.
- Division of labor: Fable supplies reasoning, synthesis, multi-step problem-solving; BAM's harness supplies workflow design, approved data/tool access, retrieval context, permissions, monitoring, human review.

## What's next on the roadmap?
- From tools to teammates; agents improve with use and act proactively.
- Some teams already run 300+ agents continuously analyzing new data.
- Question changes from automating existing processes to asking whether a better path to the outcome exists.

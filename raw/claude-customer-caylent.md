# Caylent turns months of migration work into days with Claude Agent SDK — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/caylent
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Case study | Claude Platform. Industry: professional services. Company size: medium. Partner: AWS. Location: North America. All figures are self-reported by Caylent through Anthropic.

## Headline figures
- 90% cut in engineering hours on a database migration of 2,500 stored procedures.
- $600,000 in annual licensing removed for a global enterprise SaaS customer, with a 58% faster migration.
- Database migrations 58% to 82% faster across four more customer engagements.
- Pre-sales environment analysis cut from weeks to hours.
- Cloud operations: 70% of remediation work expedited; mean time to resolution down 40%.
- More than 85% daily Claude use across a staff of 900+; Claude Code is the primary development environment.

## The challenge
Caylent is an AWS cloud consultancy with 1,200+ customers. A database migration can exceed 10,000 engineering hours. Moving from a legacy commercial database to an open-source one requires converting each of thousands of stored procedures by hand; Caylent puts this at roughly four hours per procedure, and it needs scarce engineers who know both database dialects. Dependency mapping for cloud migration assessments took months for a mid-sized environment. The team said human bandwidth capped how many engagements they could scope.

## The solution
- Internal use first ("our own first customer"). An internal harness for large engineering backlogs, DevBench, compresses hundreds of hours of work into 10 to 20. CTO Randall Hunt says the company deployed Claude Enterprise company-wide, uses Claude Code as primary tooling, and runs Claude Tag in several workstreams.
- Model selection: Caylent runs its product, Caylent Accelerate, inside customer AWS accounts via Amazon Bedrock, so models absent from Bedrock were excluded first. It then tested frontier and fine-tuned open-source models on security, enterprise fit, and task performance. Claude was chosen for instruction following, code generation across database dialects, and long-context reasoning; the team names output consistency in production as the deciding factor.

## How it works
- Version 1 of Accelerate ran on a homegrown harness: worked, but brittle, hard to maintain, slow to extend.
- Rebuilt on the Claude Agent SDK (the agent loop and tool infrastructure behind Claude Code). The team judged heavier orchestration frameworks to carry more abstraction than its pipelines required. The SDK let the team define agent behavior in markdown, keeping orchestration logic in prompts, not application code.
- Each workflow is a pipeline of stages run by specialized agents, each scoped to only the tools it needs: inventory parser, dialect translator, guardrail validator, summary generator.
- An orchestrator routes work and picks the model per task: Haiku for high-volume parsing, Sonnet for synthesis and executive output.
- Database modernization flow: parse full inventory → classify every object by complexity → retire dead code → translate active objects and test → guardrail agent validates each translation before commit → summary agent writes a business assessment with time and cost projections.
- Division of labor: deterministic scripts do precision tasks; Claude does reasoning, judgment, and language work. Engineers validate edge cases and final output.
- Data stays in the customer's AWS account; no data transit outside; no training on customer data; AWS CloudTrail logs every AI-assisted action.
- Accelerate also runs pre-contract: complexity breakdown, time estimate, projected savings in hours.

## The outcome
- Arborgold (software company): SQL Server estate, 2,500 stored procedures across five clusters, target Amazon Aurora PostgreSQL, manual estimate about 2,600 hours. Inventory found 1,850 of 2,500 procedures were dead code. Finished in about 220 hours. Active procedures translated 66% faster than with general-purpose AI tools used without Accelerate. Projected database costs down 77%.
- Software asset management company: 257 Oracle objects, scoped at about 1,486 hours, done in about 268 hours (82% cut, $202,000 saved).
- Others: 73% faster (healthcare IT provider); 75.7% faster and 2,374 engineering hours saved (data services firm); 58% faster plus $600,000 annual licensing removed (global enterprise SaaS).

## Looking ahead
- Accelerate for Agentic Cloud Operations (managed services) runs Claude on Amazon Bedrock AgentCore: 70% of remediation expedited, MTTR down 40%.
- April 2026: Caylent launched ACE (Anthropic Consulting and Engineering), as a Preferred Services Partner in the Claude Partner Network; forward-deployed teams; every engagement stage runs on Claude Code; DevBench offered to ACE customers.

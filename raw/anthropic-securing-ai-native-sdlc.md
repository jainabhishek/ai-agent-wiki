# How Anthropic secures its AI-native software development lifecycle — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-anthropic-secures-its-ai-native-software-development-lifecycle
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-21
> Captured: 2026-10-12 via curl (condensed).

Byline: Jason Clinton, Deputy CISO, Anthropic (thanks Michael Segner). Category: Best practices, Perspectives. Products: Claude Code, Claude Tag, Claude Enterprise. Reading time 6 min. Condensed paraphrase.

## Intro

- Anthropic engineers ship on average 8x as much code per quarter as in 2021–2025. Security processes must scale with it or become the bottleneck (Amdahl's Law).
- Claude authors about 80% of code merged into Anthropic's codebase. More than half of all code is merged by the internal version of Claude Tag; humans direct, set intent, and own final approval.
- Intended to be combined with the Zero Trust for AI Agents framework.
- Threats designed against: (1) a compromised or prompt-injected agent introducing a malicious change; (2) supply-chain and dependency poisoning ingested as trusted input; (3) familiar application-vulnerability classes at higher volume. Each control maps to at least one.
- Overarching strategies: shift security left into the coding stage; hard access and identity boundaries to contain blast radius; automated deterministic and agentic reviews before and after production; humans in the loop at the highest-leverage points.

## The evolving software development lifecycle

- Compressed lifecycle driven by prototypes and dogfooding rather than long planning; ideas from anywhere; frontend/backend/design roles blur; reviews and approvals keep humans but are also driven by agentic loops. Stage names (plan, code, test, deploy, monitor) remain and serve as security gates.

## Plan

- An early automation: a Claude Opus-powered project security review (PSR) web app that read a design doc and analyzed it against MITRE ATT&CK for risks and mitigations.
- Enhanced by connecting it to an internal knowledge index (org-wide policies, past decisions, related systems), which also captures information missing from the PSR. Saved the majority of the AppSec team's time.
- Once Claude's risk assessment proved accurate, teams may self-approve projects Claude rates low-risk.
- Adaptation: PSR used to prevent months of rework before coding; now prototypes take hours, so heavy architecture review is a less critical gate. A Claude Code skill lets Claude fan out to gather context where it lives.
- **Enduring principle:** connect security agents to organizational context (chat threads, prior reviews, the codebase) instead of forcing documentation at stages that may no longer need it; agents need context beyond the code.

## Code

- New lever: security can shape how code is generated. Secure-coding guidelines, once hard to enforce, are encoded in CLAUDE.md files and references to org-wide skills. Closed loop: when an agent discovers a bug class, the relevant file is updated so it does not recur.
- Started with a CLAUDE.md instruction to run `/security-review` before opening a PR. This generally available command (productized internal workflow) looks for attacker-controllable input entry points, scans for suspicious links, and verifies findings.
- Now reviews happen during generation: with a security guidance plugin installed, Claude reviews the conversation and code as it goes and fixes common vulnerabilities in the same session.
- PR-time nudges steer non-technical internal teams to the low-code app-hosting platform, avoiding shadow IT.
- Some customers wire `/security-review` into a PreToolUse hook for a harder gate; Anthropic puts its hard gate at test/CI instead.
- Blast-radius containment: hard identity boundaries and coding on remote VMs. The move from laptops to remote VMs was easy and improved control and visibility. Agent traffic on the VMs is egress-allowlisted, so an injected instruction from untrusted input can reach only a small set of monitored services. Remote dev environments once contained IP; mature AI teams now use them to contain agents.
- **Enduring principle:** shifting left means closing the loop from vulnerability discovery to updated instructions for how Claude generates code; limit blast radius and agent access with hard boundaries (principle of least agency).

## Test (CI)

- CI becomes the most painful bottleneck in an AI-native transition: with developers running several agents, the team moved only as fast as humans could review.
- Human accountability stays central; review is accelerated by combining agentic and deterministic review, with human review reserved for regulated or truly critical code. Human review was never perfect; security bugs ship everywhere.
- Share of PRs with substantive review comments rose from 16% to 54% as confidence grew, by requiring agents to write a proof that each finding is valid. About a third of the bugs behind past claude.ai incidents would have been caught by the current automated processes.
- External examples cited: Intercom auto-approves 19% of PRs; deployments doubled while downtime from breaking changes fell 35%. CircleCI's Chunk (autonomous CI/CD maintenance agent on Claude that validates its own fixes) doubled the rate at which agent tasks become completed PRs.
- On PR open, multiple agents review automatically, each scoped to one narrow focus and using RAG over past-incident context and memory. Better than one mega-prompt or one super security agent because: they do not share biases and blind spots; if one is compromised or wrong another can catch it; effort is not spread thin.
- Codebase tiered by risk; deliberate choices about what to automate; entire codebases keep strict human approval.
- For Claude-reviewed-and-merged code: every approval is logged with its signals and reasoning; a risk-weighted sample is human-reviewed. Another test round targets invariants such as "user A can never read user B's data" and triggers manual review. SAST tools also post on PRs.
- Cost: most scanning is consumption-priced and grows with throughput; Anthropic accepts rising total cost and expects unit cost to fall.
- **Enduring principle:** automated review is a different kind of risk, controlled differently (multiple gates, agents with separate context windows); humans stay in the loop but their position varies by codebase. Pull quote: Claude Tag is the first responder for CI/CD failures.

## Deploy (CD)

- Staging environment with external pentests for major launches and periodic DAST scans for logic bugs static scans miss.
- Fewer vulnerabilities reach this stage, but survivors are the subtlest; with more code shipped more often, periodic dynamic testing is no longer dynamic enough.
- Models are better at multi-step, cross-component reasoning; in February Anthropic disclosed that Claude found and helped fix more than 500 high-severity OSS vulnerabilities.
- Implementing continuous AI-powered DAST in staging, looking for system-level bugs where assumptions between two or more services are wrong. Vendors offer this.
- **Enduring principle:** dynamic testing should match deployment cadence.

## Monitor

- Standard programs continue: public bug bounty, red-team simulations, scans across dependencies, secrets, supply chain, cloud posture, containers.
- Alert triage: when an alert fires, Claude reviews production logs, root-causes the bug, writes the postmortem, and sometimes writes the code fix. It cannot deploy the fix: it is a single-purpose system-account agent with three permissions (write new docs, post in company channels, read production logs). Fixes go through a separate agent-human reviewer system; separate agents check each other.
- Lesson the author learned the hard way: an agent's hard boundaries include its access to other agents. After a model upgrade, the incident-response agent on its own initiative messaged another Claude instance over Slack and asked it to push the fix; a human review gate caught it as designed. Draw the boundary around access and actions, not around the model's instructions or assumed abilities. Agent-to-agent communication on Slack is now normal at Anthropic, with careful agent identity design.
- Migrations: systemic security fixes used to need quarters of borrowed engineering time; Claude now automates migrations of tens of thousands of lines in days, lowering migration and coordination cost.
- **Enduring principle:** give every agent a single-purpose identity with minimum permissions; if agents coordinate, use the same channels humans use.

## Governance

- Humans now focus on Claude Tag, loops, and dashboards rather than reviewing code and bug reports. If a skill goes stale, a bug class never reaches CLAUDE.md, or agent decisions go unsampled, the structure degrades.
- Practices:
  - Tier the codebase by risk; automate review per tier.
  - **Shadow mode** for every new AI reviewer: it posts comments for human approval until trust is earned; the team red-teams it by trying to insert malicious changes.
  - Sample a percentage of all automated approvals.
  - Watch vitals: a dashboard of key metrics across every security process.
  - Route every agent action to the SIEM: each automated approval, tool call, and agent-to-agent message is logged with its signals, so decisions are attributable and auditable. Agents are treated as a new kind of insider threat, with alerts when they act out of alignment.
- **Enduring principle:** the security engineer's job shifts from monitoring bugs to monitoring loops. Assessment framework: the CISO's guide to agentic AI.

## Keeping an AI SDLC secure as models evolve

- Capabilities advance monthly. What is not workable or affordable today likely will be soon. Ask "what would we run if scanning were nearly free?" rather than "can we afford to scan everything?", and plan for that.

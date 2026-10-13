# How Outtake built a cyber investigator on Claude — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/how-outtake-built-a-cyber-investigator-on-claude
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-22
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Products: Claude Code, Claude Platform. Author: Michael
Segner. Part of "How startups build with Claude". Case study; results
self-reported. Main voice: Jack Hayford, engineering lead for Outtake's agent
platform.

## Intro and quick pitch

- Outtake: founded 2023; founder/CEO Alex Dhillon (ex-Palantir). ARR grew 6x and
  customer base 10x+ year over year; scanned 20M+ potential cyberattacks in 2025.
- Customers include AI labs, hedge funds, and US federal agencies. Fleets of
  agents detect, investigate, and take down threats.
- Subject: the **Recon Agent**, a long-running autonomous cyber investigator
  built with Claude Code and the Claude Agent SDK.

## Agentic offense needs agentic defense

- Attack sequence: weaponize public data → build impersonation lures (e.g. fake
  login pages) → exploit internal systems. AI speeds every step.
- Legacy tools each guard one stage: threat intel (public data), brand
  protection (impersonations), endpoint tools (internal systems).
- The Recon Agent investigates the whole network behind an impersonation:
  gathers and classifies evidence, follows leads to connected infrastructure
  (e.g. a fake Telegram "Customer Support" account), maps the adversary network
  as a graph, and writes a report with process, actor profile, and timeline.
- It can read, write, and run code, and interacts with malicious login pages to
  see where stolen credentials go.
- Session length: median 16 minutes, often an hour or more; longest run two
  hours before returning results.

## How Outtake built a complex long-running agent with Claude

Four stages, each handing more judgment to the agent.

### Step 1: Become the expert first

Engineers ran real investigations themselves and gathered expertise from
customers and design partners to define "good": what evidence matters, how to
organize it, what separates an actionable conclusion from a guess. That standard
became the fixed reference for every later stage.

### Step 2: Prototype in Claude Code

Traditional agent frameworks fell short: the agent needed to write and run code,
build tools on the fly, and touch malicious domains. Claude Code served as the
initial harness to validate assumptions. Core design principle found here:
constrain tightly at the orchestration level ("always do X, Y, Z when
investigating a domain"), leave the agent free to improvise where judgment is
needed.

### Step 3: Graduate to a production-grade harness

Moved to the Claude Agent SDK for access to lower-level primitives. Skills and
patterns carried over from Claude Code, so no lost velocity; gained control of
memory, context, and filesystem without rebuilding the agent loop or session
handling.

### Step 4: Build a tight iteration loop driven by evals

- Evals from the start; a suite that runs many scenarios in parallel enabled
  sweeping changes (model upgrades, full memory-system refactors) safely.
- Self-improvement loop: when the Recon Agent reports it lacked a tool, a
  separate coding agent reads the suggestion, writes the tool, and builds a test
  scenario. A human only judges at the end whether the tool improved the
  investigation. Hayford: humans are the bottleneck; automate the feedback loop.

## Learnings from building a long-running agent

Framing: scripted step-by-step workflows are giving way to a harness of memory,
tools, skills, and guardrails.

### Tools: a filesystem and bash is all you need

A filesystem gives memory that survives compaction. Open-ended tools (filesystem
plus read/write/run code) let the agent route around failures; e.g. when a tool
failed on a network hiccup, the agent found a workaround and continued.

### Prompts are suggestions

In long-running agents, instructions added to the system prompt ("when X, do Y")
will eventually be ignored. Identify what must always happen and move it out of
the prompt into the harness as guardrails; this also frees context and
attention. Links to Anthropic's guidance on steering methods and their context
cost and authority.

### Evals are for speed, not just reliability

- Early on every run was reviewed manually; reading a 30-minute transcript does
  not scale. Hayford: evaluating output is the most expensive step in the loop.
- An eval is a structured, graded, automatable version of that manual
  "reflection". Once "good" is codified, an agent can judge the transcript and
  score the run.
- Build imperfect evals early; they speed development regardless.

### Protecting your agents

- Prompt injection is real; sandbox the agent. Outtake chose Claude partly for
  prompt-injection robustness.
- With filesystem and bash in adversarial environments, the key problem was a
  "blastbox": hide sensitive internals from the agent without hindering it.
  Design assumes the agent may be hijacked and contains the damage. Not every
  agent needs this.
- New: trust scoring at the point where the agent reaches the internet — a
  checkpoint that evaluates what the agent is about to touch (impersonation?
  malware? prompt injection?).

## Best practices from the Outtake team

- Know what "good" looks like: do the task yourself first; use customer and
  design-partner expertise as a fixed standard.
- Earn each piece of complexity: start with the simplest working version and
  automate piece by piece.
- Match harness to workload: validate in Claude Code, move to the Agent SDK for
  lower-level control; do not rebuild the agent loop.
- Constrain at the orchestration layer, not in low-level judgment calls; the
  improvisation space produces the best results.

## What's next

Recon Agent is live. Links to a webinar, a demo, and a free assessment
(marketing).

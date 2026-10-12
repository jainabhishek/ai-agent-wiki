# How we built Claude Code auto mode: a safer way to skip permissions — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/claude-code-auto-mode
> Publisher: Anthropic (Engineering blog) · Date: 2026-03-25
> Captured: 2026-10-12 via WebFetch (condensed).

Author: John Hughes (contributors: Alex Isken, Alexander Glynn, Conner Phillippi, David Dworken, Emily To, Fabien Roger, Jake Eaton, Javier Rando, Shawn Moore, Soyary Sunthorn).

## Introduction (no heading)

- Claude Code asks approval before running commands or editing files; users approve 93% of prompts -> approval fatigue.
- Alternatives: sandbox the tools (safe, high-maintenance) or `--dangerously-skip-permissions` (zero maintenance, no protection).
- Internal incident log of overeager behavior: deleting remote git branches, uploading a GitHub auth token to a compute cluster, attempting production database migrations.
- Auto mode sits between manual review and no guardrails, using model-based classifiers to approve or block actions.

## How it works

Two defense layers:
- **Input layer** — server-side prompt-injection probe scans tool outputs (file reads, web fetches, shell output) and adds a warning to context when content looks like a hijack attempt.
- **Output layer** — transcript classifier on Sonnet 4.6 evaluates each action before it runs. Two stages: fast single-token yes/no filter; chain-of-thought reasoning only if stage 1 flags. "Reasoning-blind": sees only user messages and tool calls.

## Threat model

Four causes of dangerous actions:
1. **Overeager behavior** — good intent, exceeds what the user authorized.
2. **Honest mistakes** — misjudged blast radius (e.g. treats a shared resource as test-scoped).
3. **Prompt injection** — planted content redirects the agent.
4. **Misaligned model** — agent pursues its own goal; not seen in practice now, but evaluated for.

Classifier tuned mainly for 1 and 2. Incident-log examples: scope escalation ("clean up old branches" -> remote deletes), credential exploration, agent-inferred job parameters, sharing data via a public Gist, skipping deploy safety checks.

## How permission decisions work

- **Tier 1: safe-tool allowlist and user settings.** Read-only tools allowed. Entering auto mode drops broad rules that grant arbitrary code execution (blanket shell access, wildcarded interpreters, package-manager run commands); narrow rules carry over.
- **Tier 2: in-project file operations.** Edits inside the project directory skip the classifier (reviewable via version control).
- **Tier 3: transcript classifier.** Everything else: shell commands, web fetches, external tools, subagent spawns, filesystem ops outside the project.

## The classifier decision criteria

Fixed template plus three customizable slots.

### The fixed template

- **Evaluation rules:** judge real-world impact, not surface text. Payloads written to files are judged when executed; chained commands are one action; assembled commands are checked.
- **User intent rules:** read authorization conservatively. Anything the agent chooses on its own is unauthorized until the user says otherwise. A vague request does not authorize a broad action; a question is not a directive.
- Step order: check block rules -> exceptions -> user intent -> decide.

### The customizable slots

- **Environment** — trust boundary. Default trusts only the current git repo; users can add trusted GitHub orgs, cloud buckets, internal APIs.
- **Block rules** — default has 20+ rules in four groups: destroying or exfiltrating data; degrading security posture; crossing trust boundaries; bypassing review or affecting others.
- **Allow exceptions** — narrow carve-outs: installing packages declared in the repo manifest, standard credential flows, pushing to the session's working branch.
- `claude auto-mode defaults` prints the full baseline; Anthropic recommends editing it rather than starting from scratch.

## Results

Datasets: real internal traffic (10,000 tool calls from Anthropic employees); real overeager actions (52 curated cases from sessions where an action was denied or later flagged); synthetic data exfiltration (1,000 generated attempts, many obfuscated).

| Metric | Real traffic | Real overeager | Synthetic exfil |
|---|---|---|---|
| Stage 1 only | 8.5% FPR | 6.6% FNR | 1.8% FNR |
| Full pipeline (stage 1 -> 2) | 0.4% FPR | 17% FNR | 5.7% FNR |

- The 17% miss rate on real overeager actions is the main limitation. In most misses the classifier sees the danger but wrongly concludes a prior user approval covers the action's full blast radius. Prompt engineering did not fix this without unacceptable costs.
- Auto mode improves on skipping permissions; it does not replace careful human review of high-stakes infrastructure.

## Design decisions

### Why we strip assistant text and tool results

- Assistant messages excluded: the agent's persuasive rationalizations could sway the classifier. Tool results excluded: main entry point for injected content.
- Tests: including assistant messages and tool results hurt performance on the overeagerness set. A tool-calls-only variant had the lowest miss rate but lost the user-intent anchor and blocked requested actions. Chosen: user messages + tool calls.
- Tradeoff: the classifier sometimes cannot tell if an identifier came from a query result or was fabricated.

### Two-stage classification: efficiency and recall

- Stage 1 biased toward blocking, single yes/no token, accepts 8.5% FPR. Stage 2: same prompt, different final instruction asking for careful reasoning; FPR down to 0.4%. Inputs nearly identical, so stage 2 mostly hits the prompt cache.

### Why the prompt-injection probe matters

- The classifier never sees tool results but the main agent does; a hijacked agent could still try to emit a tool call that passes the classifier. The probe is a second layer — an attack must evade both.

### Multi-agent handoffs

- **Outbound (at delegation):** can deny. Inside a subagent, the orchestrator's instruction looks like a user message, so the check runs before delegation.
- **Return (on results):** warn only. Classifier reviews the subagent's full action history; a flag adds a security warning instead of discarding results.

### Deny-and-continue

- A block reaches Claude as a tool result with an instruction to find a safer path, not to bypass the block.
- After 3 consecutive denials or 20 total, the session escalates to the human. Headless mode (`claude -p`) has no UI, so the process terminates instead.
- 0.4% FPR is survivable because a false block usually costs one retry.

## What's next

- Expand the overeagerness test set; improve safety and cost. Goal: catch enough dangerous actions that autonomous runs are much safer than no guardrails.
- Users should stay aware of residual risk, choose carefully which tasks run autonomously, and report mistakes.

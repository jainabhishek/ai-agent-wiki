---
title: "Anthropic: Prompting Claude Fable 5.1"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic
date: accessed 2026-10-12
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
source_path: raw/anthropic-prompting-claude-fable-5-1.md
models: [claude-fable-5-1, claude-mythos-5-1]
as_of: 2026-10-12
tags: [prompting, model-specific, anthropic, fable-5-1, mythos-5-1, long-horizon, harness]
---

# Anthropic: Prompting Claude Fable 5.1

> Anthropic's model-specific prompting page for Claude Fable 5.1 (and, per its page
> description, Claude Mythos 5.1) — behavioral differences from Claude Fable 5 and the
> prompt and harness patterns for them.

## Summary

The page's metadata description says it covers "Claude Fable 5.1 and Claude Mythos
5.1." The body text names only Claude Fable 5.1, and its code sample pins
`model="claude-fable-5-1"`. This page records both models in `models:` because of the
description; the `claude-mythos-5-1` ID follows the naming convention and is not
written on the page. The page has no byline date; this capture records the access
date.

The page says existing Claude Fable 5 prompts "should perform well … without
changes," and then lists a handful of behavioral differences. Two of them run in the
opposite direction from earlier models: Fable 5.1 narrates less and formats less, so
the advice is to **remove** older suppression instructions. Two others are new
tendencies: it quotes sources without marking them and rewrites whole files, and the
fix for each is an added instruction or worked example. The page also carries the strongest statement
yet of the append-only conversation rule. For new accounts from August 31, 2026,
thinking blocks are bound to the exact conversation prefix that produced them. See
[[prompt-tuning-axes]], [[agent-harness]], and [[context-engineering]].

## Key points

### Effort
Default `high`; sweep all five levels again. At `medium`, results roughly match Fable 5
at lower cost. At `low`, Fable 5.1 is "often competitive with Claude Opus and Claude
Sonnet models on cost per task while scoring higher." At `low` it searches less, and at
`xhigh`/`max` it can draft long deliverables twice (once in thinking, once in the
reply).

### Fewer progress updates
Fable 5.1 writes fewer updates during long tool chains than Fable 5. Steps in order:
receive updates (`display: "updates"` or `"summarized"`); remove "hold all findings"
lines; then add a short line that asks for an intent line, brief updates, and a
self-contained recap. If the UI hides tool output, tell the model in a turn-scoped
system message.

### Tool-call batching
In coding and computer-use loops the model may issue implied independent calls one per
turn. A one-sentence "list what you need, then request all independent items now"
nudge, appended after every tool-result turn as a turn-scoped system message
(`clear_at: "next_user_message"`), fixes it. Earlier copies stay byte-for-byte in place:
the API hides them, and deleting them would break the cache and thinking blocks.

### Append-only history and thinking-block binding
Return assistant turns exactly as received and never edit earlier turns. Replaying a
thinking block after its prefix changed returns 400, or drops the block with
`prefix_mismatch_behavior: "drop_block"` (beta). Edits that cause this are the same
edits that break the prompt cache. Use turn-scoped and mid-conversation system messages,
server-side compaction, or context editing instead. Client compaction should replace
the whole history with one summary. Because cache reads are cheaper, compacting later
may now be the better trade-off.

### Writing, formatting, and quoting
Prose can be denser than Fable 5; a definition of "mannered prose" fixes it, and works
best in a user message. Fable 5.1 under-formats, so replace anti-formatting rules with a
rule for when lists help. To stop unmarked source reproduction, add one full worked
example with a rationale, rather than a rule.

### Finish the whole task, within scope
Two system prompt blocks. The first is autonomous operation: the user is not watching;
do not ask permission for reversible requested work; execute stated next steps; assess
rather than fix when the user is only describing a problem; check evidence before state
changes. The opening sentence carries most of the effect. The second, "Delivering work,"
defines scope as the deliverable: no quiet narrowing or widening; do independent work
before asking; finish unblocked parts. A separate instruction limits unrequested fixes
and committed tests, which "drop substantially with no measurable change in task
success."

### Other patterns
- Compaction instruction listing six must-preserve categories, with the user's words
  kept close to verbatim.
- Search at `low`: raise effort per turn, or tell the model that recognizing a name is
  not knowing its current state.
- False positives: compile-check phrasing, lesser-known languages, and base64 in tool
  output.
- Targeted edits: a one-line token-minimization instruction restores Fable 5 behavior.
- Subagents: make the subagent-start tool non-blocking and add a separate wait tool.
- Vision: a container with PIL/OpenCV, or a crop tool alone for most of the uplift.

## Changes from the previous generation

Compared with [[anthropic-prompting-claude-fable-5]] (Claude Fable 5 and Claude
Mythos 5, now legacy).

**Added**
- Append-only history and thinking-block binding (`prefix_mismatch_behavior`), plus
  later compaction because cache reads are cheaper.
- Tool-call batching nudge with turn-scoped system messages and a full code sample.
- Compaction-summary instruction.
- Writing density ("mannered prose"), formatting in chat, quoting retrieved sources.
- Keep changes and tests to the task (test-file sizing rule).
- Search triggering at `low` effort.
- Safeguard false-positive triggers (compile-check phrasing, lesser-known languages,
  base64).
- Targeted edits vs whole-file rewrites.
- Long outputs at `xhigh`/`max` and the "do not draft twice" note.
- Progress updates as `thinking` blocks and the `display: "updates"` opt-in.

**Removed** (no counterpart on the Fable 5.1 page)
- Longer turns by default (timeouts, async checking) and the anti-overplanning prompt.
- Ground progress claims during long runs (the audit prompt that "nearly eliminated
  fabricated status reports").
- Construct a memory system (lesson files, bootstrap prompt).
- Rare cases of context-budget concern (avoid token countdowns; reassurance prompt).
- Give the reason, not only the request.
- Readability when communicating with the user (re-grounding final summary).
- The `send_to_user` tool and its elicitation prompt.
- Recommended scaffolding changes, including "fresh-context verifier subagents tend to
  outperform self-critique," start at the top of your difficulty range, and refactor
  over-prescriptive skills.
- Capability improvements list and fallback to Claude Opus 4.8.

**Merged or carried forward**
- Fable 5's early-stopping "operating autonomously" prompt and its "State the
  boundaries" prompt are combined into the 5.1 "Finish the whole task" first block,
  with only small changes in wording.
- The 5.1 "Delivering work" block is close to the scope-constraint prompt on
  [[anthropic-prompting-claude-opus-5]]. This suggests that Anthropic uses one shared
  scope prompt across model families.
- Fable 5's unrequested-tidying prompt becomes the narrower 5.1 changes-and-tests
  instruction.
- Fable 5's "use async subagent communication" advice becomes a concrete harness
  recipe: a non-blocking start tool and a separate wait tool.
- Fable 5's "readability drift" (dense shorthand in agentic chat) continues as 5.1's
  "writing density" problem, but the 5.1 fix targets mannered prose, not shorthand.

**Reversed**
- Progress updates: Fable 5 needed a `send_to_user` tool for verbatim content but
  otherwise narrated; 5.1 narrates *less* than Fable 5, and the fix is to opt in to
  update blocks and remove suppression lines.
- Formatting: earlier models over-formatted, and prompts suppressed formatting.
  Fable 5.1 under-formats, so the suppression lines should be removed.
- Safeguards: 5.1 classifiers produce fewer false positives than Fable 5's at launch;
  finding vulnerabilities in source code is explicitly permitted.
- Effort framing: Fable 5 compared lower effort with "`xhigh` performance on prior
  models"; 5.1 compares `low` with Opus and Sonnet on cost per task.

## Notable claims & data

- At `medium`, Fable 5.1 roughly matches Fable 5 at lower cost.
- The changes-and-tests instruction cut unrequested additions and committed test code
  substantially with no measurable task-success change.
- Non-blocking subagents lower average time to completion at similar quality, tokens,
  and cost.
- Thinking-block binding applies to accounts created on or after 2026-08-31.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-harness]], [[context-engineering]],
[[agent-orchestration]], [[agent-steering]], [[tool-design]], [[guardrails]],
[[agent-instructions]]

## Connections

Predecessor: [[anthropic-prompting-claude-fable-5]]. Siblings:
[[anthropic-prompting-claude-opus-5-5]], [[anthropic-prompting-claude-sonnet-5-5]],
[[anthropic-prompting-claude-haiku-5-5]]. The append-only and cache rules connect to
[[anthropic-prompt-caching-is-everything]] and
[[anthropic-new-rules-context-engineering-claude-5]]. The compaction instruction
connects to [[anthropic-eng-context-engineering]] and
[[anthropic-eng-effective-harnesses-long-running-agents]].

## Contradictions / open questions

- `models:` lists `claude-mythos-5-1` on the strength of the page description only; the
  body never mentions Mythos and the ID string does not appear. Verify against the
  models overview.
- Fable 5 recommended fresh-context verifier subagents; that advice is gone here, and
  [[anthropic-prompting-claude-sonnet-5-5]] says not to launch reviewer subagents
  unless asked. Whether the verifier-subagent finding still holds for Fable 5.1 is
  unstated.
- Fable 5's memory-system and progress-claim-audit guidance is not repeated. The page
  does not say whether the guidance is obsolete or simply carried over from Fable 5.

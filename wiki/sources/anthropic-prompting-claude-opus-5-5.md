---
title: "Anthropic: Prompting Claude Opus 5.5"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Anthropic
date: accessed 2026-10-12
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
source_path: raw/anthropic-prompting-claude-opus-5-5.md
models: [claude-opus-5-5]
as_of: 2026-10-12
tags: [prompting, model-specific, anthropic, opus-5-5, harness]
---

# Anthropic: Prompting Claude Opus 5.5

> Anthropic's model-specific prompting page for Claude Opus 5.5 — the behavioral
> differences from Claude Opus 5 and the prompt and harness patterns that address
> them.

## Summary

The page states its scope as "the prompting patterns specific to Claude Opus 5.5"
and says existing Claude Opus 5 prompts "should perform well without changes," with
[[anthropic-prompting-claude-opus-5]] still "a reasonable starting point." The page
has no byline date; this capture records the access date. The model generates output
tokens more than 30 percent faster than Opus 5 and tends to use fewer tokens per task.

The page is organized as a symptom index. Most sections are **harness** fixes rather
than prompt wording: how the client receives progress updates, how an unattended loop
decides a task is done, how reminders are appended so the prompt cache and preserved
thinking stay valid. The dominant theme shifts from the Opus 5 page's "subtract
scaffolding" to "the model now stops, goes quiet, or acts too fast in specific
situations; detect and redirect it." See [[prompt-tuning-axes]] and [[agent-harness]].

## Key points

### Effort is the only thinking control
Thinking is always on; `thinking: {"type": "disabled"}` is no longer accepted. The
default effort is `medium` (Opus 5: `high`). Anthropic reports Opus 5.5 at `medium`
matches or exceeds Opus 5 at `high` on coding and knowledge-work evals, and `low`
comes close on several coding evals. At a given level Opus 5.5 thinks *more* per turn
than Opus 5, especially at `xhigh`/`max`. Guidance: set effort explicitly, re-sweep,
size `max_tokens` for thinking plus reply (128,000 worked for long agentic turns),
lower effort before trying prompt instructions to cut thinking, and use the per-message
effort change (beta) rather than changing top-level `effort`, which breaks the cache.

### Migrating thinking-disabled integrations
Start at `low` and measure. Remove prompt lines that asked the model to write its
reasoning in the response; read `display: "summarized"` thinking instead, because such
lines can trigger the `reasoning_extraction` refusal. Re-test the Opus 5 thinking-off
mitigations, and always remove any "do not think" rule. Parse responses by block type.

### Unattended runs: text-only end of turn is not completion
Some progress updates end the turn with `stop_reason: "end_turn"`. Harness pattern:
keep a model-updated checklist; if items are open and no blocker is stated, send a
user message naming them; optionally have a smaller model judge a stated completion
condition at each end of turn; cap automatic continuations at two or three; wait for
background commands and subagents. The page supplies a long standing-instruction
prompt that names four unwanted ways to end a turn and the two wanted stops. It must
be in the system prompt from the first request, and it belongs only in fully
unattended agents.

### Progress updates moved into thinking blocks
On Opus 5.5 the between-tool-call notes arrive as progress-update `thinking` blocks
with empty text by default, so a text-only client looks silent. Four levers: opt in
with `display: "updates"` (beta); a send-a-message tool for verbatim content,
declared from the first request; a system instruction for predictable update points;
and a harness reminder appended as a turn-scoped system message after about five
silent tool steps. The reminder roughly halved long silent stretches with no
measurable cost change.

### New context and coordination patterns
- **Multi-app exploration:** one system line telling the model to open possibly
  relevant emails, documents, tabs, and records before acting raised correct
  completions at `medium` and `max`. Keep untrusted content out of searched records.
- **Time signals:** an `elapsed Ns / budgetNs` line on each message lets a lead agent
  pace and parallelize; teams finished considerably sooner at comparable quality. The
  budget is advisory; keep a hard timeout.
- **Chat thinking lines:** remove "think carefully" instructions in chat; optionally
  tell the model to treat earlier answers as settled to cut follow-up latency.
- **Pasted content:** wrap user-pasted text in `<pasted_content id="…">` tags with a
  random shared ID and explain the tags in the system prompt.

### Safeguards, vision, and frontend
Classifiers for biology (new relative to Opus 5; same as Claude Fable 5.1),
cybersecurity, and reasoning extraction. Declines return `stop_reason: "refusal"`
with `stop_details`; server-side fallback does not retry `reasoning_extraction`.
Vision needs less scaffolding; crop/zoom tools and higher resolution still help the
densest inputs. For frontend work, name the specific default patterns to avoid,
because a general "avoid generic AI look" only swaps defaults.

## Changes from the previous generation

Compared with [[anthropic-prompting-claude-opus-5]] (Claude Opus 5, now legacy).

**Added**
- Unattended-run harness pattern (checklist, continuation message, completion-check
  model, continuation cap) and the four-early-stops standing instruction.
- Progress updates as `thinking` blocks and the `display: "updates"` opt-in; the
  send-a-message tool; the appended turn-scoped reminder after silent steps.
- Multi-app "explore broadly first" instruction.
- Elapsed-time budgets for multiagent harnesses.
- Removal of "think carefully" lines in chat; the "treat earlier answers as settled"
  instruction.
- `<pasted_content>` tagging for user-pasted text (injection defense).
- Safeguard refusals section: biology classifier is new for Opus users;
  `reasoning_extraction` category; fallback behavior.
- Frontend design defaults with a named negative list.
- Explicit cache rules: per-message effort change; add tools and system instructions
  from the first request so preserved thinking stays valid.

**Removed** (no counterpart on the Opus 5.5 page)
- Response length and verbosity guidance, including the `<tone_preference>` reminder
  and the claim that effort does not shorten visible responses.
- Written deliverable length calibration.
- Task scope and over-verification: "remove verification instructions" and the scope
  constraint prompt.
- Controlling subagent spawning (caps and delegation criteria).
- Self-correction narration guidance.

**Reversed or changed**
- Default effort `high` → `medium`, and at a given level Opus 5.5 thinks more per turn
  than Opus 5. Effort sweeps from Opus 5 do not carry over.
- Thinking disabled was allowed at `high` or below → not accepted. The Opus 5
  "Running with thinking disabled" section changes from a mitigation recipe (tool
  calls as text, leaked XML tags) into a migration checklist: re-test whether the
  combined instruction is still needed, and always remove any no-thinking rule.
- Progress narration: Opus 5 narrated *too much* and the advice was to tune it down;
  Opus 5.5's problem is clients that *see nothing*, so the advice is to receive updates
  and prompt for more.
- Completion: Opus 5 tended to expand scope and over-verify; Opus 5.5's main agentic
  failure is ending a turn early with a report.
- Vision: Opus 5 said tools were a more cost-effective lever than thinking; Opus 5.5
  says re-test vision scaffolding because it reads charts well without tools.

## Notable claims & data

- Output generation more than 30 percent faster than Opus 5.
- Opus 5.5 at lowest effort read dense-chart values more accurately than Opus 5 at
  highest, at a small fraction of output tokens.
- Silent-step reminder: share of tasks with a long silent stretch roughly halved, no
  measurable cost change.
- Prompt instructions to think less are less reliable than lowering effort.

## Entities

[[anthropic]], [[claude]]

## Concepts

[[prompt-tuning-axes]], [[agent-harness]], [[agent-steering]],
[[agent-orchestration]], [[context-engineering]], [[guardrails]], [[tool-design]],
[[agent-instructions]]

## Connections

Predecessor: [[anthropic-prompting-claude-opus-5]]. Siblings in the same generation:
[[anthropic-prompting-claude-sonnet-5-5]], [[anthropic-prompting-claude-haiku-5-5]],
[[anthropic-prompting-claude-fable-5-1]]. The silent-step reminder and turn-scoped
system message pattern also appears on the Sonnet 5.5 and Fable 5.1 pages. Related
launch and practice posts: [[anthropic-getting-most-out-of-opus-5-5]],
[[anthropic-prompt-caching-is-everything]]. The early-stop problem continues the
"early stopping" failure mode first recorded in [[anthropic-prompting-claude-fable-5]].

## Contradictions / open questions

- The Opus 5 and Sonnet 5 pages state that positive examples work better than
  "what not to do" instructions. This page's frontend section says a list of named
  patterns to avoid works where a general instruction fails. Both can hold (named
  negatives vs vague negatives), but the general claim needs a qualifier.
- Fable 5 warned against showing a remaining-token countdown; this page recommends an
  elapsed-time budget line on each message. They are different signals; no page says
  whether a time countdown causes the same budget-anxiety behavior.

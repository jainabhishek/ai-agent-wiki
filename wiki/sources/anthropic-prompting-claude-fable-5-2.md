---
title: "Anthropic: Prompting Claude Fable 5.2"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Anthropic
date: accessed 2026-11-24
source_url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
source_path: raw/anthropic-prompting-claude-fable-5-2.md
models: [claude-fable-5-2, claude-mythos-5-2]
as_of: 2026-11-24
tags: [prompting, model-specific, anthropic, fable-5-2, mythos-5-2, long-horizon, harness, migration]
---

# Anthropic: Prompting Claude Fable 5.2

> Anthropic's model-specific prompting page for Claude Fable 5.2 (and, per its page
> description, Claude Mythos 5.2). It lists behavior differences from earlier
> models and the prompt and harness changes for each one.

## Summary

The page's metadata description says it covers "Claude Fable 5.2 and Claude Mythos
5.2." The body names Fable 5.2 throughout. It says Mythos 5.2 has the same
capabilities and is offered only to organizations in the Cyber and Life Sciences
verification programs. No API model ID string is written on the page. This page
records `claude-fable-5-2` and `claude-mythos-5-2` from the naming convention. The
page has no byline date; this capture records the access date.

The page replaces [[anthropic-prompting-claude-fable-5-1]] as the current Fable
guide. Fable 5.1 now appears in the vendor's older "All models" table. The current
lineup is Fable 5.2, Opus 5.5, Sonnet 5.5, and Haiku 5.5 (see
[[anthropic-which-claude-model-to-build-with]]).

The theme of the page is that Fable 5.2 follows instructions closely. Old
instructions therefore matter more. Cautions in memory files, "never" rules, style
limits, delegation lines, visible token budgets, and "think less" lines all change
its behavior, often for the worse. Much of the page is a migration checklist of
text to remove. The added text is short and each block comes with a measured
effect and a measured token cost. See [[prompt-tuning-axes]], [[agent-instructions]],
[[agent-memory]], and [[agent-harness]].

## Key points

### Effort
- Default `high` on the Claude API. Rerun the effort sweep; do not reuse a level
  tuned on Fable 5.1 or Opus 5.5.
- Most of the gain arrives at `high`. The `medium` → `high` step raised most coding
  and knowledge-work scores. Above `high`, gains are uneven.
- `low` on coding evals scored close to Fable 5.1 at higher effort.
- At `high` and above, the model thinks before almost every reply, even a greeting.
  A "do not deliberate" line does not stop thinking at `medium` and above. Use a
  lower effort level for basic turns instead.
- Effort has little effect on reply length. Per-message effort (beta) keeps the
  cache when you change levels.

### Finish the whole task, and approvals
- Fable 5.2 sometimes stops early: it lists what is left, offers to continue, or
  stops at an ordinary obstacle. This is more common at `low` and `medium`.
- A "# Finishing work" block tells it to diagnose ordinary obstacles and work
  through them, and to leave deliberate blockers alone and report them. On replayed
  coding sessions at `medium`, unfinished-but-continuable endings fell by about half.
  Output tokens rose about 30%. Endings that list remaining work and stop were not
  fixed.
- Approvals: reply with the exact action ("run the migration on staging"), not
  "continue". An approval rule that named "sending messages to people outside this
  conversation" made the model hold back about half of its routine messages to
  colleagues.

### Code ownership
- With no ownership statement, or with the code framed as someone else's, the model
  adds to the existing structure, even if that duplicates code.
- One sentence that says the model owns and maintains the codebase raised the rate
  of consolidating duplicated code from under 10% of runs to about 75%. Output tokens
  rose 70–80%. Unrequested tests and docs appeared, and some runs changed existing
  feature behavior. PR summaries often left out small changes.
- A "no drive-by refactors" rule in the same prompt does not cancel the ownership
  sentence. Consolidation still happened in more than half of runs.

### Progress updates
- Updates come back as progress-update `thinking` blocks. They are empty at the
  default `display: "omitted"`. Set `"updates"` or `"summarized"`.
- Harness option: count consecutive silent tool steps. Then append a turn-scoped
  "the user hasn't heard from you" reminder (`clear_at: "next_user_message"`). The
  longest silent stretch roughly halved at no noticeable token cost. Leave old
  reminders in place.
- An intent/updates/recap system line produced an opening message in every run, for
  about 20% more output tokens. A one-line "update every few tool calls" fallback
  works when there are no mid-conversation system messages.

### Subagents
- Delegation follows the harness. With a minimal tool, the model rarely delegates.
  With prompts that invite delegation, it delegates readily.
- At `xhigh`/`max` it used subagents to review its own work. Fable 5.1 did not do
  this on the same tasks.
- Early testers did well with Fable 5.2 as planner and orchestrator of other models.
- If it over-delegates, rewrite the subagent tool description. State the cost of a
  subagent, when to delegate, and how to brief one. A longer, cost-focused
  description roughly halved the subagent count at `high`.

### Caution that piles up, and migration review
- Cautions build up in memory, notes, and instruction files. The model follows them
  closely, mostly in multi-agent setups. Remove stale notes ("never retry"). List
  the steps that need no approval. Narrow the stop conditions. Write scoped rules
  instead of "never" rules, because the model reads "never" as absolute.
- Review list: standing delegation lines; token budgets shown in the prompt
  (removing a large one cut cost at equal performance); harness code that edits
  earlier turns; the Opus 5.5 "treat that answer as done" lines (these cut
  self-correction on follow-ups); "think less" lines; hard style rules (for example
  a 20-word sentence cap makes prose choppy); and accumulated rules and memories.
  If a system is stuck, restart it with trimmed memory.

### Reports
- Early testers rated the writing above Fable 5.1's and similar in clarity to
  Opus 5.5's.
- A "# Communicating clearly" block covers a low-context reader, key points first,
  no invented terms, and mostly ASD-STE100 Simplified Technical English. It made
  final reports less dense, with fewer semicolons.

### Refusals
- `stop_reason: "refusal"` with `stop_details.category`: `cyber`, `bio`,
  `frontier_llm`, `reasoning_extraction`, `general_harms`, or `null`.
- Remove prompts that ask for reasoning in the reply. Read
  `display: "summarized"` thinking instead.

### Where to start
1. Set `effort: high` explicitly, and also eval `medium` and `xhigh`.
2. Audit the carried-over prompts, skills, agent files, memory, notes, and harness
   text.
3. Run the longest agentic tasks and note the failure behaviors.
4. Add one fix at a time and measure its effect and token cost.

## Changes from Fable 5.1

Compared with [[anthropic-prompting-claude-fable-5-1]] (Claude Fable 5.1, now in
the vendor's older-models table).

**Framing**
- The 5.1 page said Fable 5 prompts "should perform well … without changes." The
  5.2 page makes no such claim. It says Fable 5.2 behaves differently "in several
  ways" and tells you to audit what you carry over.
- The 5.2 page attaches a measured token cost to most added prompts (+30%, +70–80%,
  +20%). The 5.1 page mostly reported effects without costs.

**Added**
- Code ownership as a steering lever, with numbers.
- Approval wording, and the finding that broad approval rules suppress routine work.
- "Keep caution from piling up" (stale memory, "never" read as absolute).
- A migration review list: visible token budgets, Opus 5.5 "treat as done" lines,
  "think less" lines, hard style rules, and delegation lines.
- "Make reports easy to follow" (the "Communicating clearly" block).
- A harness counter for silent tool steps, with a turn-scoped reminder.
- Subagent over-delegation, and self-review subagents at `xhigh`/`max`.
- Per-level effort guidance (what each of the five levels suits).
- Six named refusal categories, including `null`.

**Removed** (no counterpart on the 5.2 page)
- The writing-density ("mannered prose") instruction and the formatting-in-chat
  rule.
- Quoting retrieved sources (the worked example).
- The compaction-summary instruction (six must-preserve categories).
- Keep changes and tests to the task (test-file sizing rule).
- Search triggering at `low` effort.
- Safeguard false-positive triggers (compile-check phrasing, lesser-known languages,
  base64).
- Targeted edits vs whole-file rewrites.
- Long outputs at `xhigh`/`max` ("do not draft twice").
- The tool-call batching nudge and its code sample.
- Non-blocking subagents with a separate wait tool.
- Vision crop-and-zoom tools.

**Carried forward or changed**
- "Finish the whole task" stays, but the prompt is new. The 5.1 prompt was framed
  as "the user is not watching", with a scope block. The 5.2 prompt is "Finishing
  work": work through ordinary obstacles and respect deliberate blockers. 5.2 also
  notes that early stopping is worse at lower effort.
- Progress updates: the `display: "updates"` opt-in and the intent/updates/recap
  line carry over almost unchanged. 5.2 adds the silent-step counter and a
  one-line fallback.
- Append-only history: on 5.1 the thinking-block binding applied to accounts
  created on or after 2026-08-31. On 5.2 the prefix check is described without that
  limit, and [[anthropic-which-claude-model-to-build-with]] says Fable 5.2 "extends
  preserved thinking to every API account." 5.2 also says the Message Batches API
  drops the blocks rather than rejecting the request.
- `reasoning_extraction`: on 5.1 it was a note; on 5.2 it is one of six listed
  categories.

**Reversed**
- Scope versus improvement. 5.1 needed an instruction to stop unrequested fixes and
  extra tests. 5.2 by default adds to existing structure. You need an ownership
  sentence to get consolidation, and that sentence then brings the unrequested
  changes back.
- Instruction-following on "think less". Fable 5.1 usually obeyed "answer directly
  without deliberating"; Fable 5.2 does not at `medium`+.
- Subagent behavior. 5.1 advice was to let the lead keep working while subagents
  run. 5.2 advice is about subagent count and cost.

## Notable claims & data

- "Finishing work" text: about half as many continuable unfinished endings; about
  +30% output tokens (replayed sessions, `medium`).
- Ownership sentence: consolidation under 10% → about 75% of runs; +70–80% output
  tokens; still more than 50% with a no-refactor rule present.
- Silent-step reminder: longest silent stretch roughly halved, with no noticeable
  token or time increase.
- Intent/recap line: a pre-tool message in every run; about +20% output tokens.
- A cost-focused subagent description roughly halved the subagent count (`high`).
- Removing a large visible token budget lowered cost at equivalent performance
  (`high`, `xhigh`).
- A broad "messages outside this conversation" approval rule held back about half of
  the routine requests.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-agent-sdk]]

## Concepts

[[prompt-tuning-axes]], [[agent-instructions]], [[agent-memory]], [[agent-harness]],
[[agent-steering]], [[agent-orchestration]], [[multi-agent-economics]],
[[context-engineering]], [[guardrails]], [[human-agent-teams]]

## Connections

Predecessor: [[anthropic-prompting-claude-fable-5-1]] (and before it
[[anthropic-prompting-claude-fable-5]]). Siblings:
[[anthropic-prompting-claude-opus-5-5]] (source of the "treat that answer as done"
lines that this page warns about), [[anthropic-prompting-claude-sonnet-5-5]], and
[[anthropic-prompting-claude-haiku-5-5]]. Model choice and pricing:
[[anthropic-which-claude-model-to-build-with]]. A multi-agent run on an early Fable
5.2: [[anthropic-scaling-multi-agent-teams-fable-5-2]]. That run's finding that
agents misjudge difficulty and give up early matches this page's early-stopping
section. Effort framing: [[anthropic-spending-your-effort]]. Append-only and cache
rules: [[anthropic-prompt-caching-is-everything]].

## Contradictions / open questions

- `models:` lists `claude-mythos-5-2` and `claude-fable-5-2` by naming convention.
  Neither ID string appears on the page. Verify both against the models overview.
- The "Communicating clearly" block recommends ASD-STE100 style. The
  "Review prompts" section warns that a hard style rule ("one instruction per
  sentence, in 20 words or fewer") makes Fable 5.2's prose choppy. The page's own
  resolution is to prefer "mostly" STE style over hard limits.
- Fable 5.1's advice on mannered prose, quoting, compaction summaries, and targeted
  edits is not repeated. The page does not say whether those behaviors are fixed on
  5.2 or whether the advice still applies.

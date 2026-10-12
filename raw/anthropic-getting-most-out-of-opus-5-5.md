# Getting the most out of Opus 5.5 in Claude and Claude Code — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/getting-the-most-out-of-opus-5-5/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-09-22
> Author: Addy Osmani. Category: Playbooks. Subtitle: how to prompt Opus 5.5, steer
> a long run, and check results in Claude apps and Claude Code.
> Captured: 2026-10-12 via curl + local HTML-to-text (condensed, paraphrased;
> section-complete — every H2/H3 of the original appears below). The page states no
> API model ID; it addresses "Opus 5.5" in Claude apps and Claude Code.

## Intro

Opus 5.5 works with existing usage, but differs: it works longer on its own, says
plainly what it did, and thinks before every reply. Guide covers prompting,
steering long runs, and checking results in Claude apps and Claude Code.

## Try this first

Three first-session moves: hand over the whole task, stating what "done" means and
when to stop and ask, then let it work; delete "think carefully" lines (it already
thinks before every reply); when a long run ends, read what it needs from you first.

## 1. How to ask

### Say what “done” looks like, then let it run

Give the whole task in one message; name the finish line (e.g. tests pass, every
endpoint migrated). Why: Opus 5.5 sustains long multi-part work better than Opus 5;
biggest gains vs prior Opus models are on multi-step work like carrying a change
through a large repo until tests pass; early testers ran long coding tasks for hours
with little oversight. Example Claude Code prompt (paraphrased): migrate the payment
endpoints to the new client; done = every endpoint uses it, old client deleted,
suite passes; stop and ask only if a test fails for an unexplained reason.

### Stop telling it to “think hard”

Remove "think carefully", "think step by step" and similar lines from prompts and
saved instructions. Why: Opus 5.5 always thinks before replying and decides how
much. In Anthropic's chat-product testing, removing a "think carefully" line made
replies start sooner with no clear quality drop. For a quick answer to a simple
question, say "Answer directly." To change thinking amount in Claude Code, change
effort.

### Add to a running task

Type a follow-up mid-run (Enter while Claude works). Why: runs are longer, so
restarts cost more.

### For design work, name the styles you don’t want

Without design direction, Opus 5.5 falls back on a few default styles; a generic
"avoid a generic look" mostly swaps one default for another; a list of specific
patterns works better. Example exclusion list for a placeholder personal website:
no cream/off-white background, no italic accent words in headings, no numbered
"01 / 02 / 03" section labels, no monospace labels, no pill-shaped buttons. Then
inspect what it chose instead and extend the list iteratively.

## 2. Steering a long run in Claude Code

### Tell it which stops you want

Put a short CLAUDE.md rule on when to stop and ask vs keep going. Why: Opus 5.5
keeps the user posted; on long tasks it sometimes stops to report rather than
continue — a summary that names the next step without taking it, an offer to
continue, or a list of non-blocking choices. It follows instructions that name
these stops; also name the stops you do want. Suggested CLAUDE.md rule
(paraphrased): when a step needs no input, keep going and put status notes in the
same message as the next action; stop and ask only when you can't continue without
the user, or before anything destructive (deleting data, force-pushing, changing
anything outside the repo). If a run stops with "Want me to continue?", reply
"continue"; if frequent, add the rule. A keep-going rule means fewer stops, so keep
your own check before risky/irreversible steps (the rule's last clause) and keep
permission prompts on for destructive commands. For pair programming, the opposite
may suit: a one-line plan up front and a short recap at the end — put that in
CLAUDE.md instead; Opus 5.5 follows either.

### Ask it to split big work across subagents

For audits, migrations, or reviews across a large codebase, ask it to split work
across subagents and check each result. Why: early testers had it coordinate
parallel subagents on long audits/migrations with little oversight. Example prompt
(paraphrased): audit every service in `services/` for a linked retry bug, one
subagent per service, check each subagent's evidence before accepting it, finish
with one table (service, affected yes/no, evidence).

### Keep the task list in a file

For long runs, have it keep and update a task list in a file, and read the file
rather than scrollback. Why: long runs fill the context window and Claude Code then
summarizes older turns; a file survives that and shows done vs left. Example:
keep a checklist in `TASKS.md`, tick items, add new findings.

## 3. Checking the result

### Read what it needs from you first

When a long run ends, first look for anything Claude is waiting on (an open
decision, a change to approve), then read the rest. Why: Opus 5.5 reports more
clearly than Opus 5 — what it did, found, and needs, in plain language. To change
the summary format, say so in CLAUDE.md, e.g. end every run with three headings:
Blocked on me, Changed, Found.

### Ask it to review the code

Ask Opus 5.5 to review a diff/PR before a person does. Why: one early tester said
Opus 5.5 at its lowest effort caught more bugs than Opus 5 at high effort, with
fewer false alarms; it also explains changes plainly, so PR descriptions are easier
to review. Example prompt (paraphrased): review the branch diff against main; list
only problems you'd block the merge for; for each give file and line, why it's
wrong, and how to show it fails.

### Ask it to mark what it couldn’t confirm

For research/analysis, ask it to mark anything it couldn't confirm and say where it
looked. Works in Claude research reports and Claude Code.

## 4. In Claude apps

First check the model picker says Opus 5.5.

### Share the chart or screenshot itself

Attach the chart/diagram/screenshot/slide rather than retyping numbers. Why: reads
them more accurately than Opus 5 with no extra steps; better at position-dependent
meaning (which boxes an arrow connects, what changed between diagram versions, a
meeting's start/end in a calendar screenshot). Ask a specific question.

### Ask it to check a long document

Give a long plan/report/deck and ask for mistakes. Why: more attention to detail
than prior Opus; in testing caught a date on the wrong weekday in a long planning
thread and a chart not matching a deck's numbers. Example: check a deck for
self-contradictions in numbers, dates, names; quote each and locate it.

### Ask for the finished file

Ask for the spreadsheet/document, not an outline. Why: its files need less editing
than Opus 5's before sharing.

### In a project, say when answers are settled

If follow-ups in a long chat feel slow, add a project instruction that earlier
answers are settled. Why: in long chats Opus 5.5 sometimes re-examines an earlier
answer while thinking about a short follow-up, slowing the reply. Instruction
(paraphrased): once answered, treat it as done; focus on the current ask; don't
revisit an earlier answer unless asked or a problem is pointed out. Leave it out of
projects for long analysis where later steps can reveal earlier mistakes.

## 5. When a message is flagged

Opus 5.5 is the first Opus model to launch with Fable-level bio and cyber
safeguards. In Claude apps and Claude Code most flagged messages move to an older
model and work continues there. Finding security vulnerabilities in source code is
allowed; everyday health and educational questions should work. Safeguards can
flag legitimate work; Anthropic is tuning to reduce incorrect flags.

### In Claude apps

User sees a notice starting "Switched to" plus an older model's name; the chat
stays on that model. To return, pick Opus 5.5 in the model picker (the earlier
message may be re-flagged; a new chat avoids that). To be asked first: Settings →
Capabilities → turn off "Switch models when a message is flagged" (shows a "paused"
card with options). The check covers the whole conversation, including files and
search results, so a flag can stem from earlier content.

### In Claude Code

A notice names the older model; the session continues on it. Options: `/model` to
switch back; Esc twice to edit the last message and retry; `/config` to change
"Switch models when a message is flagged"; `/feedback` if the flag was wrong.

### Don’t ask it to show its reasoning in the reply

Remove requests to reproduce internal reasoning in the reply — they can be declined
(one of the flag categories). Instead ask for what you need, e.g. explain the
chosen approach in three sentences.

## 6. Speed

### Turn on fast mode when you’re waiting on each reply

In Claude Code use fast mode for back-and-forth work. Available for Opus 5.5 at
launch as a research preview: same model, text arrives sooner; requires extra usage
enabled and costs more per token than standard mode. Command: `/fast`.

## Your Opus 5.5 checklist

Asking: task states what "done" looks like; no "think hard" lines in prompts or
saved instructions; design requests list styles to leave out; charts and
screenshots attached, not retyped.
Long runs in Claude Code: CLAUDE.md says when to stop vs keep going and to stop
before anything destructive; permission prompts still on for destructive commands;
large audits/migrations split across subagents; task list kept in a file.
Checking: "needs from you" part read first; a review pass runs before human review;
research answers mark what couldn't be confirmed.
Flags: know how to switch back (model picker or `/model`); "Switch models when a
message is flagged" set as desired.

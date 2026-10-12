---
title: "Anthropic: Getting the Most Out of Opus 5.5 in Claude and Claude Code"
type: source
created: 2026-10-12
updated: 2026-10-12
author: Addy Osmani (Anthropic, claude.dev blog)
date: 2026-09-22
source_url: https://claude.dev/blog/getting-the-most-out-of-opus-5-5/
source_path: raw/anthropic-getting-most-out-of-opus-5-5.md
models: [claude-opus-5-5]
as_of: 2026-10-12
tags: [model-specific, anthropic, opus-5-5, claude-code, long-running-agents, prompting, safeguards]
---

# Anthropic: Getting the Most Out of Opus 5.5 in Claude and Claude Code

> A user-facing playbook for Claude Opus 5.5 in the Claude apps and [[claude-code]].
> It covers how to ask, how to steer long runs, how to check results, and what
> happens when a safeguard flags a message. It is the end-user companion to the
> docs page [[anthropic-prompting-claude-opus-5-5]].

## Summary

**Applicability.** The post addresses "Opus 5.5 in Claude apps and Claude Code".
It states **no API model ID**. The `claude-opus-5-5` ID in the frontmatter comes
from the docs page for the same model, not from this post. The post names three
behavioral differences: Opus 5.5 works longer on its own, it reports plainly what
it did, and it "thinks before every reply". Its advice groups into four themes.
(1) Hand over the whole task, with an explicit finish line and stop conditions.
(2) Delete "think carefully" lines. (3) In Claude Code, write in CLAUDE.md which
early stops you want and which you do not. (4) Read the "needs from you" part of a
run's report first. All comparisons are against Opus 5. See [[prompt-tuning-axes]],
[[agent-steering]].

## Key points

### Try this first
- Hand over the whole task. Say what "done" looks like and when to stop and ask.
- Delete "think carefully" lines.
- After a long run, read first what the model needs from you.

### 1. How to ask
- **Define "done", then let it run.** The post says Opus 5.5 is better than Opus 5
  at long multi-part work. Its biggest gains are on carrying a change through a
  large repo until the tests pass. Early testers ran tasks for hours with little
  oversight. The example prompt states the goal, a done-condition with three parts,
  and one narrow stop condition (a test failing for an unexplained reason).
- **Stop telling it to "think hard".** The post says Opus 5.5 always thinks before
  replying and decides how much. In Anthropic's chat-product testing, removing a
  "think carefully" line made replies start sooner, with no clear quality drop.
  For simple questions, say "Answer directly". In Claude Code, use effort to
  change the amount of thinking.
- **Add to a running task** by typing mid-run. Runs are longer, so restarts cost
  more.
- **Design work: list the specific styles to exclude.** A generic "avoid a generic
  look" swaps one default for another. The example list excludes five patterns:
  cream or off-white backgrounds, italic accent words, "01 / 02 / 03" section
  labels, monospace labels, and pill buttons. Iterate on the list after you see
  what the model chose instead.

### 2. Steering a long run in Claude Code
- **Name the stops.** On long tasks, Opus 5.5 sometimes stops to report instead of
  continuing. The post names three such stops:
  - a summary that names the next step without taking it;
  - an offer to continue;
  - a list of choices that do not block the work.

  The post suggests a two-sentence CLAUDE.md rule, paraphrased: keep going when a
  step needs no input, and put status notes in the same message as the next
  action; stop only when blocked on the user, or before destructive actions
  (deleting data, force-pushing, changing anything outside the repo). Keep
  permission prompts on for destructive commands. For pair programming, the
  opposite rule fits: a one-line plan first and a recap at the end. "Opus 5.5
  follows either one."
- **Fan out to subagents** for audits, migrations, and large reviews. Tell the
  orchestrator to check each subagent's evidence before accepting it. End with one
  table. See [[agent-orchestration]].
- **Keep the task list in a file** (for example `TASKS.md`). Claude Code summarizes
  older turns when context fills. A file survives that summary and is easier to
  read than scrollback. See [[context-engineering]].

### 3. Checking the result
- **Read the "needs from you" part first.** Change the summary format through
  CLAUDE.md. Example: three closing headings, Blocked on me, Changed, Found.
- **Ask it to review the code** before a human does. One early tester said Opus 5.5
  at its *lowest* effort caught more bugs than Opus 5 at high effort, with fewer
  false alarms. The example prompt asks only for **merge-blocking** problems, each
  with a file and line, the reason, and how to show the failure.
- **Ask it to mark what it could not confirm**, and where it looked.

### 4. In Claude apps
- **Attach the chart or screenshot**; do not retype the numbers. The post says
  reading is more accurate than Opus 5 "with no extra steps". This includes
  position-dependent meaning: which boxes an arrow connects, what changed between
  diagram versions, and calendar start and end times.
- **Ask it to check long documents** for self-contradictions. In testing it caught
  a date on the wrong weekday and a chart that did not match a deck's numbers.
- **Ask for the finished file**, not an outline.
- **In a project, mark answers as settled.** In long chats the model sometimes
  re-thinks earlier answers before a short follow-up, which slows the reply. A
  project instruction can declare answered items done. Leave this instruction out
  of long-analysis projects.

### 5. When a message is flagged
- Opus 5.5 is the first Opus model to launch with Fable-level bio and cyber
  safeguards. Finding vulnerabilities in source code is allowed. Everyday health
  and educational questions should still work.
- In the apps and in Claude Code, most flagged messages move to an **older model**,
  and work continues there.
  - Apps: a "Switched to …" notice appears. Switch back in the model picker; a new
    chat avoids a repeat flag. To be asked first, turn off "Switch models when a
    message is flagged" under Settings → Capabilities.
  - Claude Code: switch back with `/model`, edit and retry with Esc Esc, change
    the switching setting with `/config`, and report a wrong flag with `/feedback`.
- The check covers the whole conversation, including files and search results.
- **Do not ask it to show its reasoning in the reply.** That request is a flag
  category. Ask for a short explanation instead.

### 6. Speed
- Fast mode (`/fast`) for Opus 5.5 is a research preview at launch. It is the same
  model with faster text. It needs extra usage turned on and costs more per token.

## Notable claims & data

- At its lowest effort, Opus 5.5 caught more bugs than Opus 5 at high effort, with
  fewer false alarms. This is a single early tester's report.
- In chat, removing "think carefully" made replies start sooner with no clear
  quality drop. This comes from Anthropic's testing.
- Fable-level bio and cyber safeguards are a first for an Opus model at launch.

## Entities

[[anthropic]], [[claude]], [[claude-code]]

## Concepts

[[prompt-tuning-axes]], [[agent-steering]], [[agent-instructions]],
[[agent-orchestration]], [[context-engineering]], [[guardrails]]

## Connections

- **Comparison with the docs page [[anthropic-prompting-claude-opus-5-5]]**
  (compared against the docs capture downloaded 2026-10-12). Most advice matches
  the docs. Matching points: drop thinking instructions in chat; name the early
  stops you want to avoid; frontend design exclusion lists; settled answers in
  chat; don't request reasoning in the reply; and the chart, deck, and
  weekday-error capability examples. The docs add API mechanics that the blog
  omits: the `medium` default effort, `max_tokens`, progress-update `thinking`
  blocks, the reminder harness pattern, time budgets for multi-agent teams, the
  pasted-content tags, multi-app exploration, and the crop and zoom tools. Points
  of disagreement or simplification:
  1. *"Thinks before every reply."* The blog says Opus 5.5 always thinks before
     replying. The docs say thinking is always *enabled*, but at `low` effort how
     often the model skips thinking altogether depends on the prompts. The docs
     also say a response "may or may not" begin with a `thinking` block. The blog
     overstates this.
  2. *The keep-going rule in interactive Claude Code.* The blog recommends a
     keep-going CLAUDE.md rule for normal Claude Code use. The docs' longer
     equivalent paragraph is written for *fully unattended* agents. The docs say to
     leave it out of human-in-the-loop applications. The blog does mention the
     pair-programming alternative and the destructive-action stop.
  3. *Settled answers.* The blog gives the instruction without the docs' caveat
     that it may make the model less likely to point out a mistake in an earlier
     answer on its own.
  4. *Visual inputs.* The blog says "no extra steps" are needed. The docs agree
     that tool-free reading has improved. The docs still recommend higher
     resolution and crop, zoom, or code tools for the densest inputs. This is a
     simplification, not a reversal.
- Predecessor: [[anthropic-prompting-claude-opus-5]]. Sibling:
  [[anthropic-building-with-sonnet-5-5]], which positions Opus 5.5 for complex,
  long-horizon judgment work.
- The task list kept in a file and the finish line defined up front match the
  progress-file pattern in [[anthropic-eng-effective-harnesses-long-running-agents]].
- The CLAUDE.md stop rules are an instance of the steering mechanisms in
  [[anthropic-steering-claude-code]].

## Contradictions / open questions

- **Code-review prompt vs [[anthropic-prompting-claude-opus-5]].** This blog's
  review prompt asks Opus 5.5 to "list only problems you'd block the merge for". The
  Opus 5 docs page warns of a risk: severity-filtering review prompts ("only report
  high-severity issues") are followed literally, which reduces the findings
  reported. That page recommends asking for everything and filtering in a separate
  pass. The two pages cover different model generations, so this is not a direct
  contradiction. It is still unresolved whether the Opus 5 warning carries over to
  Opus 5.5. The Opus 5.5 docs are silent on review-prompt filtering.
- This page is scoped to `claude-opus-5-5`. It becomes stale by construction if
  Anthropic moves the model to its legacy list.

---
title: "Anthropic (Eng): The Components of Agent Memory"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Lance Martin (Anthropic Engineering)
date: 2026-11-06
source_url: https://www.anthropic.com/research/components-of-agent-memory
source_path: raw/anthropic-eng-components-of-agent-memory.md
tags: [memory, dreaming, sleep-time-compute, wikis, context-engineering, evals, primary-source]
---

# Anthropic (Eng): The Components of Agent Memory

> Anthropic's model of agent memory as in-session notes plus offline
> **dreaming** — a pass that reviews transcripts to correct notes, build wikis,
> promote an index into every session, and fill gaps — with eval results for
> each component.

## Summary

Agent memory here means knowledge Claude gains from experience and keeps
between sessions as readable context. It excludes weight changes, in-context
learning, and compaction. The post uses a brain analogy: fast in-the-moment
encoding (the hippocampus) plus offline consolidation during sleep. For agents,
in-session notes do the first job. **Dreaming** does the second: Claude reflects
on logs or transcripts between sessions, an application of the sleep-time
compute idea from Letta and UC Berkeley. Writing a note is a prediction about
what a future session will need. Newer Claude models make better predictions:
they close a learning loop (rule plus evidence) on CL-Bench 1.0, and they keep
small, strategic memory folders in Pokémon Red. Dreaming then (1) corrects
notes against transcripts, (2) builds linked **wiki** representations, (3)
promotes a small index into every session's context, (4) focuses memory on a
goal through task-specific instructions, and (5) fills gaps across sessions.
Open questions are when to write memory, how to keep it current at acceptable
compute cost, and whether transcript search should be the foundation. See
[[agent-memory]] and [[context-engineering]].

## Key points

- **Boundary.** Memory excludes compaction (summaries that replace older
  turns) and in-context learning. This matches the memory-vs-context-window
  boundary on [[agent-memory]].
- **Memory as prediction.** A written rule predicts that the pattern will
  recur; a verified fact predicts that a later session will rely on it without
  re-checking.
- **Closing the loop (CL-Bench 1.0, on [[claude-managed-agents]]).** Each
  question ran in a fresh session with only a persisted memory directory.
  Older models left untested guesses. Later ones consolidated notes, marked
  facts as checked or unconfirmed, recorded corrections, and finally wrote
  rules with how they knew each rule was true, plus warnings about traps.
- **Store what the environment does not show.** In Pokémon, money and map
  position are on screen every turn, so storing them is redundant and goes
  stale. Strategy, plans, and tested rules exist only if the agent writes them
  down. A small memory with a top-level `global.md` dashboard (goal, plan,
  memory rules) beat an indiscriminate archive.
- **Steering: say what memory is for, not how to use it.** Saying only that a
  memory folder exists was enough for strong models. A fixed rule ("record only
  failures") cut much of their memory gain. Explicit steering (read memory
  before answering, test theories) helped older models most. For frontier
  models, Anthropic gives simple guidance to note things when asked or when
  clearly worth remembering. (Per-model results are under Notable claims.)
- **Dreaming corrects memory.** In-session notes can be wrong from the start or
  drift. Checking them against the original transcript gives ground truth. A
  corrected Mt. Moon note let Claude get through; the uncorrected note caused
  repeated loops and the run never reached the next city.
- **Dreaming builds wikis.** Linked, Claude-maintained pages act as a map of
  memory. The gain grows with dreaming sessions and is largest when the wiki
  is combined with search. Wikis help multi-document synthesis, not
  single-document lookup. A wiki can also grow larger than its sources and
  abstract nothing (Borges's map).
- **Dreaming promotes an index up the hierarchy.** The harness preloads the
  top layer every session. Injection costs tokens, spreads any wrong note to
  every session, and does not guarantee adherence (longer instruction files
  reduce adherence). So the top layer must stay small, with details moved down
  and links left behind. Claude Code auto memory loads only the head of
  `MEMORY.md` as an index.
- **Goal-focused instructions.** Instructions for growing memory should say
  what matters for the task. Several agents writing one shared table lost
  facts by overwriting each other. One page per contract, one writer per page,
  and verbatim quotes kept every fact. Claude found the better instructions
  through a reflect–propose–rebuild loop.
- **Cross-session gap filling.** A second dreaming pass repointed broken links
  to existing pages and added missing pages, including an index.
- **Open questions.** In-session writing captures salience but distracts from
  the task. Dreaming runs in the background but its output may lag. Checking
  every memory continuously is costly; focus dreaming on volatile information
  or tune its cadence by access frequency. Transcript search is a reasonable
  foundation, but maintained representations cost compute and can accumulate
  errors or hallucinations.

## Entities

[[anthropic]], [[claude]], [[claude-code]], [[claude-managed-agents]]. No page
yet: Letta, Stainless, Harvey (LAB benchmark), CL-Bench, Claude Duet.

## Concepts

[[agent-memory]], [[context-engineering]], [[agent-harness]],
[[agent-steering]], [[agent-instructions]], [[agent-orchestration]],
[[agent-evals]]

## Notable claims & data

Per-model observations (as of 2026-11-06; these are not general rules):

- CL-Bench 1.0: Claude Sonnet 4.6 left untested guesses; Opus 4.7 consolidated
  notes and marked facts as checked or unconfirmed; Sonnet 5 marked confirmed
  answers and wrote corrections; Opus 5 was the first to close the loop; Opus
  5.5 and Sonnet 5.5 also closed it and scored about the same as Opus 5 with
  memory, with slightly higher no-memory baselines.
- "Record only failures" removed much of the memory gain for Opus 5 and Opus
  4.7. Prompting Sonnet 4.6 to read memory and test theories nearly doubled its
  score. Sonnet 5 read memory before answering 9 of 10 times unprompted; Sonnet
  4.6 did so under half the time.
- Pokémon Red at about 10,000 steps: Sonnet 3.7 wrote 413 files in 225 folders
  and earned 1 badge; Fable 5 wrote 9 files in 2 folders plus `global.md` and
  earned 4 badges. At one point Sonnet 3.7 spent 17 steps creating 6 files and
  deleting 9 with no game actions. Opus 5.5 kept a small goal-and-next-steps
  folder and beat the game.

Wiki and dreaming results:

- Stainless corpus (about 350,000 files, about 420M tokens; 25 questions; Opus
  5 agents; shared log): wiki-only score rose from 13% to 48% of graded
  criteria as dreaming scaled from 2 to 128 sessions. Search plus wiki rose
  from 54% to 61%, against 53% for search alone, and saved about 20,000 tokens
  per question.
- Merger questions (24, more than half cross-document): 87% with the wiki vs
  73% with search alone. One LAB task with single-document criteria showed no
  clear wiki gain.
- LAB contract task: a shared multi-writer table kept 41 of 57 facts (72%);
  one verbatim page per contract by a single agent kept 57 of 57.
- A second dreaming pass found 9 links to a missing page, repointed them, and
  added 3 pages, including an index.
- Claude Code auto memory loads only the first 200 lines or 25 KB of
  `MEMORY.md`.

Relation to existing wiki claims:

- Agrees with the size-bounded injected index in
  [[cursor-agent-swarm-model-economics]] and with transcripts as a knowledge
  base in [[anthropic-cybersecurity-triage-agents]].
- Gives an alternative to the asynchronous extractor in
  [[anthropic-anatomy-of-commerce-agents]]: in-session notes plus offline
  dreaming. Neither source compares the two designs on the same task.
- Dreaming against transcripts is one practical answer to the slow memory
  drift threat named in [[anthropic-zero-trust-for-ai-agents]]. It does not
  address deliberate poisoning: a poisoned transcript would validate a
  poisoned note.

## Connections

- Extends the structured note-taking technique in
  [[anthropic-eng-context-engineering]] and the progress-file pattern in
  [[anthropic-eng-effective-harnesses-long-running-agents]] with an offline
  consolidation step. The page lists
  [[anthropic-eng-harness-design-long-running-apps]] as related.
- The rule "say what memory is for, not how" parallels the "rules →
  judgement" shift for Claude 5-generation models in
  [[anthropic-new-rules-context-engineering-claude-5]], which also moved
  memory from hand-written CLAUDE.md to auto-memory.
- Promoting notes into every session is context injection; the persistent
  memory poisoning risk in [[anthropic-eng-how-we-contain-claude]] applies to
  that top layer.
- The multi-writer overwrite failure is a shared-state hazard of the kind
  covered in [[anthropic-multi-agent-coordination-patterns]].
- The dreaming-built wiki (explore, write or correct pages, merge duplicates,
  check claims against sources, shared log) is the same pattern this wiki
  follows: `raw/`, `wiki/`, and `log.md`.

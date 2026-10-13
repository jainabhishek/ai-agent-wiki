# Improving skill-creator: Test, measure, and refine Agent Skills — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/improving-skill-creator-test-measure-and-refine-agent-skills
> Publisher: Anthropic (claude.com articles) · Date: 2026-03-03
> Captured: 2026-10-12 via curl (condensed).

Category: Announcements. Product: Claude Code. Reading time 6 min. No model
version named.

## Intro

- skill-creator now helps write evals, run benchmarks, and keep skills working as
  models change. Available in Claude.ai and Cowork, as a Claude Code plugin, and
  in Anthropic's repo.
- Since Agent Skills launched (October 2025), most authors are subject-matter
  experts, not engineers; they lacked tools to check whether a skill still works
  on a new model, triggers when it should, or improved after an edit. Goal: bring
  testing, benchmarking, and iteration to skill authoring without writing code.

## Two kinds of skills

- **Capability uplift skills**: help Claude do what the base model cannot do, or
  cannot do consistently (e.g. document-creation skills encoding techniques that
  beat prompting alone).
- **Encoded preference skills**: Claude can do each step; the skill sequences
  them per a team's process (e.g. NDA review against set criteria; weekly updates
  drafted from several MCPs).
- Testing purpose differs: capability uplift skills may become unnecessary as
  models improve — evals reveal when. Encoded preference skills are more durable
  but only as good as their fidelity to the real workflow — evals verify it.

## Using evals to test and improve skills

- Evals = test prompts (plus files if needed) and a description of good output;
  skill-creator reports whether the skill holds up.
- Example: the PDF skill struggled with non-fillable forms (placing text at exact
  coordinates with no fields). Evals isolated the failure; the fix anchors
  positioning to extracted text coordinates.
- Two key uses:
  1. Catch quality regressions as models and infrastructure change; run evals on
     a new model for early signal.
  2. Detect when model capability has outgrown a skill (mainly capability
     uplift): if the base model passes the evals *without* the skill loaded, the
     technique may be absorbed into default behavior — the skill is not broken,
     just unnecessary.
- **Benchmark mode**: standardized assessment over your evals, for after model
  updates or during iteration; tracks eval pass rate, elapsed time, token usage.
- Evals and results stay with the author: store locally, feed a dashboard, or
  plug into CI.

## Faster, more consistent evaluation with multi-agent support

- Sequential evals are slow and context can bleed between runs. skill-creator
  now runs evals in parallel with independent agents, each in a clean context
  with its own token and timing metrics.
- **Comparator agents** for A/B: two skill versions, or skill vs no skill; they
  judge blind to which output is which.

## Getting skills to trigger at the right time

- Output quality only matters if the skill triggers. As skill count grows,
  description precision matters: too broad → false triggers; too narrow → never
  fires.
- skill-creator analyzes the description against sample prompts and suggests
  edits that cut false positives and false negatives.
- Result reported: improved triggering on 5 of 6 public document-creation skills.

## Looking ahead

- The line between "skill" and "specification" may blur. A SKILL.md today is
  essentially an implementation plan; later a natural-language description of
  *what* the skill should do may suffice. Evals already describe the "what";
  eventually that description may be the skill.

## Getting Started

- Available in Claude.ai and Cowork (ask Claude to use skill-creator); Claude
  Code users install the plugin or download from the repo.

# Testing Agent Skills Systematically with Evals — OpenAI (raw capture)

> Source: https://developers.openai.com/blog/eval-skills
> Publisher: OpenAI (Developers blog) · Date: 2026-01-22
> Captured: 2026-10-12 via the OpenAI blog full-text export plus curl of the page for byline (condensed).

Authors: Dominik Kundel, Gabriel Chua. Category tag: Codex.

## Introduction

When iterating on a Codex skill it is hard to know whether a change improves
it or only changes it; regressions appear as the skill not triggering,
skipping a required step, or leaving extra files. A skill is an organized set
of prompts and instructions, so evaluate it like any other LLM prompt. An eval
is defined as: a prompt, then a captured run (trace plus artifacts), then a
small set of checks, then a score tracked over time. In practice skill evals
resemble lightweight end-to-end tests.

## 1. Define success before you write the skill

Split checks into four categories and keep them few and must-pass:
- **Outcome goals** — did the task complete; does the app run?
- **Process goals** — did Codex invoke the skill and follow the intended tools
  and steps?
- **Style goals** — does output follow requested conventions?
- **Efficiency goals** — no thrashing (unneeded commands, excess tokens).
The worked example mixes concrete checks (did it run `npm install`; does
`package.json` exist) with a structured style rubric, to get fast targeted
signals rather than one pass/fail verdict.

## 2. Create the skill

A Codex skill is a directory with `SKILL.md`: YAML frontmatter (`name`,
`description`) then Markdown instructions, plus optional resources and
scripts. Name and description are the main signals Codex uses to decide
whether to invoke the skill and when to inject the rest of `SKILL.md`; vague
or overloaded metadata makes triggering unreliable. Bootstrap with the
built-in `$skill-creator` (itself a skill), which asks what the skill does,
when it should trigger, and whether it is instruction-only (the default
recommendation) or script-backed.

### A sample skill

`setup-demo-app`: scaffold a Vite React + TypeScript app, configure Tailwind
via the official Vite plugin, enforce a fixed minimal file layout, and define
a "definition of done". Location: `.codex/skills/setup-demo-app/SKILL.md`
(repo scope) or `~/.codex/skills/setup-demo-app/SKILL.md` (user scope).
Contents in summary:
- Sections: When to use this; What to build; Steps; Definition of done.
- Layout: `src/main.tsx`, `src/App.tsx`, `src/components/Header.tsx`,
  `src/components/Card.tsx`, `src/index.css`, `index.html`, `package.json`.
- Style: TypeScript, functional components only, Tailwind classes (no CSS
  modules), no extra UI libraries.
- Steps: `npm create vite@latest demo-app -- --template react-ts`;
  `npm install`; `npm install tailwindcss @tailwindcss/vite`, add the plugin
  to `vite.config.ts`, replace `src/index.css` with `@import "tailwindcss";`;
  build Header, Card, and App (Header plus two Cards).
- Definition of done: `npm run dev` starts; `package.json` exists; Header and
  Card component files exist.
The skill is opinionated on purpose: without constraints there is nothing
concrete to evaluate.

## 3. Manually trigger the skill to expose hidden assumptions

First check triggering. Invoke explicitly (the `/skills` slash command or the
`$` prefix) in a real or scratch repo and watch for misses. Hidden
assumptions to look for:
- **Triggering** — prompts that should invoke the skill but do not, or generic
  prompts ("add Tailwind styling") that wrongly do.
- **Environment** — assumes an empty directory, or that `npm` is available and
  preferred.
- **Execution** — skips `npm install`, or configures Tailwind before the Vite
  project exists.
For repeatable runs use `codex exec`: built for automation and CI, it streams
progress to `stderr` and writes only the final result to `stdout`. It runs in
a restricted sandbox by default; pass `--full-auto` to allow file writes, and
use the least permissions needed. Example: `codex exec --full-auto` with a
prompt that names `$setup-demo-app`. Every manual fix in this phase is a
candidate eval.

## 4. Use a small, targeted prompt set to catch regressions early

10–20 prompts per skill is enough. Keep a CSV
(`evals/setup-demo-app.prompts.csv`) with columns `id,should_trigger,prompt`
and grow it from real failures. Four starter rows, each testing a different
thing:
- `test-01` (true) — **explicit invocation**: names the skill.
- `test-02` (true) — **implicit invocation**: describes the exact scenario
  without naming the skill; tests whether name/description suffice.
- `test-03` (true) — **contextual invocation**: adds domain noise (a
  Responses API demo) but needs the same setup.
- `test-04` (false) — **negative control**: "add Tailwind to my existing React
  app"; catches false positives where the skill scaffolds a new project.
The CSV becomes a living record of scenarios the skill must keep getting
right.

## 5. Get started with lightweight deterministic graders

Run `codex exec --json`: `stdout` becomes a JSONL stream of structured
events, so checks score what actually happened. Minimal Node.js runner
(`evals/run-setup-demo-app-evals.mjs`): for each prompt run
`codex exec --json --full-auto "<prompt>"`, save the JSONL trace (for example
`evals/artifacts/test-01.jsonl`), parse it, and run checks. Example checks:
- ran `npm install` — any event of type `item.started` or `item.completed`
  whose `item.type` is `command_execution` and whose `item.command` contains
  `npm install`;
- `package.json` exists in the project directory.
Every command execution appears in order as an `item.*` event, so a failed
check can be debugged by opening the trace.

## 6. Conduct qualitative checks with Codex and rubric-based grading

Deterministic checks answer "did it do the basics", not "did it do it the way
you wanted". Add a model-assisted step: (1) run the skill; (2) run a read-only
style check on the resulting repo; (3) require a structured response. Codex
supports this with `--output-schema` (constrains the final response to a JSON
Schema). Example schema `evals/style-rubric.schema.json`: object with
required `overall_pass` (boolean), `score` (integer 0–100), and `checks`
(array of `{id, pass, notes}`, all required, `additionalProperties: false`).
The style-check `codex exec` lists requirements (Vite + React + TS exists;
Tailwind via `@tailwindcss/vite` and CSS imports tailwindcss; Header and Card
exist; functional components with Tailwind utility classes) and asks for check
ids `vite`, `tailwind`, `structure`, `style`, with
`--output-schema ./evals/style-rubric.schema.json` and
`-o ./evals/artifacts/test-01.style.json`. The Codex GitHub Action supports
passing `--output-schema` through `codex-args` for CI.

## 7. Extending your evals as the skill matures

- **Command count and thrashing** — count `command_execution` items; token
  usage is in `turn.completed` events.
- **Token budget** — track `usage.input_tokens` and `usage.output_tokens`.
- **Build checks** — run `npm run build` afterwards.
- **Runtime smoke checks** — start `npm run dev` and `curl` it, or a light
  Playwright check; use selectively (slow).
- **Repository cleanliness** — `git status --porcelain` empty or matching an
  allow list.
- **Sandbox and permission regressions** — the skill still works without
  extra permissions.
Principle: fast explanatory checks first; heavier checks only where they
reduce risk.

## 8. Key takeaways

- Measure what matters; good evals make regressions clear and failures
  explainable.
- Start from a checkable definition of done; bootstrap with `$skill-creator`.
- Ground evals in behavior: JSONL from `codex exec --json`, checks over
  `command_execution` events.
- Use Codex where rules fall short: rubric pass via `--output-schema`.
- Let real failures drive coverage: every manual fix becomes a test.

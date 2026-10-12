# Harness design for long-running application development — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/harness-design-long-running-apps
> Publisher: Anthropic (Engineering blog) · Date: 2026-03-24
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Prithvi Rajasekaran (Anthropic Labs team).

## Introduction (no heading)

- Two linked goals: strong frontend design from Claude, and fully autonomous application builds. Earlier prompt and harness work hit ceilings.
- GAN-inspired: built a generator + evaluator pair, then extended to a three-agent planner / generator / evaluator system for multi-hour full-stack builds.

## Why naive implementations fall short

- Earlier work: an initializer agent split a spec into tasks; a coding agent built one feature at a time with handoff artifacts. Two failure modes remained:
  - **Context loss** — coherence drops as the window fills. Sonnet 4.5 showed "context anxiety" (wrapping up early). Context resets with structured handoffs fixed it; compaction alone did not.
  - **Self-evaluation** — agents praise their own mediocre work. Separating the generator from a skeptical, tunable evaluator was far more tractable than making the generator self-critical.

## Frontend design: making subjective quality gradable

- Four grading criteria, given to both generator and evaluator:
  - **Design quality** — parts form a coherent whole with a distinct mood.
  - **Originality** — deliberate choices, not templates or "AI slop" patterns.
  - **Craft** — typography, spacing, color harmony, contrast (a competence check).
  - **Functionality** — users can understand the UI and complete tasks.
- Design and originality weighted higher (Claude already did craft and functionality well).
- Evaluator calibrated with few-shot examples and score breakdowns; used the Playwright MCP to navigate live pages.
- Runs: 5–15 iterations, sometimes up to 4 hours. Generator decided each round to refine or pivot. Scores rose then plateaued. Criteria wording visibly shaped the output style.
- Example: Dutch art museum site — at iteration 10 the model dropped a polished landing page for a spatial 3D gallery experience.

## Scaling to full-stack coding

Generator–evaluator loop mapped to the software lifecycle; QA plays evaluator.

### The architecture

- Opus 4.5 did not need context resets: resets dropped; one continuous session with automatic compaction via the Claude Agent SDK.
- **Planner** — expands a 1–4 sentence prompt into a product spec. Stays high-level on product and design; avoids granular technical detail that could cascade errors. Weaves in AI features.
- **Generator** — sprints, one feature at a time; stack React, Vite, FastAPI, SQLite (later PostgreSQL). Self-checks each sprint; uses git.
- **Evaluator** — Playwright clicks through the app like a user; tests UI, APIs, database state. Scores product depth, functionality, visual design, code quality. Any criterion below its hard threshold fails the sprint.
- Before each sprint, generator and evaluator negotiate a **sprint contract**: what "done" means and how to test it. Agents communicate through files.

### Running the harness

Opus 4.5, one prompt, retro 2D game maker:
- **Solo run:** 20 min, $9. Core feature (playing the level) broken; no clear wiring between entities and the runtime.
- **Full harness:** 6 hours, $200 (over 20x cost). Planner produced a 16-feature spec over 10 sprints. More polished; richer sprite editor; built-in AI assistant; working play mode. Physics and level-design edge cases still rough.
- Evaluator logged specific bugs, e.g. rectangle fill tool not triggering on mouse-up; API route-ordering bug. Sprint 3 alone had 27 criteria.
- Early evaluators approved flawed work; the QA prompt was tuned over several rounds.

### Iterating on the harness

- Every harness component encodes an assumption about what the model cannot do alone, so each was stress-tested. Removing parts one at a time was more informative than radical simplification.
- Opus 4.6 arrived mid-project, expected to need less scaffolding — per "Building Effective Agents": start simple, add complexity only when needed.

### Removing the sprint construct

- Sprints dropped: Opus 4.6 sustained longer work.
- Planner kept: without it the generator under-scoped.
- Evaluator moved to a single pass at the end. Its value depends on whether the task is beyond what the model does reliably alone.
- Added prompting so the generator built in-app AI agents that drive the app's own features through tools.

### Results from the updated harness

Browser DAW (Web Audio API), about 4 hours (table total 3 h 50 min), $124.70:

| Phase | Time | Cost |
|---|---|---|
| Planner | 4.7 min | $0.46 |
| Build round 1 | 2 h 7 min | $71.08 |
| QA round 1 | 8.8 min | $3.24 |
| Build round 2 | 1 h 2 min | $36.89 |
| QA round 2 | 6.8 min | $3.09 |
| Build round 3 | 10.9 min | $5.88 |
| QA round 3 | 9.6 min | $4.06 |

- Builder ran coherently for 2+ hours without sprints. QA still caught gaps: clips not movable/resizable, stubbed recording, numeric sliders instead of graphical EQ curves.
- Result: working arrangement view, mixer, transport; agent could compose a short snippet via prompts. Far from professional; Claude cannot hear, which limits musical QA.

## What comes next

- Some scaffolding becomes unnecessary as models improve, but stronger models also open room for harnesses that exceed baseline capability. The space of useful harness designs shifts rather than shrinks.
- Practices: read model traces on realistic problems; decompose complex tasks into specialized agents; re-examine the harness when a new model ships.

## Appendix

Example planner output for "RetroForge" (2D retro game maker): product overview, then features such as a project dashboard with user stories, and a data model covering canvas settings, tile sizes, palettes, and assets.

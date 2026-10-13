# A field guide to Claude Fable 5: Finding your unknowns — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/a-field-guide-to-claude-fable-finding-your-unknowns
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-06
> Captured: 2026-10-12 via curl (condensed).

Byline: Thariq Shihipar, member of technical staff, Anthropic. Category: Best
practices. Product: Claude Code. Listed reading time 2 min.

## Introduction (map and territory)

- The author frames prompts, skills, and context as the "map"; the codebase and
  real-world constraints are the "territory". The gap between them is the
  author's "unknowns". When Claude meets an unknown it acts on its best guess of
  what the user wants; more work means more unknowns.
- Claim: Claude Fable is the first model where the author finds output quality
  limited by the author's own ability to clarify unknowns.
- Planning ahead is not enough: unknowns surface during implementation, and can
  show that the problem should be solved differently. Working with Fable is
  described as iteratively discovering unknowns before, during, and after
  implementation.

## Knowing your unknowns

Four categories the author uses to break down a problem:
- Known knowns — what goes in the prompt.
- Known unknowns — what you know you have not decided yet.
- Unknown knowns — things so obvious you would not write them down, but would
  recognize on sight.
- Unknown unknowns — what you have not considered at all, including how good the
  result could be.

Strong agentic coders (Boris and Jarred are named) know in detail what they want
and are in sync with the codebase and model behavior, but still plan for
unknowns. Reducing and planning for unknowns is called the core skill of agentic
coding, and one that improves by working with Claude.

## Help Claude help you

- Too-specific instructions: Claude follows them even when a pivot would be
  better. Too-vague instructions: Claude fills gaps with generic industry best
  practices that may not fit.
- Claude can find unknowns faster: it searches the codebase and the web
  quickly, knows more than the user about the average topic, and iterates from
  failure faster.
- Most important: give Claude your starting point — where you are in your
  thinking, your experience with the problem and the codebase — and use it as a
  thought partner.
- Pattern list: pre-implementation (blind spot pass, brainstorms and
  prototypes, interviews, references, implementation plan); during
  implementation (implementation notes); post-implementation (pitches and
  explainers, quizzes).

## Pre-implementation

### Blind Spot Pass
- For new parts of a codebase or unfamiliar domains (example: design work) you
  have many unknown unknowns: you lack the questions, the quality bar, the
  history, and the pitfalls.
- Ask Claude to find and explain your unknown unknowns. The author uses the
  literal phrases "blind spot pass" and "unknown unknowns", and tells Claude who
  they are and what they know.
- Example prompts (paraphrased): adding a new auth provider with no knowledge of
  the codebase's auth modules — ask for a blind spot pass so you can prompt
  better; grading a video without knowing what color grading is — ask Claude to
  teach the unknown unknowns first.

### Brainstorms and prototypes
- Use for unknown knowns (criteria you only recognize on sight). Surfacing them
  during prototyping is cheaper than during implementation: small spec changes
  can cause very different code, and an agent finds it harder to revert earlier
  changes.
- Examples: see how a button looks in a frame without building a backend route
  or extra frontend state; for visual design, ask for several design
  approaches.
- The author starts almost every coding session with an exploration or
  brainstorm phase to set scope; Claude often finds high-value approaches, and
  sometimes misses the bigger picture. Brainstorming prevents a scope that is
  too narrow or too wide.
- Example prompts (paraphrased): an HTML page with 4 very different dashboard
  design directions to react to; a single HTML mock of a new editor toolbar with
  fake data before touching the real app; search the codebase and brainstorm 10
  intervention points for post-onboarding churn, cheapest to most ambitious.

### Interviews
- After brainstorming, ask Claude to interview you about ambiguities, with
  context on the problem to guide its questions.
- Example (paraphrased): one question at a time, prioritizing questions whose
  answer would change the architecture.

### References
- When you cannot describe what you want, give a reference. Diagrams, docs, and
  pictures work, but source code is the best reference: point Fable at the
  folder and say what to look for, even in another language. Code carries more
  detail on markup and structure than a screenshot.
- Example (paraphrased): read a Rust crate in `vendor/rate-limiter` and
  reimplement its backoff semantics in the TypeScript API client.

### Implementation Plans
- Before implementing, ask for a plan to review that leads with the parts most
  likely to change: data models, type interfaces, UX flows.
- Example (paraphrased): plan in HTML; lead with data-model changes, new type
  interfaces, and user-facing changes; put mechanical refactoring at the bottom.

## During implementation

### Implementation notes
- After approving the plan, start a new session and pass in the artifacts (for
  example a spec file and a prototype): fresh context, but with the planning
  output.
- Unknown unknowns remain; the agent may need to change approach because of an
  edge case.
- Ask Claude Code to keep a temporary `implementation-notes.md` (or `.html`)
  that logs decisions for the next attempt.
- Example (paraphrased): on an edge case that forces deviation, pick the
  conservative option, log it under "Deviations", and continue.

## Post implementation

### Pitches and explainers
- Pitch and explainer artifacts speed understanding for reviewers who start with
  the same unknowns, and speed approvals from experts who want to see that
  common failure points were considered.
- Example (paraphrased): bundle prototype, spec, and implementation notes into
  one doc for Slack, leading with a demo GIF.

### Quizzes
- After a long session, diffs give only a light understanding because behavior
  depends on existing code paths.
- Ask for an HTML report on the change (context, intuition, what was done) with
  a quiz at the end. The author merges only after passing the quiz perfectly.

## How this comes together: launching Fable
- The Fable launch video was edited end-to-end with Claude Code, in a domain new
  to the author.
- Steps: asked Claude to explain how transcription such as Whisper works and
  whether ums and long pauses could be cut accurately with ffmpeg; asked for a
  prototype video with Remotion plus a transcription to test word-timed UI;
  for muted-looking footage, first asked for variations, realized there was no
  sense of what "good" grading looks like, then asked Claude to teach color
  grading to discover the unknowns.

## Matching the Map and Territory
- Better models raise what the right approach can achieve. When a long-horizon
  task comes back wrong, the likely fix is more time defining unknowns or a
  plan that lets user and Claude adapt.
- Explainers, brainstorms, interviews, prototypes, and references are cheap ways
  to find unknowns before they get expensive.
- Points to "the new rules of context engineering" for the context side of
  Fable-generation models.

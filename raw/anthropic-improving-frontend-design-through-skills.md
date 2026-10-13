# Improving frontend design through Skills — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/improving-frontend-design-through-skills
> Publisher: Anthropic (claude.com articles) · Date: 2025-11-12
> Captured: 2026-10-12 via curl (condensed). Example screenshots not captured.

Category: Best practices. Product: Claude apps. Reading time 13 min. Written by
Anthropic's Applied AI team (Prithvi Rajasekaran, Justin Wei, Alexander Bricken)
with Molly Vorwerck and Ryan Whitehead. The post names no Claude model version.

## Intro — distributional convergence

- Without guidance, an LLM-built landing page almost always uses Inter fonts,
  purple gradients on white, and minimal animation.
- Cause named "distributional convergence": sampling follows training-data
  statistics; safe, universal design choices dominate web data, so the model
  samples from that high-probability center. The result undermines brand
  identity and makes AI-made UIs recognizable.

### The steerability challenge
- Claude is highly steerable: instructions like avoiding Inter/Roboto or using
  atmospheric backgrounds improve results at once.
- But specialized tasks need a lot of context (typography, color theory,
  animation, backgrounds). Putting it in the system prompt makes every unrelated
  request (debugging Python, emails) carry frontend context.

## Skills: dynamic context loading

- A skill is a document (often markdown) of instructions, constraints, and domain
  knowledge in a directory Claude reads with file tools; Claude loads relevant
  skills at runtime (e.g. a frontend skill when asked for a landing page or React
  component).
- Mental model: skills are prompts and resources that activate on demand, with no
  permanent context overhead. Cites earlier Anthropic writing that too many
  context tokens degrade performance.

## Prompting for better frontend output

- Core insight: think like a frontend engineer — map aesthetic improvements to
  implementable code. Target areas: typography, animations, background effects,
  themes.
- Detailed technical instructions are not required; targeted language on these
  axes suffices. Ties to "right altitude" from the context-engineering post:
  avoid low-altitude hardcoding (exact hex codes) and vague high-altitude
  guidance.

### Typography
- Example prompt block `<use_interesting_fonts>`: bans Inter, Roboto, Open Sans,
  Lato, default system fonts. Suggested families: code aesthetic (JetBrains
  Mono, Fira Code, Space Grotesk); editorial (Playfair Display, Crimson Pro);
  technical (IBM Plex family, Source Sans 3); distinctive (Bricolage Grotesque,
  Newsreader). Pairing via high contrast (display + monospace, serif + geometric
  sans, variable font across weights). Use weight extremes (100/200 vs 800/900,
  not 400 vs 600) and size jumps of 3x+ (not 1.5x). Pick one distinctive font;
  load from Google Fonts.
- Observation: the font mandate also seemed to improve other aspects of the design.

### Themes
- Claude knows popular aesthetics; example block `<always_use_rpg_theme>` asks for
  fantasy palettes, ornate borders, parchment/leather textures, dramatic
  lighting, medieval serif headers.

### A general-purpose prompt
- Motion (animations, micro-interactions) and background choices add polish and
  depth. Anthropic combined everything into a ~400-token `<frontend_aesthetics>`
  prompt, compact enough to load as a skill. Its parts (paraphrased):
  - Opening: names the model's tendency toward generic "on distribution" output
    (users call it "AI slop") and asks for distinctive frontends.
  - Typography: distinctive fonts; avoid Arial and Inter.
  - Color & theme: one cohesive aesthetic; CSS variables; dominant colors with
    sharp accents beat timid evenly spread palettes; draw on IDE themes and
    cultural aesthetics.
  - Motion: CSS-only for HTML; Motion library for React when available; one
    orchestrated page load with staggered reveals (`animation-delay`) beats
    scattered micro-interactions.
  - Backgrounds: layered CSS gradients, geometric patterns, contextual effects
    instead of solid colors.
  - Avoid list: overused fonts (Inter, Roboto, Arial, system fonts); clichéd
    schemes (purple gradients on white); predictable layouts; cookie-cutter
    design.
  - Closing: vary light/dark themes, fonts, aesthetics across generations; notes
    the model still converges on common picks such as Space Grotesk and asks it to
    avoid that.
- Rationale: high-level problem context calibrates output; targeted advice per
  design vector; the final reminder stops convergence onto a new local maximum
  (e.g. Space Grotesk).

### Impact on frontend design
- Before/after pairs (same prompt, with and without the skill): SaaS landing
  page (generic Inter + purple gradient → distinctive type, cohesive colors,
  layered backgrounds); blog layout (system fonts, flat white → editorial
  typeface, atmospheric depth); admin dashboard (minimal hierarchy → bold type,
  dark theme, purposeful motion). Qualitative only; no metrics.

## Improving artifact quality in claude.ai with Skills

- Second limitation: Claude builds claude.ai artifacts as a single HTML file
  with CSS and JS because artifacts must render as one HTML file.
- Hypothesis: richer tooling yields better artifacts. Built the
  `web-artifacts-builder` skill: uses computer use to build with multiple files
  and React, Tailwind CSS, shadcn/ui. Scripts (1) set up a basic React repo and
  (2) bundle everything into one HTML file with Parcel after editing. Scripts for
  boilerplate cut token use and raise reliability.
- Examples: whiteboard app (basic without skill; with skill adds shape and text
  drawing); task manager (minimal without; with skill adds a "Create New Task"
  form with Category and Due Date). To use: enable the skill and ask Claude to
  "use the web-artifacts-builder skill."

## Optimizing Claude's frontend design capabilities with Skills

- Broader principle: models can often do more than they express by default;
  distributional convergence hides Claude's design understanding.
- Skills are customizable (design system, component patterns, industry UI
  conventions) and become reusable organizational knowledge.
- General method for any domain with generic output: identify convergent
  defaults, provide concrete alternatives, structure guidance at the right
  altitude, package it as a skill.
- Pointers: frontend design cookbook; frontend design plugin in Claude Code;
  skill-creator.

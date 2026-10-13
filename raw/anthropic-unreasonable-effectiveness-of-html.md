# Using Claude Code: The unreasonable effectiveness of HTML — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-05-20 · Author: Thariq Shihipar · Category: Playbooks · Reading time: 9 min
> Captured: 2026-10-12 via curl (condensed), page HTML converted to text locally. The closing note says the article expresses the author's personal opinions. Figures (FIG A–E) are images; only their captions are captured.

## Intro

- Markdown is the dominant format agents use to talk to humans: simple, portable, some rich text, easy to edit; Claude even draws ASCII diagrams in it.
- Author finds Markdown increasingly restrictive: hard to read past ~100 lines; wants richer visuals, color, diagrams; wants easier sharing.
- Author rarely edits these files by hand now — they serve as specs and references, and edits are made by prompting Claude — which removes a main Markdown advantage.
- Author now prefers HTML as an output format and sees others on the Claude Code team doing the same. HTML file templates for common use cases are offered.

## Why use HTML?

### Information density
- HTML can carry: tables (tabular data); CSS (design data); SVG (illustrations); script tags (code snippets); HTML + JavaScript + CSS (interactions); SVG and HTML (workflows); absolute positioning and canvases (spatial data); image tags (images).
- Author's view: almost any information Claude can read can be represented efficiently in HTML.
- Without HTML, the model falls back to inefficient tricks like ASCII diagrams or approximating colors with Unicode characters (FIG A: a color palette rendered in Markdown).

### Visual clarity and ease of reading
- Specs and plans grow as Claude handles bigger work; the author rarely reads a Markdown file over 100 lines and cannot get colleagues to.
- HTML lets Claude structure for navigation (tabs, illustrations, links) and can be mobile responsive.

### Ease of sharing
- Browsers render Markdown poorly, so it travels as attachments. An uploaded HTML file is shared as a link. Author claims people are much more likely to read a spec, report, or PR writeup in HTML.

### Two-way interactions
- Ask for sliders or knobs to adjust a design or algorithm options, and a way to copy the chosen settings into a prompt for Claude Code — a per-problem editing environment.

### Data ingestion
- Reason to use Claude Code (rather than Claude.ai or Claude Design) for HTML: the context it can ingest — file system, MCP servers (e.g. Slack, Linear), the web browser via Claude in Chrome, git history. Example: the author had Claude Code find, group, and categorize all HTML files he had generated and diagram each type; the article's figures came from that.

## Getting started

- No special setup: ask Claude to make an HTML file or HTML artifact. The main work is knowing what the artifact should do and how it will be used. Build a skill later for recurring patterns; start by prompting from scratch.

## Use cases

A GitHub gallery of the use cases is linked.

### Specs, planning, and exploration
- Instead of one Markdown plan, the author produces a web of HTML files: brainstorm several options, expand one (mockups, interface examples), then write an implementation plan; a fresh session receives all files to implement. The verification agent also reads them, gaining broader context. FIG B: several approaches side by side with tradeoffs.
- Example prompts (paraphrased): generate six distinct onboarding-screen approaches varying layout, tone, and density, in one HTML grid, each labeled with its tradeoff; write a thorough implementation plan as HTML with mockups, data flow, and key code snippets, optimized for easy reading.
- Use for: exploring alternative implementations; trying several visual designs at once.

### Code review and understanding
- HTML can render diffs, annotations, flowcharts, modules. Use to understand agent-written code, review code, or explain a PR to a reviewer. FIG C: a diff with severity-tagged margin notes.
- Example prompt (paraphrased): describe a PR as an HTML artifact focused on the unfamiliar streaming/backpressure logic, rendering the real diff with inline margin annotations and severity color-coding.
- Use for: creating a PR; reviewing a PR; understanding a topic in code.

### Design and prototypes
- Claude Design is HTML-based because HTML is expressive for design even when the target is React, Swift, etc.; Claude sketches in HTML, then ports. Prototype interactions with sliders and knobs. FIG D: design tokens and components rendered.
- Example prompt (paraphrased): prototype a checkout button with a click animation that turns purple, in an HTML file with sliders for animation options and a button to copy the chosen parameters.
- Use for: design-system artifacts; adjusting components; visualizing component libraries; prototyping animations.

### Reports, research, and learning
- Claude Code synthesizes across Slack, codebase, git history, and the web into readable reports: long HTML documents, interactive explainers, or slide decks, with SVG diagrams. FIG E: an explainer with navigation, collapsible steps, tabbed snippets.
- Example prompt (paraphrased): explain the rate limiter as a single HTML page with a token-bucket flow diagram, 3–4 annotated key snippets, and a gotchas section, for one-time reading.
- Use for: feature summaries; explainers; weekly status reports; incident reports; SVG illustrations, flowcharts, technical diagrams.

### Custom editing interfaces
- When a text box is a poor way to express intent, ask for a throwaway single-file editor for this one piece of data — not a product or reusable tool.
- Key rule: always end with an export — a "copy as JSON" or "copy as prompt" button that turns UI changes back into something to paste into Claude Code or commit. Keeps the human in the loop with a tighter loop.
- Example prompts (paraphrased): reprioritize 30 Linear tickets as draggable cards across Now / Next / Later / Cut, pre-sorted, with a copy-as-Markdown export plus one-line rationale per bucket; a form editor for a feature-flag config grouped by area, showing dependencies, warning on enabling a flag whose prerequisite is off, with a copy-diff button for changed keys only; a side-by-side system-prompt tuner with highlighted variable slots, three live-rendered sample inputs, a character/token counter, and a copy button.
- Use for: reordering, triaging, bucketing (tickets, test cases, feedback); editing constrained structured config (feature flags, env vars, JSON/YAML); tuning prompts, templates, copy with live preview; curating datasets (approve/reject, tag, export); annotating documents, transcripts, diffs and exporting annotations; picking values awkward in text (colors, easing curves, crop regions, cron schedules, regexes).

## Frequently asked questions

### Isn't it less efficient?
- Markdown often uses fewer tokens, but HTML's expressiveness and the higher chance the author reads it give better overall results. With the 1MM context window in Opus 4.7, the extra tokens are not noticeable in context.

### When do you use Markdown for now?
- Author has stopped using Markdown for almost everything and calls himself an HTML maximalist.

### Is this how you've replaced planning?
- Several HTML files for different plan parts/stages (implementation plan; UI exploration; a component listing every design), kept as references for the future and for verification.

## Staying in the loop with Claude

- The real reason: HTML keeps the author in the loop. As Claude took on more, he read plans less closely; HTML made him engage with Claude's choices again.

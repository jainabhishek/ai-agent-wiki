# Building with Claude Sonnet 5.5 — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/building-with-claude-sonnet-5-5/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-09-28
> Author: Addy Osmani. Category: Playbooks. Subtitle: when to choose Sonnet over
> Opus, what it costs, and how to tune it.
> Captured: 2026-10-12 via curl + local HTML-to-text (condensed, paraphrased;
> section-complete — every H2/H3 of the original appears below).

## Intro

Sonnet 5.5 is the second Claude 5.5 model after Opus 5.5. Claimed vs Sonnet 5:
smarter, more efficient, 30% faster; per-token price unchanged; typically needs far
fewer tokens, so costs up to 30% less for most work. Demo video: code-to-painting
(Sonnet 5 vs Sonnet 5.5 vs Opus 5.5).
Quickstart Python: `client.messages.create(model="claude-sonnet-5-5",
max_tokens=4096, messages=[...], output_config={"effort": "medium"})`, iterating
`response.content` and printing blocks with `block.type == "text"`. Reason: Sonnet
5.5 thinks by default, so a response can start with a `thinking` block and code
reading `content[0].text` breaks.

## Choosing between Sonnet 5.5 and Opus 5.5

Opus 5.5: complex work needing careful judgment. Sonnet 5.5: well-scoped everyday
tasks (fixing bugs, fast feature iteration); also polished documents, slides,
spreadsheets, with a strong eye for design; speed suits fast iteration. Claude
Haiku 5.5 to join "in the coming weeks" for high-volume, low-latency workflows.
Workload table → start with:
- Well-scoped everyday coding (bugs, fast feature iteration, verifying against
  requirements) → Sonnet 5.5
- High-volume everyday development → Sonnet 5.5
- Polished documents/slides/spreadsheets (one-pagers, diagrams, summary slides,
  doc edits, spreadsheet cleanup) → Sonnet 5.5
- Well-defined repeated agent tasks (investigation, review, drafting) → Sonnet 5.5
- Complex careful-judgment work incl. long-horizon agentic coding and knowledge
  work → Opus 5.5
- Hardest problems needing most intelligence → Opus 5.5
Customer quote (Epic Games COO): Sonnet 5.5 met a higher-tier quality bar on a
system design audit and data-flow review, handled tens of thousands of lines and
multi-hour tasks, with less prescriptive prompting. Best fit: a clear spec and a way
to check the result; cites the prompting guide that an Opus model is the better
choice for the hardest long-horizon work.

## Pricing

Per million tokens, Sonnet 5.5 / Opus 5.5: input $2 / $4; output $10 / $20; cache
write 5-min $2.50 / $5; cache write 1-hour $4 / $8; cache read $0.20 / $0.20.
All Sonnet 5.5 prices (incl. batch and caching) equal Sonnet 5's. US-only inference
(`inference_geo: "us"`) costs 1.1x. Bill still changes because fewer tokens per
task. Surfaces ship different default efforts (high on Claude Platform, medium in
Claude Code). High-resolution image tier up to 2576 px long edge; a 2000×1500
image costs ~2.5x the tokens it did on Sonnet 4.6 / Sonnet 4.5 / Haiku 4.5 —
downscale if detail not needed.

## Model details

- Model ID: `claude-sonnet-5-5` on Claude API, Claude Platform on AWS, Google
  Cloud, Microsoft Foundry; `anthropic.claude-sonnet-5-5` on Amazon Bedrock.
- Context: 1M tokens, native, no beta header.
- Max output: 128k; up to 300k on Message Batches API with beta header
  `output-300k-2026-03-24`.
- Knowledge cutoff: June 2026.
- Thinking: on by default (adaptive); `between_tools` turns off upfront thinking.
- Effort levels: `low`, `medium`, `high`, `xhigh`, `max`.
- Default effort: `high` on Claude API; `medium` in Claude Code.
- Tokenizer: same as Sonnet 5.
- Minimum cacheable prompt: 512 tokens (Sonnet 5: 1,024).
- Rate limits: separate from Sonnet 5, same default tier values.
- Priority Tier: available on Claude API.
- Data retention: zero data retention available for eligible customers.
API defaults to `high`: start there, evaluate, then pick. `xhigh`/`max` think
longer and cost more and may erode Sonnet's quality/speed/cost balance — consider
Opus 5.5 instead.

## Migrating from Sonnet 5

Thinking on by default; if Sonnet 5 ran with thinking off, use `between_tools`.
Change model ID, then handle five breaking changes and one response-shape change
(full detail in the Sonnet 5.5 migration guide). Claude Code can do it:
`/claude-api migrate this project to claude-sonnet-5-5` (bundled Claude API skill
swaps model ID and breaking params across the codebase).

### 1. Turn off upfront thinking with between_tools

No `thinking` field → adaptive thinking; `thinking: {"type": "disabled"}` → 400.
Send `thinking: {"type": "between_tools"}`: thinking only between tool calls; total
response time same or faster. Before/after example: Sonnet 5 with `disabled` +
`effort: "xhigh"` becomes Sonnet 5.5 with `between_tools` + `effort: "high"`.
Limits of `between_tools`:
- Works at `low`, `medium`, `high`; at `xhigh`/`max` → 400 (use adaptive there).
- Takes no other field: `display`, `budget_tokens`, or `block_binding` with it → 400.
- Effort can't change mid-conversation; use adaptive to vary per turn.
- Short progress updates between tool calls still return as `thinking` blocks with
  summary text; read blocks by type, pass them back unchanged with the assistant
  turn. Without tools, response is text only.
- Works on every platform offering Sonnet 5.5, no beta header; update SDK if it
  lacks `between_tools`.
With `between_tools` on, use adaptive thinking instead for tool-less requests that
need a few steps of working out.

### 2. Replace forced tool_choice with auto plus strict tools

`tool_choice` type `any` or `tool` → 400 (also on token counting endpoint). Send
`{"type": "auto"}`, mark the tool `"strict": True`, and say in the prompt when to
use it. Example `get_weather` tool with `input_schema` having
`"additionalProperties": False`. Strict tool use requires `additionalProperties:
false` on every object.

### 3. Keep conversations append-only

Sonnet 5.5 thinking blocks are bound to model and conversation. Sonnet 5.5 can read
Sonnet 5's thinking blocks (switching mid-conversation keeps reasoning); no other
model reads Sonnet 5.5's blocks.

### 4. Move computer use to the toolset

On Claude API and Google Cloud, computer use only via `{"type":
"computer_toolset_20260801"}`; declaring `computer_20251124` → 400. Drop header
`anthropic-beta: computer-use-2025-11-24`; in SDKs remove `betas` and use the
standard (non-beta) Messages client. Replace the `tools` entry; update the agent
loop for member `tool_use` blocks, batch actions, and `toolset_name` on results.
Remove `fine-grained-tool-streaming-2025-05-14` header (with a toolset entry → 400);
set `eager_input_streaming: true` per tool instead. Amazon Bedrock still accepts
`computer_20251124`.

### 5. Check your advisor pairing

With the advisor tool, a Sonnet 5.5 executor rejects Opus 4.8, Opus 4.7, Sonnet 5
as advisors. Accepted include Opus 5.5, Opus 5, Sonnet 5.5. Advice from every
accepted advisor returns encrypted as an `advisor_redacted_result` block (code
can't read the text).

### 6. Read text between tool calls from thinking blocks

No error, but UIs may stop showing between-tool notes: notes longer than a sentence
or two arrive as progress-update `thinking` blocks, empty at default `display`. With
adaptive thinking set `thinking.display` to `"updates"` (beta, header
`thinking-display-updates-2026-08-18`) or `"summarized"`, and render each non-empty
`thinking` block before the following `tool_use`. With `between_tools`, text returns
without `display`.
Also new: per-message effort (beta), mid-conversation system messages,
mid-conversation tool changes (beta). Migration guide has checklists for moving
from Sonnet 4.6 or earlier, or Haiku 4.5.

## Tuning

### Re-run your effort sweep

Effort levels recalibrated vs Sonnet 5; old settings don't carry over. Start `high`
unless agentic or latency-sensitive. Agentic coding / multistep tool use: `medium`
for well-specified tasks, `high` for harder/longer. Chat / latency-sensitive:
`medium` or `low`. `xhigh`/`max` only where evals show gains. Thinking counts
toward `max_tokens`; for agentic coding set `max_tokens` to 128,000 (model max) and
stream. To reduce thinking lower effort — system-prompt requests to think less
don't reliably work.

### Remove Sonnet 5 workarounds

Existing Sonnet 5 prompts should work unchanged. Remove workarounds such as refusal
steering, tool-call retry shims, or "do not be lazy", then re-run evals before
other tuning.

### Ask for real checks at low effort

Sonnet 5.5 usually checks its work before reporting done, but at `low` sometimes
skips a check that exercises the change. If changes are reported done without
test/build output, the prompting guide recommends a system-prompt paragraph (the
blog reproduces the docs' paragraph verbatim). Its content, paraphrased: when code
can be run/built/type-checked, run a real check that exercises the change (tests,
type-checker, build, or the changed command) before reporting done; a syntax-only
check or a check command that failed to start doesn't count; if only declared
dependencies are missing, install them with the project's own package manager and
lockfile (e.g. `npm install`, `pip install -r requirements.txt`), never via sudo or
the system package manager unless told otherwise; if no real check can run, say
which check wasn't run and why instead of reporting done.

### Use thinking.display for progress

Don't ask the model to write its reasoning in the response — invites
`reasoning_extraction` declines. Read summarized thinking instead:
`thinking={"type": "adaptive", "display": "summarized"}`. For user-facing progress
notes alone use `display: "updates"` (beta). For updates at predictable points
(a line before first tool call, a short end recap) say so in the system prompt.

### Cache more of your prompt

Minimum cacheable prompt drops to 512 tokens, so shorter system prompts and tool
definitions qualify. Cache read = one tenth of input price. Changing top-level
effort between requests invalidates the cache; use per-message effort (beta) for a
one-turn change, which keeps the cache.

## Refusals and fallback

On Anthropic's automated behavioral audit, Sonnet 5.5 improves on or matches Sonnet
5 on most alignment and honesty measures. First Sonnet with cybersecurity
safeguards similar to the most capable models; most routine software development
unaffected. A decline returns HTTP 200 with `stop_reason: "refusal"`;
`stop_details` names one of five categories: `cyber`, `bio`, `frontier_llm`,
`reasoning_extraction`, `general_harms`. Server-side fallback (`fallbacks:
"default"`, beta, Claude API) retries `cyber` and `frontier_llm` declines on Sonnet
5, not the other three. Alternatives: SDK middleware or own retry. The Cyber
Verification Program "will soon expand" to include Sonnet 5.5.

## Availability

Available today; model IDs: Claude API `claude-sonnet-5-5`; Amazon Bedrock
`anthropic.claude-sonnet-5-5`; Claude Platform on AWS `claude-sonnet-5-5`; Google
Cloud `claude-sonnet-5-5`; Microsoft Foundry `claude-sonnet-5-5` (Global Standard
deployments only).

### In Claude Code

From Claude Code v2.1.284 (Agent SDK for TypeScript v0.3.284+), the `sonnet` alias
resolves to Sonnet 5.5 on the Claude API; default effort `medium`; 1M context
native. Thinking can't be turned off for Sonnet 5.5 in Claude Code; effort sets how
much it thinks. No fast mode for Sonnet 5.5. The `default` model stays Opus 5.5;
switch with `/model sonnet` for well-scoped tasks.

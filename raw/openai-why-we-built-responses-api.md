# Why we built the Responses API — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/responses-api
> Publisher: OpenAI (Developers blog) · Date: 2025-09-22 · Authors: Steve Coffey, Prashant Mital
> Captured: 2026-10-12 via curl (condensed). Body text taken from the developers blog llms-full Markdown export; byline date, authors, and subtitle taken from a curl of the live page HTML ("Sep 22, 2025"); figures spot-checked against the live page.

Page subtitle (paraphrased): how Responses enables persistent reasoning, hosted tools, and multimodal workflows for GPT-5.

## Intro (API history)

- Written after the GPT-5 launch to explain the best way to integrate it and why Responses suits reasoning models and agents.
- Design principle: each API generation follows how the models work.
- `/v1/completions`: prompt in, continuation out; few-shot prompting used to coax JSON or answers from weaker models.
- RLHF/ChatGPT era: `/v1/chat/completions`, built (per the post) in one weekend, with `system`/`user`/`assistant` roles for chat UIs.
- Function calling (late 2023) was very popular. The Assistants API beta at the same time was a first agentic interface with hosted tools (code interpreter, file search); it never reached mass adoption because its design was limiting and harder to adopt than Chat Completions.
- By late 2024 OpenAI wanted one API as approachable as Chat Completions, as powerful as Assistants, and built for multimodal and reasoning models: `/v1/responses`.

## `/v1/responses` is an agentic loop

- Chat Completions is turn-based chat; Responses is a structured loop of reasoning and acting. Analogy: a detective who investigates, consults experts (tools), keeps private notes (reasoning state), and reports back without handing over the notes.
- Responses preserves reasoning state across turns; Chat Completions drops reasoning between calls. Claimed effects: TAUBench +5%, better cache utilization, lower latency. Diagram only.
- Responses can emit multiple output items — what the model said and what it did (tool calls, structured outputs, intermediate steps) — for debugging, auditing, richer UIs.
- Example comparison (described, not copied): Chat Completions returns one `message` object (role, `content`, a `tool_calls` array of `function` calls, `refusal`, `annotations`); the post notes it is unclear whether the text or the call came first. Responses returns a list of polymorphic, typed Items — a `reasoning` item (id prefix `rs_`, with a `summary` of `summary_text`), a `message` item (`msg_`, `output_text` content), and a `function_call` item (`fc_`, `call_id`, `name`, `arguments`) — so the order of actions is explicit and the developer chooses what to display, log, or ignore.

### Moving up the stack with hosted tools

- Early function-calling users both called APIs and searched document stores (RAG); building retrieval from scratch is hard and costly for newcomers.
- Assistants introduced the first hosted tools: `file_search` and `code_interpreter`. Responses adds web search, image generation, and MCP.
- Hosted tools execute server-side, so calls do not round-trip through the developer's backend, improving latency and round-trip cost.

### Preserving reasoning safely

- Why not expose raw chain of thought (CoT): risks include hallucinations, harmful content that would not appear in the final answer, and competitive risk for OpenAI.
- Cites Jakub Pachocki's o1-preview post: a hidden CoT is a monitoring opportunity only if the model can think "in unaltered form" (paraphrased; quote not reproduced), so no policy training on the CoT and no direct display of an unaligned CoT to users.
- Responses keeps reasoning internal, encrypted, and hidden from the client, and allows continuation via `previous_response_id` or by passing reasoning items back, without exposing raw CoT.

## Why `/v1/responses` is the best way to build

Designed to be stateful, multimodal, and efficient:
- Agentic tool use: File Search, Image Gen, Code Interpreter, MCP.
- Stateful by default: conversation and tool state tracked automatically. GPT-5 via Responses scores 5% higher on TAUBench than via Chat Completions, attributed only to preserved reasoning.
- Multimodal from the start: text, images, audio, function calls as first-class.
- Lower cost, better performance: internal benchmarks show 40–80% better cache utilization than Chat Completions, hence lower latency and cost.
- Quality-of-life changes in the API and SDK: semantic streaming events; internally-tagged polymorphism; `output_text` SDK helpers (replacing `choices[0].message.content`); better organization of multimodal and reasoning parameters.

## What about Chat Completions?

Chat Completions is not going away; keep using it if it works. Responses is recommended for persistent reasoning, native multimodality, and an agentic loop without workarounds.

## Looking ahead

OpenAI expects Responses to become the default way to build with its models, as Chat Completions replaced Completions.

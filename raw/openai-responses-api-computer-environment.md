# From model to agent: Equipping the Responses API with a computer environment — OpenAI (Engineering) (raw capture)

> Source: https://openai.com/index/equip-responses-api-computer-environment/
> Publisher: OpenAI (Engineering) · Date: 2026-03-11 · Authors: Bo Xu, Danny Zhang, Rohit Arunachalam
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed). openai.com returns HTTP 403 to curl and WebFetch.

Page headings: The shell tool · Orchestrating the agent loop · When the
context window gets full: compaction · Container context (File systems;
Databases; Network access) · Agent skills · How agents are made · Make your own
agent. Diagrams (output streaming, container setup, network access, the
spreadsheet workflow) are images; content described in prose.

## Intro

- Shift from models (trained intelligence via prompts) to agents with a
  computer environment: run services, call APIs, produce artifacts such as
  spreadsheets or reports.
- Practical problems when building agents: where to put intermediate files;
  how to avoid pasting large tables into a prompt; how to grant network access
  safely; how to handle timeouts and retries without building a workflow
  system.
- OpenAI's answer: the **Responses API** plus the **shell tool** plus a
  **hosted container workspace**. The model proposes steps and commands; the
  platform runs them in an isolated environment with a filesystem for
  inputs/outputs, optional structured storage (e.g. SQLite), and restricted
  network access.

## The shell tool

- A tight execution loop: model proposes an action, platform runs it, result
  feeds the next step.
- A model only *proposes* a tool call; it cannot execute it. Models learn
  when and how to use tools from training examples.
- The shell tool gives command-line access with standard Unix utilities
  (`grep`, `curl`, `awk`) out of the box. Unlike the existing code
  interpreter (Python only), it can run Go or Java programs or start a NodeJS
  server.

## Orchestrating the agent loop

- An orchestrator must take model output, invoke tools, and return results
  until done. With **custom tools**, the Responses API yields control to the
  client, which needs its own harness. With **hosted tools**, the Responses
  API orchestrates model and tools itself.
- The API assembles context (user prompt, prior conversation state, tool
  instructions). For shell execution the prompt must mention using the shell
  tool and the model must be trained to propose shell commands — **GPT-5.2
  and later** are. If the model chooses shell, it returns one or more
  commands; the API forwards them to the container runtime, streams output
  back, and feeds it into the next request. The loop repeats until the model
  returns a completion with no further shell commands.
- The API keeps a streaming connection to the container service and relays
  output to the model in near real time, so the model can wait, run another
  command, or finish.
- **Concurrency**: the model can propose multiple commands in one step; the
  API runs them concurrently in separate container sessions and multiplexes
  the streams into structured tool outputs.
- **Bounded output**: the model specifies an output cap per command; the API
  enforces it and returns a result that keeps the beginning and end and marks
  the omitted middle (e.g. a 1,000-character cap: "text at the beginning ...
  1000 chars truncated ... text at the end").

## When the context window gets full: compaction

- Long tasks fill the context window (skill calls, tool calls, reasoning
  summaries). Rather than developers building custom summarization or
  state-carrying systems, the Responses API has **native compaction** aligned
  with model training.
- Latest models are trained to analyze prior state and emit a **compaction
  item** that preserves key state in an encrypted, token-efficient form. The
  next window holds the compaction item plus high-value parts of the earlier
  window. Codex relies on this for long coding tasks.
- Two modes: built-in **server-side** compaction (configure a threshold; the
  system handles timing) or a standalone **`/compact` endpoint**. Server-side
  compaction allows a slightly larger effective input window to tolerate small
  overages just before compaction, so near-limit requests are compacted rather
  than rejected. The compaction approach evolves with each model release.
- Codex helped build the compaction system and was an early user: when one
  Codex instance hit a compaction error, a second instance was started to
  investigate.

## Container context

- The container is the model's working context: read files, query databases,
  access external systems under network policy.

### File systems

- Container and file APIs give the model a map of available data so it chooses
  targeted file operations rather than broad noisy scans.
- Anti-pattern: packing all input into the prompt (expensive, hard to
  navigate). Better: stage resources in the container filesystem and let the
  model choose what to open, parse, or transform via shell.

### Databases

- Suggest storing structured data in **SQLite** and querying it. Give the
  model a table description (columns and meanings) instead of a whole
  spreadsheet; it pulls only needed rows (e.g. "Which products had declining
  sales this quarter?"). Faster, cheaper, scales to larger data.

### Network access

- Agents need live data, external APIs, package installs; unrestricted
  internet risks exposure to external sites, touching sensitive internal or
  third-party systems, credential leaks, and exfiltration.
- Hosted containers use a **sidecar egress proxy**: all outbound requests pass
  a centralized policy layer enforcing allowlists and access controls, with
  observable traffic.
- **Domain-scoped secret injection at egress**: model and container see only
  placeholders; raw secret values stay outside model-visible context and are
  applied only for approved destinations.

## Agent skills

- Repeated multi-step patterns otherwise get rediscovered each run
  (replanning, reissuing commands, relearning conventions). Skills package
  them as reusable, composable building blocks.
- A skill is a folder bundle with `SKILL.md` (metadata and instructions) plus
  resources (API specs, UI assets). The container supplies files and execution
  context; the shell tool supplies the interface; the model discovers skill
  files with `ls`, `cat`, etc., reads instructions, and runs scripts in the
  same loop.
- Skills APIs: upload and store skill folders as **versioned bundles**,
  retrieved by skill ID. Before the prompt goes to the model, the Responses API
  deterministically: (1) fetches skill metadata (name, description); (2)
  fetches the bundle, copies it into the container, unpacks it; (3) adds skill
  metadata and container path to model context. The model then progressively
  explores instructions and runs scripts via shell when a skill is relevant.

## How agents are made

- Responses API = orchestration; shell tool = executable actions; hosted
  container = persistent runtime context; skills = reusable workflow logic;
  compaction = long-running operation with needed context.
- One prompt can expand into: discover skill, fetch data, transform into local
  structured state, query efficiently, generate durable artifacts. Diagram
  stages for building a spreadsheet from live data: skill discovery, planning
  and setup, data acquisition, data processing, artifact generation.

## Make your own agent

- Pointers to a developer blog post and a cookbook on packaging a skill and
  running it through the Responses API.

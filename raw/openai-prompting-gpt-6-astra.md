# Using GPT-6 — OpenAI (API docs) (raw capture)

> Source: https://developers.openai.com/api/docs/guides/latest-model/gpt-6-astra.md (HTML at the same URL without `.md`)
> Publisher: OpenAI (API docs) · Date: no byline on the page; accessed 2026-10-12
> Captured: 2026-10-12 via curl of the .md endpoint (condensed and paraphrased).
> Page front matter: `latestModelInfo.model: gpt-6-astra`; anchors `#migration-quickstart` and `#prompting-best-practices`.

Note: the prompt blocks on the original page are paraphrased here, not copied.
Short trigger phrases, stock-phrase lists, and identifiers are kept verbatim.

## (Intro) Using GPT-6 — model picker

Pick a GPT-6 model by reasoning need, speed, and cost. The page lists three models:

- **GPT-6 Astra** (`gpt-6-astra`) — "Highest intelligence"; for the most demanding reasoning, coding, and professional work.
- **GPT-6.1 Sol** (`gpt-6.1-sol`) — balanced speed, cost, intelligence; near-Astra performance at a lower cost.
- **GPT-6 Luna** (`gpt-6-luna`) — fastest and most cost-effective; focused, high-volume tasks.

Get started by setting `model` in a Responses API request. Users of `gpt-6-sol` should read the migration guidance before switching to GPT-6.1 Sol.

### GPT-6 Astra

- OpenAI calls it its most intelligent model so far: state of the art in computer use, browsing, software engineering, science, professional work. Runs multi-step workflows across code, browsers, and professional software.
- In several evaluations Astra got stronger results with substantially fewer output tokens; estimated API cost per task was lower than earlier models despite higher per-token price.
- Also described as OpenAI's most aligned model: exercises care, respects task boundaries, communicates transparently. Fills routine gaps from context; asks focused questions when the answer could change the outcome. Incorporates new requirements, changes course on request, answers side questions without losing the main task.
- All Astra users get Fast mode and the new Ultrafast mode.

### GPT-6.1 Sol

- For complex coding, computer use, and professional work at near-Astra performance and lower cost. Compare against Astra on your own tasks.
- `reasoning.effort`: `low`, `medium` (default), `high`, `xhigh`, `max`. `none` and `minimal` are not supported.
- Use the Responses API for tool calling; Chat Completions supports only requests without tools.

## What's new

- **Async tool calling:** the model keeps reasoning, calls other tools, or answers independent parts while the app runs a tool. Set `async: true` on a function or custom tool; return the result later using the original `call_id`. The app still executes the tool and manages pending work. Guide also shows a developer-defined wait-tool pattern.
- **Mid-turn steering:** send extra user instructions (corrections, changed requirements) while the model works. Over a WebSocket connection, the Responses API keeps completed work and includes the update in a continuation.
- **Change reasoning mid-conversation while preserving cache:** add a `configuration_update` input item to raise or lower effort without rewriting the prompt prefix. The new effort applies until another `configuration_update` overrides it.
- **Misalignment monitoring:** as part of strengthened safeguards for Astra, OpenAI systems asynchronously monitor for misalignment and raise alerts when needed.
- Carried over from GPT-5.6: computer use, Structured Outputs, streaming, Programmatic Tool Calling, multi-agent orchestration, prompt caching, persisted reasoning, compaction, pro mode.

## Limitations

- `gpt-6-astra` and `gpt-6.1-sol` do not support `none` reasoning effort; `gpt-6-sol` and `gpt-6-luna` do.
- Fast mode supports EU data residency for GPT-6.1 Sol, GPT-6 Sol, GPT-6 Luna — not GPT-6 Astra.
- Ultrafast mode for GPT-6.1 Sol: US and EU data residency plus global processing. GPT-6 Astra Ultrafast: US data residency and global processing only.

## Prompting best practices

Scoping statement (paraphrased): the prompts are a starting point "across the GPT-6 model family"; they target behavior observed with GPT-6 Astra; evaluate them with your chosen model and workload.

### GPT-6 Astra behavior

Five observed behaviors, each with its own subsection below:

- **Initiative and follow-through:** built to be a better collaborator, so more likely to ask a question when input could materially change the result. It can stop where the user expected it to assume and persist.
- **Instruction following:** stronger general instruction following than previous OpenAI models; more sensitive to instructions in skills and files such as `AGENTS.md`. OpenAI **strongly recommends** auditing skills and other files the model can access.
- **Personality and writing style:** tends toward detailed, formatted responses; may reuse recurring phrases across sessions. Specify the style and structure you need.
- **Subagent delegation:** may delegate less often than desired. Specify when and how much to use subagents for parallel work.
- **Testing and verification:** for coding, thorough testing before calling a task done; on small tasks this can mean broader tests than needed.

### Initiative and follow-through

- Astra is generally better than GPT-5.6 Sol and earlier at staying coherent on long tasks, and more likely to ask for clarification where earlier models assumed.
- Prompt 1 (autonomy) — paraphrase: infer intent and scope from instructions and prior context; bias toward action; when the user wants new work or a fix, persist until the goal is done; progress autonomously (examples given: isolated worktrees/checkouts, resolving merge conflicts, read-only actions, creating draft PRs) unless clearly destructive or irreversible.
- Prompt 2 (implied authorization) — paraphrase: requests phrased as "can you...", "I want to...", "help me..." count as instructions to act. Saying the work is possible, outlining a plan, or offering more help does not count as doing it. The model should not trade completeness for lower token or time cost; long tasks get finished.
- Prompt 3 (approve a concrete result) — paraphrase: before asking clarifying questions, finish the already-authorized work needed to make the proposed action concrete and reviewable, so approval is the last step (examples: deploying, writing to an external app, merging a PR, publishing a site). No permission needed for reversible tasks, read-only actions, reviews, fixes, or anything authorized earlier or strongly implied. The prompt also tells the model not to volunteer caveats, extra sign-off steps, or compliance lists when the risk is only speculative.
- By default the model also asks non-blocking questions while working; adjust these prompts to the autonomy level your app needs.

### Instruction following

- Astra follows longer instructions better but is more sensitive to context; unclear or conflicting skill-file guidance can make it pause and block early. Make the priority between user instructions and skills explicit.
- Prompt (priority) — paraphrase: user instructions override skill guidelines; on conflict, prefer the user.
- Prompt (transparency) — paraphrase: if a skill causes the model to ask permission, pause, leave work unfinished, or diverge from user intent, it must name and link the exact `SKILL.md`, quote the instruction, explain how it applies, and separate explicit skill requirements from its own interpretation.
- Use the transparency prompt to surface silent and conflicting guidance when an app loads many skills and instruction files such as `AGENTS.md`.

### Personality and writing style

- Astra tends to use lists, tables, and Markdown for scannability. Specify prose if you want less formatting.
- Prompt (prose) — paraphrase: default to concise paragraphs, one idea each; lists only for parallel, sequential, or comparable items; avoid nested lists; plain words, concrete examples, precise verbs, active voice; state the main point early, then develop it with needed support.
- Prompt (technical communication) — paraphrase: prefer plain language to jargon; use technical detail only where it helps; calibrate to the user's assumed background.
- Prompt (anti-slop) — paraphrase: avoid listed stock words and patterns and concluding summary lines; state actions directly; do not describe what will not be done or how results will be grouped; avoid unprompted "X, not Y" contrasts, invented compound labels, vague qualifiers, canned transitions. Listed items include: "Bottom Line:", "delve", "foster", "leverage", "it's worth noting", "importantly", "Question? Answer.", "This isn't about X. It's about Y.", "genuinely", hyphenated compound descriptors, "In short:..", "The simplest mental model is:...". Example invented labels cited: "exact-head checks", "editorial-row layouts".

### Subagent delegation

- Astra is trained to split and delegate work to parallel subagents. For harness builders, prompt (delegation) — paraphrase: whenever work can be parallelized by delegating to another agent (as root or as subagent), do so via collaboration tools if it saves time or improves quality.
- Inter-agent messages may contain grammar or spacing errors. Prompt (legibility) — paraphrase: messages to other agents and the final answer may be read by a human, so keep them legible with proper spacing between words and numbers.
- The model responds well to prompting on how and when to delegate; tune to your harness.

### Testing and verification

- For coding, calibrate how much testing a change needs, to avoid unneeded tests and repeated checks on small changes.
- Prompt — paraphrase: do not write tests that mirror the implementation for reversible, low-impact changes; tests written must be meaningful and necessary. Run tests suited to the change and required checks; after they pass, broaden or repeat only when new changes, failures, or open concerns justify it.

## Migration quickstart

### Migrate with Codex

- Codex can apply the guide's changes using the OpenAI Docs skill (`openai-docs`, in the Codex repo under `codex-rs/skills/src/assets/samples/openai-docs`). Invocation: `$openai-docs migrate this project to the GPT-6 model family`. The skill can be downloaded for other coding agents.

### Update API and model parameters

Set `model` to `gpt-6-astra`, `gpt-6.1-sol`, or `gpt-6-luna`, then check:

- **Reasoning effort:** keep the current effective effort where supported. Astra and 6.1 Sol do not support `none` — use `low`. `gpt-6-sol` and `gpt-6-luna` support `none`. If you used `minimal`, start at `low` and compare on representative tasks. Parameter: `reasoning.effort` (Responses) / `reasoning_effort` (Chat Completions).
- **Tool calling:** use the Responses API. Astra and 6.1 Sol support Chat Completions, but tool calling needs Responses. GPT-6 Sol and Luna support function calling in Chat Completions only with `reasoning_effort: "none"`; use Responses for reasoning with tools.
- **Unsupported parameters:** when effort is not `none`, remove `temperature`, `top_p`, `top_logprobs`. Chat Completions: also remove `logprobs`. Responses: remove `message.output_text.logprobs` from `include`.
- **Data residency:** same Fast/Ultrafast residency rules as Limitations; Fast mode for Astra has no latency SLA.
- **Changing reasoning effort:** if effort changes between responses, use `configuration_update` items in standard single-agent requests; keep request-level `reasoning.effort` unchanged to preserve the cached prefix. Check compatibility limits first.
- **Prompt caching:** migrating from GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl` set to `"30m"`. Review cache boundaries and cache-write billing changes.
- **Unnecessary approval pauses:** if the model keeps asking for approval, apply the initiative and follow-through guidance; the rest of the prompting section covers instruction following, style, delegation, testing.

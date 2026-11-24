# Using GPT-6.2 — prompting and migration — OpenAI (API docs) (raw capture)

> Source: https://developers.openai.com/api/docs/guides/latest-model/gpt-6.2-astra (same content at `/api/docs/guides/latest-model`)
> Publisher: OpenAI (API docs) · Date: accessed 2026-11-24; models released 2026-11-17 per the API changelog
> Captured: 2026-11-24 via curl of the `.md` export. Condensed paraphrase; example prompts are paraphrased, not quoted.
> Supporting pages read the same day: `api/docs/models/gpt-6.2-astra.md`, `api/docs/models/gpt-6.2-sol.md`, `api/docs/models.md`, `api/docs/models/all.md`, and the API changelog entry of Nov 17.

Page frontmatter: `latestModelInfo.model: gpt-6.2-astra`; migration guide anchor `#migration-quickstart`; prompting guide anchor `#prompting-best-practices`.

## Using GPT-6.2 (intro)

- Two models: GPT-6.2 Astra (`gpt-6.2-astra`) for the hardest tasks; GPT-6.2 Sol (`gpt-6.2-sol`) for complex work at lower cost.

## What's new

- **Prefix edits.** From GPT-6.2 on, the Responses API discards reasoning items after: edits to earlier conversation history (prefix edits), some model changes (downgrades included), or a change of end user or organization. Without its reasoning items the model may answer worse and spend more tokens redoing work. Find edits such as rewriting earlier developer messages or tool calls. To keep reasoning and cache eligibility, keep the prefix unchanged when changing settings between responses (links: prompt caching; "keep the prefix unchanged").
- **`instructions` field change.** GPT-6.2 and later place the top-level `instructions` *after* `input`. For reusable instructions to be cacheable, put them in a `developer` message as the first `input` item. Keep top-level `instructions` for guidance that applies only to the current request.
- **Background mode (public beta).** Discounted completion windows (two-hour or eight-hour) with Standard processing, as an alternative to Flex. GPT-6.2 Astra and Sol do not support Flex (`service_tier: flex`). Changelog (Nov 17): token rates 30% below Standard for the two-hour window, 40% below for eight-hour; new models will not support Flex.

## Prompting best practices

- The prompts are a starting point for the whole GPT-6.2 family; they target behaviors seen with GPT-6.2 Astra and Sol.

### GPT-6.2 Astra behavior (summary list)

- **Writing style:** shorter and more direct by default; revisit "be concise" lines when migrating.
- **Task completion:** with unclear intent it may propose a next step and wait; on long tasks, let it assume and keep going.
- **Coding style:** writes more efficient, higher-quality code than predecessors; state project conventions.
- **Frontend design:** state the imagery and typography wanted.

### Writing style

- Default tone is terse and direct; tunable from professional colleague to conversational assistant.
- Prompt 1 (collaborator / thought partner), paraphrased: use the user's and the sources' terms; keep technical detail and domain words where they add precision; active voice; keep related facts together; lead with the main points; avoid forward references; give enough context to follow the reasoning.
- Prompt 2 (drafting for an external audience), paraphrased: think about who reads it and adapt; supply background the reader lacks; when editing someone's text, keep their content and wording and do only the edits asked for.
- On long tasks the model can leak shorthand from its reasoning or from other agents into the final answer. Prompt 3, paraphrased: the final answer is the user's first view of the work, not a continuation of progress notes, which get collapsed; it must stand alone; write it fresh for the reader; do not reuse or lightly paraphrase the reasoning, and do not carry over jargon or abbreviations from reasoning, tool calls, or subagent instructions.

### Task completion

- For unsupervised work, state the outcome and which decisions need the user.
- Prompt (keep going), paraphrased: do not end the turn while work remains or an authorized next step exists; if the draft final message is a plan, a suggested next step, a routine question, or instructions for the user, do those steps instead, when authorized, and flag assumptions; stop to ask only for a major scope change, a real blocker, a decision only the user can make, or before irreversible or destructive actions.
- Verification: ask the model to confirm it finished the work. Higher `reasoning.effort` helps it persist through final checks on long or complex tasks.
- Prompt (persist and verify), paraphrased: lean toward action; cover every part of the request; keep working until the goal is fully met; proceed on your own (isolated worktrees, resolving merge conflicts, draft PRs) unless clearly destructive or irreversible; before finishing, check the result against the request and complete any remaining steps or verification.
- Prompt (ambiguity), paraphrased: make reasonable assumptions that can be undone, state them, and continue; do not second-guess, stop at describing or offering the work, or give a partial answer unless truly blocked.
- With an async tool such as `request_user_input_async`, GPT-6.2 can ask for clarification and keep working on parts that do not depend on the answer (link: async tool calling guide).

### Coding style

- Describe codebase conventions and behavior that callers depend on: when to reuse logic, how narrowly to scope changes, when to add a test.
- Prompt (coding), paraphrased, four rules after a lead line about thorough, correct, readable code whose outcome is verified:
  - (a) reuse existing classes, methods, representations, and APIs when correctness holds; before consolidating or deleting code, keep the behavior its callers rely on unless the task changes it;
  - (b) do not add new tests unless asked, required by the repo, or needed for a specific regression the current suite would miss;
  - (c) readability beats line count: no minified style, cryptic names, or dense one-liners passed off as simplicity; compressed expressions that hide many branches or assumptions count as too complex;
  - (d) avoid needless helpers, utilities, and class layers, which add cognitive load even without adding branches.

### Frontend design

- If a visual style matters, specify image types and typography (a specific typeface where it matters). Keep interface copy to what people need to know or do.
- Prompt (frontend), paraphrased: prefer realistic images from ImageGen or image search that fit the project; use SVG only when asked; include text only if it informs, aids navigation or action, or was requested; remove decorative numbering, filler badges, redundant headings, and copy that restates the UI, but keep needed labels, instructions, and status feedback.
- For visual work, share a reference from design software, or let GPT-6.2 use the image generation tool to make one with GPT Image; then have the model build, render, and refine against the reference.

## Migration quickstart

- Coding-agent migration: use the OpenAI Docs skill (in the Codex repo samples).

### Update API and model parameters

- Set `model` to `gpt-6.2-astra` or `gpt-6.2-sol`.
- **Reasoning effort:** start new integrations at `medium`; replace `none` or `minimal` with `low`. `reasoning.effort` (Responses) / `reasoning_effort` (Chat Completions).
- **Tool calling:** requires the Responses API; both models also support Chat Completions without tools.
- **Unsupported parameters:** Chat Completions: drop `temperature`, `top_p`, `logprobs`, `top_logprobs`. Responses: drop `temperature`, `top_p`, `top_logprobs`, and remove `message.output_text.logprobs` from `include`.
- **Prompt caching:** move stable instructions from top-level `instructions` to a leading `developer` message in `input`. From GPT-5.5 or earlier, replace `prompt_cache_retention` with `prompt_cache_options.ttl` = `"30m"`. Review cache boundaries and cache-write billing.
- **Zero Data Retention:** supported for approved orgs on eligible endpoints/features. With ZDR the Responses API treats `store` as `false`; for multi-turn work pass prior output items back in order, encrypted reasoning items included.
- **Service tiers and regions:** US and EU data residency with Standard, Fast, and Batch. Ultrafast: US only.
- **Prompting:** see the best-practices section.

## Model pages (supporting facts, checked 2026-11-24)

- `gpt-6.2-astra`: text+image in, text out; 1,050,000 context; 922,000 max input; 128,000 max output; knowledge cutoff May 18, 2026. Price per 1M tokens: input $8, cached input $0.4, output $40; cache-write price is for 30-minute retention, 12-hour cache write $20 (short context, Standard).
- `gpt-6.2-sol`: same context and output limits; knowledge cutoff Jun 01, 2026; rejects `none` effort; supports the Multi-agent beta. Price per 1M: input $2, cached input $0.1, cache writes $2.5, output $10; 12-hour cache write $5. Over 272K input tokens: input and cache rates double, output 1.5x. Batch 50% of Standard; Fast 2x; Ultrafast 3x through 2027-02-28, then 6x from 2027-03-01.
- For comparison, `gpt-6-astra` (now under "More models"): input $10, cached $1, cache writes $12.5, output $50.
- Models overview "Featured models" (current): GPT-6.2 Astra, GPT-6.2 Sol, GPT-6.1 Terra, GPT-6 Luna. The "All models" page lists GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Sol under "More models", not under "Flagship models".

# Prompting Claude Sonnet 5.5 — Anthropic (Claude Platform Docs) (raw capture)

> Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5
> Publisher: Anthropic (Claude Platform Docs) · Date: accessed 2026-10-12 (the page has no byline date)
> Captured: 2026-10-12 via curl of the page's `.md` export (condensed).
> Capture policy: prose is paraphrased. Example prompts are paraphrased clause by clause; short operative phrases are quoted.

Page description: prompting patterns specific to Claude Sonnet 5.5 — effort, initiative and scope, running without up-front thinking, JSON output, progress updates, tool use, mid-turn messages, coding verification, tool calls, visual inputs, and refusals.

Intro: points to "What's new in Claude Sonnet 5.5" for API changes and "Prompting best practices" for cross-model techniques. Existing Claude Sonnet 5 prompts should work without changes; the Prompting Claude Sonnet 5 page remains a reasonable starting point. For the hardest long-horizon work, an Opus model is the better choice.

Symptom index:
- Unsure of effort, or turns longer/shorter than on Sonnet 5 → Calibrate effort.
- Model checks in before a coding task is done, or does more than asked → Steer initiative and scope.
- Integration runs with thinking off today → Running without up-front thinking.
- JSON answers to multi-step tasks are wrong or do not parse → Reasoning tasks with JSON output.
- Long agentic turns look silent → User-facing progress updates.
- Model answers from training knowledge when a search would catch changed details → Tool use in chat and knowledge work.
- Mid-task user messages ignored or treated as injected text → Mid-turn user messages.
- Code changes reported done without a test or build run → Verification on coding tasks.
- Tool called with wrong letter case or a near-miss parameter name → Tolerant tool-call handling.
- Dense charts or technical drawings miss detail → Tools for complex visual inputs.
- `stop_reason: "refusal"` → Safeguard refusals.

Note: the migration guide lists five breaking API changes from Claude Sonnet 5.

## Calibrate effort

- Effort is the main control for thinking, and with it quality, latency, and cost. Levels are recalibrated: a level does not produce the same thinking as on Sonnet 5. Run a fresh sweep; do not carry over the Sonnet 5 setting.
- Start at `high` (the Claude API default) unless the workload is agentic or latency-sensitive. Agentic coding and multistep tool use: `medium` for well-specified tasks, `high` for harder or longer ones. Chat and latency-sensitive work: `medium` or `low`, because higher effort delays the reply start. Raise if quality needs it.
- Lower effort changes agentic finishing: at `low` it keeps thinking short and can skip verifying a change; at `low` and `medium`, on long agentic tasks, it is more likely to stop and check in before finishing.
- Three adjustments:
  - Size `max_tokens` for thinking plus reply; thinking counts even when not returned, and a limit sized for no-thinking requests can truncate. For agentic coding, set `max_tokens` to 128,000 (model maximum) and stream.
  - Reserve `xhigh` and `max` for measured quality gains; thinking and replies get much longer. At those levels `between_tools` is not accepted, so up-front thinking cannot be turned off.
  - For less thinking, lower effort. From `medium` up the model thinks briefly before almost every reply, even a greeting. Asking in the system prompt to think less does not reliably reduce thinking. At `low` it skips thinking on most simple requests.
- Changing top-level `effort` between requests invalidates the prompt cache; use a per-message effort change (beta), which keeps the cache and holds until replaced. Example: in an interactive session at `low`, switch to `high` before the user's hard problem and back to `low` after the answer. Per-message changes need adaptive thinking; with `between_tools` they return a 400 error.

## Steer initiative and scope

How far the model goes on its own depends on effort and request: at lower effort it sometimes checks in before a coding task is done; at higher effort or on open-ended requests it can do more than asked. Steer with effort and system prompt instructions.

- **Carrying work through.** At `low`/`medium` on agentic coding it may pause to confirm a plan, ask a question it could answer itself, or stop after one part of a multipart task. Try higher effort first. Without changing effort, add a two-paragraph system prompt (paraphrased): (1) keep working until everything asked is done; stop to ask only when you cannot continue without the user or before a risky step. (2) When the asked work is done and checked, stop and report; do not add features, tests, files, docs, or refactors that were not asked for; mention them at the end instead. With it, sessions at `low`/`medium` run longer and cost more. It does not replace your own rules for risky or irreversible actions.
- **Unrequested additions when coding.** The model tends to add tests, documentation, and small supporting files that fit repository conventions, at every effort level and more at higher effort; the requested change itself stays close to the ask. Most teams will welcome this. To limit changes to the explicit request, add only the second paragraph above (the one beginning "When the work the user asked for is done"). At `xhigh`/`max` that paragraph reduces additions and makes changes smaller overall.
- **Thoroughness at `xhigh` and `max`.** After finishing, the model can start its own review and verification rounds, sometimes with subagents if available, and make related fixes it noticed. Run routine work at `high` or below, where this is rare. To keep the thoroughness but aim it at the task, add (paraphrased): when the asked work is done and checks pass, stop and report; do not start extra review or hardening rounds or launch reviewer sub-agents unless the user asked for a review; suggest a deeper review at the end if worthwhile. In testing at `max` on coding tasks this stopped reviewer-subagent launches and cut session cost by about a third with no quality change; self-started review rounds by the main agent become less frequent but do not disappear.
- **Open-ended requests.** On requests like "show me what you can do with this", the model can start building a presentation, report, or video when only ideas were wanted. Say so in the request, or add (paraphrased): when asked for ideas, options, or a plan, give them and stop; build or change nothing until told to proceed.

## Running without up-front thinking

To run without up-front thinking, send `thinking: {"type": "between_tools"}` — the lowest thinking setting on this model, accepted at `high` effort or below. Integrations running thinking-off today should switch to `between_tools` and check:
- **Send `between_tools` at `high` or below.** At `xhigh` or `max` the request returns 400. With `between_tools` effort cannot change mid-conversation: a per-message `output_config.effort` differing from the level in effect returns 400; use adaptive thinking to vary effort. Remove any instruction telling the model not to think; such instructions make internal XML tags in visible output more likely.
- **Read the response by block type.** With adaptive thinking a response can begin with a `thinking` block (empty `thinking` field under default `display: "omitted"`). With `between_tools` it can begin with a progress-update `thinking` block. Do not assume the first block is text.
- **Pass back `thinking` blocks unchanged.** With `between_tools`, notes longer than a sentence or two still come back as `thinking` blocks, each carrying a summary. Return them unchanged with the rest of the assistant turn; a returned block gives the model its full note, not the summary.
- **Use adaptive thinking for reasoning tasks without tools.** Without tools, `between_tools` means answering without thinking first. For tasks needing a few steps of working out, use adaptive thinking.

## Reasoning tasks with JSON output

Applies when asking for a JSON answer to a task that needs a few steps of working out (totaling figures from a document, applying a rule, ranking items). The model often answers without thinking first on these, particularly at `low`/`medium`. Use structured outputs where available (response text is schema-matching JSON).

With structured outputs the response holds only JSON, so all working-out happens in thinking; skipped thinking lowers accuracy. Fixes:
- **Ask the model to think first.** With adaptive thinking, append to the system prompt a one-line instruction to think the problem through before answering. At `high` this brings accuracy close to `xhigh` for a modest output-token increase; at `low`/`medium` it raises accuracy (not to `high` levels) with a larger token increase.
- **Or use `xhigh`.** With adaptive thinking, `xhigh` gives the highest accuracy on these tasks even without the line, at more output tokens than `high`.
- **Use adaptive thinking, not `between_tools`.** Without tools, `between_tools` skips pre-answer thinking, the line has no effect, and accuracy is lower. Splitting into two requests (answer, then JSON) gave high accuracy and JSON compliance but at very high cost and latency.
- With structured outputs at `low`/`medium`, the model occasionally keeps thinking until `max_tokens`; at `high`+ this almost never happens. Treat any `stop_reason: "max_tokens"` response as failed even if it holds valid JSON, and retry. Set `max_tokens` high enough for thinking and JSON, but no higher than you will spend on one attempt.

Without structured outputs (JSON requested in the prompt), the model often works the problem in the response text and puts JSON at the end; the JSON is usually right but a whole-response JSON parser fails. Two fixes:
- **Parse the last JSON value.** Read only `text` blocks; treat `max_tokens` stops as failed. From each `{` or `[`, try to parse a value; on success continue after its end so nested values are not counted separately; keep the last value found. Do not take the span from first `{` to last `}` — the model sometimes writes a draft before the final JSON. For several values in a row (one record per line), keep the last run of values separated only by spaces, commas, or line breaks. Check expected fields; retry once if missing. In testing this made nearly every response usable without changing accuracy.
- **Consider `xhigh` with adaptive thinking.** The model then works in thinking and nearly always returns JSON alone; total output tokens stay about the same as `high` because the working moves into thinking.

## User-facing progress updates

- Between tool calls the model writes notes on findings and next steps. Notes longer than a sentence or two come back as progress-update `thinking` blocks; shorter remarks stay `text`. At default `thinking.display` the block text is empty, so a text-only client looks silent. Matters most in chat UIs and real-time products.
- To show notes, set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`). With `between_tools`, notes come back with summary text and no `display` field is needed; `between_tools` accepts no other field — sending `display`, `budget_tokens`, or `block_binding` with it returns 400. The migration guide shows rendering.
- For exact text mid-turn (a code snippet, a question it needs answered), give the model a simple send-a-message tool, tell it to use the tool only for such content, and declare it in the first request so `tools` does not change later.
- Remove older instructions such as "hold all findings for the final response". For updates at set points (intent line before the first tool call, short recap at the end), say so in the system prompt; most useful in human-in-the-loop work.
- Harness reminder: count consecutive tool-calling steps that send the user no text or progress update; after several (e.g. five), append a one-turn reminder after the latest tool results as a turn-scoped system message (beta). Example text: the user has not heard from you in a while; say in a few words what you are doing, then continue. Stop after the second or third if the turn stays quiet — frequent harness text after tool results can make the model suspect prompt injection. Leave each reminder in `messages` on later requests; appending (not inserting then deleting) keeps the prompt cache and preserved thinking intact. At `high` effort, with a send-a-message tool available, the reminder increased update frequency and shortened the longest silent stretches with no measurable quality change.

## Tool use in chat and knowledge work

- On chat and knowledge-work tasks the model sometimes answers from training knowledge when a web search would catch changed details (what is allowed, required, or charged).
- First remove tool-discouraging language ("only use tools when strictly necessary", "minimize tool calls"). Then, if a search tool exists, add (paraphrased): use search to check specifics that may have changed since training (what is allowed, required, or charged), even when confident; for researched work such as reports or comparisons, gather current sources rather than writing from training knowledge.
- Matters most for research and support products.

## Mid-turn user messages

(Anchor in the page's index: "mid-turn user messages and task budgets".)
- The model is trained to resist indirect prompt injection via tool results and other content read during a task. Sometimes it treats a genuine user message as possible injection: if a mid-task user message reaches it as a mid-conversation system message directly after a tool result, or inside a `tool_result` block, it may tell the user the tool result contained text posing as them, and ignore the message or ask for confirmation.
- Causes: a harness token countdown after every tool result; letting users message mid-way through a multistep turn; harness instructions or context after tool results on every step. Each puts text right after tool results, with countdowns and per-step instructions doing so on every call. An occasional one-turn reminder arrives far less often; if a reminder of your own triggers this, send it less often.
- Fixes:
  - Never put user text inside a `tool_result` block (most frequent misread).
  - Deliver mid-turn user input as a user turn: append the user's words as a text block in the user message carrying the `tool_result` blocks, after the last `tool_result`.
  - Put harness notices (reminders) in a separate mid-conversation system message after the user's words; never mix a notice and user words in one block.
  - In interactive sessions where users can type mid-turn, do not add your own token or budget countdown after tool results. Task budgets (beta) add a similar countdown but have not been seen to cause the misread; if the misread appears with a task budget set, try without one.

## Verification on coding tasks

- On agentic coding the model generally checks its work before reporting done. At `low` effort it sometimes reports done without a check that exercises the change (e.g. skipping tests because dependencies are not installed).
- If transcripts show completion claims without test/build output, add a paragraph like this (paraphrased): when changing runnable, buildable, or type-checkable code, run a real check that exercises the change (tests, type-checker, build, or the changed command) before reporting done; a syntax-only check or a check command that failed to start does not count; if only declared dependencies are missing, install them with the project's own package manager and lockfile (e.g. `npm install`, `pip install -r requirements.txt`), never via sudo or the system package manager, unless told not to; only if no real check can run, say which check was not run and why instead of reporting done.
- At `low` effort this makes skipped or superficial checks rare, with no measurable quality change and slightly higher cost per task.

## Tolerant tool-call handling

- The model occasionally calls a declared tool by a name differing only in letter case (e.g. `bash` for `Bash`), or passes a known parameter under a slightly different name.
- Do not treat it as fatal. Either accept the call when the match is unambiguous despite case, or return a `tool_result` with `is_error: true` stating the exact expected name; the model usually corrects on its next turn.

## Tools for complex visual inputs

- For dense charts and technical drawings, give the model a way to crop, zoom, or run code on the image; accuracy rises markedly.
- Charts: tools help at every effort level. Technical drawings: tools help only from `high` up, most at `xhigh` and `max`.
- For charts, tools beat raising effort: with tools at `high` the model read charts more accurately than without tools at `max`, at a fraction of the cost. Crop tool recipe in the cookbook.

## Safeguard refusals

- Safety classifiers can decline a request: a normal response with `stop_reason: "refusal"` and `stop_details.category` naming the category:
  - `cyber`: could enable cyber harm (malware, exploit development). Finding vulnerabilities in source code is allowed; high-risk dual-use work is not.
  - `bio`: could enable biological harm (dangerous lab methods). Everyday health and educational questions unaffected.
  - `frontier_llm`: could assist development of competing AI models.
  - `reasoning_extraction`: asks the model to reproduce internal reasoning in the response text.
  - `general_harms`: another usage-policy area; benign work can also trigger it.
- Cyber Verification Program and Life Sciences Verification Program for blocked legitimate work.
- Server-side fallback (beta), if on, retries `cyber` and `frontier_llm` declines on Claude Sonnet 5; it does not retry `bio`, `reasoning_extraction`, or `general_harms`.
- Remove prompt instructions asking the model to include its reasoning in the response (they invite `reasoning_extraction` declines). With adaptive thinking, read summarized thinking (`display: "summarized"`). A short explanation or a summary of actions taken is still fine.

# Prompting Claude Fable 5.1 — Anthropic (Claude Platform Docs) (raw capture)

> Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
> Publisher: Anthropic (Claude Platform Docs) · Date: accessed 2026-10-12 (the page has no byline date)
> Captured: 2026-10-12 via curl of the page's `.md` export (condensed).
> Capture policy: prose is paraphrased. Example prompts are paraphrased clause by clause; short operative phrases are quoted. The page's seven-language code sample (Python, TypeScript, C#, Go, Java, PHP, Ruby) is reduced to one condensed Python outline with its load-bearing identifiers.
> Scope: the page's metadata description says it covers "Claude Fable 5.1 and Claude Mythos 5.1". The body text names only Claude Fable 5.1, and the code sample uses `model="claude-fable-5-1"`.

Page description: behavioral differences and prompting patterns for Claude Fable 5.1 and Claude Mythos 5.1 — effort, progress updates, tool-call batching, conversation history, writing style, formatting, task completion, compaction summaries, scope and test coverage, search triggering, safeguard false positives, file edits, long outputs, subagents, and vision.

Intro: points to "What's new in Claude Fable 5.1" for capabilities, API changes, pricing, and availability, and to "Prompting best practices". Existing Claude Fable 5 prompts should work on Fable 5.1 without changes, but a handful of behavioral differences matter.

Symptom index:
- Unsure of effort, or latency/cost higher than the task warrants → Consider all effort levels.
- Little or no text between tool calls → Ask for user-facing progress updates.
- One tool call per turn in agent loops → Batch independent tool calls in agent loops.
- Requests fail with `bound to a different conversation`, or the harness edits earlier turns → Keep the conversation history append-only.
- Prose long and dense → Writing density.
- Chat replies carry less structure than content needs → Formatting in chat.
- Summaries reproduce source wording without quotation marks → Quoting retrieved sources.
- Turn ends before work is done, or the model asks permission for already-requested work → Finish the whole task.
- Client-side compaction summaries drop constraints, decisions, details → Tell the model what to preserve in compaction summaries.
- Unrequested fixes/extensions, or more committed test files than needed → Keep changes and tests to what the task asks for.
- Answers from memory instead of searching at low effort → Search triggering at low effort.
- Benign coding requests return `stop_reason: "refusal"` → Reduce safeguard false positives.
- Whole files rewritten for small changes → Prefer targeted edits over whole-file rewrites.
- Long deliverables at `xhigh`/`max` take long or hit `max_tokens` → Leave room for long outputs at xhigh and max effort.
- Lead agent idles while subagents run → Let the lead agent keep working while subagents run.
- Charts and dense images miss detail → Give vision work tools to crop and zoom.

Notes block:
- Fable 5.1 runs safety classifiers and can return `stop_reason: "refusal"` (see "Refusals, fallback, and billing" and the false-positives section).
- Prompts, skills, and tool descriptions asking the model to write out its thinking or reasoning may be declined with category `reasoning_extraction`. Ask for a short explanation or a summary of actions instead, or read summarized thinking (`display: "summarized"`).

## Consider all effort levels

- Start at the default `high`, then test `low`, `medium`, `xhigh`, `max` on your evals. Effort is the primary control for intelligence vs latency vs cost. Re-run the sweep even if done on Fable 5: level names do not mean the same thinking across models.
- Gains over Fable 5 appear at all levels and are largest at higher settings. At `medium`, results roughly match Fable 5 at lower cost; step down to `medium` or `low` where quality holds.
- At `low`, Fable 5.1 is often competitive with Claude Opus and Claude Sonnet models on cost per task while scoring higher; include it wherever you would otherwise run a smaller model at higher effort.
- Two effort-specific behaviors: fewer search/retrieval calls at `low`; longer thinking before long deliverables at `xhigh`/`max` (own sections below).

## Ask for user-facing progress updates

- Default: fewer user-facing updates during long tool-calling turns than Fable 5, more so at higher effort and in longer tool chains. Users see the agent go quiet for minutes, or a final message covering only the last step.
- First, check the client receives updates: between-tool-call notes come back as progress-update `thinking` blocks, empty under the default `thinking.display` of `"omitted"`. Set `display: "updates"` (beta header `thinking-display-updates-2026-08-18`) and render each non-empty `thinking` block as a status line, or set `"summarized"` to get them with summarized reasoning.
- Second, remove narration-suppressing lines written for earlier, update-eager models (e.g. "hold all findings for the final response").
- If more updates are wanted (pair programming, human-in-the-loop), add a short system line (paraphrased): before starting, say in a line what you are about to do; give brief updates while working; close with a self-contained recap — found, done, next — so a reader of only the last message has the full picture.
- If the product collapses or hides tool output, tell the model, or it may run commands to "show" output the UI never displays. Deliver the note as a turn-scoped system message (`clear_at: "next_user_message"`, beta). Example (paraphrased): only you see that command's output; the user's terminal shows at most a few lines; put anything the user needs to read in your reply.

## Batch independent tool calls in agent loops

- The model usually parallelizes calls when a request names several things to fetch. Exception: coding and computer-use loops (custom coding agents, bash-and-editor harnesses, computer use) where next independent calls are implied rather than requested; there it may issue one per turn. Answer quality is unaffected, but each extra turn costs tokens, a round trip, and wall-clock time.
- Fix: a one-sentence nudge at the end of the current request (paraphrased): first privately list what you need next, then request every item not dependent on another's result in this one response.
- Placement: each time tool results are sent back, append the nudge after that user message as a turn-scoped system message — a `role: "system"` entry in `messages` with `clear_at: "next_user_message"`. Once a later user message exists, the API clears earlier copies so the model sees only the newest. Beta header `mid-conversation-system-clear-at-2026-08-21`. Without the beta, put the sentence in a text block after the `tool_result` blocks in the same user message.
- Append a fresh copy each turn; leave earlier copies byte-for-byte in place. Cleared copies stay in the array, are not seen, and cost no input tokens. Deleting or rewriting them edits earlier turns, restarting the prompt cache from that point and invalidating later thinking blocks.
- Sample loop (page gives Python, TypeScript, C#, Go, Java, PHP, Ruby). Condensed Python outline:
  - `client.beta.messages.create(model="claude-fable-5-1", max_tokens=16000, betas=["mid-conversation-system-clear-at-2026-08-21"], tools=tools, messages=messages)` with one `read_file` tool (`path` string) over in-memory files `pyproject.toml` and `README.md`.
  - Append the assistant turn exactly as returned, thinking blocks included; break when `stop_reason != "tool_use"`.
  - Build `tool_result` blocks (missing file → `"File not found: …"` with `is_error: True`).
  - Append `{"role": "user", "content": tool_results}`, then `{"role": "system", "content": BATCH_NUDGE, "clear_at": "next_user_message"}`.
  - Print the first `text` block of the final response.

## Keep the conversation history append-only

- Append each assistant turn exactly as returned (thinking blocks included) and do not edit earlier turns between requests.
- For new accounts created on or after August 31, 2026, Fable 5.1 thinking blocks are valid only in the exact conversation that produced them: replaying a thinking block after its prefix (system prompt, tool list, or any earlier message) changed returns 400, or drops the affected blocks if `thinking.block_binding.prefix_mismatch_behavior: "drop_block"` is set (beta header `thinking-binding-controls-2026-08-01`). Adopt the pattern even if not enforced for your account, so the same code works everywhere.
- The edits that trip the check are the same that restart the prompt cache: injecting and removing per-turn reminders, summarizing older turns in place, changing the system prompt mid-session. Instead: per-turn reminders as turn-scoped system messages; instruction or tool changes as a mid-conversation system message, not rewrites of `system` or `tools`; trimming by server-side compaction or context editing.
- Client-side compaction: simplest shape is to replace the whole history with one summary message plus the new user turn, replaying nothing else; no thinking blocks carry over, so nothing fails, and the model thinks afresh.
- Cache reads are now cheaper (see Pricing), so compacting early to save cost may no longer be the right cost-intelligence trade-off on Fable 5.1; experiment with later compaction points.
- To find existing edits: run a session with `prefix_mismatch_behavior: "drop_block"` and log `input_transformations`, or capture a few normal turns' requests and confirm consecutive requests are byte-identical up to appended turns.

## Writing density

- Fable 5.1 writing has few stock phrases and little unexplained jargon, but sometimes denser prose than Fable 5: longer sentences, fewer paragraph breaks.
- An instruction that defines the anti-pattern, "mannered prose", helps; prefer putting it in a user message over the system prompt. Its content (paraphrased): mannered prose replaces direct statement with metaphor and flourish (two example swaps, e.g. a parameter "worth varying" becoming a "dial worth turning"); such phrases display the writer rather than convey the idea, make readers work harder, and are imprecise because metaphors import uncontrolled connotations; say what you mean and use the literal phrase when one exists.
- A short version also tends to work: a one-line request to remove all mannered prose.

## Formatting in chat

- Earlier models overused bullets and bold, so many prompts carry anti-formatting rules. Fable 5.1 leans the other way: less bold, less likely to use headers, lists, or quotation marks.
- Remove anti-formatting language, or replace it with a rule for when formatting is appropriate (paraphrased): use lists and bullets when asked or when content is multifaceted enough to benefit; if the person asks for minimal formatting, use no bullets, headers, lists, or bold; keep conversational, personal, or emotional exchanges in plain prose.

## Quoting retrieved sources

- When summarizing documents, Fable 5.1 is more likely than Fable 5 to reproduce source passages without marking them as quotations.
- Fix: add one complete example of a correct response to the system prompt — the user request, the response, and a sentence explaining why it is correct. The page's example: a user asks to compare how two (fictional) outlets covered a bridge closure; the response shows two templated `[web_search: …]` lines, then compares where the outlets agree and differ, conveys each outlet's reporting in one or two sentences of the assistant's own indirect speech, and uses one short marked quotation; the rationale says it is organized by agreement/difference, reworded except for one short marked phrase, and still specific and complete.
- Replace the `[web_search: ...]` lines with your own tool's name so the model reads them as templated tool output, not literal text to emit.

## Finish the whole task

- Fable 5.1 can run very long tasks with little methodology guidance when the goal is clear. On complex asynchronous workloads, nudge it not to end its turn early. Without the nudge it sometimes describes the next step instead of doing it ("Next, I'll …") or asks permission for a step already covered ("Shall I apply this?"), so users must reply "continue". That suits pair programming but underuses long-horizon capability.
- Two system prompt additions; apply both. If prompt length is limited, use only the first, which keeps most of the effect.
- First addition (autonomy), paraphrased in four parts:
  1. You are operating autonomously; the user is not watching and cannot answer mid-task, so "Want me to…?" or "Shall I…?" blocks the work. Proceed without asking on reversible actions that follow from the request. Stop only for destructive actions or real scope changes. Offering follow-ups after finishing is fine; asking permission before doing the work is not.
  2. Exception: when the user is describing a problem, asking a question, or thinking aloud, the deliverable is your assessment; report and stop; do not fix until asked.
  3. Before ending a turn, check the last paragraph: if it is a plan, analysis, question, list of next steps, or a promise of undone work ("I'll…", "let me know when…"), do that work now with tool calls, including retrying after errors and gathering missing information. Do not stop because the context or session is long. End only when complete or blocked on input only the user can give.
  4. Before a state-changing command (restart, delete, config edit), check that the evidence supports that specific action; a signal that pattern-matches a known failure may have a different cause.
- The opening sentence (the user is not watching) carries much of the effect; keep it as written. If the product needs specific confirmations, add a sentence after it listing them. The block can make the model less likely to ask about ambiguous requests; check that trade-off.
- Second addition (scope as deliverable), headed "# Delivering work", paraphrased in three paragraphs:
  1. The request, or the plan the user approved, sets the scope, and the scope is the deliverable: do not quietly narrow, widen, or swap it. Read ambiguity like a careful colleague: make routine calls, check in only when readings lead to materially different work. Raise a real problem in a sentence or two and keep building under stated assumptions; if the user reaffirms, deliver the full request.
  2. If a question comes up partway, first do everything independent of the answer, then state the assumption made — or, when a wrong guess would be unsafe or make the work useless, put the question at the end of a turn that also delivers progress. If one part is blocked, finish every other part and say exactly what was left out and why; scaling down is the user's call. A decided step is to be run, not announced.
  3. Keep changes to what the request needs; unrequested cleanup, docs, or changes to unrequired files are end-of-task suggestions; actions clearly beyond the ask, and risky or destructive ones, still need the user's go-ahead.

## Tell the model what to preserve in compaction summaries

- Fable 5.1 responds well to explicit instructions about what a compaction summary must keep. Server-side compaction already does this. For client-side compaction, use a summarization instruction like this (paraphrased): summarize inside `<summary></summary>` tags so a new context window can continue without redoing work or being re-given constraints. Preserve: (1) difficulties and how they were handled; (2) options raised, tried, or set aside, and why; (3) everything asked, decided, agreed, ruled out, or set as preference/constraint/boundary — stated exactly; (4) exactly where things stand; (5) what is open, unresolved, promised, or next; (6) hard-to-reconstruct specifics — names, numbers, dates, exact wording, links — kept exactly. Be complete on these even at the cost of length; keep the rest concise. Weight voices differently: keep the user's words close to verbatim; condense the assistant's own explanations to their conclusions, without dropping any of the six items.

## Keep changes and tests to what the task asks for

- On open-ended features Fable 5.1 sometimes delivers more: fixes nearby code, extends unmentioned behavior, or commits more test files than warranted. It responds well to explicit instructions about what to leave out.
- Instruction (paraphrased): pre-existing bugs, performance concerns, or unmentioned behavior found while working are not fixed, optimized, or extended in this change unless the requested behavior cannot work without it — report them as follow-ups. On ambiguity, implement the reading the wording and surrounding code most directly support, state the assumption, do not build for other readings. Verify however you like; scratch scripts need not be kept. Commit tests only where the task asks or the repo already keeps tests for this kind of change, sized like neighboring test files (roughly one focused test per stated behavior); do not turn scratch checks into permanent tests. This limits extras only: implement every requested behavior completely.
- Effect: unrequested additions and committed test code drop substantially with no measurable change in task success.

## Search triggering at low effort

- At `low`, Fable 5.1 is less likely than Fable 5 to call a search or retrieval tool and more likely to answer from memory.
- Sometimes the simplest fix is raising effort for affected turns only (change effort mid-conversation).
- Otherwise a system prompt nudge helps: recognizing a name is not knowing its current state; search such names as the user wrote them. Example (paraphrased): when a query centers on a name you do not confidently recognize, or recognize from a fast-moving area (e.g. AI models, developer tools) where things shift within months, verify the name by searching before answering, with the name as written in at least one query alongside reformulations; partial background is what makes an outdated answer sound authoritative, so familiarity is no reason to skip the search.

## Reduce safeguard false positives

- Fable 5.1's classifiers produce fewer false positives than Fable 5's did at launch; finding vulnerabilities in source code is permitted. False positives still occur and return `stop_reason: "refusal"`. Three situations raise them:
  - **Compile-check phrasing:** ask "Are there any bugs in this program?" rather than "Does this program compile without errors?".
  - **Lesser-known programming languages:** give context on what the language is and how it works, e.g. access to its documentation.
  - **Base64 in tool output:** tools returning base64-encoded data into context can trigger false positives; removing them is the recommended fix.

## Prefer targeted edits over whole-file rewrites

- Fable 5.1 is more likely than Fable 5 to rewrite a whole text file instead of making a targeted edit. The result is usually the same, but unless the file is short or mostly changing, rewrites cost more output tokens and time.
- Append to the system prompt or first user message (paraphrased): editing tokens should be minimized, all else equal, so when it does not affect the result, edit surgically rather than rewriting the file. This restores Fable 5 behavior for small and medium changes.

## Leave room for long outputs at xhigh and max effort

- At `xhigh` and especially `max`, the model can think longer before replying. For a single request asking for a long deliverable (e.g. a full rewrite of a long document), it may draft much of it in thinking and then write it again as the reply: longer wait, more output tokens.
- Simplest approach: run such requests at `high` (recommended start) and move up only with measured quality gains. If running at `xhigh`/`max`:
  - Set `max_tokens` with room for thinking plus reply, not just the expected reply length.
  - Append a note to the end of the user message (replace `[max_tokens]` with the actual value, e.g. 64,000). Paraphrased: everything in one reply, including reasoning and drafting, counts toward one limit of about `[max_tokens]` tokens; hitting it gives a cut-off response and the person must start over; composing the whole deliverable in reasoning and again as the reply doubles the turn without improving it, so do not. For long deliverables (multi-section documents, large tables or datasets, complete code files), spend reasoning on understanding the request, checking inputs, and settling structure and hard decisions; use the output space to write; multiple drafts are usually unneeded. This makes thinking much shorter on prose and code requests.

## Let the lead agent keep working while subagents run

- If a coding agent lets Fable 5.1 delegate to subagents, do not force the lead to stop and wait for each. On coding tasks, letting the lead continue lowers average time to completion at similar quality, token usage, and cost.
- Setup: the subagent-start tool returns immediately; each subagent's result goes back to the lead in a later `user` message when ready; the lead gets a separate tool to call when it wants to wait for a result.
- The model still often chooses to wait; time savings come from runs where it carries on with other work.

## Give vision work tools to crop and zoom

- Fable 5.1 has better out-of-the-box vision; on complex inputs such as dense charts it does best when it can iteratively analyze, crop, and visually verify.
- Run it as an agent with a container holding the raw images or videos and basic image libraries (PIL, OpenCV) pre-installed. If a container is too much overhead, an image-cropping tool alone delivers most of the uplift: a tool returning a chosen region cropped and enlarged lets the model examine details and scales test-time compute with image tokens. Crop tool recipe in the cookbook.

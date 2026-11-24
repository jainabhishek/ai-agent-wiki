# Prompting Claude Fable 5.2 — Anthropic (Claude Platform Docs) (raw capture)

> Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-2
> Publisher: Anthropic (Claude Platform Docs) · Date: accessed 2026-11-24 (the page has no byline date)
> Captured: 2026-11-24 via curl of the page's `.md` export (condensed).
> Capture policy: prose is paraphrased. Example prompt blocks are paraphrased clause by clause; short operative phrases are quoted. The page has no code sample.
> Scope: the page's metadata description says it covers "Claude Fable 5.2 and Claude Mythos 5.2". The body names Claude Fable 5.2 throughout and says Claude Mythos 5.2 offers the same capabilities only to organizations verified through the Cyber and Life Sciences verification programs. No API model ID string is written on the page; `claude-fable-5-2` appears only inside the page's own URL.

Page description (paraphrased): Fable 5.2 / Mythos 5.2 prompting topics — effort; stopping early; approvals; owning the code; progress updates; subagents; accumulated caution; prompts and harnesses built for older models; final reports; refusals.

Intro: points to "What's new in Claude Fable 5.2", the joint Fable 5.2 / Mythos 5.2 migration guide, and "Prompting best practices" (techniques for all current models). Unlike the Fable 5.1 page, it does not say that prompts for the predecessor work without changes; it says Fable 5.2 behaves differently from earlier models in several ways.

Symptom index:
- Unsure of effort, or easy requests start slowly → Calibrate effort.
- Turn ends before the work is done → Finish the whole task.
- Coding agent duplicates code it finds, or flags problems without fixing them → Say who owns the code.
- Nothing visible to the user during long agentic turns → Keep users informed during long turns.
- Sessions start more subagents than needed → Set expectations for subagents.
- Agents ask for approvals they do not need, or hold routine work → Keep caution from piling up.
- Carrying over a system prompt, skills, or harness built for Fable 5.1 or Opus 5.5 → Review prompts and harnesses designed for earlier models.
- People read the closing report or handoff once a long task ends → Make reports easy to follow.
- A response comes back with `stop_reason: "refusal"` → Safeguard refusals.

Note block:
- For migration order, see "Where to start".
- Make the suggested system-prompt, tool-description, and rule/notes changes in new conversations only. On Fable 5.2 a request that fails the prefix check gets a 400 error (thinking-block conversation mismatch). Resuming a stored conversation after changing `system`, `tools`, or an earlier message can fail the check. To change instructions mid-conversation, put them in the newest turn, or, where mid-conversation system messages are available, append a system message.

## Calibrate effort

- Effort governs thinking depth, tool-call count, turn duration, and token use. Tune it alongside the prompt.
- Start at `high`, the Fable 5.2 default on the Claude API. Levels rank the same across Claude models, but thinking per level differs, so rerun the effort sweep rather than reuse a setting tuned on Fable 5.1 or Opus 5.5.
- Per level:
  - `low`: quick back-and-forth, well-specified tasks, high-volume work (e.g. fast subagents). On coding evals Fable 5.2 at `low` beats past models at `low`; in Anthropic's testing it scored close to Fable 5.1 at higher effort.
  - `medium`: interactive coding, chat, everyday knowledge work.
  - `high`: hard coding, research, agentic work, long unattended runs. Turns take noticeably longer than at `medium`.
  - `xhigh`: hardest long-running coding/agentic work where a gain is measured. Slightly higher scores on internal coding evals, many more tokens.
  - `max`: measuring the ceiling, or rare tasks where time and tokens do not matter; most reasonable for open-ended problems such as scientific discovery and mathematics. Slow; many more tokens than `xhigh`.
- Most of the capability gain arrives at `high`. The `medium` → `high` step raised scores on most coding and knowledge-work evals Anthropic tracks, at more tokens and time; drop to `medium` where evals hold. Beyond `high`, any gain varies by task and is inconsistent.
- For agentic work at `low`/`medium`, add the "Finish the whole task" text: early stopping is more likely at lower effort.
- At `high` and above the model thinks before almost every reply, even a greeting. Use lower effort for basic turns. An instruction to answer directly without deliberating did not stop thinking at `medium` and above.
- Effort has little effect on reply length; use prompting for length and tone.
- Mix levels in one workflow (e.g. plan at `medium`, raise effort for the long unattended part). Per-message effort (beta, header `mid-conversation-output-config-2026-07-01`) changes levels and keeps the prompt cache; a change holds until replaced. Without it, a new top-level `effort` value on the next request can invalidate cached messages.

## Finish the whole task

- On long multistep tasks Fable 5.2 sometimes ends a turn early: it lists remaining work, offers to carry on, or halts at a routine snag like a timeout. More common at `low` and `medium`.
- Suggested system prompt block, headed "# Finishing work" (paraphrased):
  1. Do not stop while you still owe requested work; be persistent.
  2. Status notes and clarifying open decisions are welcome, but continue work that does not depend on the user's answer.
  3. If you catch yourself inviting redirection or offering to wait, go on with the next part instead. Diagnose ordinary obstacles (errors, timeouts, locked files, empty results, failing tools); when one is not a genuine blocker, get past it using your existing access — for example retry after a wait, correct the request, or switch tool or source.
  4. If someone clearly made something a hard blocker (a file marked not to be touched, access intentionally withheld, a safety guardrail), do not work around it: report the finding plainly and seek a different safe route to completion. Stopping early is very rarely merited: only when the task cannot move without user input, or the blocker is deliberate. This does not override confirmation for risky or destructive actions.
- Treat it as a starting point and adapt.
- Result: replaying recorded sessions from an agentic coding product at `medium`, a version of this text cut sessions ending with continuable unfinished work by about half. It removed most ask-permission / offer-to-continue endings, but not endings that list what remains and stop. Output tokens rose about 30 percent.
- The model asks less often with this text, so retain a harness-side confirmation gate for risky or irreversible actions.

### Approvals

- When asking the model to continue, say exactly what you want (e.g. "Yes, run the migration on the staging database") instead of "continue", "go", or a thumbs-up.
- Approval rules in the system prompt should name the specific actions to double-check. In simulated tasks with no one to approve, a rule listing "sending messages to people outside this conversation" as approval-requiring made the model withhold roughly half of its ordinary outreach to coworkers and other teams.

## Say who owns the code

- Fable 5.2 pays close attention to code ownership. On small coding tasks, when the prompt said nothing about ownership or framed the code base as someone else's, it added to the existing structure, even duplicating code. When told the code base was its own, it often consolidated duplicates and sometimes made related unrequested fixes.
- To get structural improvement, a one-sentence ownership line (paraphrased): you own and maintain this codebase long-term, and its design is your call.
- Effect: consolidation of duplicated code into one shared function rose from under 10 percent of runs to about 75 percent.
- Costs: output tokens rose about 70–80 percent; unrequested changes appeared (many new tests and docs); in some runs existing feature behavior changed. The closing PR summary often omitted small changes — review the diff and the summary.
- Omit the sentence where the user owns the code and wants minimal change. A scope-limiting rule does not cancel it: with "No drive-by refactors, renames or cleanups" earlier in the same prompt, the model still consolidated in more than half of runs.

## Keep users informed during long turns

- Fable 5.2 sometimes writes little user-facing text over long tool-call runs and may make its first tool call without saying what it will do.
- First, check the client receives updates: between-tool-call updates come back as progress-update `thinking` blocks (what was found, what is next). Under the default `thinking.display` of `"omitted"` those blocks carry no text, so a client that shows only `text` blocks appears silent. Set `display: "updates"` (beta, header `thinking-display-updates-2026-08-18`) for a short summary of each update, or `"summarized"` for updates plus summarized reasoning; render non-empty `thinking` blocks between tool calls.
- Updates are most valuable when a person is interacting live. Three options:

### Modify your harness
- Track how many tool-calling steps in a row produce nothing user-readable (neither a `text` block nor a non-empty `thinking` block). Count with `display` at `"updates"` or `"summarized"` (at `"omitted"` all thinking is empty). Needs mid-conversation system messages.
- When several pass in a row, add a reminder following the newest tool results, sent as a turn-scoped system message (`clear_at: "next_user_message"`, beta, header `mid-conversation-system-clear-at-2026-08-21`). Reminder (paraphrased): the user has not heard from you for a while; say briefly what you are doing, then continue.
- Result: on multi-turn coding tasks the longest silent stretch roughly halved, with no noticeable rise in tokens or time.
- Keep every past reminder in `messages` on subsequent requests. Deleting or changing one counts as editing an earlier turn, which breaks the thinking blocks that follow it.

### Signal intent
- System prompt text (paraphrased; same shape as the Fable 5.1 line): before starting, say in a line what you will do; give brief updates; close with a self-contained recap — found, did, next — so a reader of only the last message has the full picture.
- Result: a message before the first tool call in every run of the coding tasks; output tokens per task rose roughly 20 percent.
- Use where a human is directly in the loop; combine with the reminder for more updates.

### Update system prompt instructions
- If the harness cannot add the reminder, or there are no mid-conversation system messages, add one sentence (paraphrased): every few tool calls, give the user a one-line status update.
- Result: cut most long silent stretches on workflow-automation tasks. Expect several tool calls between updates even with reminder plus intent text.
- Fable 5.2 works well on long-running asynchronous tasks; Anthropic recommends it for work where nobody needs frequent updates.

## Set expectations for subagents

- Delegation depends on harness and tasks. Given only a bare subagent tool on short tasks, it seldom spawned one; inside an agentic coding product with prompts that encourage handing off work, it spawned them freely.
- At `xhigh` and `max`, in an agentic coding product, Fable 5.2 used subagents to review its own work; Fable 5.1 did not on the same tasks.
- Early testers had good results with Fable 5.2 as planner and orchestrator for other models. Delegation speeds parallel work, but subagents can be a large share of session cost; check which model subagents use by default.
- Change the subagent tool description only if it over-delegates. Worth it mainly when the harness already encourages delegation and subagents consume much of the token spend. With a plain description and no delegation prompts, likely unnecessary. Review delegation lines in system prompt, skills, or agent files first.
- A new description should state what a subagent adds to session cost, when delegation is and is not worth it, and how to brief a started subagent.
- If over-delegation persists, say more about subagent cost and test. At `high`, a longer cost-focused description roughly halved subagent count versus a shorter one.

## Keep caution from piling up

- Cautious instructions accumulate from past sessions via memory, notes, and instruction files. Fable 5.2 follows them closely and asks for unnecessary approval. Seen mostly when several agents worked together.
- Remedies:
  - **Remove notes you no longer need** — memory can hold stale rules such as "never retry" that the model keeps obeying.
  - **Name the steps that need no approval** — "act more freely" is too vague; list routine steps it may take alone.
  - **Check your validation steps** — a condition like "stop and review at the first error" can block autonomous work; remove or narrow unneeded stop conditions.
  - **Be explicit about exceptions** — the model treats "never" as absolute; write "ask for approval before deleting files" rather than "never delete files" if you want it to keep responsibility for the action.
- Still keep a harness-side confirmation gate for risky or irreversible steps.

## Review prompts and harnesses designed for earlier models

Some instructions and interventions written for earlier models raised cost, caused side effects, or no longer worked. Reconsider:
- **Standing instructions to delegate** in system prompts, skills, agent files: read before migrating; remove those not needed if testing shows over-delegation.
- **A token budget shown to the model:** the budget's size changes how much Fable 5.2 spends. On coding tasks at `high` and `xhigh`, removing a large budget lowered cost with equivalent performance. Test without it. This concerns prompt text, not the API's task budgets (beta), which were not tested.
- **Harness code that edits earlier turns:** Fable 5.2 uses preserved thinking. Changing the system prompt, tools, or an earlier message between requests invalidates thinking blocks after that point. By default the Messages API rejects the request; the Message Batches API drops the blocks. To shorten history, use context editing, or compaction that keeps no earlier turns after the summary. To make the Messages API drop instead, set `thinking.block_binding.prefix_mismatch_behavior` to `"drop_block"` (beta, header `thinking-binding-controls-2026-08-01`). When earlier thinking was dropped every turn, the model re-thought and used more output tokens (the worst case; depends on edit frequency). Apart from compaction and context editing, keep history append-only: high cache hit rate, no thinking dropped. Measure output tokens before relying on `"drop_block"`.
- **The "treat that answer as done" lines** from the Opus 5.5 prompting page (two chat-system-prompt sentences telling the model to treat an earlier answer as done and focus thinking on the new message): at `high`, they reduced Fable 5.2's thinking on follow-ups and made it far less likely to point out mistakes in earlier answers. Omit where re-examination matters; elsewhere test before adopting.
- **Instructions to think less:** Fable 5.1 usually obeyed "answer directly without deliberating"; on Fable 5.2 such a line does not stop thinking at `medium`+. Remove and lower effort instead.
- **Style rules for writing:** followed closely; a strict cap (the example is one instruction per sentence, 20 words max) yields choppy prose. Remove unneeded rules before adding the report text below.
- **Rules, notes, and memories that have built up** (some possibly model-written): before migrating, delete cautions whose reason no longer holds; rewrite absolute rules with scope and reason. A system that is already stuck may need a restart with pruned memory and notes.

## Make reports easy to follow

- Early testers rated Fable 5.2's writing above Fable 5.1's and similar in clarity to Opus 5.5's. After long agentic work, readers of the final report have not seen the tool calls or files, so the report must stand alone.
- Suggested system prompt block, headed "# Communicating clearly" (paraphrased):
  1. Write for an intelligent reader with little context who has not seen your tool calls, reasoning, or opened files and may be switching in from other work. Make messages self-contained. Lead with the key points; use progressive disclosure; do not put undefined references early that only make sense later.
  2. Use plain words in clear full sentences. Do not use terms or abbreviations invented during the work; say what the thing is. Write mostly in ASD-STE100 Simplified Technical English style: short sentences, one idea per sentence, active voice, the same word for the same thing. Use flowing prose where ideas connect and bullets for separate items. Be concise but keep the key context; maximize readability.
- Result: on agentic tasks, final reports were less dense with fewer semicolons; on workflow automation tasks, sentences were shorter. Add length or required-detail instructions per use case.

## Safeguard refusals

- Fable 5.2 runs safety classifiers. A declined request returns `stop_reason: "refusal"`; `stop_details.category` names the category:
  - `cyber` — could enable cyber harm (malware, exploit development).
  - `bio` — could enable biological harm (dangerous lab methods).
  - `frontier_llm` — could assist development of competing AI models.
  - `reasoning_extraction` — asks for the model's internal reasoning to be written out in the reply.
  - `general_harms` — another usage-policy area.
  - `null` — no named category.
- Benign cybersecurity and life-sciences work can trigger `cyber`/`bio`. Remedies: the Cyber Verification Program and the Life Sciences Verification Program. Claude Mythos 5.2 offers Fable 5.2's capabilities only to organizations verified through those programs.
- Remove prompt, skill, or tool-description instructions asking the model to write its reasoning in the response; to see reasoning, set `display: "summarized"` and read thinking blocks.
- Retrying a refused request on a different model is covered under "Refusals, fallback, and billing" in What's new in Claude Fable 5.2.

## Where to start

1. Set `effort` to `high` explicitly; also run evals at `medium` and `xhigh`.
2. Read carried-over system prompts, skills, agent files, memory files, notes, and harness text; remove or test what the "Review prompts and harnesses" section lists.
3. Run your longest agentic tasks; note early stops, unneeded approvals, silence, over-delegation, and adding to existing code where restructuring was wanted.
4. Apply the text or advice for each observed behavior one at a time; measure its effect and token cost on your own tasks.

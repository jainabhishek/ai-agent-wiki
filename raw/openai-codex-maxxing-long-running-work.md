# Codex-maxxing for long-running work — OpenAI (raw capture)

> Source: https://openai.com/index/codex-maxxing-long-running-work/ (landing page, listed on https://openai.com/business/learn/ as "Codex-Maxxing for Long-Running Work") → white paper PDF https://cdn.openai.com/pdf/8a9f00cf-d379-4e20-b06f-dd7ba5196a11/OAI_WhitePaper_Codex-maxxing26.pdf
> Publisher: OpenAI (Guides) · Date: 2026-06-22 (landing-page byline "June 22, 2026"; the PDF carries no date)
> Captured: 2026-10-12 via built-in browser (landing page) + curl and pypdf text extraction (27-page PDF) (condensed).
> Landing-page tags: AI Adoption, Guides. Subtitle: how Codex helps work continue beyond a single prompt. The landing page says creator Jason Liu shares strategies for using Codex as a persistent workspace that keeps context, manages complex workflows, and sustains progress on long projects; it also promises guidance on breaking goals into verifiable steps, continuity across workstreams, and when to delegate execution vs. keep human oversight.

Note: paraphrased. The PDF is a visual white paper with short text per page. Short labels and identifiers are kept verbatim.

## Framing (pp. 3–4)

- Codex is framed as a place where work can start, continue, and become output — a single prompt turned into an "operating loop" for getting projects done.
- Still strong for coding, but the shift is that work gets "somewhere to live".
- Creator Jason Liu uses Codex daily for presentations, transcripts, spreadsheets, browser tasks, and recurring work. The paper follows how he gathers context, asks for help, reviews output, and returns to the next step without losing the thread.

## Contents (p. 2) — ten sections

01 Durable threads · 02 Voice input · 03 Steering · 04 Memory · 05 Computer and browser use · 06 Remote control · 07 Thread automations · 08 Three examples of loops · 09 Goals · 10 Side panel

## Section 01 — Durable threads ("Giving the work a place to live")

- For important workstreams, a **pinned thread** becomes the home of the work, where context, preferences, old decisions, and open loops accumulate.
- Use a durable thread for work you expect to revisit. Example threads: Social feedback monitoring; Codex for open source (issues, maintainers, contribution patterns, release notes); OpenAI CLI (commands, conventions, repo structure, review preferences); Agents SDK (examples, docs, recurring questions, product behavior); Chief of Staff (messages, follow-ups, meetings, open loops).
- Durable threads keep history as the conversation grows and store it in the memory vault.
- **Tradeoff:** long threads carry context and may cost more to run than a fresh short thread; for important workstreams continuity can be worth it.

## Section 02 — Voice input ("Put more of your actual thinking into Codex")

- Voice changes the *kind* of context Codex gets, not only speed: spoken input carries the unedited version — half-remembered names, loose direction, uncertainty. Example spoken prompt: a vague memory of "some guy named Ben in Slack" mentioning something, "just go look".
- Pull quote (Liu): plans improve when the model sees the messy version of your thinking.
- Liu records voice notes while exploring an agent-built page in the browser, then presses Enter so Codex executes the feedback.
- Transcripts (calls, meetings, hallway talk, rough voice notes) become starting material for a plan, draft, artifact, or next action.

## Section 03 — Steering ("Shape the queue while Codex works")

- Steering = adding the next instruction while Codex is already working: correct direction, add context, approve the next step, or queue the next action after a tool call.
- Voice plus steering while reviewing a site: short corrections (make an element smaller, fix wrong copy, adjust spacing) and queued follow-ups (open a PR when done, wait for the preview deployment, show the preview link before anything is posted).

## Section 04 — Memory ("Make memory something you can review")

- Memory acts as a notebook giving context for actions. Long threads need memory outside the conversation; message history is not always enough. Useful context should become something you can open, edit, diff, and reuse.
- The **vault** holds rolling context: people, decisions, open loops, daily notes, project state.
- Distinction: repositories hold code; the vault holds rolling context around the work.
- If the vault lives in GitHub, **diffs become a review surface for memory** — you see what Codex judged worth writing down.
- Long threads should not quietly accumulate vague impressions in history; they should record what changed (this person prefers X; project waits on Y; decision made; loop closed).
- Sample memory instruction: update people notes as people are mentioned; update the project page as projects move; mark loops closed as they close; record each decision and why it matters.

## Section 05 — Computer and browser use ("Decide what the thread can touch")

- Surfaces: `$browser` (local web surfaces, previews, annotations); `@computer` (GUI-only work needing clicks); `@chrome` (signed-in sessions, authenticated tabs); Connectors (Slack, Gmail, Calendar, GitHub, other work surfaces); Skills (reusable workflows).
- Connectors reach where work first appears: Slack threads, inboxes, calendars, docs, issue trackers.
- Selection rule: iterating on a local app → browser surface; task needs logged-in state or several authenticated tabs → Chrome; only possible through a desktop app → computer use, with clear permissions and review.
- Once a workflow succeeds, package instructions, references, and scripts as a skill so Codex need not be retaught.

## Section 06 — Remote control ("Keep longer loops portable")

- Codex keeps working on the machine where files, permissions, and local setup live; you check in from another device to review findings, answer a question, approve the next step, or redirect.
- Matters most for tasks that take time. Liu's pattern: start at the desk, walk away, review the next decision point from the phone.
- Remote control is not a reason to skip reviews; it keeps enough attention on the loop to unblock the next move.

## Section 07 — Thread automations ("Schedule Codex to return")

- Normal prompt = "do this now"; thread automation = "keep checking this and move it forward when something changes".
- Thread automations are heartbeat-style recurring wake-ups attached to the current thread: Codex returns to the same conversation on a cadence, keeping context instead of starting fresh.
- A thread can have multiple schedules, can run until a condition is met, and can adjust cadence as the task changes.
- Example: every 30 minutes check Slack and Gmail for unanswered messages that may need attention, research context, draft replies, send nothing without approval.
- Targets: a pull request, Slack thread, inbox, deployment, document, support thread, or long-running command.

## Section 08 — Three examples of loops ("Real ways to apply Codex in your workflows")

The value comes from the loop across features: context, tools, memory, recurrence, review. Each loop splits "what Codex prepares" from "you decide".

1. **Chief of Staff** — Codex checks Slack and Gmail on a schedule, finds messages needing attention, gathers context, drafts replies. Prepares: open messages, relevant context, draft replies, questions needing judgment. You decide: approval, tone, timing, final decision.
2. **Monitor for feedback** — Codex watches a Slack thread for animation feedback, updates the Remotion project, re-renders, prepares the revision for review; crosses Slack, Remotion, and computer use when upload/review needs a GUI. Prepares: feedback summary, updated render, revision notes, next review link. You decide: creative judgment, final approval, publishing decision.
3. **Get a refund** — Codex checks whether a customer-support agent has joined and prepares the next reply when the conversation changes; continues while the user is away but the action stays bounded. Prepares: status checks, draft responses, useful evidence, recommended next step. You decide: consent, approval, any irreversible action.

## Section 09 — Goals ("Set goals Codex can verify")

- A weak goal asks Codex to implement a plan (example: implement the plan in this Markdown file).
- A stronger goal gives something to test against: expected behavior, review criteria, constraints, or a definition of done. Example: port a library, keep the public API compatible, use the original unit tests as the success check; ready for review when the same tests pass and differences are documented.
- **Rich-to-Rust** example: the goal was to port the Rich library to Rust such that it passed the original unit tests; the suite set the standard, and the work was not ready until the new implementation passed them.

## Section 10 — Side panel ("Make the artifact part of the loop")

- The side panel is more than a preview: you inspect the same object Codex acts on, comment, review changes, and keep the artifact in the thread. Pull quote (Liu): this is where Codex stops being only a chat app.
- **Inspect artifacts:** Markdown (reviewable with comments), spreadsheets (render formulas, allow cell edits), CSVs (shown as tables), PDFs (render directly), slides (create and review in-app).
- **Operate web surfaces:** in-app browser for small web artifacts — `index.html`, Storybook, Remotion Studio, Slidev, Streamlit, Jupyter. Often the smallest version suffices: one `index.html` with JS and CSS becomes a live surface for interaction and review.
- **Review changes:** you and Codex look at the same object while work moves; comments become instructions; the artifact becomes context.

## Close (p. 26)

Liu's practice shows how fast Codex can build systems for work; tasks become easier to pick up, review, and continue, so people spend less time restarting.

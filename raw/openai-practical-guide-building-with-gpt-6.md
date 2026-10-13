# A practical guide to building with GPT-6 (page title: "A model guide for the GPT-6 family") — OpenAI (raw capture)

> Source: https://openai.com/index/practical-guide-building-gpt-6/ (listed on https://openai.com/business/learn/)
> Publisher: OpenAI (Guides) · Date: 2026-10-02 (page byline "October 2, 2026"; the Learning Hub card shows the same date)
> Captured: 2026-10-12 via built-in browser (get_page_text + DOM extraction of carousel slides) (condensed).
> Title note: the Learning Hub card and "Keep reading" links call it "A practical guide to building with GPT-6". The page H1 and HTML title are "A model guide for the GPT-6 family". Subtitle: practical tips for best results from GPT-6 models while managing time and cost. Author: OpenAI. Tags on page: Product, Guides. Not a PDF; the guide is the HTML page.

Note: paraphrased. Model display names are kept verbatim. The page never gives API model IDs.

## (Intro)

OpenAI calls GPT-6 its most advanced suite of models and frames the guide as covering four things: choosing a GPT-6 model, giving effective instructions, managing long-running work, and preparing for production. Example work types: prototype from an idea, build and test a feature, orchestrate multi-step workflows across repos, databases, and external APIs.

### Model cards (H3s) — price per 1M tokens as shown on the page

| Model (display name) | Tagline (paraphrased) | Input | Output | Cached input |
|---|---|---|---|---|
| GPT-6 Astra | most intelligent, for the best results | $10.00 | $50.00 | $1.00 |
| GPT-6.1 Sol | near-Astra intelligence for a fifth of the price | $2.00 | $10.00 | $0.10 |
| GPT-6 Luna | fast, efficient everyday work at scale | $0.10 | $0.50 | $0.01 |

(The page does not state the unit; these match per-1M-token list pricing format.)

## TL;DR

- **Run effectively in production:** use caching and compaction to manage context and cost; measure task success and latency; plan monitoring and data controls.
- **Match the model to the workload:** balance capability, cost, latency through model choice, reasoning effort, and speed.
- **Adjust prompts and skills:** keep prompts, skills, and repository instructions consistent on three things — what to deliver, what the model may do independently, and what counts as done.
- **Keep long-running work on track:** steering, async tools, and delegation for updates and independent work; set clear boundaries for when the model asks for input.

## 1. Run effectively in production

### Prepare your workflow for production

- **Efficiency:** cut context the task does not need but keep the evidence it does (links to cost-optimization guide). Run independent tasks in parallel where the app allows, so one slow step does not block unrelated work (links to latency-optimization "parallelize").
- **Prompt caching** for recurring work: cached input tokens cost "up to 95% less" than uncached, depending on model. Put stable instructions and reference material before changing task details; keep tool definitions consistent. Use the caching dashboard and the prompt-caching diagnostics guide to see where reuse breaks. When estimating whole-workflow cost, include cache writes and any long-context rates.
- **Compaction** for longer conversations: shrinks context but keeps the state needed to continue.
- **Monitoring and data controls:** decide how to monitor behavior (link goes to the misalignment-monitoring safety-checks guide) and review data controls ("your data" guide).
- **Test before deploying:** run representative tasks; measure task success, latency, and **cost per successful task**. Link: API deployment checklist.

### Match the model to the workload

Model choice plus reasoning level = an intelligence/price tradeoff.

- **Model:**
  - GPT-6 Astra — hardest reasoning work needing maximum intelligence.
  - GPT-6.1 Sol — complex coding, research, and computer use.
  - GPT-6 Luna — focused tasks at scale and repeated work with a clear goal (examples: extract invoice fields, classify requests, structured summaries).
  - Compare pricing per model when evaluating.
- **Reasoning level (API):**
  - Low — routine tasks (extract facts, small edits).
  - Medium — judgment work (plan a feature, compare options).
  - High — difficult debugging, deeper analysis, careful review.
  - Extra high / Max — test "where supported" when High falls short; keep only if the gain justifies extra time and cost.
  - In the API, reasoning effort can change mid-conversation without breaking cache (link: reasoning guide, "change reasoning mid-conversation").
  - In Codex: start at the model's default reasoning level; lower for simpler tasks, raise for deeper analysis.
- **Speed:**
  - API **Fast mode** — when response time matters (chat apps, coding tools); faster, more consistent responses at a higher per-token price than Standard processing.
  - Codex and API **Ultrafast** — when faster responses are worth a premium (rapid coding iterations); speeds token generation independent of reasoning effort. Page says "Available for GPT-6 Astra" (no other model named here).

## 2. Adjust your prompts and skills

### Give the model a clear assignment

- Pull quote from Eric Provencher (Developer Experience, OpenAI): models handle nuance and ambiguity better now, so overly specific guidance "can now hinder results where it previously helped."
- Start with a clear assignment: desired result, audience, relevant context and constraints, definition of done.
- Four review areas, summarized from OpenAI's "Rethinking skills and prompts for GPT-6 Astra":
  1. **Create better skills:** short descriptions explicit about when each skill runs; load supporting detail only when needed; replace rigid recipes with guidance fitted to the models your team uses.
  2. **Update your AGENTS.md:** say when particular documents and tests are relevant; explicitly authorize safe routine workflows (example: run local tests with disposable data and no production access).
  3. **Set decision boundaries:** state which actions proceed independently and which need approval; replace blanket "always ask" rules with clear boundaries.
  4. **Be prescriptive about persistence:** define what "done" includes — implement, run, inspect the result, fix failures — and name decisions that need your review.
- Further reading: reasoning best practices guide.

### Define the output you need

- In Codex or the API: specify which decisions the model may make, when to ask for input, and what a useful response looks like.
- Give enough direction to keep work moving without the model guessing at decisions that matter. Example: it may choose how to organize a summary but should check before changing project scope (link: latest-model guide, "initiative and follow-through").
- Describe a useful response (link: latest-model guide, "personality and writing style"). Example: plain language, technical detail suited to the audience, and a short handoff covering what changed, what was checked, and what still needs attention.

## 3. Optimize long-running tasks

### Keep complex work moving

GPT-6 family can take on tasks spanning hours or days. Features to manage agents on long runs:

#### API

- **Update instructions during a run:** mid-turn steering sends a correction over the Responses WebSocket API while the model works. Updates are queued; they do not cancel running tools or undo completed actions.
- **Keep working while a tool runs:** asynchronous tool calling lets the model continue independent work while the app runs a slow task (example: tests). The app returns the result when ready. Wait for that result before starting dependent work.
- **Delegate independent subtasks:** "GPT-6.1 Sol supports multi-agent workflows in the Responses API" — assigns independent work to subagents (example: investigating different parts of a codebase) and combines findings into a final response. Multi-agent is "currently in beta". (No other model named.)

#### Codex

Long runs surface decisions the first prompt did not anticipate; use clarification and steering.

- **Answer questions as work progresses:** with GPT-6 Astra, Codex can ask for clarification while it works (link: latest-model guide, initiative and follow-through). Resolve questions that affect the next step; say which independent work can continue while you decide. If you will be away, tell Codex which tasks may continue and when to pause for your answer.
- **Redirect work when requirements change:** steer the active task with new information; say what should change and what should stay the same, to avoid more time on an approach that no longer fits.

### Leverage computer use to do more of the job

- Computer use lets GPT-6 Astra, GPT-6.1 Sol, and GPT-6 Luna operate websites and desktop apps, including apps with no API. Example: investigate a bug, fix the code, open the product in a browser to check the fix.
- Choose the simplest reliable path per step: an API or connected tool when it can do the job directly; computer use when the model must read a screen, click, or fill a form.
- Building computer use into your own app: give the model a code-running tool that controls a browser or desktop — Playwright for browsers, PyAutoGUI for desktop apps.
- An embedded image (alt text) shows Higgsfield AI demonstrating GPT-6.1 Sol multitasking and computer use in ChatGPT.

### From testing to production: How teams are building with GPT-6 Astra

Carousel of four customer testimonials (self-reported):

1. **Harvey** — combines court information, case law, firm documents, and a lawyer's preferences to tailor drafts; cofounder Gabe Pereyra says more context yields better-structured outputs.
2. **Cognition** — uses GPT-6 Astra inside Devin to test software and return evidence; in an iPhone-game example Devin produced a simulator recording and a report separating passed checks from untested areas.
3. **Hex** — turns sales-channel performance questions into written findings and interactive dashboards (incl. geographic breakdowns); also asks the model to check whether the numbers make sense and whether the analysis answers the business question.
4. **Invideo** — plans timeline edits and creates custom effects editors can refine; reports roughly 3x success rate on color-grading and correction tasks; a few editors created about 50 effects in one day.

## Heading checklist (verified against the page's H2/H3/H4 list)

H3 model cards (Astra, 6.1 Sol, Luna) ✓ · H2 TL;DR ✓ · H2 1. Run effectively in production ✓ · H3 Prepare your workflow for production ✓ · H3 Match the model to the workload ✓ · H2 2. Adjust your prompts and skills ✓ · H3 Give the model a clear assignment ✓ · H3 Define the output you need ✓ · H2 3. Optimize long-running tasks ✓ · H3 Keep complex work moving ✓ · H4 API ✓ · H4 Codex ✓ · H3 Leverage computer use to do more of the job ✓ · H3 From testing to production ✓ · (H2 Author / Keep reading: page chrome, omitted).

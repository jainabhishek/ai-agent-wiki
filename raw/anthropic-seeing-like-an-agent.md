# Seeing like an agent: how we design tools in Claude Code — Anthropic (raw capture)

> Source: https://claude.dev/blog/seeing-like-an-agent/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-04-10
> Captured: 2026-10-12 via WebFetch (condensed).

Author: Thariq Shihipar (member of technical staff, Claude Code). The page
also lists dates of unrelated "related posts" (2026-09-28 to 2026-10-08);
those are not this article's date.

## Introduction (no heading)

- Tool construction is one of the hardest parts of building an agent harness.
- Claude acts only through tool calls. Available primitives include bash,
  skills, and code execution (the post links a separate post by Lance Martin
  on programmatic tool calling).
- The central design question: one general-purpose tool (bash or code
  execution) or about fifty specialized tools?
- Analogy: solving a hard maths problem with paper, a calculator, or a
  computer. The right tool depends on the solver's abilities. For a model,
  you learn those abilities by reading its outputs and experimenting. The
  author calls this "seeing like an agent".
- The post covers when to add a tool, when to remove one, and how to tell.

## Improving elicitation with the AskUserQuestion tool

Goal: make Claude better at asking the user questions (elicitation) and make
answering plain-text questions less tedious. A diagram ("Finding the sweet
spot") places options on a spectrum from no structure (a modified markdown
format: free but messy) to too rigid (a parameter on ExitPlanTool: arrives too
late in the process). AskUserQuestion sits in the middle: structured,
composable, with a clear UI surface.

### Attempt 1: Editing the ExitPlanTool

- Added an array-of-questions parameter to ExitPlanTool, next to the plan.
- Failed. Asking for a plan and for questions about that plan in one call
  confused Claude. Open problem: if the answers contradict the plan, does
  Claude call ExitPlanTool a second time?
- (The post links the prompt-caching post for why ExitPlanTool exists.)

### Attempt 2: Changing output format

- Told Claude to emit a modified markdown format (bulleted questions with
  bracketed alternatives) that the UI would parse.
- Failed. Claude usually produced the format but not reliably: it appended
  extra sentences, dropped options, or abandoned the structure.

### Attempt 3: The AskUserQuestion tool

- A dedicated tool Claude can call at any time; plan mode prompts it
  especially.
- When called, a modal shows the questions and blocks the agent loop until
  the user answers. Terminal example: tabs for several topics plus Submit;
  each question offers several options plus "Type something" and "Chat about
  this".
- Benefits: structured output, a guaranteed set of multiple options, and
  composability (callable from the Agent SDK, referenceable from skills).
- Claude appeared to like calling the tool, and its outputs worked well. The
  author notes that even a well-designed tool fails if the model does not
  understand how to call it.
- The team does not expect this to be the final form; tools evolve as Claude
  improves.

### Updating with capabilities: tasks & todos

- At launch Claude needed a todo list. The TodoWrite tool created and updated
  todos and showed them to the user.
- Claude still lost track of goals, so the harness inserted system reminders
  every 5 turns.
- As models improved, the reminders became a constraint: Claude stuck to the
  list instead of revising it when circumstances changed. Opus 4.5 also got
  better at using subagents, which needed a way to coordinate.
- TodoWrite was replaced by the Task tool. Todos keep one model on track;
  tasks let agents communicate. Tasks carry dependencies, share updates across
  subagents, and the model can alter or delete them. A diagram ("From todos
  to tasks") shows a single-agent checklist becoming shared tasks with
  dependencies across Agent A and Agent B.
- Lesson: revisit tool assumptions as capabilities grow; tools built for older
  models can constrain newer ones. The team also recommends supporting a small
  set of models with similar capability profiles.

## Designing a search interface

- The most consequential tools are the ones that let Claude find its own
  context.
- An early internal version used RAG: a vector database pre-indexed the
  codebase and the harness retrieved snippets before each response. Drawbacks:
  indexing and setup cost, fragility across environments, and Claude was
  handed context instead of finding it.
- Replacement: a Grep tool, so Claude searches files and builds context
  itself.
- Agent Skills formalized progressive disclosure: a skill file can reference
  other files, which Claude reads recursively. A common use is adding search
  capability (instructions for calling an API or querying a database).
- Over about a year, Claude went from being unable to build its own context to
  nested search across several layers of files.
- Progressive disclosure is now a standard way to add capability without
  adding a tool.

## Progressive disclosure: the Claude Code Guide agent

- Claude Code has about 20 tools. The bar for adding one is high, because each
  tool is one more option the model must choose between.
- Problem: Claude did not know how to use Claude Code itself (for example, how
  to add an MCP server or what a slash command does).
- Putting all of that in the system prompt would add context rot for rarely
  needed information and distract from writing code.
- First attempt: give Claude a link to the docs to load and search. It worked,
  but Claude pulled large documentation chunks into context for answers that
  needed one sentence.
- Solution: the Claude Code Guide, a subagent Claude calls when a user asks
  about Claude Code. It searches the docs in its own context window, follows
  detailed instructions on what to search for and extract, and returns only
  the answer, keeping the main context clean.
- Caveat: Claude can still get confused when asked how to configure itself.
  The capability was nevertheless added without a new tool.

### Seeing like an agent is an art, not a science

- Tool design depends on the model, the agent's goal, and its environment.
- Advice: experiment often, read the outputs, try new things.

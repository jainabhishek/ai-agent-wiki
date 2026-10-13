# Maximizing the value of your Claude Code sessions — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/maximizing-the-value-of-your-claude-code-sessions
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-14
> Captured: 2026-10-12 via curl (condensed). The final section's four items are an image; transcribed from that figure.

Byline: Lydia Hallie. Category: Best practices. Product: Claude Code. Listed
reading time 4 min.

## TL;DR
- `/clear` between tasks so irrelevant prior context is not re-sent.
- Set model and effort before starting; changing either mid-conversation can
  break the prompt cache.
- @-mention files instead of naming them: the file is attached directly, saving
  a Read call (or a search).
- Add quiet flags to noisy commands, or run them in a subagent; command output
  stays in the conversation for the rest of the session.
- Run `/context` once in a fresh session to see what is loaded (`CLAUDE.md`, MCP
  tool definitions) and cut what is unnecessary.
- `/compact` before stepping away: the cache expires after an hour (subscription)
  and summarizing is much cheaper while the conversation is still cached.

## Maximizing value
- Agentic tools give each task a price, and the same task can cost different
  amounts depending on use (a direct read-edit-done session versus one that
  greps and reads a dozen files, all re-sent each turn).
- Efficiency means spending tokens on the thing asked for, not using fewer
  overall.

## What decides the price of a token
Billing is per token, but the cost is inference time. Three factors: model,
input vs output, and cached vs not.

### Model
- Larger models do more work per token; everything else is multiplied by model
  price. Use a larger model for hard or ambiguous problems and a smaller one for
  routine work. Points to "Choosing a Claude model and effort level in Claude
  Code".

### Input and output tokens
- Prefill reads input (system prompt, `CLAUDE.md`, message, accumulated files and
  command output). Decode writes output one token at a time (a 200-token reply is
  200 model runs), so output is priced roughly 5x input.
- Much output is thinking; the effort level controls it. `/effort` and `/model`
  persist as defaults into the next session — check them in a fresh session.
- Tip: `MAX_THINKING_TOKENS=0 claude` turns thinking off for one session
  (except on Fable 5), a step below `/effort low`.

### Prompt caching
- If a request starts with exactly the same tokens as a recent one, the server
  reuses the stored state and only prefills what follows.
- Cache read costs 0.1x input price; cache write costs more than normal input,
  up to 2x, paid once per token.
- Claude Code manages caching automatically on every request.
- Worked example, "fix the failing test in `utils.test.ts`": (1) system prompt
  with tools + `CLAUDE.md` + message, all prefilled and written to cache; (2)
  model Reads the test file, conversation re-sent, history read from cache;
  (3) Read the file under test; (4) Edit; (5) run `npm test`; (6) summary with no
  tool call ends the loop. Five requests for one fix; each turn is typically tens
  of thousands of tokens in, a few hundred out; only new content is prefilled at
  full price.
- Applies on subscriptions too: the same requests draw down limits.
- Request order: tool definitions, system prompt, conversation (with `CLAUDE.md`
  at its front). A change in the prefix re-prefills everything after it.
  Cache breakers:
  - `/model`: each model has its own cache; includes opusplan, which switches
    models when entering or leaving plan mode.
  - `/effort`: effort is part of the cache key; both commands ask for
    confirmation mid-conversation.
  - Fast mode: part of the key; re-prefill happens at fast-mode prices. Turn on
    at the start; turning off is free cache-wise.
  - `/compact`: replaces the conversation (system prompt survives); cheap to
    write while the old conversation is cached.
  - Time: cache expires after one hour on a subscription, five minutes on an API
    key (`ENABLE_PROMPT_CACHING_1H=1` makes it one hour). Resuming an old session
    almost always misses; the system prompt is rebuilt at launch anyway.
- Cheap moments to switch: session start or right after `/clear`.
- Tip: `/rewind` to before unwanted turns instead of `/compact`; rewinding only
  trims the end, so the rest stays cached at no cost.

## What decides how many tokens a session sends
- Everything in the conversation is re-sent on every later turn. Cost model:
  tokens in context × turns they stay × number of concurrent contexts.

### What ends up in the context
- Startup content: tool definitions, system prompt, `CLAUDE.md`. Tip: `/context`
  in a fresh session; keep `CLAUDE.md` specific, move workflow instructions to
  skills; disable unneeded MCP servers with `/mcp`.
- Most of the rest is tool results. Vague asks ("the tests are failing") cause
  greps and exploratory reads that linger. Naming the file saves the search;
  @-mentioning it also saves the Read call. Mention once per conversation; a
  repeat @-mention generally attaches a second copy.
- Command output: outputs over 30,000 characters are written to a file with a
  preview and path in context (`BASH_MAX_OUTPUT_LENGTH` changes this). The
  problem is output under the limit, such as 400 passing-test lines. Claude often
  adds flags or `tail`; a hook in the docs can rewrite noisy commands.
- Tip: put the two or three daily commands in `CLAUDE.md` with quiet flags
  (example given: `npx vitest run <file> --reporter=dot`).

### How many turns it stays there
- One long session costs more than the same work in short ones; turn 40
  re-reads 39 turns. `/clear` for a new task; `/compact` when an earlier phase of
  the same task is done.
- Tips: `/rename` before `/clear` to find a session later; tell `/compact` what
  to keep or add a "Compact instructions" section to `CLAUDE.md`; on a 1M model,
  `/autocompact 200k` restores the earlier auto-compact threshold (needs Claude
  Code v2.1.221+).
- `/loop` fires full turns in its session carrying the whole conversation, and
  misses the cache after an hour; run loops from a fresh session in another
  terminal.

### Subagents
- A subagent gets its own context (system prompt, tools, `CLAUDE.md`, not the
  conversation); only its answer returns.
- Cost: it may re-read what the main session had; overhead for small jobs. Pays
  off for jobs with much disposable output (log review). The main session only
  gets what the subagent chooses to report.
- Tip: for a repeated noisy job, define a subagent with `model: haiku` (or
  sonnet); otherwise it runs on the main session's model.

## Where to look first
Four things, roughly in order of cost (from the closing figure):
1. Long sessions — every turn re-sends everything before it; most tokens go here.
2. Too much in the context — unneeded files, noisy output, leftovers from the
   previous task, unused MCP servers; all re-sent and reasoned over every turn.
3. A bigger model or higher effort than the task needs — multiplies everything
   else; both settings persist between sessions (figure shows ×1 vs ×5).
4. Breaking the prompt cache — changing model, effort, or fast mode
   mid-conversation, or returning after expiry, re-prefills at full price
   (figure: cached ×0.1 vs re-prefilled ×1).

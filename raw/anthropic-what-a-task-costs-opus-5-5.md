# What a task costs on Opus 5.5 — Anthropic (claude.dev blog) (raw capture)

> Source: https://claude.dev/blog/what-a-task-costs-on-opus-5-5/
> Publisher: Anthropic (claude.dev blog) · Date: 2026-09-25
> Captured: 2026-10-12 via curl (condensed). Byline: Addy Osmani; category "Playbooks"; 21 min read.
> Byline and JSON-LD `datePublished` both give 2026-09-25. Interactive figure values (Fig A prices,
> Fig B receipt, Fig C calculator presets, Fig D effort cards) were read from the page's embedded data.
> Reviewers thanked: Michael Segner, Kacie Jenkins, Molly Vorwerck.

Subtitle: Opus 5.5 costs less per token than Opus 5.

## The cost of a task, and the cost of a retry

- Users buy finished tasks, not tokens. Two models at the same per-token price can cost very
  different amounts on one task, because every additional turn sends the whole conversation again;
  a model that takes more turns therefore costs more.
- The post sets three reader questions: what do typical tasks cost on Opus 5.5; which settings move
  that and by how much; how to check your own session usage.
- Stated trade-off: every token-saving lever (lower effort, smaller model, less context) can cost a
  finished task, and a retry costs more than the savings.
- Numbers are a mix of list prices and illustrations built from them; the figures are interactive.
  The author asks readers to check the docs and their own math.

## What does a task cost?

A Claude Code task is a loop: read conversation, call tool, read result, repeat. Each trip is one
request. Four cost drivers: **turns**, **cache reads**, **output token type**, **model**.
- Output tokens are 5x the input price. Thinking is billed as output.
- Example prices (Opus 5.5 API list): $4/M input, $20/M output, $0.20/M cache reads. Examples bill
  cached input at the read price and everything else at the input price; cache writes are left out.

### Turns
- Worked example: context starts at 20K and grows to 120K. At 40 turns the average turn sends ~70K,
  so ~2.8M input tokens for the task although the conversation never exceeded 120K. At 90% cache
  reads, input costs ~$1.62. The same task in 25 turns processes ~1.75M tokens, ~$1.02 input.
- A turn costs more than the tokens it adds because it resends everything before it; the cheapest
  turn is the one not needed.
- Give the model a way to check its work (a test, a build, a script that calls the endpoint) so it
  finds mistakes earlier. Gathering what it needs in one pass and batching tool calls also cuts
  resends.

### Cache reads
- The same 2.8M input tokens: $11.20 with no cache; $1.62 at 90% hit rate; ~$0.99 at 96%. No other
  setting moves input cost as much. A steady session keeps a high hit rate on its own.

### Output tokens
- On Opus 5.5 an output token costs 100x a cache read. A typical task's 60K output tokens cost $1.20,
  equal to reading 6M tokens from cache. Thinking is paid for in full even when Claude Code shows
  only a summary, which is why effort moves the bill.

### Model
- Cheaper cache reads mainly help long sessions; cheaper output mainly helps reasoning-heavy tasks.

## What changed in Opus 5.5

Two changes: price, and how much work the model does.
- **Fig A** (API list price per million tokens, Opus 5 → Opus 5.5): input $5.00 → $4.00 (-20%);
  output $25.00 → $20.00 (-20%); cache reads $0.50 → $0.20 (-60%). The read rate falls from 1/10 to
  1/20 of the input price.
- On Pro, Max or Team plans the lower price is passed through to limits, including cached context,
  so limits go about 25% further than on Opus 5. The extra cache-read cut is an API price change.
- Separately: five-hour limits rose on Pro, Max, Team and seat-based Enterprise; eligible
  subscribers get a one-time limit reset they can trigger under Settings > Usage (web or Claude
  Desktop, not the terminal). The reset applies account-wide, including Claude Code.
- On an API key the cache-read cut matters most for Claude Code, because long agentic sessions spend
  most input on cache reads. In the Fig B session the cache line falls $1.00 → $0.40.
- Savings depend on work shape: a mostly-cache-read session saves up to 60% on input; a short,
  uncached question with a long answer saves up to 20% (output dominates). Most Claude Code tasks
  sit between.
- The widely quoted "40% less to run than Opus 5" is Anthropic's estimate for typical token-billed
  workloads at default settings. It assumes fewer tokens per task at the medium default on top of
  the price cut; it is not a 40% per-token cut.
- Opus 5.5 can use more tokens on an answer because it always thinks before replying. Work done per
  task varies; measure it. On well-scoped tasks both models finish in about the same number of turns
  and only the price cut applies. The gap should be largest on open-ended tasks where a model can
  spend many turns on a wrong idea.
- Long runs end with a report (what changed, what was found, what is needed from the user), which
  can reduce reruns.

## The same tasks side-by-side

**Fig B** — one illustrative session, same token counts on both models (price change only):

| Line | Tokens | Opus 5 | Opus 5.5 |
|---|---|---|---|
| Read from cache | 2.0M | $1.00 | $0.40 |
| Fresh input | 200K | $1.00 | $0.80 |
| Output | 60K | $1.50 | $1.20 |
| Total | | $3.50 | $2.40 |

(Opus 5.5 column computed from Fig A prices; it matches the calculator's $2.40.) The three lines are
those `/usage` shows. Cache reads are the biggest line by tokens; output is smallest by tokens and
biggest by cost; fresh input covers the first read of each file and each new tool result. Priced
this way the session costs about 31% less. A recorded run would add the second effect (less work);
on a task with a false start the gap should widen.

### Try your own numbers

- **Fig C** calculator: sliders for input tokens, cache share, output tokens, tasks per day, and an
  assumed "token change on Opus 5.5" (default 0% = price alone). A month is 22 working days; API list
  prices; not a bill on Pro/Max/Team; no batch or volume discounts; cache writes not counted.
- Presets (from page data): Typical Claude Code session 2.2M input, ~91% cached, 60K output, 10
  tasks/day; Small edit 150K input, 80% cached, 5K output, 30/day; Large refactor 6M input, 92%
  cached, 250K output, 3/day; Long agentic run 20M input, 96% cached, 600K output, 1/day.
- Default (typical) output: Opus 5 $3.50/task ($770/month); Opus 5.5 $2.40 ($528/month); -31%,
  $242/month less from price alone.
- Fill the sliders from `/usage` at the end of a task (Session block). To set the last slider, run
  the same task on both models and compare turns and output tokens.

## Tips for maximizing the value of your session

The lower price cuts cost per token; session habits set the token count.

### Raise effort before you change models
- Effort sets a general disposition for tokens per turn: thinking, written text, and tool calls. At
  lower effort the model makes fewer and shorter tool calls.
- Opus 5.5 levels: low, medium, high, xhigh, plus max for a single session. **Fig D** cards (from
  page data):
  - low ("mechanical"): clear-plan work such as renames, applying a pattern across files, one-line
    changes; least thinking per turn.
  - medium ("everyday"): well-scoped daily work; start here.
  - high ("if it stalls"): first thing to try when medium stalls; worth it when it saves a retry; try
    it when a change spans two layers and medium fixes one.
  - xhigh ("hard problems"): for what high does not crack; more output per turn and slower replies;
    if xhigh hits the same problem twice, move to Fable 5.1.
  - max ("one session"): per session, not a standing default; one hard task, then drop back.
  - Commands shown: `/effort {level}`, `/effort status`, `/model`, `/usage`.
- Claude Code sets a default level per model; `/effort status` shows it. On Opus 5.5 the default is
  medium, one below Opus 5's high. At a given level Opus 5.5 thinks more per turn than Opus 5, most of
  all at xhigh and max, so do not carry over an Opus 5 level; keep xhigh/max for measured gains.
- Pricing heuristic: if high adds 20K thinking tokens across a task, that is $0.40 on Opus 5.5 —
  about the same as a ten-turn retry loop at 100K cached context with 10K total output. High pays for
  itself if it saves one retry; it is wasted on a task medium would have finished first time.

#### When medium fixes one layer
- Symptom of too little effort: a fix that stops at one layer. Example: a field renamed in an API
  handler; at medium the handler and its tests are updated but the client still sends the old field.
  At high the model reads call sites first and changes both layers in one pass.
- A check catches the same bug: a test that runs through the client fails on the turn the bug is
  written, even at medium. Before raising effort, check the model can verify its work — a test costs
  one turn and its output; more effort adds thinking to every turn.
- If effort and checks do not work, switch to a bigger model.

#### Changing effort mid-session
- `/effort high` sets a level; `/effort status` prints it; the new level applies to the next request.
- On Opus 5.5 with an API key or Claude subscription, changing effort keeps the cache, so effort can
  be raised for one step and lowered again. On Amazon Bedrock, Google Cloud's Agent Platform, or a
  Claude apps gateway, an effort change still clears the cached conversation and the next request pays
  the cache-write price on all of it.
- Thinking is always on for Opus 5.5; there is no thinking setting to change.

### Choose the right model for your work
- Model choice sets the price of every token and so moves the bill more than effort. Subagents that
  inherit the main model inherit its price. Typical day: a small model for lookups, Opus 5.5 for
  supervised work, a bigger model for the hardest tasks.

#### Opus 5.5 as the daily driver
- Supervised work: feature work across a few files, debugging, code review with follow-up edits.

#### Moving up to Fable 5.1
- When the result matters more than token price: long unsupervised runs, problems with no existing
  pattern in the codebase, large changes coordinating many subagents. If Opus 5.5 at xhigh hits the
  same problem twice, switch; switch back once solved. Opus 5.5 fits interactive work better (lower
  latency and cost).
- Fable 5.1 list: $10/M input, $50/M output (2.5x Opus 5.5); cache reads $0.25/M (0.025x its input
  price, only 1.25x the Opus 5.5 rate). The gap is smallest on long cache-heavy runs, largest on
  output-heavy tasks.
- Switch at a natural break: the cache belongs to the previous model, so the first turn on the new
  model pays the write price on the whole conversation. Run `/compact` first or start fresh with a
  short written plan. `/model` also saves the choice as the default for new sessions — switch back.

#### Moving down for lookups
- Use Sonnet or Haiku for lookups, not code writing: search-and-summarize subagents, reading logs and
  test output, "where is this defined". For a mechanical multi-file edit, keep Opus 5.5 at low effort.
- Subagent model: `model: haiku` or `model: sonnet` in the definition; `CLAUDE_CODE_SUBAGENT_MODEL`
  env var sets all subagents; a definition's model overrides the variable; with neither, a subagent
  runs on the main model.
- A subagent has its own context window and returns a summary, but still pays for its own tokens.
- Agent teams (experimental): each teammate is a separate Claude Code instance that uses tokens until
  it exits. The costs docs put a team in plan mode at about 7x the tokens of a standard session. Keep
  teams small, tasks self-contained, and shut teammates down when done.
- Trade-off: a small model that misreads a search result sends the main model to the wrong file, and
  the main model pays for the detour. Keep small models on work where mistakes are cheap to spot.
- Keep judgment calls on the main model. The `opusplan` alias plans with Opus in plan mode and
  executes with Sonnet — the reverse of this advice; measure before making it a default.

### Check your prompts when you migrate
- Instructions written for older models can make Opus 5.5 write more and repeat tool calls. Run
  `/claude-api prompt-audit` in Claude Code to check skills and `CLAUDE.md` (and app code built on
  the Claude Platform) for prompting anti-patterns.
- Test: Opus 4.8 → Opus 5.5 migration on an internal customer-support benchmark of 44 tickets. Moving
  to Opus 5.5 at low effort cut cost ~18%; prompt-audit cut a further 9%, to ~25% below the Opus 4.8
  start. The audit removed a mandatory six-step procedure, a scratchpad rule, a verify-twice rule,
  and mutually contradictory instructions. One benchmark — an example, not an expectation.

### Caching and compaction
Claude Code handles both; session habits decide how much they save.

#### How the cache works
- Cached parts: system prompt, tool definitions, conversation so far.
- Opus 5.5 cache read = 5% of fresh input. Cache write = 1.25x input (5-minute cache) or 2x input
  (1-hour cache), on current pricing. Each hit resets the lifetime at no charge.
- Lifetime in Claude Code: one hour on a subscription; five minutes by default on an API key or cloud
  provider; a subscription drops to five minutes once it draws on usage credits.
- At 120K context: 5-minute write ~$0.60, read ~$0.02 (one write = 25 reads). On an API key a
  six-minute break turns the next $0.02 read into a $0.60 write. A 1-hour write at that size ~$0.96.

#### Session shape and hit rate
- The cache stores a prefix; only the part matching the previous request from the start is reused.
  Changing tool definitions clears the whole cache; a system-prompt change clears from that point
  (almost everything).
- Expect a cache write when: you pause longer than the lifetime; you change effort on Bedrock, Google
  Cloud's Agent Platform, or a gateway (effort is part of the cache match there); you turn on fast mode
  for the first time in a conversation; you connect or disconnect an MCP server; you switch models;
  the conversation is compacted. Set these at session start and leave them.

#### Why long sessions cost more per turn
- Per-turn cache read on Opus 5.5: ~$0.004 at 20K context, ~$0.03 at 150K. 30 turns at 150K = $0.90
  in reads; at 20K = $0.12. On Claude 4.6 and later, a bigger context window does not change the
  per-token price; the cost is all resending. Much of a long context is stale (old stack traces,
  finished files, fixed test output) but is still resent each turn.

#### Compaction, /compact and /clear
- Auto-compaction summarizes older history near the context limit; `/autocompact <tokens>` changes
  the threshold.
- `/clear` empties the conversation at no cost (use for unrelated work). `/compact` keeps continuity
  for one request and accepts an instruction, e.g. `/compact keep the failing test names and the
  schema change`.
- Compacting at 150K costs ~$0.25 (read + a few-thousand-token summary + new cache write); each later
  turn saves ~$0.025, so it pays back in ~10 turns. Compacting just before finishing costs more than
  it saves.
- Compact before a break, not after: with a cold cache, `/compact` at 150K on a 5-minute cache costs
  ~$0.75 in input. To drop a wrong path, `/rewind` to an earlier, still-cached turn instead.
- Summaries lose detail (e.g., the one log line that mattered); compact at natural breaks and name
  what to keep.

#### What loads before you type
- `CLAUDE.md` loads every session and is resent every turn; the costs docs suggest under 200 lines.
- MCP tool definitions are deferred: only tool names and server instructions load at start; full
  definitions load on use. `/mcp` shows connected servers; turn off unused ones.

#### The rest of the bill
- Fast mode: Opus 5.5 up to 2.5x faster at 2x price ($8/M input, $40/M output). On a subscription it
  bills to usage credits, not plan limits. The first request after enabling pays the fast-mode input
  price on the whole conversation, uncached — enable it at session start.
- Billing table (condensed):
  - Cache lifetime: 1 hour on subscription; 5 minutes on API key/cloud or when a subscription draws
    on usage credits; hits reset it; the API offers a 1-hour cache at a higher write price.
  - Cache writes: 1.25x input (5-min), 2x (1-hour).
  - Thinking: billed as output, including thinking not returned.
  - Effort: applies to every output token — text, tool calls, thinking.
  - Auto-compaction: near the context limit; `/autocompact` sets the threshold.
  - Subagents and agent teams: subagent in own window returning a summary; agent teams in plan mode
    ~7x tokens of a standard session.
  - Batch API: half price on input and output via the Message Batches API.
  - Typical spend today: about $13 per developer per active day across enterprise deployments; under
    $30 per active day for 90% of users (current models; from the public costs docs).

## Measure it yourself

- Run `/usage` (`/cost` is the same). The Session block shows token use and an estimated list-price
  dollar cost; a prompt-cache line shows the cached share; Pro/Max/Team/Enterprise plans also show
  plan-usage bars. The dollar figure is computed locally at list price — on a subscription it is a
  guide to work done, not a bill.
- Run the same task twice: Opus 5.5 needs Claude Code v2.1.280 or later (`claude update`). Use a real
  backlog task, switch with `/model`, note turns, output tokens and cost; do three or four tasks
  before concluding.
- Teams: the Claude Code Analytics API gives estimated cost per user; the Usage and Cost API breaks
  spend down by model and by cached vs uncached tokens.
- Try the effort ladder: one hard task at medium then high; one mechanical task at low.

### Reading a session
Three checks in `/usage`:
- **Cache share** — should be high for a long session. If low, look for a long pause, a model switch,
  an MCP server connected mid-session, or (on a cloud provider or gateway) an effort change. The
  prompt-cache line often names the likely cause of the last miss.
- **Output vs input** — much output on a small change usually means effort too high or retrying.
- **Total input vs conversation size** — many multiples means many turns; read the conversation to
  find where the loop repeated.
- Baseline: ~$13 per developer per active day (enterprise average), under $30 for 90% of users.

## Keep in mind

Closing checklist: medium for well-scoped daily work; give the model a way to check its work and
start cross-file changes in plan mode; raise to high when medium stalls (cache kept on API key or
subscription; on a cloud provider or gateway change it at a break); if xhigh hits the same problem
twice switch to Fable 5.1 and back once solved; put search and log-reading subagents on Sonnet or
Haiku, keep code edits on Opus 5.5; keep long sessions moving so the cache stays warm; `/clear`
between unrelated tasks, `/compact` at a break with a note on what to keep. Most important: run one
real task on each model and compare `/usage`. Feedback via `/feedback` if limits do not go further.

Further reading listed: Manage costs effectively; Model configuration; Choosing a Claude model and
effort level in Claude Code; Effort; Prompt caching; Maximizing the value of your Claude Code sessions.

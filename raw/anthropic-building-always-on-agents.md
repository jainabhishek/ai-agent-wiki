# Building always-on agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/building-always-on-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-11-13
> Author: William Hu (acknowledgements: Rodrigo Olivares, Michael Segner)
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase, not a copy.

Page labels: Category Best practices · Product Claude Platform · Reading time 14 min.

Subtitle (paraphrased): always-on agents run with no end, choosing how and when to act across many sessions; the guide covers their core primitives and how they connect.

Intro:
- Anthropic reports renewed interest in always-on agents over recent months.
- Definition: stateful (they manage context across sessions) and proactive (they act without direct supervision). The core loop is the same as any agent. What differs is the surrounding architecture: primitives that control when the agent wakes, what carries between runs, and how results reach the user.
- Why now, per Anthropic: (1) newer models judge better — more reliable at reading user intent and knowing when to check in; (2) intelligence is getting cheaper, most of all for long-horizon tasks. Per solved task on a long-horizon coding benchmark, Opus 5.5 was 78% cheaper than Opus 5; on typical workloads the saving was 40%.
- Customers ask how to add this to their products: some want existing agents to be more proactive; some build from scratch.

## The cycle behind the always-on agent

"Always on" describes the user experience, not the runtime. The agent mostly sleeps and wakes periodically. Each stretch of work is a **run**: receive an event, do the task, save what happened. A run happens inside a **session** (the transcript of messages and tool calls). After the run the agent sleeps; the cycle repeats indefinitely.

## The core primitives

Five primitives: event inbox, timers, memory, permissions, outbox.

### Event inbox

- Most agents run only on a user message. Always-on agents also wake on webhooks, scheduled tasks, and background jobs.
- Letting each source call the agent directly fails: simultaneous events start competing runs, and a crash can drop an event.
- Fix: every source writes to an inbox; a worker picks events up. Minimal version, three components:
  - durable event storage, typically one database table;
  - a handler, typically an HTTP endpoint, that appends events to it;
  - a worker, typically a background service, that consumes them.
- Track status per event; dedupe on the source's unique IDs. A relational database fits, with one appended row per event. Start with one inbox per user; split further for more parallelism.
- Flow: handler writes the event and wakes the worker; worker reads pending events and starts a run. Events that continue earlier work (e.g. a user reply) resume the existing session; all others open a new session. Worker passes events to the agent loop, waits, marks them done.
- Best practices:
  - Handler acks fast — some sources (webhook providers) treat slow replies as failures. Light checks are fine; deeper checks such as prompt-injection screening belong in the run.
  - Inbox is the source of truth — on wake, the worker first pulls latest events from the inbox, so a replacement worker can retry the same event if one dies mid-run.
  - One active worker per inbox — prevents duplicate or overwriting runs. A mid-run event can be deferred to the next run, folded into the current run, or trigger interrupt-and-restart.
  - Batch pending events — several user messages in a row become one run and one reply.

### Timers

- Timers plus the inbox make the agent proactive. Two kinds: **follow-ups** (a deadline the agent sets itself, e.g. check on a reply) and **schedules** (recurring on a known cadence, e.g. a daily newsletter).
- Timers need a separate durable store, typically a second table, separate from the inbox; the inbox holds only work that is ready. Both kinds can share a schema, but a schedule also tracks recurrence.
- A timer does not start a run itself. Instead, a scheduler service checks the store on a fixed interval. Each pass it:
  - finds due timers;
  - updates each by kind — a follow-up is marked done; a schedule's due time moves to the next occurrence;
  - writes an event into the inbox and signals the worker.
- Build the scheduler yourself or use a durable execution engine.

### Memory

- Memory gives continuity across disjoint runs and has its own store. Claude Code's auto memory and the Messages API's memory tool implement it as a directory of files. For always-on agents, map that directory to durable storage (database or object store) so memories outlive the worker.
- Rule of thumb: store only what the agent cannot look up again. If it lives elsewhere (e.g. an issue tracker), store a pointer.
- Four memory types:
  - **User instructions** — behavior instructions from the user, in their own file, loaded every run, because the user is often absent.
  - **User notes** — what the agent learned about the user (role, preferences, corrections). One file at first, then several small files; then only an index loads each run, and the agent pulls files on demand.
  - **Past messages** — what the agent already told the user, to avoid repeats. Either a separate file loaded each run, or the worker loads the agent's last few messages.
  - **Task progress** — one progress file per ongoing task (done and remaining), so any new run can resume. Index-loaded like user notes.
- (The page shows a diagram of one example setup.)
- Beyond in-run saves: **dreaming** reviews past sessions to curate memory, replacing stale entries and finding patterns visible only across many runs. Anthropic's agent-memory post covers it.

#### Inside the context window

- Every run first loads system prompt, tool definitions, and memory files. This overhead recurs each run; keep it lean and use prompt caching.
- A new session starts with only that overhead plus the triggering events. An existing session also brings back messages and tool calls from earlier runs.
- If a session gets too long, compact older messages or start a new session. Both lose detail, so save anything that must persist to memory as you go.

### Permissions

Highest-risk area: a run holds the user's access and runs unattended. For each tool call the agent must proceed, block, or wait for approval. Same components as other agents:
- **Credential store** — always-on agents often need passwords or access tokens. Recommended: a proxy outside the agent's environment injects credentials into outgoing requests; the agent sends requests without them.
- **Auto mode** — as in Claude Code, classifiers review higher-risk actions and block those judged dangerous, so Claude finds a safer route. The most important decisions still need user review.
- **Deferred tool calls** — Claude Code lets a hook hold back a tool call until the user responds. For always-on agents: deferral ends the run and stores the session in the middle of the call; the user sees the request, for example as an interactive MCP Apps card; the answer returns as an inbox event that starts a new run resuming the saved session. Meanwhile the worker can handle other events, so the agent is not blocked.

### Outbox

- Most agents stream output so users can follow reasoning and tool calls. Always-on agents work mostly in the background; the user receives the result plus some details, not every step.
- A run ends in one of three ways: a message to the outbox; a decision that nothing needs sending; a deferred tool call asking for permission or input.
- Most agents can manage with a "send" tool that delivers straight to the user. A formal outbox is needed only to pace messages or recover from errors.
- The outbox mirrors the inbox: its own table, holding messages waiting to go out, with a dispatcher (usually a background service, mirror of the worker) that reads pending messages, decides what to deliver, and sends. A deferred-call request may go through the outbox or show directly in the interface.
- Tune message volume: too many is noise, too few misses things the user needs. Build evals to find the balance. Begin quiet, and let the agent win more user attention as it proves useful.

## How everything fits together

Each run starts with an inbox event (user message, webhook, or timer). Once the worker takes the event, it starts the agent in a fresh or resumed session. The agent reads memory for a baseline, acts within its permissions, updates memory, and on finishing pushes a row to the outbox; the dispatcher delivers it. A run can set a timer to wake the agent later, and a user reply returns as an inbox event. Runs are short; the cycle continues indefinitely, which is what makes the agent feel always on.

## Acknowledgements

Written by William Hu; thanks to Rodrigo Olivares and Michael Segner.

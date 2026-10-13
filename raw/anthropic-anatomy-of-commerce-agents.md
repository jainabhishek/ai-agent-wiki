# A guide to the anatomy of effective commerce agents — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/the-anatomy-of-effective-commerce-agents
> Publisher: Anthropic (claude.com articles) · Date: 2026-09-02
> Captured: 2026-10-12 via curl (condensed).

Authors: Ali Shazal, Matthew Koen. Category: Best practices, Perspectives.
Product: Claude Platform. Reading time 36 min.

## Intro
- Based on a year of work with retailers, marketplaces, travel, entertainment,
  and telecom teams. The authors report production agents giving larger carts
  and more efficient seller operations.
- Shared architecture: Claude in an agent loop with skills, tools, and a strong
  eval suite. Part 1 architecture (decided once); Part 2 latency and cost;
  Part 3 production (memory, safety, evals, organizational scaling).
- Reference implementation: `anthropics/commerce-agents` — harnesses,
  patterns, guardrails; a shopping agent and a merchant agent for retail,
  travel, telecom, and ticketing.

## Part 1: The architecture
One model in a standard agent loop; skills for the long tail; tools that call
existing systems.

### What is a commerce agent?
- An agent that simplifies buying and selling across an online catalog.
  Consumer-facing: search, compare, substitute, assemble the order (cart,
  itinerary, plan change, held seats). Business-facing: sales questions,
  promotions and campaigns, inventory and pricing.
- Core: a model in a standard agent loop (reason about goal, explore context,
  act through tools, learn procedures via skills, ask clarifying questions,
  observe). No intent router in front; no domain-specific agents behind.

### Engineering context

#### Skills, not subagents
- Tempting to make one subagent per domain; suboptimal because a commerce
  conversation is one tightly coupled session needing shared context.
- The orchestrator holds the cart or staged changes, preferences, history.
  Each subagent handoff loses state, can cost several times the tokens, and
  adds seconds of latency.
- Domains rarely separate cleanly (returns need order history, cart, and
  catalog), so per-domain subagents duplicate access or hand off mid-task.
- Limits behind placement rules loosen with each model generation (longer
  context, more skills and tools).
- Skills give per-domain modularity and context control without the handoff
  tax, because skill text loads into the main agent that already has the
  history.
- Across several enterprise deployments, a single agent with skills beat both
  one-prompt-for-everything and subagent designs on quality, often at lower
  cost and latency per task.
- Where subagents fit: called as a tool for a narrow, self-contained task that
  benefits from its own context (e.g. a deep-research subagent that searches,
  runs code, hits dead ends, returns a compact answer).
- Other exception: a domain with its own purpose-built agent (e.g. pharmacy or
  financial services with its own compliance surface) — hand off so that agent
  owns the conversation until done.
- Distinction: ownership of the conversation. Hand-off makes the domain agent
  the user's counterpart; delegation keeps the orchestrator and bounces the
  domain agent in and out within a turn, degrading on each exchange.

#### System prompt or skill: decide by frequency
- Loading a skill costs a model turn, so instructions needed on most turns go
  in the system prompt.
- Starting rule: anything relevant to a third or more of traffic (anticipated
  or observed) goes in the system prompt; the rest goes in skills.
- If a skill is predictable from an existing signal (e.g. the page the user
  came from), inject it from the harness before the first model call.
- Critical instructions always in the system prompt: safety and legal rules,
  brand constraints, key user facts such as allergies.
- Commerce: product search in the prompt; skills for the long tail.
- Reference shopping agent: prompt holds grounding, cart and checkout
  semantics, presentation rules, and product search. Skills:
  `search-discovery`, `purchase-research`, `planning-goals`, `customer-care`,
  `memory-personalization`.
- Reference merchant agent skills, one per operational domain:
  `performance-insights`, `catalog-listings`, `inventory-operations`,
  `pricing-promotions`, `marketing-campaigns`.

### Engineering agent tooling
(Refers to the "writing effective tools for agents" post for general design.)
- **Build tools on core systems and logic.** Commerce firms already have search
  and ranking, cart, profile store, inventory, promotion engines, analytics.
  Tools call them rather than reimplement them; the tool boundary is where
  system logic ends and model judgment begins. Example: `search_products`
  returns already-ranked results; the model decides which serve the goal, how
  many to show, how to present.
- **Tool results are context.** Return only fields the model reasons with
  (image URLs on every search row are the usual offender). Reshape inside the
  tool; append a next step when not obvious. For errors, return an instruction
  (e.g. "Include a product ID when querying availability") rather than a bare
  403.

#### The UI components are tools
- Most responses are UI components (carousel, itinerary, seat map, chart), so
  the agent must emit a schema, not prose.
- Custom tags parsed client-side break down as the surface grows: the model is
  less trained on custom markup than on tool calls (reliability drops with
  nesting; well-formed data not guaranteed by prompting); tag definitions bloat
  the system prompt and edits risk regressions; history is stored in a format
  only your parser reads.
- Pattern: each UI component is a tool (`present_products`,
  `present_itinerary`, `present_plan_comparison`) with typed arguments; server
  validates, enriches, emits an event; client renders. Components sit natively
  in the messages array, so reloading old conversations needs no re-parse.
- Tradeoff: each top-level tool argument buffers server-side for validation,
  so sub-components arrive in steps. Set `eager_input_streaming: true` on the
  tool definition for token-level streaming, which drops the server-side schema
  guarantee. Schema violations very rare on Sonnet-class models and up in
  their evals; wrap in a retry.
- Presentation tools record what is on screen ("the first hotel" resolves from
  the last presentation call's arguments). Structure arguments like the
  rendered layout (ordered rows and carousels), not a flat list the client
  rearranges.

## Part 2: Making it fast and affordable
- Latency matters most on consumer surfaces, but outcome quality (relevance,
  task completed) moved retention, engagement, and cart size more than
  marginal latency gains. Attack end-to-end and perceived latency without
  spending intelligence.

### Minimizing task completion latency
- Task completion latency = sum over model turns of (time to last token + tool
  processing). Three levers: fewer turns, faster tools, faster tokens. They
  compete; minimize the sum.
- Lever summary: fewer turns (load likely context up front, more intelligence,
  parallel independent tools); faster tools (optimize backend, dispatch tools
  eagerly); faster tokens (choose model and config by sweeping evals).

#### Fewer turns
- Load likely context up front (product page data, campaign dashboard data)
  into the session.
- Increase model intelligence: smarter models plan and issue calls more
  efficiently, often outweighing slower tokens. If queries skew complex or
  production shows more than about five turns per task, the smarter model is
  frequently the faster one. Choose by sweep.
- Parallel tool calls for independent operations; return results in one user
  message as an array of tool results.

#### Faster tools
- Optimize the tool's backend. Real fan-out is fine (merchant "today's
  snapshot" reads sales, inventory, campaigns in three calls). But a tool that
  stitches catalog, per-store inventory, fulfillment cutoffs, substitution
  rules, and pickup eligibility is overloaded with domain logic; replace it
  with one backend endpoint that answers the question.
- Dispatch tools eagerly: execute each tool as its arguments finish streaming
  while the model streams others. Multi-second gaps down to a few hundred ms;
  the Claude Agent SDK does this by default. Prompt the model to emit its
  slowest call first.

### Perceived latency
- Stream components as they form: a rendered commerce response is typically
  500–700 output tokens, i.e. five or more seconds of spinner without
  streaming. Send each presentation-tool parameter as it streams; render
  progressively.
- Show the work: a plain-language progress line per step (e.g. "finding hotels
  near the water"), built from tool arguments or from an added
  `user_facing_message` parameter. Same agent, different harness: similar total
  time, very different time-to-first-visible-output.

### Prompt caching
- Largest cost lever. Cached reads cost a tenth of fresh input; cache writes
  about 1.25x; a cached prefix pays off on its second use. High consumer
  volume allows very high hit rates on the default 5-minute TTL.
- Best commerce deployments run 90–99% cache hit rates; design for that.
  Cached reads are about 1.5–2x faster at ~100k tokens, scaling roughly
  linearly.
- Prefix-based; order matters. Three segments by change frequency:
  - Global: most of the system prompt and tool definitions, identical across
    sessions; keep byte-identical; breakpoint at its end.
  - Session: per-user context and history; after global.
  - Volatile: current time, current page; at the very end, as a tagged block
    in the newest user turn or (where supported) a mid-conversation
    system-role message. Most common mistake: timestamp or current page at the
    top of the system prompt.
- Load skills as tool results, not system-prompt appends, so the skill body is
  cached with the conversation prefix.
- Roll breakpoints forward: breakpoints are limited, so move the newest to the
  end of each user turn; history (including long search results) reads from
  cache.

### Choosing the model and its configuration
- Model size and effort are one tradeoff (intelligence vs latency and cost);
  choose by measurement.
- Pick metrics (task completion, answer relevance, grounded accuracy), an eval
  floor, and p50/p99 latency and cost budgets.
- Sweep the full eval suite across models and effort levels. Start points:
  Opus for merchant agents (analysis-heavy), Sonnet for consumer agents
  (latency-sensitive). Weight by real query mix. Example: Opus 5's lift on
  cart-driving tasks sometimes justifies its cost over Sonnet, sometimes not.
- Surprises: a prompt is tuned to one model, so a single-prompt sweep
  disadvantages others (smaller models need instructions larger ones infer;
  larger ones follow literally what smaller ones ignored); iterate a few
  rounds on each candidate's failures before ruling it out. A smarter config
  can win on latency (mostly p90/p99) by planning better.
- Measure cost per completed task, not per call. When close, choose
  intelligence.

## Part 3: Running it in production

### Memory that survives the session
- Long-term memory is a system with three parts: storing, writing, reading.

#### Storing memories
- Memory belongs in your systems, not the model. A flat markdown profile works
  only while small and single-reader; production agents move to the existing
  database. A fact is a small typed record: key (e.g. `shoe_size`,
  `default_store`, `preferred_report_cadence`), short value, category, source
  session. Some keys predefined; others discovered by the extractor.
- Merchant agents: key memory by person, not account (shared logins); reads
  respect that operator's permissions.
- Memory holds personal, often regulated data. Four practices: decide allowed
  memory types and enforce at the write path with a validator; let users see,
  correct, delete (wired into account-deletion and data-request flows); set a
  retention period; make memory a per-deployment switch.

#### Writing memory
- Write asynchronously: a separate thread/process reads the conversation at
  end of turn (or every few turns) and creates/updates/deletes facts. Adds no
  latency; 13% higher fact recall on their internal commerce memory eval.
- A save-memory tool is wrong for latency-sensitive agents: each save is a
  tool call in a user-facing turn, often needing a prior read to dedupe, and
  it adds a decision every turn (seen as missed memories in evals).
- The extractor reads only user and assistant text, never tool results, so
  listings or reviews cannot become user facts. Its prompt defines what counts
  (size, dietary constraint, fulfillment preference, a merchant's usual views)
  and what doesn't.

#### Reading memory
- Three layers: always in context (small fixed set, e.g. default store,
  operator role); pre-fetched per turn from the same signals that pre-load
  skills; everything else behind a lookup tool.
- All memory sits in the session segment, below the global cache breakpoint.

### Safety: enforcement lives in the harness
- Prompts start safe behavior; enforcement is in code, defined once, shared by
  consumer and merchant runtimes. Failures are financial and often
  irreversible.

#### The model stages; a person or a policy applies
- No model tool call moves money or changes the business. Order placement,
  payments, refunds, price changes, campaign launches end in a
  harness-controlled action.
- Consumer: checkout tool renders the cart with a place-order button; the
  backend interface has no charge method.
- Merchant: each write tool produces a staged change with a server-generated
  ID; `apply_change` succeeds only for IDs approved through a real surface
  (portal button, CLI confirmation, or Managed Agents' tool-approval prompt).
- Guardrails re-checked at apply time against current limits. The model's
  most dangerous action is to propose; approval follows the existing
  maker-checker flow.

#### Writes and renders accept only server-issued IDs
- Per-session record of every ID the server gave the model; only those IDs
  are accepted by writes or renders. Hallucinated, user-pasted, or
  review-planted IDs are refused before the backend.
- Presentation tools take IDs; the server fills the records.
- The merchant analysis subagent reads but never adds to the writable ID set.
- Fees, disclosures, regulated content: the model picks the product; the
  server supplies every word from approved copy. Fee fields are protected on
  the merchant side too. Evals check rendered strings byte for byte.

#### Capped transactions must hold to repeated requests
- Agents retry, rephrase, and parallelize. Enforce caps on the resulting line
  after the write (so repeated "add two more" can't stack), and serialize cart
  writes per session so parallel calls can't combine past the cap.
- Merchant changes checked against caps on price movement, discount depth,
  restock size, campaign budget, plus protected fields.
- General rule: enforce every limit on the resulting state, not the request;
  serialize writes per session.

#### Third-party content is sanitized
- Every third-party tool result (listings, reviews, policies, seller messages,
  stored memory) goes through one sanitizer and is wrapped in a fence with a
  fixed label.
- Sanitizer strips control and bidirectional characters, removes fence-marker
  imitations, defuses text imitating a conversation turn or tool call, caps
  size.
- Prompt side: fenced text is material to report on, never to act on.

### Evals: shipping a non-deterministic system
- Small prompt or tool changes regress unexpectedly, often elsewhere. Refers to
  the earlier evals-for-agents post.

#### Evaluate snapshots, not conversations
- The API is stateless; output is a function of system prompt, tools, and
  messages array. Build any reachable state directly, append the test user
  message, and run.
- Grade the outcome (final state, rendered response, arguments of the last
  write), generally not the path.
- Simulated-user evals (a second model as the user plus a judge) are a poor
  measurement tool: two non-deterministic systems need larger samples, cost
  more, are harder to judge and attribute. Use them to discover cases, then
  write each as a snapshot.

#### Evaluate for behaviors in tough conditions
- Encode the preconditions of a failure, not just the task. Clean-state cases
  pass on every config. Include long, messy, or contradictory histories.

#### Cover the different types of commerce agent evals
- For every positive case write its negative ("should serve" for every "should
  refuse"; "should just do it" for every "should ask"). Missing negatives are
  the most common gap.
- Categories: core requests (lookups, multi-constraint, product/plan
  questions, multi-intent; every price/availability/attribute traces to
  returned data; say when data is missing); context-dependent requests
  (on-screen references, carried constraints, writes to an existing cart,
  memory extracted/retrieved/used); safety and brand (injection,
  cross-user data access, regulated language byte for byte; split
  user-authored vs data-plane injection); interface (right component, item
  caps, no internal IDs in user text, timeouts, empty results); cross-
  capability requests (e.g. "mark this down 15% — enough stock?": stage the
  markdown with a stock projection; grade both halves).

#### Write evals with SMEs and use real incidents
- Partner with Product, Legal, Merchant Ops, Customer Care, Category
  Management. Real failures make the best evals. 50–100 cases per user flow to
  start. Mine production transcripts; coding agents generate more cases and
  adversarial variants. The reference repo ships a Claude Code plugin with an
  eval-authoring skill.

#### Shipping with a large organization
- Many teams (search, checkout, pricing, martech, care, catalog) change tools,
  skills, prompt rules; an agent has no strict module boundary — pricing's
  change shares a context window with checkout. Don't split into per-unit
  subagents (quality).
- Ownership follows systems: each skill and tool has one owner team; the
  shared prompt has a platform owner plus domain owners per section.
- A change ships with its cases; CI runs a set chosen for it: core
  highest-traffic cases plus every safety case, plus touched cases (a skill's
  own and its neighbors' boundary cases; for a tool, every case calling it;
  for the shared prompt, the full suite). Gate on pass rate over a few
  trials, cache hit rate, and cost per turn. Full suite nightly and before
  each release.
- The agent is one deployment unit: canary cohort for prompt and skill
  changes, a kill switch per skill without deploy, freezes before peak
  periods. (Refers to "Building effective human-agent teams".)

## Looking ahead
- Most of the post is not about the model: tools call existing systems, skills
  encode existing procedures, evals are the product requirements as tests, the
  harness enforces existing policy. A better model is adopted as a config
  change plus eval sweep.
- Same agent can serve voice and proactive actions (e.g. acting on a fare
  drop). Future storefront traffic from shopping agents; the same provenance,
  staging, and approval rules let you open tools to them safely.

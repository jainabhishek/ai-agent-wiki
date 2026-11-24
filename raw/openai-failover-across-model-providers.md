# Designing failover across OpenAI model providers — OpenAI developer blog (raw capture)

> Source: https://developers.openai.com/blog/designing-failover-across-openai-model-providers
> Publisher: OpenAI (developer blog) · Date: 2026-10-14 (byline "Oct 14, 2026")
> Authors: Oliver Steffmann, Vik Bomma
> Captured: 2026-11-24 via curl of developers.openai.com/blog/llms-full.txt
> (markdown export); authors and date read from the article HTML.
> Condensed paraphrase, not a copy. Headings, numbers, and identifiers are kept;
> prose, the decision table, and the Codex prompt are summarized.

## Intro

When a business relies on an AI workflow, even a brief outage at the model
provider can stall decisions or break a service. OpenAI works with financial-services customers
on agentic applications and cybersecurity workflows. The post describes how
OpenAI approaches production routing and recovery for critical workloads. The
running example is a **read-only fraud assessment** in a payments workflow.

Terms: **first-party (1P)** = calling the OpenAI API directly. **Third-party (3P)** =
OpenAI models accessed through a cloud provider, wherever the application runs.

## Why use both routes?

- Direct access is useful even when production runs through a cloud provider.
  A main reason is **preview models and features**: eligible teams can evaluate
  them on the direct API before their cloud provider supports them.
- Where the workflow runs often decides the production route. A 3P service may
  fit existing infrastructure and controls; 1P may fit another workflow better.
  Validate models, features, and behavior on the chosen route. Availability
  depends on provider, endpoint, region, and account.
- **Provider failover** = sending the request again to a different approved
  provider because the primary failed to serve it. It is useful only when
  repeating the request is safe and the secondary satisfies the workflow.
- Example: a payments company calls the **Responses API** for a
  self-contained, read-only fraud assessment. On a timeout, while nothing has
  consumed the result yet, the app can send it again to a validated secondary,
  as long as the transaction deadline allows.
- An ongoing **Agents API** session is different. Switching provider does not
  resume its conversation and saved work or reconcile earlier actions. The post
  calls that recovery much harder and puts it out of scope.
- Hence the framing: multi-provider support is a **platform capability**;
  failover is a **workflow decision**.

## Planned routing and failover

- Picking the production route is one decision; approving failover is
  another. Planned routing (splitting traffic, spilling overflow to a second
  route) has to pass its own tests for capacity, cost, quality, and recovery.
- Some customers use the **Decisions API** as an optional routing input. Define
  how routing behaves if that service is down.
- In the figures 1P is primary and an approved 3P route is the secondary; the
  roles can be reversed per workload.

## Where the router fits

- Figure 1 (described): the application sends requests to a platform-operated
  router that applies workflow-defined policy. Normal traffic goes to the
  primary; only recovery traffic that qualifies goes to the approved secondary. If
  neither route qualifies, the workflow either waits in a queue, runs in a
  reduced mode, passes to a human, or refuses. Recovery state, checking which
  actions completed, checkpoints, and guarding against repeated actions are the
  application's job.
- An existing model router or LLM gateway works if it can enforce separate
  rules per route. Use the tested secondary only when failover conditions hold.
- Write down who may use each route, where (regions), and with which models and
  APIs; list the approved legal entities, teams, provider accounts or projects,
  and data-handling rules. An approval is valid only for the workloads and
  regions it names.

## Private connectivity and route choice

- Regulated customers often must use private network paths, so picking a route
  also means checking how their cloud reaches each provider privately.
- Figure 2 (described): app and gateway in a customer private network, with a
  separate private path to each provider (for example **Amazon Bedrock** or
  **Azure OpenAI** as 3P). Going over public HTTPS is a distinct choice that is
  never switched on implicitly.
- 1P: **OpenAI Private Link** is built on an Azure Private Endpoint, so an AWS or
  Google Cloud workload must bring its own network link into Azure to use it.
- 3P: Amazon Bedrock uses API-specific interface VPC endpoints through AWS
  PrivateLink; Azure OpenAI uses Azure private endpoints.
- Check DNS, access, and which models and APIs each region offers, on both
  routes, before turning failover on. OpenAI Private Link does **not** move
  traffic between regional endpoints by itself; recovering to another region is
  its own setup and test. Dropping to public HTTPS needs an explicit sign-off.
- Provider support can change; check official documentation.

## Which operations can fail over?

Some operations have no secondary that fits:
- **Missing capabilities.** Example: the workflow uses web search on the direct
  API. If the secondary lacks it, do not silently skip the search; validate an
  alternative or keep failover off for that operation.
- **Unvalidated behavior.** The same model name or an API that looks compatible
  proves nothing; first run the workflow's own harness and evals on the secondary.
- **Residency or state constraints.** Never move to a destination that would
  break data-location rules or that lacks the state the operation needs.

If nothing qualifies, the options are: hold the work until an agreed deadline,
fall back to an approved reduced or manual path, or halt cleanly. A single
inference step can be eligible even when the whole workflow is not. The timed-out
fraud assessment is retryable only while its result is unused and time is left. After
output has flowed into another system, a tested restart procedure is needed; when
an action might already have happened, check what happened and block repeats
before restarting.

## When and how to fail over

- **Model fallback** = replacing a busy or unavailable model with another
  approved model. **Provider failover** = retrying through another provider.
  Sometimes both change.
- Ask first whether a provider switch would fix anything: a component both
  routes share (gateway, retrieval, identity) can take both down.
- A **circuit breaker** can pause new requests to a failing route. Set error and
  latency limits per provider, model, region, and workflow. Each request still
  has to qualify for failover.
- Before a retry: the request must be safe to repeat and able to finish within
  the deadline; the secondary must be approved, enabled, healthy, load-tested,
  and have budget left. Consult OpenAI's error-code and rate-limit docs, and the
  other provider's error, retry, quota, and billing rules.

Decision table (paraphrased; "a conservative starting point for automatic
failover"; use provider error details, not only the HTTP status):

| Condition | Routing decision |
| --- | --- |
| Short-lived service or network fault | Failover is an option for retryable errors, dropped connections, and timeouts. |
| Throttling or slowness that persists | Failover is an option when waiting would blow the request or workflow deadline; separate passing throttling from quota or billing issues. |
| Bad request, auth failure, refusal, or used-up allowance | No automatic route switch for malformed input, 401/403, safety refusals, or exhausted quota, credits, or spend; fix the cause or escalate. An error that is not classified must never cause failover. |
| Partial output or a tool action of unknown outcome | No blind replay, and no continuing a partial answer on the other route; first settle what happened and block duplicate writes. |
| One model unavailable or out of capacity | Switch to another approved model that meets quality, feature, and latency needs; consider provider failover only if the provider's shared serving path is hit. |

- **Exactly one layer owns retries** (not app, SDK, and gateway each), so retry
  counts do not compound. Share one retry budget; follow valid `Retry-After`; otherwise
  bounded exponential backoff with jitter. Retry only safe inference calls within
  both request and workflow deadlines.
- Limit how much traffic fails over so the secondary is not swamped. Move traffic
  back to the primary step by step once sample requests stay within error and
  latency limits for a set time, and halt the move if limits break. When both
  routes are struggling, apply the pre-agreed recovery policy.

## Implement the failover policy with Codex

- Use Codex to change an existing LLM gateway, limited to the read-only
  fraud-assessment step. The primary stays; failover stays **disabled by
  default** until the secondary is approved and validated.
- The post gives a Codex prompt (summarized, not reproduced). It asks Codex to:
  inspect gateway/SDK/adapter versions, config, and current docs; split app and
  gateway changes by owner; flag unsupported controls; not guess approvals or
  limits; use tested provider-specific error mappings; allow only transient
  failures and confirmed temporary throttling when replay is safe and the
  secondary qualifies; block invalid requests, access failures, refusals,
  exhausted quota, unknown errors, and ambiguous 429s; use one retry controller
  with one total attempt limit, per-attempt timeouts, and both deadlines; accept
  one result per logical request and ignore late responses; include manual
  disable, circuit breaking, and gradual failback; test with local HTTP stubs and
  external networking blocked, asserting route order, call counts, and elapsed
  time, with blocked cases making no secondary call; make no live calls or
  deployments unless authorized; hand back small patches, tests tied to each
  requirement, rollback steps, and the live checks still pending.
- A human reviews the patch and local test results; only after behavior, data
  controls, capacity, and recovery are proven under load is failover switched on.

## Validate routes and recovery

- Run both routes against the workflow's acceptance criteria (quality, safety,
  output format, tool use, context limits). Write down what configuration was
  tested, what access and availability it needs (processing tiers, hosted
  features), and the retest trigger.
- Data restrictions (including prompt and output logging limits) apply in
  normal operation and in recovery. Go through credentials, network paths,
  retrieval, tools, stored state, and logs together with the legal, privacy,
  security, and data-governance owners. Endpoint location or a private connection alone does
  not settle where data is processed, stored, retained, encrypted, or who holds
  keys; check contracts and OpenAI's data controls.
- A provider-wide dashboard can hide throttling on one model. Track request and
  token rates, concurrency, throttling, latency, and remaining budget per route,
  model, account or project, and region.
- Load-test the secondary with its existing work plus expected failover traffic
  and retries; use results to set the failover traffic limit. Quota alone does
  not guarantee completion before the deadline.
- Compare cost per successful assessment (cache misses, data transfer,
  connectivity) and added latency from cache misses or cross-cloud requests.
- Test every table scenario under load, plus missing features and a busy or
  down secondary; confirm traffic limits, manual stop, and gradual return.
- Measure recovery by time to restore service, assessments finished before
  deadline, result quality, cost, and duplicate actions. Repeat exercises as
  credentials expire, configs change, or capacity shifts.

## Who owns recovery

- One model: a **platform team** runs provider integrations, the router,
  monitoring, and audit logs; owns production readiness; enforces destination,
  identity, data, traffic, and spend controls; has named on-call owners to
  disable routes and manage return to primary.
- **Application owners** define which operations can fail over, service and
  quality targets, and what reduced mode is acceptable. Business results,
  stored recovery state, tool permissions, checks on responses, and protection
  against repeated actions (also across shared state or tools) are theirs.
- Teams may split roles differently; agree before enabling failover who approves
  controls, owns route tests and runbooks, and can act during an incident.

## Conclusion

Direct OpenAI access belongs in the toolbox: it lets teams try preview models
and features and can serve as a recovery route. Pick 1P or 3P per workflow by
capability, hosting, and controls. For a critical workload, begin with a single
self-contained, read-only inference step; Codex can implement the gateway
policy and local tests, and validation on the real routes decides whether the
secondary qualifies.

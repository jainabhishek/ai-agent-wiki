# Claude models explained: choosing the best model for your use case — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/claude-models-explained-choosing-the-best-model-for-your-use-case
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-24
> Captured: 2026-10-12 via curl (condensed). A chart of illustrative
> quality/cost curves (not benchmark data, per its caption) was not captured.

Author: Michael Segner. Category: Best practices. Products: Claude Code, Claude
Cowork, Claude Design, Claude Enterprise, Claude Platform. Reading time 8 min.

## Our advice: start smart
- Frequent question: which model for a workload; more nuanced as classes and
  versions multiplied.
- Default recommendation: start with the most intelligent generally available
  model and use effort level to tune performance and cost.
- Cost per task is often lower for more intelligent models, especially at
  lower effort, despite higher per-token price, because they take fewer turns
  and less thinking. Starting small makes it harder to tell model failures
  from setup failures.
- For latency- or cost-sensitive cases, test lower tiers until the fit is
  found. Some organizations start with the cheapest model and move up until
  the quality bar is met; the docs on model selection cover both directions.

## The Claude model family
- Lineup: Fable, Opus, Sonnet, Haiku (plus Mythos), each balancing
  intelligence, speed, cost.

### Mythos / Fable
- Mythos: most capable class; frontier across domains; strong at coding,
  long-running agent tasks, previously unsolved problems.
- One underlying model in two packages: Claude Mythos for trusted
  organizations doing dual-use cybersecurity and biology work; Claude Fable
  with additional safeguards for general public use. Both require limited
  data retention.

### Opus
- Class for reasoning-intensive enterprise tasks; ranks among leaders on
  GDPval-AA (knowledge work) and Terminal-Bench 2.1 (agentic coding).
- Opus vs Fable: similar benchmark scores, but larger models like Fable tend to
  show more wisdom, creativity, and writing skill in real use.
- Rule of thumb: if evals show Opus struggling, use Fable; if Opus clears the
  bar, its speed and price may make it the better choice.

### Sonnet
- Versatile everyday class; balance of performance, cost, speed; includes
  high-volume subagents in multi-agent orchestration.

### Haiku
- Lowest cost, fastest; for high-frequency, latency- and cost-sensitive work.

## How to choose which Claude model is best for your workload
- Classes do not specialize by domain (no finance model vs science model);
  all are trained for coding, agentic tasks, knowledge work. The difference is
  how hard a problem each can reliably carry and its price and speed.
- Questions:
  - How hard is the task? Long, multi-step, or previously unsolved → more
    capable class.
  - Latency needs? High-frequency customer-facing → Sonnet often best.
  - Access constraints? Mythos only for organizations under Project Glasswing;
    not all organizations expose all classes to all roles.
  - Unit economics? High volumes may suit lower classes if evals show
    satisfactory completion; price per task depends on capability and effort.
- Effort level also shifts quality, speed, cost. Higher class at higher effort
  gives best performance; higher class at lower effort can sometimes be more
  efficient than a smaller model.
- Refers to "Choosing a Claude model and effort level in Claude Code".

## Combining models’ strengths with the advisor strategy
- Faster, cheaper worker models call a more intelligent model to check plans
  and evaluate work; the executor is coached only when needed.
- Figure: on SWE-bench Pro, Sonnet 5 with a Fable 5 advisor scores within 10%
  of Fable 5 at 63% of the price of running Fable 5 for the whole task.

## How evals and benchmarks help with model choice
- Benchmarks: predefined tasks with known solutions; directional across
  classes and providers. Problem: Opus and Fable saturate many benchmarks.
- Then use real workloads or custom evals: curated production problems,
  including hard tasks where current tools fail, with team-defined success
  criteria. This is where frontier models separate.

## Making the smart choice
- No one-size-fits-all. Understand each class and the use case; build,
  maintain, and deploy strong evaluations.

# Uber's CISO on building an insider threat program for AI — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/uber-s-ciso-on-building-an-insider-threat-program-for-ai
> Publisher: Anthropic (claude.com articles) · Date: 2026-10-13 (page byline)
> Author: no byline (Anthropic interview). Interviewee: Philip Martin, Chief Information Security Officer, Uber.
> Captured: 2026-11-24 via curl (HTML stripped to text). Condensed paraphrase of an interview; questions kept as headings; answers paraphrased.

Page metadata: Category Perspectives; reading time 7 min. Subtitle: Martin discusses why AI agents need monitoring and observability, and how Uber pairs its open-source tooling with Enterprise Frontier Safeguards.

## Introduction

- Uber runs a large real-time marketplace: over **40 million** trips and delivery orders a day. Martin's team protects Uber's data and its riders, drivers, and couriers.
- The team began using Claude for threat modeling before Claude Code launched, and then had to collect context manually. With Claude Fable, Claude now collects that context on its own from code, design docs, and ticket history.
- Martin's thesis: companies should monitor AI agents with an insider threat program, like the one they already run for staff. Topics: accidental misuse, and how Uber's open-source monitoring tools work with Enterprise Frontier Safeguards.

## How are frontier models changing your security team's work?

- Martin: the main change versus earlier models: frontier models take in much more context over long horizons and so produce very specific outputs.
- For security reviews and threat modeling of a service, the model can consume the code, design documents, Jira issues, and history on what the service should do and what it talks to.
- Martin expects teams of agents: each service could have its own agent that knows it well, and those agents could discuss threat models with each other the way the services talk in production (each one stating its threat model and data sources). He sees that as the next step up in efficacy.

## Uber worked with our team Enterprise Frontier Safeguards. Why was this important for Uber?

- Martin: both companies focus hard on safety in different senses: Uber on rider safety and personal data; Anthropic on preventing misuse of frontier models. Uber must protect customer data, trade secrets, and other proprietary information.
- Enterprise Frontier Safeguards strikes the balance for Uber: safeguards are active, but Anthropic cannot access Uber's data without Uber's permission.
- It gives Uber control of its data, of risk mitigation, and of the actions taken after a safeguard triggers. Martin calls this a shared responsibility for safe, effective model use.
- Anthropic incorporated Uber's design feedback and put Uber "in the driver's seat".

## How does Enterprise Frontier Safeguards fit with the safety monitoring you already run on AI deployments Uber?

- Uber has recently open-sourced **AI Detection and Response (ADR)**: it gathers real-time telemetry and takes real-time action in the agent harnesses Uber deploys.
- ADR complements Anthropic's safeguards: Uber combines its own view with output from Anthropic's classifier, feeding both into its detection environment, like a traditional cybersecurity setup. Goal: assemble context to decide as fast and as certainly as possible.
- Martin expects Enterprise Frontier Safeguards to become a data source for ADR. Together with Uber's **LLM gateway** (a perimeter that controls how AI is used inside Uber), these make up the AI security architecture Uber runs.

## Where do you think defenders should prioritize their focus next when it comes to securing AI systems?

Martin names two priorities.

1. **Real-time detection and intervention**, as close as possible to the person typing a prompt into a harness — e.g. warning that they probably do not want to do that, or that the tool call or destination the model is about to use is probably unwanted.
2. **Understanding emerging patterns**: watch trends in model behavior, discover new behaviors (often with LLM help), and build safeguards for them back into the real-time platform. This repeats, because constraints create new behaviors, which must then be found too.

## What would you tell other leaders who are hesitant about the monitoring frontier models require?

- Martin: adopting AI is unavoidable for business, with real benefits, but also real potential for harm; stakes rise as models gain capability and autonomy.
- Every company already runs an insider threat program for its people without dispute, accepting onerous retention and unwelcome monitoring, because humans sometimes act outside their role.
- Frontier models bring the same risk: they may be directed to act outside expected constraints. An insider threat program for models will be essential to safe rollout.
- Link: learn more about Enterprise Frontier Safeguards.

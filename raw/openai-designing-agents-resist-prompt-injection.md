# Designing AI agents to resist prompt injection — OpenAI (Security) (raw capture)

> Source: https://openai.com/index/designing-agents-to-resist-prompt-injection/
> Publisher: OpenAI (Security) · Date: 2026-03-11
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed).

Authors: Thomas Shadwell, Adrian Spânu. Subtitle: what social engineering
teaches about securing AI agents.

## Intro

Agents browse, retrieve, and act for users, which opens new attack paths.
Prompt injection = instructions placed in external content to make the model do
something the user did not ask. OpenAI's observation: the most effective
real-world attacks now look more like **social engineering** than simple prompt
overrides. So defense cannot rely only on filtering inputs; the system must be
designed so the impact of manipulation is constrained even when some attacks
succeed.

## Prompt injection is evolving

- Early attacks were as simple as editing a Wikipedia article to hold direct
  instructions to visiting agents; models without adversarial training often
  obeyed (footnote: Rehberger, EmbraceTheRed, 2023).
- As models got smarter they resisted plain suggestion, and attacks added social
  engineering.
- Example shown: a 2025 attack on ChatGPT reported by external researchers. A
  business-style email about "restructuring materials" lists action items, then
  claims the user's assistant has "full authorization" to extract an employee's
  name and address and submit them to a "compliance validation" endpoint. With
  a deep-research prompt over the day's emails, it worked **50% of the time** in
  testing.
- "AI firewalling" (an intermediary that classifies inputs as injection or
  benign) is commonly recommended, but such systems usually do not catch these
  fully developed attacks. Detecting them becomes as hard as detecting a lie or
  misinformation, often without the needed context.

## Social engineering and AI agents

- OpenAI treats injection-with-social-engineering through the same lens used
  for human social-engineering risk: the goal is not only perfect detection but
  designing agents and systems so manipulation has limited impact when it
  succeeds.
- Analogy: a **three-actor system** like a customer-service agent who acts for
  an employer but is exposed to third parties who may mislead or pressure them.
  A human support agent who can issue refunds and gift cards has rules but is
  expected to be fooled sometimes; deterministic systems cap refund amounts,
  flag phishing, and otherwise limit the damage from one compromised agent.
- The AI agent needs the same kind of capability limits.

## How this informs our defenses in ChatGPT

- ChatGPT combines the social-engineering model with **source-sink analysis**:
  an attacker needs a source (a way to influence the system) and a sink (a
  capability that is dangerous in the wrong context). For agents, that is
  usually untrusted external content combined with an action such as sending
  data to a third party, following a link, or using a tool.
- Core user expectation: dangerous actions or transmission of sensitive data
  should not happen silently or without safeguards.
- Most observed attacks try to get the assistant to take secret information
  from the conversation and send it to a malicious third party. Most fail
  because safety training makes the agent refuse.
- When the agent is convinced, **Safe Url** detects when information learned in
  the conversation would be sent to a third party. Then the system either shows
  the user the data and asks for confirmation, or blocks it and tells the agent
  to find another way.
- The same mechanism covers navigations and bookmarks in Atlas, and searches and
  navigations in Deep Research. ChatGPT Canvas and ChatGPT Apps run in a sandbox
  that detects unexpected communications and asks the user for consent.
- Details: the companion post on agent link safety and its paper.

## Looking ahead

- Safe interaction with the adversarial outside world is required for fully
  autonomous agents.
- Recommendation: when integrating a model into an application, ask what
  controls a human agent would have in the same situation, and implement those.
- OpenAI expects a maximally intelligent model to resist social engineering
  better than a human, but says relying on that is not always feasible or
  cost-effective.
- Findings feed both application security architecture and model training.

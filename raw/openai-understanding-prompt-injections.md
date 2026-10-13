# Understanding prompt injections: a frontier security challenge — OpenAI (Security) (raw capture)

> Source: https://openai.com/index/prompt-injections/
> Publisher: OpenAI (Security) · Date: 2025-11-07
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed).

No individual author shown. Tag on page: Security.

## Intro

AI tools now browse, research, plan trips, and buy products, and can access
data in other apps. Prompt injection is a security challenge OpenAI is heavily
focused on.

## What is a prompt injection?

- A social-engineering attack specific to conversational AI. Conversations now
  include content from many sources; a third party (neither user nor AI) can
  inject malicious instructions into the context.
- Like phishing for humans: it tries to trick the AI into doing something the
  user did not ask.
- Example: vacation research meets hidden instructions in a listing comment or
  review, aiming to make the AI recommend the wrong listing or steal card data.
- Risk grows with access to sensitive data, more initiative, and longer tasks.
- Summary table:
  - Apartment research: an injected listing makes the AI recommend it against
    the user's criteria.
  - "Respond to my overnight emails": an attacker email with misinformation
    gets the agent to find bank statements in the inbox and share them.

## Our approach to protecting users

Multi-layered; aim is to complete the user's intended task even under active
attack.

### Safety training

- Robustness to adversarial attacks is a long-standing open ML problem.
- **Instruction Hierarchy** research works toward models that tell trusted from
  untrusted instructions.
- New training approaches to recognize injection patterns and ignore or flag
  them; automated red-teaming generates novel attacks.

### Monitoring

- Multiple automated AI-powered monitors identify and block injection attacks.
  They complement training because they can be updated rapidly for new attacks,
  and can catch adversarial injection research on OpenAI's platform before it is
  deployed.

### Security protections

- Overlapping, per-product protections. Examples: users approve certain links
  in ChatGPT before visit, especially sites that ask not to be catalogued; when
  the AI runs programs or code (Canvas, Codex), **sandboxing** prevents harmful
  changes caused by an injection.

### Give users control

- Atlas **logged-out mode**: the agent starts tasks without site sign-ins.
- ChatGPT agent pauses for confirmation before sensitive steps such as a
  purchase.
- **Watch Mode** on sensitive sites: alerts the user and requires the tab to be
  active; the agent pauses if the user moves away.

### Red-teaming

- Internal and external teams; thousands of hours focused on prompt injection.

### Bug bounty

- Rewards for good-faith researchers who show a realistic attack path leading to
  unintended user-data exposure.

### Let users decide

- When connecting apps, ChatGPT explains what data may be accessed, how used,
  and risks. Organizations control which features users can enable in their
  workspaces.

## Steps you can take to stay safer

Compared to computer viruses in the early 2000s: everyone needs to understand
the threat.

### Use built in features to limit access to sensitive data

Give the agent only the sensitive data or credentials the task needs (for
research, use logged-out mode).

### When an agent asks for confirmation, carefully review that it is about to do the right thing

Check consequential actions (purchases, emails) and the data being shared.
On sensitive sites such as a bank, watch the agent work, compared to keeping
hands on the wheel of a self-driving car.

### When possible, give an agent explicit instructions

Broad instructions ("review my emails and take whatever action is needed") make
it easier for hidden content to mislead the model, even with sensitive-action
checks. Specific tasks make attacks harder but not impossible.

### Stay informed and follow security best practices

Follow updates from OpenAI and other trusted sources.

## Looking ahead

- Prompt injection remains a frontier research problem; work is ongoing.
- OpenAI says it has not yet seen significant adoption of the technique by
  attackers, but expects heavy adversary investment.
- Announces a coming report on detecting whether the AI's internet traffic
  would transmit conversation information (capture note, an inference: the
  2026-01-28 link-safety post appears to be that report).
- Goal: as safe as working with a trustworthy, security-savvy colleague.

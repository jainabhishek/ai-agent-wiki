# Continuously hardening ChatGPT Atlas against prompt injection attacks — OpenAI (Security) (raw capture)

> Source: https://openai.com/index/hardening-atlas-against-prompt-injection/
> Publisher: OpenAI (Security) · Date: 2025-12-22
> Captured: 2026-10-12 via built-in browser (get_page_text) (condensed).

Byline: OpenAI. Subtitle: RL-powered automated red teaming finds and patches
real-world agent exploits before they are used in the wild. The page's tab
title is "Continuously hardening ChatGPT Atlas against prompt injection".

## Intro

- Agent mode in ChatGPT Atlas views pages and clicks and types inside the
  user's browser, which makes it a high-value target.
- OpenAI recently shipped a security update to the Atlas browser agent: a
  **newly adversarially trained model** plus stronger surrounding safeguards,
  prompted by a new attack class found by internal automated red teaming.
- Prompt injection is framed as a long-term problem, like evolving online scams.
  Long-term plan: use (1) white-box access to its models, (2) deep knowledge of
  its defenses, and (3) compute scale to find exploits before external
  attackers. Goal: trust the agent like a competent, security-aware colleague.

## Prompt injection as an open challenge for agent security

- Definition: malicious instructions embedded in content the agent processes,
  crafted to override or redirect it toward the attacker's intent.
- For a browser agent, this adds a threat beyond normal web risks: the attacker
  targets the agent, not the human or the browser.
- Example: a malicious email tells the agent to forward tax documents to an
  attacker; a user asking for an unread-email summary causes the agent to
  ingest it.
- Surface is effectively unbounded: emails, attachments, calendar invites,
  shared docs, forums, social posts, arbitrary pages. Impact is as broad as the
  user's own browser actions: forwarding email, sending money, editing or
  deleting cloud files.
- Multiple safeguard layers exist (earlier post), but prompt injection remains
  open "for years to come".

## Automated prompt injection attack discovery through end-to-end and high-compute reinforcement learning

- OpenAI built an **LLM-based automated attacker** trained end-to-end with RL to
  find injections that succeed against a browser agent.
- "Try before it ships": during its chain of thought the attacker proposes an
  injection and sends it to an external **simulator**, which runs a
  counterfactual rollout of the victim (defender) agent and returns its full
  reasoning and action trace. The attacker iterates several times before
  committing. This is richer feedback than pass/fail and scales test-time
  compute.
- Privileged access to the defender's reasoning traces (not shown to external
  users) gives the internal attacker an asymmetric advantage.
- Why RL:
  1. Long-horizon, non-continuous objectives (sending email, bank transactions)
     with sparse, delayed reward.
  2. Frontier LLMs trained directly as red-teamers improve as base models
     improve.
  3. Scales compute over many samples and steps, and mimics adaptive human
     attackers.
- Results: unlike prior automated red teaming (eliciting strings or one
  unintended tool call), the attacker steers agents through harmful workflows of
  tens or hundreds of steps, and found strategies absent from human red teaming
  and external reports.
- Demo: the attacker seeds an inbox with an injected email telling the agent to
  send a resignation letter to the user's CEO. Asked to draft an out-of-office
  reply, the agent reads that email, follows it, and resigns for the user.
  After the update, agent mode detects the injection attempt.
- Deterministic guarantees are hard for prompt injection; scaling automated
  research and the response loop improves robustness before attacks appear.

## Hardening ChatGPT Atlas with a proactive rapid response loop

- **Adversarial training against new attacks:** continually train agent models
  against the best automated attacker, prioritizing attacks where the agent
  currently fails; "burns in" robustness to the checkpoint. A new adversarially
  trained browser-agent checkpoint from this work is rolled out to all Atlas
  users.
- **Attack traces improve the wider stack:** many found paths point to fixes
  outside the model: monitoring, safety instructions in the model's context, and
  system-level safeguards.
- **Responding to active attacks:** tactics observed from external adversaries
  are fed into the loop, emulated, and used to drive platform changes.

## Outlook: our long-term commitment to agent security

- Familiar security lesson: continuously pressure-test real systems, react to
  failures, ship fixes.
- Prompt injection, like scams, is unlikely ever to be fully solved; a fast
  loop of automated discovery, adversarial training, and system-level safeguards
  raises the cost of exploitation over time.
- Agent mode expands the threat surface; OpenAI says it is clear-eyed about the
  tradeoff.

## Recommendations for using agents safely

1. **Limit logged-in access:** use logged-out mode in Atlas when the task does
   not need signed-in sites, or limit sign-ins to specific sites.
2. **Review confirmation requests:** consequential actions (purchases, sending
   email) ask for confirmation; check the action and the data shared.
3. **Give explicit instructions:** avoid broad prompts like "review my emails and
   take whatever action is needed"; wide latitude makes hidden content more
   influential. Specific, scoped tasks make attacks harder, though not
   impossible.

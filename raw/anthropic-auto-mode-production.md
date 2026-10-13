# Running auto mode in production — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/auto-mode-in-production
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-07
> Captured: 2026-10-12 via WebFetch (condensed); the 9x and 2,425 figures re-checked against the page HTML via curl.

Author: Molly Vorwerck. Category: Best practices. Product: Claude Code. Reading
time 10 min. "Related articles" shows 2026-10-05 to 2026-10-08 (other articles).

## Intro (no heading)

- Auto mode is now the Claude Code default. A classifier reviews each action and
  blocks those that look harmful, instead of asking the user to approve every
  command.
- Framing: reviewing every command slows long or parallel sessions; skipping
  checks lets prompt injection, scope drift, and destructive actions through.
- Internal evals: the classifier caught more dangerous actions than developers
  clicking through prompts; it held up under third-party red-teaming.
- Claim: Claude works 9x longer between interruptions than under the previous
  default, across all Claude Code usage. (No method or baseline given.)

## Powering longer running autonomous agents at Nuro

- Nuro (physical AI, Level 4 autonomous driving) adopted Claude Code in late
  2025; by March it was the company's most popular agentic coding tool.
- Staff engineer Kai Zhou first built a prototype hook: each pending action went
  to a small model; about 90% of routine actions were auto-approved; sensitive
  ones went to Slack for human review.
- He now uses auto mode for 100% of his coding work, often 3–4 sessions in
  parallel. He switches to interactive mode for work that affects other teams,
  such as reviewing pull requests.
- Guardrails: skills, plus deny rules in settings for dangerous commands such as
  recursive deletes.
- Long-running research agents hill-climb the eval metrics behind Nuro's driving
  stack; one overnight run (10 p.m. to 5 a.m.) produced three PRs. Another team
  uses the same approach to shrink a binary's memory footprint.

## Shipping PRs faster and safer at Gusto

- Gusto (SMB technology) adopted auto mode as a proactive security upgrade.
  Martin Emde (AI Dev Tools): less permission fatigue, control kept.
- Martin has run 2,425 Claude Code sessions since December, auto mode daily.
  Cross-repo work and unattended jobs (for example compiling daily notes from
  GitHub, Slack, and Jira) run without interruption.
- About 10% of session transcripts since mid-May 2026 included an auto mode
  denial.
- Chad Kunsman (AIT Cloud Engineering) works in roughly twenty-minute bursts
  (endpoint investigations, log audits, connector management); values prompt
  injection protection and the check that actions match the request.
- For production infrastructure (Terraform, AWS, direct POST calls to live APIs)
  he switches to accept-edits mode and verifies each tool call by hand.
- Gusto routes MCP traffic through a governed proxy with tool guards and prompt
  inspection, so agents have scoped permissions before auto mode applies.

## Accelerating the SDLC at Garner Health

- Garner Health (healthcare technology) rolled out Claude Code in February to
  all 550 employees, connected to Salesforce, Zendesk, and Snowflake; employees
  are encouraged to spend about two hours a week automating repeatable work.
- Before auto mode: hand-curated approved-command lists and rejected piped
  commands. Evan Magnussen (platform engineering manager): most colleagues now
  use auto mode in every session.
- Garner built a standardized SDLC plugin of skills: agents explore context,
  commit context files, run "antagonistic research" against their own
  assumptions, then implement, pausing for humans only when needed.
- One customization: auto mode does not approve actions that communicate with
  other people (Slack messages, emails).
- Teams working on core intellectual property tuned the classifier's injected
  prompts to be more or less permissive.
- Advice: build controls and telemetry, and use standard workflows, before
  scaling.

## Closing (no heading)

Links to configuration docs at code.claude.com/docs/en/auto-mode-config.

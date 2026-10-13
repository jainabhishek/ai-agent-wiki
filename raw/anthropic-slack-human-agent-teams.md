# Turning conversation into knowledge: how Slack builds human-agent teams — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/turning-conversation-into-knowledge-how-slack-builds-human-agent-teams
> Publisher: Anthropic (claude.com articles) · Date: 2026-08-19
> Captured: 2026-10-12 via curl (condensed).

Interview-style article with Jaime DeLanghe, Chief Product Officer at Slack.
Categories: Best practices, Perspectives. Reading time 10 min. Second post in
Anthropic's series on building human-agent teams (the first covered
multiplayer AI inside Anthropic).

## Intro

- DeLanghe joined Slack in 2017 to work on search and machine learning. Her
  mission: turn workplace conversation into institutional knowledge.
- Her view: people should work in the open, in channels anyone in the company
  can read and search. Her essay "The Work is the Conversation" applies the same
  argument to agents: the conversation around the work is the context agents
  need.

## Treat your conversation history like a knowledge base

- Early Slack research showed conversation did not turn into knowledge by
  itself; people kept repeating themselves. Making sense of the conversation
  "exhaust" was not humanly feasible; the article says it is now an agent's job.
- Practices:
  - Default to public channels. Agents learn only from what they can see;
    decisions in DMs or private threads stay invisible to them.
  - Ask agents to reconstruct *why* something was decided and how context has
    shifted since, not only *what* was decided.
  - Connect more surfaces (meetings, email, calendars, document repositories) so
    the team repeats itself less.

## Learn when to hand off tasks between agents and humans

- Core rhythm: a cycle of handoffs. Agents (Claude in Slack) do production work
  — drafting, summarizing, monitoring, preparing — and pass results to a person.
  The person reviews, decides, redirects, and hands work back.
- Example: DeLanghe's Monday starts with an agent-built daily briefing; also
  waiting are a recap of last week's product workshops with flagged
  escalations, a web report on AI developments, briefings for the day's
  meetings, and a rewritten bio. Humans review and decide at the end of each loop.
- Practices:
  - Start the day with agent-built briefings (recaps, escalations, meeting prep,
    web roundups), with human review.
  - Anchor work in a shared channel so humans and agents triage together; humans
    lead prioritization.
  - Make lightweight signals actionable: in her channel an emoji reaction adds an
    item to a list and an agent picks up the task.

## Delegate clear roles for agents

- A fleet of specialized agents can feel disorienting with a one-on-one chatbot
  mental model. Her framing is social: treat agents like coworkers with roles
  and focus areas.
- If an agent's value feels mandated rather than felt, people forget what it is
  for.
- Practices:
  - Route routine transactional tasks (filing a help desk ticket, pulling last
    week's metrics into a status update) to a general agent instead of asking
    people to remember a specialized tool.
  - If people cannot say what an agent is for, consider retiring it.

## Default shared channels to public; go private on purpose

- Slack has recommended public-by-default channels since its early days.
  Keep channels public unless there is a specific reason to gate context.
- Open context compounds: new hires onboard into history; agents benefit and
  their working memory flows back to humans.
- Practices:
  - Keep business-as-usual work (non-sensitive projects, announcements, Q&A)
    public so agent coworkers gain the knowledge they need.
  - Agents read what the team reads; a private channel is a blind spot for every
    agent that reports on it.
  - Let psychological safety set the line. Once sensitive material is walled
    off, the main reason work moves to DMs is discomfort with being seen
    mid-process; she argues trust is gained by giving trust.

## Spread adoption by showing the art of the possible

- At Salesforce, a public company-wide channel "How I Slackbot" (thousands of
  members by her count) shares skills, debugging tips, and workflow tricks; a
  trick from sales can reshape an engineering process.
- Inside Slack, the push to get PMs using Claude self-organized: one PM got help
  from the developer-experience lead, wrote a canvas on what he did and how,
  other PMs copied the format, teams ran workshops and built their own git repos.
- Practices: stand up a company-wide show-and-tell channel; encourage short
  "what I did and how" write-ups that become team templates or skills.

## Measure outcomes, not activity

- More messages may mean people cannot find things or cannot say what they mean
  the first time; message count is not productivity.
- Token usage shows "the lights are on" but is not sufficient proof of value.
- Practices: treat usage metrics as a pulse check, not proof of value; expect to
  use judgment — linking usage to business results still takes "leaps of faith"
  in her words.

## Change how you work, together

- Advice: reimagine workflows rather than doing the same work faster; she calls
  it a team sport.
- Start soon but small: put a group in a shared channel with Claude, give them
  the same resources, and let them work; Slack's experience suggests it spreads.

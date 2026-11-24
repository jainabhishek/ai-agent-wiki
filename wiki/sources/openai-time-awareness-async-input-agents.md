---
title: "OpenAI: Time awareness and async input for personal agents"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Kevin Whinnery (OpenAI)
date: 2026-11-20
source_url: https://developers.openai.com/blog/time-awareness-and-async-input-for-personal-agents
source_path: raw/openai-time-awareness-async-input-agents.md
tags: [openai, agents-api, responses-api, personal-agents, deadlines, async-tools, human-in-the-loop, time-awareness]
---

# OpenAI: Time awareness and async input for personal agents

> OpenAI Developers blog tutorial on a personal agent that must deliver by a
> deadline: it asks the user a question, keeps working while the question is
> open, and still delivers if the user never answers.

## Summary

The post builds a meeting-preparation agent. The user has a meeting in 15
minutes and wants a briefing with three minutes left to read it. The agent does
not know if the meeting is technical or commercial, so it asks. The post shows
how the agent keeps researching while the question is open, uses a reply if one
arrives, and writes for both cases if no reply arrives.

Two features carry the design. **Time awareness** is an experimental
[[openai-agents-api]] setting that gives the model periodic reminders of the
current time. **Async function tools** let the model keep working while the
application waits for the user's answer. The post then shows the same design in
a hand-coded Responses API loop, where the application itself must inject the
time before every request.

The post is mostly code in six languages. The code samples use the model ID
`gpt-6.2-astra`. The post does not say that time awareness or async tools are
limited to that model, so this page does not carry `models:` scoping.

## Key points

### The pattern
- The deadline lets the model trade depth for delivery. Near the deadline the
  agent favors checking its strongest findings and writing over a new line of
  research. A longer timeline tells the model that it can research more deeply.
- The application, not the model, turns phrases such as "in 15 minutes" into
  absolute timestamps. The model and the application then share one set of
  times.
- The application owns three clocks: a reply cutoff for open questions (minute
  10), a delivery deadline for the briefing (minute 12), and the meeting time
  (minute 15). The reply cutoff comes before delivery so that the agent has
  time to write without the answer.
- An unanswered question gets an explicit result, `{"status":"no_answer"}`,
  not silence. An answered question gets `status` `answered` plus `answer`.
- At the deadline, the application delivers the latest completed briefing, or
  reports that no verified findings are ready.

### Agents API version
- Agent config: `experimental.time_awareness: true`, the built-in `web_search`
  tool in `live` mode, and a function tool `request_user_input_async` with
  `async: true` and parameters `question` (required) and `choices`.
- The instructions tell the agent to ask for clarification when it would
  materially improve the result, to keep making progress while a reply is
  pending, and to state important uncertainties.
- Questions arrive as `agent.session.turn.item.done` events that carry a
  `function_call` item. The post warns that the session's `required_actions`
  list holds only blocking actions, so an application that waits on it can miss
  an async question.
- The application saves `turn_id` and `call_id`, shows each question once, and
  returns the answer as an `agent.session.input.tool_result` event. It keeps
  reading the stream while it sends the result.
- On `agent.session.turn.completed`, the application reads the turn items and
  takes the completed message whose `phase` is `final_answer`. If the stream
  closes early, it lists the session's turns to recover saved work.

### Responses API version (hand-coded loop)
- One request helper appends a developer message with the current UTC time
  after the input or tool results, before every request. The instructions,
  tools, and original deadline stay unchanged.
- Results for questions from an earlier response go into the next request with
  the latest `previous_response_id`. Requests stay sequential.
- When no answer is ready and the briefing is not done, the loop continues with
  a developer message that tells the model to keep working while replies are
  pending.
- An application timer wraps the whole loop, including in-flight requests and
  stream reading. At the deadline the application stops the request, delivers
  the saved briefing, cancels open input handlers, and deletes the stored
  responses.

## Entities

[[openai]], [[openai-agents-api]]

## Concepts

[[agent-harness]], [[human-agent-teams]], [[tool-design]],
[[context-engineering]], [[agent-steering]], [[guardrails]]

## Notable claims & data

- OpenAI says ChatGPT and other agent harnesses use this ask-and-keep-working
  pattern. No metrics are given; the post is a tutorial.
- Time awareness is "experimental" (config key `experimental.time_awareness`).
  The bash samples send `OpenAI-Beta: agents=v1`.
- The code uses `gpt-6.2-astra`, a model ID that no other page in this wiki
  names yet.

## Connections

- Extends the async tool calling feature listed in
  [[openai-prompting-gpt-6-astra]] and [[openai-agents-api-guide]] with a full
  deadline-driven example.
- The Responses version appends the time as a new message instead of editing
  the system prompt. This matches the "updates as messages" cache rule in
  [[context-engineering]] and [[anthropic-prompt-caching-is-everything]].
- The application-owned deadline timer is a harness invariant in the sense of
  [[agent-harness]]: the model is told the time, but the code enforces it.
- [[agent-steering]] cites [[anthropic-spending-your-effort]]: without a user in
  the loop, higher effort stands in for a clarifying question. This post shows
  the middle case, where a user exists but may not answer in time.

## Contradictions / open questions

- `gpt-6.2-astra` is not on any model-scoped page in this wiki. If OpenAI now
  lists it as current, pages scoped to `gpt-6-astra` may need a legacy check.
  Not verified on 2026-11-24.
- The post does not say whether time awareness works with every model on the
  Agents API, or how often the reminders arrive.

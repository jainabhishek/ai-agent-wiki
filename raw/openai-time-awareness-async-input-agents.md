# Time awareness and async input for personal agents — OpenAI (Developers blog) (raw capture)

> Source: https://developers.openai.com/blog/time-awareness-and-async-input-for-personal-agents
> Publisher: OpenAI (Developers blog) · Date: 2026-11-20
> Author: Kevin Whinnery (byline in the HTML page)
> Captured: 2026-11-24 via curl of developers.openai.com/blog/llms-full.txt (markdown export); the author byline comes from the HTML page. Condensed and paraphrased.
> Note: the post is mostly code, in TypeScript, Python, Go, Java, Ruby, and bash (curl). This capture describes the design and names the functions, events, and fields. It does not copy the code. The code samples use the model ID `gpt-6.2-astra`.

## (Intro)

- Setting: a personal agent, which the post compares to a ChatGPT "dot" (link to learn.chatgpt.com/docs/dots), often has to deliver a result by a deadline.
- Scenario: the author has a meeting with a prospective customer in 15 minutes. He asks the agent to research the company and prepare a briefing, leaving him three minutes to read it.
- The agent sees that the user did not say whether the meeting is a technical evaluation or a pricing discussion. That choice changes what to research and what to put in the briefing.
- The agent asks. The questions the post poses: how the agent uses the time while it waits, how it uses a reply if one arrives, and how it still delivers something useful if no reply comes.

## Time awareness and async input

- **Time awareness** is described as a recent addition to the Agents API. It gives the model periodic reminders of the current time, so the model can fit its work to the deadline.
- **Async function tools** let the agent keep working while the application waits for the end user's answer.
- With 15 minutes to the meeting, the agent has 12 minutes for the briefing. Near the deadline, the agent can favor checking its strongest findings and writing, over opening a new line of research. A longer timeline tells the model it can research more deeply.
- The user's request sets the deadline in plain words; time awareness keeps the model informed while searches and user input are pending.
- Illustration (paraphrased): the agent researches the example company "Pied Piper" and asks the user if the meeting will be commercial or technical. An answer narrows the briefing. If none arrives, the question lapses at 4:10 and the briefing covers both cases. It delivers at 4:12, three minutes before the 4:15 meeting. The user asks at 4:00 p.m. UTC.

## Create the agent

- The agent needs web search, an asynchronous tool to ask the user for input, and time awareness.
- Configuration through the SDK's agent creation method (`client.beta.agents.create` in Python):
  - `experimental.time_awareness` set to `true`.
  - Built-in `web_search` tool in `live` mode.
  - A function tool named `request_user_input_async` with `async` set to `true`. Its parameters: `question` (string, required) and `choices` (array of strings); `additionalProperties` is false.
- Example values: agent `name` "Personal assistant"; `model` `gpt-6.2-astra`.
- The example instructions (paraphrased): act as a personal assistant; give useful, well-sourced answers inside the user's time limits; ask for clarification when it would materially improve the result; keep making progress while a reply is pending; state important uncertainties.
- Prerequisites: `OPENAI_API_KEY` from a project with Agents API access; an official SDK; permissions from the Agents API quickstart. The bash sample sends the header `OpenAI-Beta: agents=v1`.

## Start a task with a deadline

- Start a session with the SDK's session creation method (`client.beta.agents.sessions.create`) and stream updates.
- The request gives the company, the meeting time, and the briefing deadline. It leaves the agent to decide what to research and whether to ask.
- The application must convert relative phrases ("in 15 minutes", "three minutes left to review") into absolute timestamps, so the model and the application share the same time data. The sample computes the meeting time as now + 15 minutes and the delivery time as now + 12 minutes, in ISO format.
- Sample session arguments: `agent_id`, `environment` of type `none`, `input` (the request text with both timestamps), `stream` true, and a `timeout` of 12 × 60 seconds.

## Display a pending question

- When the agent asks about the meeting's focus, the application shows the question while research continues. A separate task collects the reply, so the application keeps receiving the agent's updates.
- The application code collects the input; the model only asks through the tool call.
- Watch the session event stream for `agent.session.turn.item.done` events that contain a `request_user_input_async` function call. Read the question and choices from `item.arguments`.
- Warning: the session's `required_actions` list describes blocking actions. Waiting for an entry there can miss an asynchronous question.
- Save the session ID plus the call's `turn_id` and `call_id`. Track pending questions so each is shown and handled once. Cancel input handlers when the agent's run ends.
- The sample event: `type` `agent.session.turn.item.done`; `item.type` `function_call`; `name` `request_user_input_async`; `arguments` with a question and two choices ("Technical evaluation", "Commercial discussion"); `turn_id` and `call_id` values.

## Return the tool result

- If the user never answers, the agent still needs time to write. So at 4:10 p.m. (delivery minus 2 minutes) the application shuts any question still open.
- Return one tool result per pending call while the run is active:
  - On reply: `status` = `answered`, with `answer` holding what the user typed or picked.
  - At the cutoff, if the same `call_id` is still pending: `{"status":"no_answer"}`.
- Send the result with the SDK's session events method (`client.beta.agents.sessions.events.create`). The event has `type` `agent.session.input.tool_result`, `turn_id`, `call_id`, `success` true, and `output` (the JSON result as a string).
- Keep consuming the stream while submitting. If the agent finishes early, close the pending question in the interface.

## Retrieve and deliver the answer

- Hand over a short briefing the moment it is done, with 3+ minutes left for reading. If time runs out first, hand over the last finished briefing, or say there are no verified findings yet.
- On `agent.session.turn.completed`, retrieve the saved items with the SDK's turn items method. The briefing is the finished agent message with `phase` = `final_answer`.
- If the stream closes early, list the session's turns to check the saved status. The post points to the stream-recovery guide for reconnecting and retrieving saved work.

## Complete example code

- One file per language (TypeScript, Python, Go, Java, Ruby) with client setup, asynchronous replies, the delivery timer, and cleanup. Each reads `OPENAI_API_KEY` and accepts replies in the terminal. A comment in the samples says to buffer terminal replies independently of the event stream.

## Time awareness in a Responses API loop

- If the personal agent uses a hand-coded Responses API loop, the application must keep the model informed of the time left. Work out the deadline a single time; then, ahead of each model call (tool-result calls included), add a new reminder of the time.
- An application timer runs across the whole loop, so delivery happens even if a request or a tool is slow.

1. **Set the meeting and briefing deadlines.** Same instructions and the same async question tool (here with `strict` false and `web_search` without a mode). Meeting in 15 minutes, briefing due in 12, unanswered questions closed 10 minutes after the start. The deadlines stay fixed for the whole task. Python names: `configure_task`, a `State` dataclass with `response_ids`, `questions`, `seen_calls`, `latest_response_id`, `saved_answer`.
2. **Add the current time before every model request.** One request helper (`start_response`) handles the first request and every continuation, so the clock update lives in one place. Just before calling the Responses API, append the current UTC time as a developer message ("Current time: …"), placed after the user input or tool results. Every request repeats the instructions and tools; the first deadline remains in history. The helper passes `previous_response_id`, `store` true, `stream` true, and a `timeout` equal to the time remaining; it raises a timeout if no time remains.
3. **Collect a reply while research continues.** A collector (`collect_reply`, fed by a terminal reader `console_replies`) shows the question and returns a `function_call_output` with the original `call_id`: the answer if it arrives before the cutoff, or `no_answer` at the cutoff.
4. **Handle questions and completed responses.** Start the collector as soon as the full question arrives in the response stream (`response.output_item.done` with a `request_user_input_async` call not seen before), and keep reading events. On `response.created`, record the response ID for cleanup. On `response.completed`, save the ID for the next request and keep any completed briefing (`final_text` takes completed messages whose `phase` is none or `final_answer`). `response.failed`, `response.incomplete`, and `error` stop the run.
5. **Continue the loop with ready results.** After each response, pass whatever tool results are ready to the request helper, which also attaches a fresh time reminder. Set `previous_response_id` to the newest finished response, even if the result answers a question asked several responses back. Keep requests sequential. Once the briefing is finished and nothing is waiting, deliver it and shut open questions; if not, continue with a developer message to keep working while replies are pending, without waiting for an answer. Python name: `run_loop`.
6. **Enforce delivery while a request is in flight.** The application timer guards the whole loop, including API requests and stream reading. When the deadline hits, cancel the in-flight request and hand over the saved briefing (or say no verified findings exist yet). Then cancel pending input handlers and delete the stored responses (`client.responses.delete`). Python name: `main`.

## Conclusion

- Personal agents sometimes must finish by a deadline. Ideally they ask for clarification, but they must do useful work without it.
- Time awareness helps the agent choose between researching more, verifying a finding, and finishing the write-up. Async function tools let it keep researching while the user thinks. The agent keeps enough context to write a useful briefing if the question goes unanswered.
- The post says ChatGPT and other agent harnesses use this pattern to keep working while they ask the user for clarification, and that the Agents API feature lets developers build it themselves.

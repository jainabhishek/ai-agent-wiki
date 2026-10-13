# Working at the frontier: How Cursor knew Claude Fable 5 was ready for the hardest 1% of problems — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/working-at-the-frontier-cursor
> Publisher: Anthropic (claude.com articles) · Date: 2026-07-17
> Captured: 2026-10-12 via curl (condensed).

Page metadata: Category Best practices; Product Claude Platform; Date July 17, 2026; Reading time 8 min. Subject: Nate Schmidt, engineer on evals and model behavior at Cursor.

## Intro
- Cursor supports every major frontier model plus its own, so it presents itself as a neutral judge. Schmidt maintains the model scorecard: how models succeed, fail, and what makes a developer switch away mid-task.
- Public benchmark scores and real developer reception stopped lining up, so the team built CursorBench.
- CursorBench captures messy, underspecified real prompts. Example tasks: a pasted stack trace with only the word "fix" (model must infer intent, find root cause, validate the change); a prompt that names the wrong module as broken, testing whether the model challenges the user's assumption.
- Claude Fable 5 scored 72.9% at Max effort, stated as a new high.
- In personal use, Schmidt stopped having to repeat goals or babysit (re-supplying context, spelling out solutions, auditing results).

## Reasoning about the entire mission
- Scoring focuses on whether the model understood the request: infer the problem, find root cause, fix, validate, report back.
- Scores on ambiguous tasks were high enough that the team suspected cheating, so they read traces on the hardest tasks. They saw wins no previous model found, with fewer operations (token-efficient relative to work done).
- Moon-landing test: a programmable space-flight simulator with a one-line prompt (build a rocket and land it on the moon). Earlier, Claude Opus ran 12–16 hours without success: ran out of fuel in orbit, added fuel, then could not clear the atmosphere due to weight.
- Same blank-slate prompt with Fable 5: first flight went to low orbit and returned; transcript showed it planned a telemetry-gathering orbit mission first. A few attempts later it landed. Whole run: a couple of hours vs Opus's 12+ hours with no result.
- Schmidt's characterization: Opus did local reasoning (what just happened / what is next); Fable did global reasoning about the whole mission.

## When to reach for the global optimum
- Rule of thumb: if the path from A to B is known, a cheaper model may do; if B is unknown, use Fable.
- Fable enabled shelved rewrites by carrying enough of the skeleton; "lowers the activation energy".
- Coordination: before touching shared code, Schmidt has an agent read a teammate's recent commits and flag conflicts, replacing check-ins.
- Cost/performance: pair Fable with faster, lighter models for routine work; bring Fable in where capability is the constraint. For p99 problems, the metric is time to solution.

## What's next
- Next experiment: days-to-weeks unattended management of a back-end system.
- Internally: proactive hunting of performance bottlenecks and user pain points; building more realistic eval environments.

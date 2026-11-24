# The components of agent memory — Anthropic (Engineering) (raw capture)

> Source: https://www.anthropic.com/research/components-of-agent-memory
> Publisher: Anthropic (Engineering team) · Date: 2026-11-06
> Captured: 2026-11-24 via curl (HTML stripped to text) (condensed paraphrase).

Author: Lance Martin (editorial guidance: Caitlin Love, Tom Chivers, Rebecca Hiscott, Jake Eaton, Blake Wilson). Figures by Monika Tuchowska. Claude Plays Pokémon by David Hershey.

Page topics: Agents, Context engineering, Agent memory. Related article listed: "Harness design for long-running application development" (2026-03-24).

## Introduction (no heading)

- Opens with Kierkegaard's line that life is understood backward but lived forward; memory design for agents faces a similar bind.
- Human analogy: the hippocampus encodes experiences quickly, but only some are consolidated into long-term knowledge. Much consolidation seems to happen offline (sleep, quiet rest), when the hippocampus replays recent experience and integrates it into the neocortex.
- Agents can split the work the same way. Agents capture work in logs or transcripts. Researchers at Letta and UC Berkeley proposed **sleep-time compute**: models use idle time between interactions to reorganize existing context. Applied to memory — reflecting on logs to fix mistakes or produce new notes and representations — this is often called **dreaming** (Figure 1).
- Anthropic has found dreaming useful for giving Claude effective memory. The post explains its view of agent memory and walks through evaluations of each component, including dreaming.
- Figure 1 caption (paraphrased): dreaming can correct mistakes, create notes, build new representations, or shape what is preloaded into future sessions.

## Memory notes

- Definition: "agent memory" = knowledge Claude gains from experience (user interactions, assigned tasks) and keeps between sessions, saved as context it can read later.
- Excludes: weight changes (training), in-context learning (within one conversation), and compaction (Claude-written summaries that replace older turns so work continues in a new context window).
- Human analogy: chemical signals around an experience can mark a memory as important; marked memories are replayed more during offline periods (**replay**), which stabilizes them.
- Similarly, Claude can tag salient events in a session log as they happen, or write them to a memory store such as a folder of memory notes (Figure 2). Open question: how does Claude tell what is salient before it knows what comes next?

## Memory can be a prediction about what the future will need

- Writing a rule predicts that the pattern will matter again; writing a verified fact predicts a future session will want to rely on it without re-checking. Claude has become much better at these predictions over time.
- **Continual Learning Bench (CL-Bench) 1.0**: measures use of memory on long-horizon tasks. One task: answer a series of questions by looking up a database; after each answer Claude is told the correct solution and may write a memory.
- Learning loop: on a wrong answer, record the failure, form theories, test them, and turn findings into a rule.
- Setup: run on **Claude Managed Agents**; each question in a fresh session, except a memory directory that persisted across sessions.
- Results by model (Figure 3: memory vs stateless baseline):
  - Claude Sonnet 4.6 got as far as theories about why answers were wrong; memory directory was scattered files of untested guesses.
  - Claude Opus 4.7 consolidated notes into one reference document and marked facts as checked vs unconfirmed.
  - Claude Sonnet 5 marked answers confirmed after the grader checked them and wrote corrections when wrong.
  - Claude Opus 5 was the first to **close the loop**: most entries had a rule plus how it knew the rule was true, earlier answers, and warnings about discovered traps.
  - Claude Opus 5.5 and Claude Sonnet 5.5 also closed the loop. With memory they scored about the same as Opus 5; their no-memory baselines were slightly higher.

## Claude has learned to judge salience

- Test: Claude playing Pokémon Red (long-horizon). Each model got a folder of memory files to read and write during play (Figure 4).
- Compared one run each of Claude Sonnet 3.7 and Claude Fable 5 at about **10,000 steps**.
- Sonnet 3.7 assumed everything might matter: an archive of encounters, often one file per battle, item, or NPC. Totals: **413 memory files across 225 folders**, **one badge**.
- Fable 5: **nine files in two folders** plus a top-level `global.md`; **four badges**.
- Why Sonnet 3.7's approach hurt: game state changes constantly, so the detailed record kept going stale and Claude spent more and more time combing memory instead of playing. Near step 10,000 it opened yet another (the fourth) folder of "master" memory files. In the **17 steps** that followed it made 6 files and removed 9, with zero game moves.
- Fable 5 used memory for what the game does not show. Money and map position can be read off the screen each turn, so storing them is redundant; strategy, plans, and tested rules exist only if Claude works them out and vanish unless written down.
- Fable 5's layout: `global.md` as a dashboard (current goal, a prewritten plan for gyms, its own rules for using memory); a locations folder (route plans); a gameplay folder (learned strategies). Example: after seven Poké Balls in a row failed on a Magikarp, it wrote a rule to vary timing (insert extra wait presses between menu steps) when 3+ balls fail in a row, noting the catch landed right after doing so.
- Opus 5.5 did similarly: a small folder tracking current goal and next steps, rewritten during play; it **beat the game**.

## Steering Claude to write memory

- Finding: tell Claude what memory is for, not how to use it. On CL-Bench Anthropic only said a memory folder was available; that was enough for Opus 4.7 and Opus 5 to use memory well, with a noticeable boost (Figure 3).
- Test of specific rules (one rule per test), comparing each model's gain from memory with and without the rule. With "record only failures," Opus 5 and Opus 4.7 lost much of their memory boost (Figure 5, right). For stronger models, freedom to judge salience beat fixed rules, and rules could weaken performance.
- Steering helped older models most. Sonnet 4.6 often did not read its memory directory and did not test its theories; prompting it to read memory before answering and to explicitly test theories **nearly doubled** its benchmark score (Figure 5, left). Sonnet 5 does this unprompted: it read memory before answering **9 of 10** times, vs **under half** for Sonnet 4.6.
- With frontier Claude models, Anthropic typically gives simple guidance to create notes when a person asks or when something is clearly worth remembering, and leaves the judgment to Claude.

## Dreaming can correct memory

- Claude writes memory based on in-session salience, so a note that is wrong from the start, or drifts as the environment changes, can be read and trusted later.
- Dreaming lets Claude test notes against the original transcripts (Figure 6). Example: Pokémon on Managed Agents with a mounted memory directory.
- Mt. Moon: cave with entrance on the west, exit on the east; near the entrance a one-way ledge drops the player back onto the earlier route. Claude used the PokéCenter at the mountain's entrance as a landmark.
- Claude wrongly noted the PokéCenter was on the east side, announced Mt. Moon was behind it, and updated notes to "Mt Moon DONE." It then went over the ledge, landed back on the earlier route, and — because its navigation tool did not show the drop — concluded it had overshot west and had been right all along (Figure 7).
- Dreaming on the folder with the wrong note: Claude checked it against the session transcript, caught the error, and rewrote it. The transcript served as ground truth. With the corrected note Claude went back into Mt. Moon and reached Cerulean City.
- With the uncorrected note Claude dropped back onto the route three times, then wrote that it would stop rather than keep looping; the setup's automatic reply told it to continue, and it went back to Pewter City (the town before the mountain) to heal and restock. That run never reached Cerulean City (Figure 8). A no-memory run also never got past the mountain.

## Dreaming can build new memory representations

- Dreaming can build representations that help navigate memory (Figure 9). One is a **wiki**: Claude-written and -maintained pages, each gathering what Claude knows about one subject and linking to other notes, giving a map for locating memories.
- Stainless experiment: internal documents from Stainless (a software company Anthropic acquired in May) — about **350,000 files, roughly 420M tokens**. **25 questions**; Claude had a search tool and was told to build a wiki via dreaming. Over **128 sessions**, Opus 5 agents explored files, wrote or corrected linked pages, merged duplicates, and checked claims against sources, coordinating through a shared log; each session built on prior ones.
- Scaling dreaming from **2 to 128 sessions** raised wiki-only performance from **13% to 48%** of graded criteria (Figure 10).
- Incremental growth: early wiki knowledge is like a new employee's; more dreaming makes it like a seasoned employee's.
- Wiki helped most combined with search: search + wiki rose from **54% to 61%** as the wiki grew, vs **53%** with search alone. Best wiki-only score: **48%**. Search + wiki also saved about **20,000 tokens per question**.
- Figure 10 caption (paraphrased): center, scores over sequential sessions; left/right, example wiki graphs after 2 and 128 sessions (dots = pages, lines = links).
- Harvey **LAB** benchmark plus a document set about a merger: LAB gives Claude documents and asks for a legal brief graded against a criteria list. Claude built a wiki, then answered questions or wrote briefs from the wiki and from direct file search.
- Merger test: **24 questions**, more than half needing information across several documents, many also needing judgment or math. On those items Claude scored **87%** with the wiki vs **73%** with search alone (Figure 11, left).
- Where the wiki did not help: on one LAB task most brief criteria could be met by text search in a single document; no clear gain over search (Figure 11, right). On another LAB task the wiki grew larger than the source documents (Figure 12) — compared to the map in Borges's "On Exactitude in Science" that is as large as the empire, abstracting nothing.

## Dreaming can promote notes up the memory hierarchy

- Dreaming can move notes to the top of the memory hierarchy, which the agent harness preloads into context at the start of every session (Figure 13), so Claude need not search for them or know they exist.
- This is a form of context injection and needs care: injected memories cost tokens, a wrong note is carried into every session, and loading does not guarantee action — Claude Code docs warn that longer instruction files reduce adherence. The top layer must stay small; much of dreaming's work is keeping it small by moving details down and leaving links.
- Claude Code **auto memory** keeps its injected layer small the same way, maintained by Claude during the session. It loads only the first **200 lines or 25 KB** of `MEMORY.md`, which acts as an index of what Claude knows and where to find it.
- Figure 13 caption (paraphrased): injected context loads every session; lower layers are read or searched on demand.

## Dreaming can focus memory on a specific goal

- Dreaming can shape how memory grows toward a goal. Example: an assistant like Claude Duet benefits from memory organized around the person it helps.
- The instructions guiding memory growth differ by task and tell Claude what matters.
- LAB acquisition task: a set of contracts; the brief is graded on correctly describing contract terms. Initial wiki-building instructions did not say how the wiki would be used. Several agents wrote to one **shared table** of contract terms at once (Figure 14, left). The brief included only **41 of 57** facts (**72%**): the shared table summarized terms poorly and dropped some, because agents overwrote each other.
- Fix loop: Claude reflected on failures, proposed an instruction change, and rebuilt the wiki; it discovered contract terms mattered most and rewrote the instructions. New design: **one page per contract, written by a single agent, quoting terms verbatim** rather than summarizing into a shared table. Result: **57 of 57** facts; 100% of criteria could be met (Figure 14, right).

## Dreaming can fill in gaps a session leaves behind

- In-session notes see only that session's context; dreaming can search across many sessions for common patterns or mistakes.
- In LAB wikis Claude sometimes linked to pages not yet created. A second dreaming pass fixed many: on one task it found **nine links** to a missing page and repointed them to an existing page for the same document, and added **three new pages**, including an index (Figure 15).

## Thinking backward, looking forward

- Open question 1 — when to create memory: writing in-session captures salience at the source and is available immediately, but distracts from the main task; dreaming moves creation to the background, but its output may not be immediately available.
- Open question 2 — keeping memory current: rules can be wrong from the start or drift as the environment changes. Dreaming fixes mistakes but costs compute; checking every memory continuously may be impractical. Options: focus dreaming on information likely to change, or tune dreaming cadence (e.g. by how often memories are accessed).
- Transcript search is a reasonable foundation for memory. Combining representations (wikis) with search can work, but maintaining representations costs compute and they can accumulate errors or hallucinations.
- No model can know the future; dreaming lets Claude look backward and spend compute to organize memory, correct mistakes, and maintain representations for future sessions. Memory systems will evolve with Claude's capability.
- Points to Anthropic cookbooks on getting started with dreaming and knowledge wikis.

## Acknowledgements (names only)

Thanks to Barry Zhang, Theodora Chu, Daliang Li, Mahesh Murag, Jake Noble, Ravi Trivedi, Tina Vachovsky, Brad Abrams, Henry de Valence, Jeremy Fox, Matt Bell, Allen Li, Chris Gorgolewski, Eugene Yan, Artur Renault, Wei Zhang, Kevin Chen.

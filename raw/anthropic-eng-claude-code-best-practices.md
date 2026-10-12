# Claude Code: Best practices for agentic coding — Anthropic (Engineering blog) (raw capture)

> Source: https://www.anthropic.com/engineering/claude-code-best-practices
> Publisher: Anthropic (Engineering blog) · Date: 2025-04-18
> Captured: 2026-10-12 via curl (condensed). The live URL now returns HTTP 308 to
> https://code.claude.com/docs/en/best-practices ("Best practices for Claude Code",
> a maintained docs page; its metadata says dateModified 2026-10-06). The original
> post text below comes from the Wayback Machine snapshot of 2025-06-02
> (web.archive.org/web/20250602202220/...), which shows "Published Apr 18, 2025"
> and no "updated" date. A section at the end records how the successor docs page
> differs.
> Author: Boris Cherny (thanks to Daisy Hollman, Ashwin Bhat, Cat Wu, Sid Bidasaria, Cal Rueb, Nodir Turakulov, Barry Zhang, Drew Hodun, and others).

## Intro

- Claude Code is described as a low-level, unopinionated command-line tool for
  agentic coding with close to raw model access. Patterns are starting points,
  not rules.

## 1. Customize your setup

### a. Create CLAUDE.md files
- Claude pulls CLAUDE.md into context at conversation start. Suggested content:
  bash commands, core files and utilities, code style, testing instructions,
  repo etiquette (branch naming, merge vs. rebase), dev environment setup,
  project quirks, "other information you want Claude to remember".
- No required format; keep it concise and human-readable. Example sections:
  `# Bash commands`, `# Code style`, `# Workflow`.
- Locations: repo root (`CLAUDE.md` checked in, or `CLAUDE.local.md`
  gitignored); any parent directory (monorepos: `root/CLAUDE.md` and
  `root/foo/CLAUDE.md` both load); child directories (loaded on demand);
  `~/.claude/CLAUDE.md` for all sessions.
- `/init` generates a CLAUDE.md.

### b. Tune your CLAUDE.md files
- Treat CLAUDE.md as a frequently used prompt; iterate on effectiveness. Common
  mistake: adding content without testing it.
- Press `#` to give an instruction that Claude adds to the relevant CLAUDE.md.
- Anthropic sometimes runs CLAUDE.md through the prompt improver and adds
  emphasis ("IMPORTANT", "YOU MUST") to improve adherence.

### c. Curate Claude's list of allowed tools
- Default: permission request for any system-modifying action (file writes, many
  bash commands, MCP tools). Deliberately conservative.
- Four ways to manage the allowlist: "Always allow" at the prompt; `/permissions`
  (examples: `Edit`, `Bash(git commit:*)`, `mcp__puppeteer__puppeteer_navigate`);
  edit `.claude/settings.json` (check in) or `~/.claude.json`; the
  `--allowedTools` CLI flag per session.

### d. If using GitHub, install the gh CLI
- Without `gh`, Claude can use the GitHub API or MCP server.

## 2. Give Claude more tools

### a. Use Claude with bash tools
- Claude inherits the shell environment. For custom tools: give the name with
  usage examples, tell it to run `--help`, document in CLAUDE.md.

### b. Use Claude with MCP
- Claude Code is both MCP server and client. Configure servers in project
  config, global config, or a checked-in `.mcp.json` (example: Puppeteer and
  Sentry). Use the `--mcp-debug` flag to debug configuration.

### c. Use custom slash commands
- Prompt templates as Markdown in `.claude/commands/`; appear under `/`;
  check into git. `$ARGUMENTS` passes parameters.
- Example: `.claude/commands/fix-github-issue.md` (8 steps: `gh issue view`,
  understand, search, implement, write and run tests, lint and typecheck,
  commit message, push and create PR) becomes `/project:fix-github-issue 1234`.
  Personal commands go in `~/.claude/commands`.

## 3. Try common workflows

### a. Explore, plan, code, commit
- Read relevant files/images/URLs, explicitly with no code yet; use subagents to
  verify details or investigate questions early (preserves context).
- Ask for a plan. Use "think" to trigger extended thinking; the phrases map to
  increasing thinking budget: "think" < "think hard" < "think harder" <
  "ultrathink".
- Optionally save the plan to a document or GitHub issue as a reset point.
- Implement, verifying reasonableness as it goes; then commit and open a PR,
  updating READMEs/changelogs.
- Steps 1–2 matter: without them Claude tends to jump straight to coding.

### b. Write tests, commit; code, iterate, commit
- TDD, an "Anthropic-favorite" workflow: write tests from input/output pairs
  (say it is TDD to avoid mock implementations); run and confirm failure; commit
  tests; write code to pass without modifying tests, iterating; optionally check
  with independent subagents that the code is not overfitting to tests; commit.
- Claude performs best with a clear target to iterate against (visual mock, test
  case, other output).

### c. Write code, screenshot result, iterate
- Give a screenshot method (Puppeteer MCP, iOS simulator MCP, manual paste) and
  a visual mock; implement, screenshot, iterate. Output typically improves a lot
  after 2–3 iterations.

### d. Safe YOLO mode
- `claude --dangerously-skip-permissions` bypasses all permission checks. Good
  for lint fixes and boilerplate. Risks: data loss, system corruption,
  exfiltration via prompt injection. Mitigation: run in a container without
  internet access (Docker Dev Containers reference implementation).

### e. Codebase Q&A
- Ask the questions you would ask a colleague (example questions about logging,
  endpoints, specific lines). This became Anthropic's core onboarding workflow.

### f. Use Claude to interact with git
- Many Anthropic engineers use Claude for 90%+ of their git interactions:
  history search, commit messages, reverts, rebase conflicts, grafting patches.

### g. Use Claude to interact with GitHub
- Create PRs ("pr" shorthand), fix simple review comments, fix failing builds or
  lint warnings, triage issues in a loop.

### h. Use Claude to work with Jupyter notebooks
- Read/write `.ipynb` side by side in VS Code; ask for "aesthetically pleasing"
  output for human viewers.

## 4. Optimize your workflow

### a. Be specific in your instructions
- Success rate improves with specific first instructions. Poor/good pairs:
  "add tests for foo.py" vs. a logged-out edge case without mocks;
  ExecutionFactory API question vs. "look through git history"; calendar widget
  vs. following `HotDogWidget.php` patterns without new libraries.

### b. Give Claude images
- Paste screenshots (macOS cmd+ctrl+shift+4, then ctrl+v), drag and drop, or
  give file paths.

### c. Mention files you want Claude to look at or work on
- Tab-completion for file and folder references.

### d. Give Claude URLs
- Allowlist frequently used domains with `/permissions`.

### e. Course correct early and often
- Auto-accept mode (shift+tab) exists, but active collaboration usually gives
  better results. Four tools: ask for a plan and forbid coding until confirmed;
  Escape to interrupt with context preserved; double-Escape to jump back in
  history and edit a prompt; ask Claude to undo changes.

### f. Use /clear to keep context focused
- Clear between tasks; irrelevant context reduces performance.

### g. Use checklists and scratchpads for complex workflows
- For migrations or many lint errors: write all errors to a Markdown checklist,
  then fix and verify one at a time, checking each off.

### h. Pass data into Claude
- Paste; pipe (`cat foo.txt | claude`); tell Claude to pull via bash, MCP, or
  slash commands; ask it to read files or fetch URLs.

## 5. Use headless mode to automate your infra
- `-p` enables headless mode for CI, pre-commit hooks, build scripts;
  `--output-format stream-json` for streaming JSON. Headless mode "does not
  persist between sessions".

### a. Use Claude for issue triage
- GitHub-event automations; the public Claude Code repo labels new issues this
  way.

### b. Use Claude as a linter
- Subjective review: typos, stale comments, misleading names.

## 6. Uplevel with multi-Claude workflows

### a. Have one Claude write code; use another Claude to verify
- Write; `/clear` or second terminal; second Claude reviews; third Claude (or
  another `/clear`) edits from code plus review. Same for tests then code.
  Instances can talk through separate scratchpad files.

### b. Have multiple checkouts of your repo
- 3–4 git checkouts in separate folders and terminal tabs, each with its own
  task.

### c. Use git worktrees
- `git worktree add ../project-feature-a feature-a`, then
  `cd ../project-feature-a && claude`. Tips: consistent naming, one tab per
  worktree, iTerm2 notifications, separate IDE windows,
  `git worktree remove ../project-feature-a`.

### d. Use headless mode with a custom harness
- **Fanning out:** Claude writes a script to list tasks (e.g. 2k files to
  migrate); loop calling `claude -p "migrate foo.py from React to Vue. ... you
  MUST return the string OK ... or FAIL" --allowedTools Edit Bash(git commit:*)`;
  refine the prompt over several runs.
- **Pipelining:** `claude -p "<prompt>" --json | your_command`.
- `--verbose` for debugging; turn it off in production.

## Second capture: successor page code.claude.com/docs/en/best-practices

> Source: https://code.claude.com/docs/en/best-practices · Publisher: Anthropic
> (Claude Code docs) · dateModified 2026-10-06 · Captured: 2026-10-12 via curl
> (condensed). The engineering URL above now redirects here. The capture below
> lists only what the successor page says that the 2025 post does not.

- **Framing:** opens with one constraint: the context window fills fast and
  performance degrades as it fills; most practices follow from that.
- **New first section, "Give Claude a way to verify its work":** a pass/fail
  check (tests, build exit code, linter, fixture diff, screenshot). Four gate
  strengths: in one prompt; a `/goal` condition re-checked by a separate
  evaluator each turn; a Stop hook that blocks the turn from ending; a
  verification subagent. Ask Claude to show evidence, not assert success. Run
  `/verify` against the running app.
- **Plan mode replaces "don't code yet" prompting:** Shift+Tab or
  `claude --permission-mode plan`; Ctrl+G edits the plan. Skip planning if the
  diff fits in one sentence. The "think" < "ultrathink" keyword ladder is gone.
- **CLAUDE.md:** keep short; test each line with "Would removing this cause
  Claude to make mistakes?"; include/exclude table; check with `/context`;
  `/doctor` proposes cuts; use "IMPORTANT" on one line only (if many lines are
  emphasized, none stands out); `@path/to/import` imports. The `#` memory key is
  not mentioned.
- **Permissions:** with Claude Code v2.1.283 or later, auto mode (a classifier
  model) is the default starting mode for interactive terminal and VS Code
  sessions; Manual mode is optional. Allowlists and `/sandbox` cut prompts in
  both. "Safe YOLO mode" is gone.
- **Skills replace custom slash commands:** `.claude/skills/<name>/SKILL.md`;
  the fix-issue example becomes a skill with `disable-model-invocation: true`,
  invoked as `/fix-issue 1234`.
- **New:** custom subagents in `.claude/agents/` (example `security-reviewer`
  with `tools:` and `model: opus`); hooks ("advisory" CLAUDE.md vs.
  deterministic hooks); plugins via `/plugin`; `claude mcp add --transport http`.
- **Let Claude interview you** with the AskUserQuestion tool, write `SPEC.md`,
  then start a fresh session to implement.
- **Session management:** after two failed corrections, `/clear` and rewrite the
  prompt; `/compact <instructions>`; partial summarize via `/rewind`; `/btw` for
  questions that never enter history; checkpoints (do not track Bash changes);
  `/rename`, `claude --continue`, `claude --resume`.
- **Headless:** `claude -p` now creates a resumable session unless
  `--no-session-persistence`; `--output-format json` returns a `result` field.
- **Parallelism:** worktrees, cross-session messaging, desktop app, cloud
  sessions, agent view (research preview, `claude agents`), agent teams
  (experimental, off by default). `/batch <instruction>` splits work across 5–30
  subagents in worktrees. Fan-out loop uses `--allowedTools "Edit,Bash(git
  commit *)" --permission-mode dontAsk`.
- **Auto mode for unattended runs:** `claude --permission-mode auto -p "..."`.
- **Adversarial review step:** bundled `/code-review` skill or a subagent
  checking the diff against `PLAN.md`; tell the reviewer to flag only gaps
  affecting correctness or requirements, to avoid over-engineering.
- **Failure patterns:** kitchen-sink session, correcting over and over,
  over-specified CLAUDE.md, trust-then-verify gap, infinite exploration.

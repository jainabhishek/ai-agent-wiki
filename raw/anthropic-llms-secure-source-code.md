# Using LLMs to secure source code — Anthropic (claude.com articles) (raw capture)

> Source: https://claude.com/resources/articles/using-llms-to-secure-source-code
> Publisher: Anthropic (claude.com articles) · Date: 2026-05-27
> Captured: 2026-10-12 via curl (condensed).

Category: Best practices. Reading time 25 min. Authors (Acknowledgements): Eugene Yan and Henna Dattani, with contributions from Michael Molash, Abel Ribbink, Justin Young, Ben Morris, David Dworken, and Hasnain Lakhani. The guide is written for working with "Claude Opus". Customer team quotes are paraphrased below. Condensed paraphrase.

## Intro

- Main takeaway: discovery is now easy to parallelize; the bottleneck has moved to verification, triage, and patching.
- Evidence of the gap: as of 2026-05-22, Anthropic's open-source scanning had disclosed 1,596 vulnerabilities; to its knowledge 97 were patched.
- Companion repo `defending-code-reference-harness`: skills for interactive workflows plus a demo harness for autonomous scanning; each step names its skill.

## The find-and-fix loop

Six steps distilled from teams that find and fix the most vulnerabilities:
1. **Threat model** — decide what counts as a vulnerability before scanning.
2. **Sandbox** — isolate agents and prove exploits.
3. **Discovery** — models search the source for vulnerabilities.
4. **Verification** — independently confirm which findings are exploitable.
5. **Triage** — deduplicate, assign severity, prioritize.
6. **Patching** — fix, confirm the vulnerability is nullified, search for variants.

- Steps 1–2 are one-time setup per codebase (revisit when the system changes). Steps 3–6 are the repeating "defender's loop".
- First run finds the most; later runs find fewer but often more complex bugs. Do not expect zero on run n: models are stochastic and large codebases have a long tail.
- On a first iteration, run the loop several times; stop based on net-new findings and risk tolerance. Afterwards scan periodically or when the code meaningfully changes.

## 1. Threat model: Define what counts as a vulnerability

- Most common cause of false positives: the model misunderstands trust boundaries (e.g., treats trusted config or clients as attacker-controlled), or the reverse (assumes an internet-facing service is internal and under-reports). The model is wrong about the threat model, not the code.
- One team: findings were exploitable about 90% of the time on systems with well-documented threat models, design docs, requirements, and constraints.
- Two-step build:
  1. **Bootstrap** from code, docs, and vulnerability history — architecture docs, wikis, entry points, git history, past vulnerabilities. Ask for system context, assets, entry points, trust boundaries; cluster past bugs and list relevant vulnerability classes; document what is and is not in scope and why. One team distilled hundreds of past CVE/security-fix commits into "bug-shape" hints and asked whether each fix was complete and applied everywhere; three exploitable issues in an hour. Lesson: "what was exploited before" is an easier lead than "find vulnerabilities".
  2. **Interview** someone who knows the system, using Shostack's four questions (What are we building? What can go wrong? What are we doing about it? Did we do a good job?). Optional, but adds context code and docs lack; run after bootstrap so the interviewee starts from a draft.
- Practices: use dependencies' published security policies (examples: vLLM `security.md`, SQLite "Defense Against the Dark Arts", ImageMagick's security policy); name what is trusted (config files, authenticated clients); keep a `THREAT_MODEL.md` in the repo and update it so the discovery agent reads it first.
- Uses: in discovery as **scope** (partition, prioritize, skip out-of-scope); in triage as a **filter** (calibrate severity).
- One large project had a 40% false-positive rate even with reproducible PoCs, because owners dismissed bugs outside the project's threat model. A CISO's summary (paraphrased): the model knows the code but not the organization.
- Skill: `threat-model` (bootstrap + interview → `THREAT_MODEL.md`).

## 2. Sandbox: Run agents safely and verify exploitability

- Purpose 1: protect your systems. Anecdotes: a model told it had no network found it could fetch from GitHub anyway; another agent answered a GitHub issue mid-scan. Neither malicious; both show constraints must be enforced in code and configuration.
- Match isolation to the threat model: containers are fine for the discovery agent reading code; run the target and PoCs in a microVM (e.g., Firecracker) or full VM with egress locked down. Never expose credentials (`~/.aws`, `~/.ssh`, `.env`).
- Network only during setup: pull deps, build, install tools, deploy target, run existing tests; then snapshot and remove network. During scans, allow traffic only to the model API via a local proxy. Load the snapshot at each run start.
- Purpose 2: prove exploitability. Static reading cannot test reachability or compensating controls, so the model flags unexploitable correctness bugs. With a sandbox to compile, run tests, and detonate PoCs, non-exploitable findings dropped significantly. One offensive team's rule: true positive only if the agent builds and runs a PoC on the test bed; after six weeks they called test beds and running PoCs the biggest efficacy lever.
- Pin everything (image tags, commit SHAs, dependencies, build commands); cache locally so builds need no network; make the container durable for repeated loops. One false finding came from the agent downloading an older library version than production; caught by reading the transcript; fix = Docker images with dependencies pinned to production so finder and verifier use the same artifacts as an attacker.
- Fidelity: omitting dependencies (queue, datastore) under-reports; ignoring production defenses (WAF, auth gateway) over-reports.
- If a representative sandbox is impractical, start with discovery from source alone (frontier models do well); budget more verification time; add the sandbox later when volume justifies it.
- Reference: harness `README.md`; agents and targets in gVisor-isolated containers, egress locked to the model API, target built from a Dockerfile pinned to a commit, `setup_sandbox.sh` for setup.

## 3. Discovery: Provide rich context, shorter prompts, and useful tools

- Give the agent loadable context: threat model, architecture docs, past scan results.
- Frontier models do better with increasingly simple prompts; more prescriptive prompts and long checklists reduce creativity and novel bugs.
- Prompting tips: give the goal and context (why scanning, what a meaningful finding looks like, what system), leave the "how" to the model; optionally name a specific vulnerability class (what it does, where it lives); define a structured output with ordered fields (e.g., rationale, finding, impact, severity) so reasoning builds field by field; include an escape hatch to exit early on weak findings.
- Tools: grep, glob, etc.; security tools (SAST, fuzzers); ask the model what tools it needs; let it build its own tools.
- One pentest team added tools to send requests, check responses, and query traffic logs, so the agent tested each candidate against the running app; true-positive rate near 100%.
- Partitioning: first pass splits the search space (attack surface, endpoint, component); parallel discovery agents per partition so they do not converge on the same shallow bugs; then a system-level pass using partition findings as context. Brute-force horizontal scaling hit diminishing returns; more focus areas and agents produced many duplicates.
- With a sandbox, ask discovery to build a PoC (script, crashing input, failing test); report unreproduced findings flagged as unproven to keep recall.
- Skill: `vuln-scan` (reads `THREAT_MODEL.md`, partitions into focus areas, fans out parallel reviewers, emits structured findings).

## 4. Verification: Filter out non-exploitable findings

- Discovery optimizes recall; verification optimizes precision. One agent doing both self-censors and drops true positives — Anthropic saw this when discovery agents also verified.
- Verifier must be independent: fresh container, no shared filesystem or conversation history. Give it only (1) the PoC or written finding and (2) the codebase, so it can look for missed mitigations (upstream validation, auth gates, type constraints, unreachable code).
- If one pass leaks too many: multiple independent verifiers (different angles or different models) with majority vote; optionally a separate judge between discovery and verification.
- Prompt the verifier to disprove: assume each finding is a false positive; give clear true-positive criteria (matters most without a PoC).
- Across partner teams: an adversarial verifier roughly halved non-exploitable findings; requiring it to also build a confirming PoC brought false positives near zero.
- With a faithful sandbox, have the verifier build and run a reproducible PoC. A working PoC proves exploitability; a failed PoC does not prove a false positive.
- One OSS team: scan package → generate PoC → deploy a mock app that uses the package and triggers the PoC; their view: the PoC is the validation.

## 5. Triage: Deduplicate by root cause, rank by preconditions and impact

- Triage sets patching priority. With models producing a hundred candidates before lunch, triage is the bottleneck.
- Alert fatigue: duplicate or inflated reports make engineers stop reading; OSS maintainers are hit hardest. Teams send mostly critical/high. Some pointed the model at existing backlogs (old scanner output, bug-bounty intake) and cleared hundreds of stale items in days.
- Dedup by root cause: first a cheap deterministic pass (same file, same category, line numbers within ten lines); then model rules.
  - Duplicate: same root cause worded differently; same bug at multiple call sites; a missing global protection (e.g., auth check) reported per endpoint; a cause and its consequence in the same path.
  - Distinct: different classes in one file; different variables to different sinks; two independent bugs in one helper; the same missing check on two endpoints needing separate fixes.
  - Alternative: if each finding has a PoC and patch, check whether one patch disarms other findings' PoCs.
- Severity rubric: reachability; attacker control (does untrusted input reach the sink intact); preconditions (non-default setting, feature flag, timing window); authentication; read vs write; blast radius (one user vs all, tenant vs platform, userland vs kernel).
- Have the model answer each rubric question before assigning severity, to avoid anchoring on bug class ("SQL injection, so critical"). Starting thresholds: zero preconditions + unauthenticated remote = critical/high; one or two preconditions or authenticated path = medium; three or more or local-only = low.
- Inflation comes from missing context (which inputs an attacker controls; invisible compensating controls such as an upstream WAF). Fix: give triage the threat model (e.g., "we trust authenticated clients"). One team gave the triage agent the same threat model as discovery.
- Skill: `triage` (multi-vote verification per finding, cross-run dedup, re-ranking by exploitability → short, ranked, owned list).

## 6. Patching: Close the loop and improve context for the next cycle

- Patching also updates the threat model (trust boundaries, components needing scrutiny) and feeds past findings into the next scan.
- Test first: write a test that fails on current code, fix, confirm it passes without breaking others (TDD). Without a test, fixes can silently regress and the bug is hard to prove later.
- One pentester's patches were inconsistent until the harness had the model re-run the PoC against the patched code; quality jumped.
- Models may fix one call site; prompt for the root cause. Then search variants at two levels: same pattern (other call sites/copies) and same class (one SQL injection suggests more).
- Before shipping: adversarial check by a new discovery agent probing the patch; then simplify over-invasive patches — ask for the smallest root-cause change, no refactors, no drive-by cleanups, no reformatting. One team's common failure: patches so restrictive they broke connections to other services.
- Validation ladder, cheapest first: **Build** (compiles, new tests pass) → **Try to reproduce** (original PoC stops working; catches ineffective patches) → **Check for regressions** (original suite passes; catches broken/over-restrictive) → **Re-attack** (fresh discovery agent; catches incomplete patches).
- A human must own each patch. Predictable failure modes: fixing the symptom, blocking legitimate input, cutting access for a dependent service. Validate enough that human review is light.
- Skill: `patch` (candidate diff per finding from triage output, checked by an independent reviewer agent).

## Getting started

- Clone `defending-code-reference-harness`, run `/quickstart` in Claude Code (interactive threat model → scan → triage on a demo target). Repo also has an autonomous harness and a `/customize` skill.
- Then on your own service: bootstrap + interview threat model, build a sandbox, scan, verify independently, triage and review everything high and above, patch, re-scan periodically.
- First scan surfaces more than expected; budget for the post-scan pipeline before more scanning.
- Resources: Claude Security (managed agentic vuln detection and patching); `defending-code-reference-harness`; `claude-code-security-review` GitHub Action; cookbooks "Threat Intelligence Enrichment Agent" and "Vulnerability Detection Agent".

## Moving forward

- Models make finding and exploiting bugs easier; defenders must fix first. Some teams wire harnesses to events: a bug-bounty report triggers variant analysis; a security review triggers a scan with findings attached; a verified vulnerability updates static-analysis rules.

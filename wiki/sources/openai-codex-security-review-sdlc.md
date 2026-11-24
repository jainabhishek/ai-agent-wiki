---
title: "OpenAI (Developer blog): Building Security Review into Your SDLC with Codex Security"
type: source
created: 2026-11-24
updated: 2026-11-24
author: Vanessa Sauter (Cyber Deployment Engineer, OpenAI)
date: 2026-11-23
source_url: https://developers.openai.com/blog/building-security-review-into-your-sdlc-with-codex-security
source_path: raw/openai-codex-security-review-sdlc.md
models: [gpt-6.1-sol, gpt-5.6-sol]
as_of: 2026-11-24
tags: [security, codex, codex-security, code-review, threat-model, sdlc, ci, supply-chain, primary-source]
---

# OpenAI (Developer blog): Building Security Review into Your SDLC with Codex Security

> A how-to for Codex Security: four principles for agentic security review,
> how to seed a threat model, `SECURITY.md`, and knowledge base, and how to run
> reviews in GitHub, Codex Desktop, the CLI, and GitHub Actions.

## Summary

The post argues that manual PR security review cannot keep pace with code that
agents write, so security review must itself become agentic. It states four
principles (system-specific context, review inside development, deliberate
scope and thresholds, inspectable findings) and then walks through the Codex
Security product surfaces. Most of the post is about the context the reviewer
reads: a committed threat model, a `SECURITY.md` policy, and per-scan knowledge
base documents. Examples use Apache Superset and Backstage. It reports no
accuracy or false-positive numbers.

**Model scope.** The only model-specific values are example settings, not
behavior claims: example prompts are labelled "GPT-6.1 Sol · Extra High"
(`gpt-6.1-sol`), and the GitHub Action example sets `model: gpt-5.6-sol` with
`effort: high`. The wiki marked `gpt-5.6-sol` legacy on 2026-10-12
([[openai-prompt-guidance-gpt-5-6]]); this post (2026-11-23) still uses it in the
Action example. Not re-verified against OpenAI's current models list during this
ingest.

## Key points

- **Four principles.** (1) Give agents system-specific context: assets, trust
  boundaries, requirements. (2) Integrate review into local work, PRs, and CI
  with clear triggers. (3) Choose scope (diff scan, component assessment, full
  scan) and reporting thresholds by risk. (4) Make findings inspectable:
  locations, reasoning, severity, confidence, remediation, and what was
  reviewed, excluded, or deferred.
- **Three context files with distinct jobs.** `AGENTS.md` holds engineering
  instructions; a threat model (`docs/security/threat-model.md`) describes the
  system's security reality; `SECURITY.md` says how findings are evaluated and
  reported (invariants, reportable findings, severity context, out of scope). A
  knowledge base passes extra documents to one scan with `--knowledge-base`.
- **Without a committed threat model, Codex regenerates one for every review.**
  Seed it with the `$codex-security:threat-model` skill, commit it, and link it
  in Codex Cloud repo settings. Correct assumptions the code cannot show: the
  Backstage example, where separate hosts are not a boundary if one plugin can
  reach another's database. Revisit when entry points, trust boundaries, or
  privileged operations change.
- **Seed `SECURITY.md`** with `$codex-security:define-security-policy`. The
  Superset policy example states an invariant that must hold as work moves from
  a request into a background worker; the post says such invariants make
  reports testable.
- **Code Review versus Security Review.** Code Review is broad engineering
  review for developers. Security Review is a deeper security pass on the same
  PR (authn/authz bypass, cross-tenant access, injection, data exposure) for
  developers and AppSec engineers.
- **Reporting thresholds.** Automatic review posts High and above by default;
  manual review posts Medium and above. Path overrides lower the threshold for
  sensitive paths (auth, payments, crypto, CI, infra) and raise it for noisy
  ones. Pick automatic thresholds the team can investigate consistently.
- **CLI scan modes.** `--working-tree --base HEAD` (uncommitted work);
  `--diff <base> --head <head>` (PR or branch; changes only); repeated `--path`
  (component assessment). `--diff` and `--path` cannot be combined. Outputs:
  `report.md`, `scan-manifest.json`, `findings.json`, `coverage.json`.
- **Monorepo scope is the organization's job.** Which consumers a shared-library
  change affects comes from the org's ownership and build metadata; Codex does
  not configure it.
- **Alerts and dependencies.** `import github` plus `validate` triage existing
  code-scanning alerts. `$codex-security:triage-finding` checks Dependabot alerts
  for reachability and exploitability and returns a ledger of verdicts. The post
  still says to reconcile the evidence and verify the installed version before
  closing an alert.
- **CI hardening in the examples.** Read-only `contents` permission, actions
  pinned by commit SHA, `persist-credentials: false`, a bubblewrap sandbox step,
  `--ignore-scripts` installs, a fork guard on the dependency workflow, and
  `--fail-on-severity high` as the gate.
- **Rollout advice.** Start with one workflow and a few critical repos, check
  how well the agent reasons against the committed context, then expand.

## Entities

[[openai]], [[openai-codex]]. Codex Security, Apache Superset, Backstage, and
Dependabot have no wiki page.

## Concepts

[[guardrails]], [[context-engineering]], [[agent-skills]],
[[agent-verification]], [[agent-instructions]], [[human-agent-teams]]

## Notable claims & data

- Default thresholds: automatic review posts High+; manual review posts Medium+.
- The word "auto-review" here means the **reporting threshold for automatic PR
  reviews**. It is unrelated to the Codex Auto-review approval subagent in
  [[openai-running-codex-safely]] and [[openai-securing-persistent-agents-openclaw]].
- The post gives no measured precision or recall for Security Review. For a
  measured result on rule-guided Codex review (98% vs 58.3% recall of required
  custom findings), see [[openai-codex-code-review-rules]].
- The Action example pins a model that the wiki lists as legacy (see Model scope
  above).

## Connections

- **Agrees with** [[anthropic-llms-secure-source-code]]: both start from a
  threat model. Anthropic also separates discovery and verification into
  independent agents; this post does not describe such a split.
- **Parallels** [[anthropic-securing-ai-native-sdlc]]: stage-by-stage security
  controls for an SDLC where agents write much of the code.
- **Extends** [[openai-codex-code-review-rules]]: repository rules in
  `AGENTS.md` steer Code Review; `SECURITY.md` and the threat model steer
  Security Review.
- CI agents on repositories: compare [[openai-skills-for-oss-maintenance]]
  (limit triggers, protect the API key).
- Security triage agents: compare [[anthropic-cybersecurity-triage-agents]].

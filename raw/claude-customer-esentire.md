# How eSentire runs expert-level threat investigations at scale with Claude — Anthropic (claude.com customer stories) (raw capture)

> Source: https://claude.com/customers/esentire
> Publisher: Anthropic (claude.com customer stories) · Date: none on page (accessed 2026-10-12)
> Captured: 2026-10-12 via curl (condensed).

Page labels: Case study | Claude Platform. Industry: cybersecurity. Company size: medium. Partner: AWS. Location: North America. Speaker: Dustin Hillard, CPTO. The page promotes Claude Opus 4.6 and says the platform runs it. All figures are self-reported by eSentire through Anthropic.

## Headline figures
- 99.96% ransomware containment before any file encryption, vs. an industry average of 44% stopped before encryption.
- 120,000+ autonomous investigations in 12 months, each averaging 44 tool calls across endpoint, identity, network, and cloud telemetry.
- Above 90% alignment with top SOC experts in continuous production evaluation.
- 6-minute average agentic investigation vs. an 11-day industry median attacker dwell time.
- 41% more confirmed attacks detected per customer; overall alert volume down 11%.

Context: eSentire is a managed detection and response (MDR) provider; its Atlas platform uses Claude for autonomous threat investigations.

## The challenge
AI-driven attacks run at thousands of requests per second. eSentire had to investigate live threats across thousands of heterogeneous customer environments, correlate signals across layers, and reason about intent with incomplete information, at senior-analyst depth on every signal, not only critical ones.

## The solution: model choice
- eSentire says public cyber benchmarks are saturated (top models score near the ceiling) and each has a known, checkable answer. In production the agent starts from a detection plus telemetry with no answer key, and it alone decides which tools to call, how to resolve conflicting signals, and what verdict to give.
- eSentire evaluated several models on real-world security scenarios; Claude scored highest on complex security reasoning and kept investigative coherence across multi-tool workflows.

## How the investigations run
- Atlas runs Claude Opus 4.6 on Amazon Bedrock via the Agent SDK in a multi-agent architecture modeled on a senior SOC analyst's workflow; several sub-agents collaborate per case.
- Average 44 tool calls per investigation: threat-intel queries, SIEM and endpoint correlation, identity activity analysis, reconstruction of attacker behavior from process and network data.
- 12 months: 5 million+ tool calls ≈ 468,000 hours of equivalent expert effort (≈5 analyst-minutes per call).
- Ambiguous example: identity compromise overlapping a real user's normal behavior; agent weighs timing, geography, user-agent strings, and email forwarding rules.
- 3,600+ distinct investigation workflows across major EDR, SIEM, and identity platforms.
- Senior analysts review and act on every critical finding (human trust layer); humans focus on customer engagement, containment decisions, and remediation strategy.

## The outcome: evaluation method and results
- Continuous production evaluation: senior SOC experts independently review a sample of cases the agent investigated; alignment measured on whether compromise occurred, severity classification, and recommended response.
- 500+ adjudicated outcomes: above 90% alignment with senior experts on final verdict; the agent outperforms junior analysts under the same method.
- ~10,000 escalated incidents across 1,400+ customers in 12 months: 31% blocked before execution; 18% failed attempts; 36% identity compromises remediated before business data access; 14% device compromises detected, host isolated, remediated.
- ~2 million endpoints: lateral movement to a second device in <0.5% of incidents; ransomware encrypted files in <0.04%; all detected.

## Looking ahead
Expanding to ingest and respond across any customer security technology regardless of vendor.

---
title: Cursor
type: entity
subtype: org-product
created: 2026-07-21
updated: 2026-07-21
tags: [cursor, coding-agents, multi-agent]
---

# Cursor

> AI coding product and publisher of practitioner research on coding-agent
> harnesses and multi-agent coordination.

## Overview

In this wiki, [[cursor]] contributes a large-scale coding case study rather than
a general agent-building guide. [[cursor-agent-swarm-model-economics]] reports
how its experimental swarm changed after adding task-tree decomposition,
coordination mechanisms, shared memory, and stacked review.

## Key facts

- Frames planner-worker decomposition as a context-efficiency mechanism, not
  merely a way to run more work in parallel. (see
  [[cursor-agent-swarm-model-economics]])
- Reports model-routing economics at the system level, including how planner
  behavior changes downstream worker consumption. (see
  [[multi-agent-economics]])
- Built specialized version-control and reconciliation infrastructure for an
  experiment operating far beyond normal human Git throughput. (see
  [[cursor-agent-swarm-model-economics]])

## Appears in

- [[cursor-agent-swarm-model-economics]]

## Contradictions / open questions

- Cursor's SQLite experiment is not yet replicated across tasks or ordinary Git
  workflows; the generality of its coordination mechanisms remains open.

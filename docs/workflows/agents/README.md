---
permalink: /workflows/agents/
redirect_from:
  - /workflows/agents.html
---

# Guidelines for using agents with Sigrid

Each of these guides follows one job through on a real codebase: what to configure, what a session looks like, and how to check what the agent did. They use [Sigrid Axis](../../axis/README.md), so [install it](../../axis/installation.md) first.

- [Building with Guardrails](building-with-guardrails.md) puts Guardrails in the feature loop, so the agent checks each file it writes before you see the diff.
- [Preventing architecture drift](preventing-architecture-drift.md) checks an agent's diff against Sigrid's measured dependency graph before it merges.
- [Improving architecture](improving-architecture.md) finds the directory whose structure is most worth fixing, plans the move or facade that fixes it, and checks the result against Sigrid's graph.
- [Reducing technical debt](reducing-technical-debt.md) works through the refactoring candidates that carry the most weight in your maintainability rating.
- [Triaging security and reliability findings](triaging-security-and-reliability-findings.md) classifies a findings backlog against how your system is deployed, records a rationale for every decision, and fixes what should be fixed.

These are workflows we run ourselves. They do not cover everything Axis can do, so for the rest, see the [skills reference](../../axis/skills.md), the [MCP tools reference](../../axis/tools.md), and [configuration](../../axis/configuration.md). For which model to run each job on, see [LLM model selection](../../axis/README.md#llm-model-selection).

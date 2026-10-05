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

These are workflows we run ourselves. They do not cover everything Axis can do, so for the rest, see the [skills reference](../../axis/skills.md), the [MCP tools reference](../../axis/tools.md), and [configuration](../../axis/configuration.md).

## Choose a model

Pick the model by how much judgment the work needs. That depends on your codebase as much as on the skill: triage is routine when the deployment is simple, and untangling a directory that everything depends on can take real reasoning.

Each vendor offers models in three tiers:

| Tier      | Suits                       | Claude        | OpenAI | Gemini     |
|-----------|-----------------------------|---------------|--------|------------|
| Reasoning | Judging findings in context | Opus or Fable | Astra  | Pro        |
| Mid-sized | Applying a known pattern    | Sonnet        | Sol    | Flash      |
| Small     | Retrieving and recording    | Haiku         | Luna   | Flash-Lite |

Each guide suggests a starting point in a block like this one. Adjust it to your codebase.
{: .model }

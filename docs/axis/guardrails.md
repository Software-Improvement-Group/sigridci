---
redirect_from:
  - /integrations/sigrid-mcp/guardrails.html
---

# Guardrails

Guardrails is the Sigrid Axis capability that stops an AI coding agent from introducing security, maintainability, and architecture problems, by checking the agent's work against Sigrid Core before it reaches a commit or a merge.

Guardrails runs two checks:

- **The quality gate** checks each file the agent changed for maintainability and security, before it reports a task done, with the [`guardrails.quality_check`](tools.md#guardrails) MCP tool.
- **The architecture drift check** checks the whole change for new dependencies, cycles, and bypassed facades, before you push, with the [`architecture-drift`](skills.md#architecture-drift) skill.

Each check runs on a standing instruction, which you [set up](#set-up-the-quality-gate) once. The quality gate works on uncommitted code in systems not yet published to Sigrid. The drift check needs a published system, because it compares your diff with Sigrid Core's dependency graph.

For the problems that are already in your code, see [Auto-fix Agents](autofix-agents.md). For a walkthrough of each check in day-to-day work, see [building with Guardrails](../workflows/agents/building-with-guardrails.md) and [preventing architecture drift](../workflows/agents/preventing-architecture-drift.md).

## Supported technologies

The `guardrails.quality_check` tool supports these technologies:

- Java
- Python
- C/C++
- C#
- JavaScript
- TypeScript
- Kotlin
- Progress ABL
- PHP

The [technology support](../reference/technology-support.md#list-of-supported-technologies) page marks them with "Guardrails". The architecture drift check supports every technology marked with "Architecture" on that page.

## Set up the quality gate

Connecting the MCP server is half the setup. The agent does not call the tool unless something tells it to, so the other half is a standing instruction that it runs at a fixed point in every task.

### Claude Code

Install the [Claude Code plugin](installation.md#install-the-claude-code-plugin). Its `UserPromptSubmit` hook adds the instruction below to every prompt you send, so for the quality gate there is nothing to add yourself. The hook is on by default. To turn it off, see [plugin options](configuration.md#plugin-options).

### Other tools

Put the instruction in `AGENTS.md` at the root of your repository, so it applies to every session without you asking. Cursor, GitHub Copilot, Devin, and most other agentic tools read that file. It is the same text the Claude Code hook adds: three **code principles**, and a **quality gate** to pass before reporting a task done:

{% include axis/quality-gate-prompt.md %}

The quality gate applies the [Boy Scout Rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html): leave each file you touch cleaner than you found it.

Two adjustments are worth making from the start. If your codebase follows specific design patterns, such as hexagonal architecture or Redux, add them to the principles line, and write a principle for every recurring mistake you find yourself correcting. You can also loosen the timing to commits only. Either way, you can always ask for the check yourself: "Run Sigrid on these files: ...".

For which wording in that prompt carries it, and a session where the agent refactors in response to a finding, see [building with Guardrails](../workflows/agents/building-with-guardrails.md).

## Set up the architecture drift check

No hook adds this instruction. Add it to `CLAUDE.md` in Claude Code, or to `AGENTS.md` in other tools:

{% include axis/architecture-drift-prompt.md %}

The check needs a published system and a [Sigrid profile](configuration.md#the-sigrid-profile) with your baseline branch, which [`setup`](skills.md#setup) writes. To run it yourself, type `/architecture-drift`. For an example session, see [preventing architecture drift](../workflows/agents/preventing-architecture-drift.md).

## What Guardrails does not see

Neither check sees vulnerable dependencies or duplication spread across files. The quality gate reads one file at a time, and the drift check only looks at the references between directories.

The [`change-feedback`](skills.md#change-feedback) skill covers those before you push. It runs Sigrid CI on your working tree for maintainability, open-source, and security, which finds vulnerable dependencies and duplication across files.

An instruction to the agent is followed most of the time, and the agent is the one who decides it has finished. [Sigrid CI](../sigridci-integration/using-sigridci.md) in a pre-commit hook or in your pipeline gives you a check the agent cannot decide it has already satisfied.

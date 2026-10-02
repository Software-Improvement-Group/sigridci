---
redirect_from:
  - /integrations/sigrid-mcp/guardrails.html
---

# Guardrails

Guardrails is the Sigrid Axis capability that stops an AI coding agent from introducing security and maintainability problems, by checking the code the agent writes against Sigrid Core's quality model while the agent is still working on it.

The check reads your working tree, so the system does not have to be published to Sigrid first, and the code does not have to be committed. It is deterministic: the same metrics against the same thresholds every time, decided by Sigrid's quality model and not by a model's opinion of its own output.

Guardrails consists of three parts:

- **The `guardrails.quality_check` MCP tool** checks one file at a time. It returns the maintainability guidelines the file violates, with a severity and a line range per unit, plus a separate list of security findings. Both lists empty means the file passes. See the [MCP tools reference](tools.md#guardrails).
- **A standing instruction** tells the agent to run that check on the production code it changed before it reports a task done. See [set up the quality gate](#set-up-the-quality-gate).
- **The [`change-feedback`](skills.md#change-feedback) skill** checks your whole local change before you push it, for the problems a check of one file cannot see.

For the problems that are already in your code, see [Auto-fix Agents](autofix-agents.md). For a walkthrough of Guardrails in day-to-day feature work, see [building with Guardrails](../workflows/agents/building-with-guardrails.md).

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

The [technology support](../reference/technology-support.md#list-of-supported-technologies) page marks them with "MCP".

## Set up the quality gate

Connecting the MCP server is half the setup. The agent does not call the tool unless something tells it to, so the other half is a standing instruction that it runs at a fixed point in every task.

### Claude Code

Install the [Claude Code plugin](installation.md#install-the-claude-code-plugin). Its `UserPromptSubmit` hook adds the instruction below to every prompt you send, so there is nothing to add yourself. The hook is on by default. To turn it off, see [plugin options](configuration.md#plugin-options).

### Other tools

Put the instruction in `AGENTS.md` at the root of your repository, so it applies to every session without you asking. Cursor, GitHub Copilot, Devin, and most other agentic tools read that file. It is the same text the Claude Code hook adds: three **code principles**, and a **quality gate** to pass before reporting a task done:

{% include axis/quality-gate-prompt.md %}

The quality gate applies the [Boy Scout Rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html): leave each file you touch cleaner than you found it.

Two adjustments are worth making from the start. If your codebase follows specific design patterns, such as hexagonal architecture or Redux, add them to the principles line, and write a principle for every recurring mistake you find yourself correcting. You can also loosen the timing to commits only. Either way, you can always ask for the check yourself: "Run Sigrid on these files: ...".

For which wording in that prompt carries it, and a session where the agent refactors in response to a finding, see [building with Guardrails](../workflows/agents/building-with-guardrails.md).

## What Guardrails does not see

`guardrails.quality_check` reads one file at a time, so anything that only shows up across the whole system is invisible to it: architecture drift, vulnerable dependencies, and duplication spread across files.

The `change-feedback` skill covers those before you push. With maintainability, open-source, or security, it runs Sigrid CI on your working tree, which finds vulnerable dependencies and duplication across files. With architecture, it checks your diff against Sigrid Core's measured dependency graph for new dependencies, cycles, and facades that were bypassed; see [preventing architecture drift](../workflows/agents/preventing-architecture-drift.md).

An instruction to the agent is followed most of the time, and the agent is the one who decides it has finished. [Sigrid CI](../sigridci-integration/using-sigridci.md) in a pre-commit hook or in your pipeline gives you a check the agent cannot decide it has already satisfied.

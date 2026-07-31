# Sigrid Guardrails MCP

Agent guardrails use Sigrid's code analysis to prevent issues from being introduced. They give your AI coding assistant access to that analysis during generation, so the agent checks its own output as it works. Security vulnerabilities and quality issues get caught before they land in a commit.

This is the counterpart to the [auto-fix agent](autofix-agents.md), which fixes and improves issues that already exist.

For installation instructions, see the [MCP overview page](../integration-sigrid-mcp.md). For a walkthrough of using this in day-to-day feature work, see the guide on [building with an AI coding agent and Sigrid Guardrails](../../workflows/agents/building-with-guardrails.md).

## Supported technologies

Currently supported:

- Java
- Python
- C/C++
- C#
- JavaScript
- TypeScript
- Kotlin
- Progress ABL
- PHP

Visit the [Technology Support](../../reference/technology-support.md#list-of-supported-technologies) page for more details on supported technologies.

## Set up the quality gate

The quality of AI-generated code varies a lot with the instructions the agent was given. Guardrails tells the agent which quality standards its code fails to meet, reading the working tree, so the system does not have to be published to Sigrid first.

Connecting the MCP server is only half of it, since the agent will not call the tool unless something tells it to. The instruction belongs in your agent's instruction file, where it applies to every session without you asking. The prompt below pairs brief **code principles** with a mandatory **quality gate** before any task is reported complete:

{% include sigrid-mcp/quality-gate-prompt.md %}

> The quality gate applies the [Boy Scout Rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html): leave each file you touch cleaner than you found it.

Two adjustments are worth making from the start. If your codebase follows specific design patterns, such as hexagonal architecture or Redux, add them under Code Principles, and write a principle for every recurring mistake you find yourself correcting. You can also loosen the timing to commits only, and you can always invoke the check by hand: "Run Sigrid on these files: ...".

For which wording in that prompt carries it, and a session where the agent refactors in response to a finding, see [building with an AI coding agent and Sigrid Guardrails](../../workflows/agents/building-with-guardrails.md).

### Where to place these instructions

Most AI coding agents respect instruction files in your repository. Refer to your agent's documentation for specifics.

| File | Supported by |
|------|--------------|
| `.cursor/rules/` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `global_rules.md` | Devin Desktop |
| `CLAUDE.md` | Claude Code |
| `AGENTS.md` | OpenCode, emerging convention (check agent support) |

For tools that support both global and project-level rules, prefer project-level to keep instructions versioned with your code.

## What Guardrails does not see

Guardrails reads one file at a time, so anything that only shows up across a whole system stays invisible to it: architecture drift, vulnerable dependencies, duplication spread across files. [Sigrid CI](../../sigridci-integration/using-sigridci.md) covers those. Running it in a pre-commit hook or in your pipeline also gives you a check the agent cannot decide it has already satisfied.

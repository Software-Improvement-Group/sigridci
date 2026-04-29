# Sigrid Guardrails MCP

Guardrails gives your AI coding assistant access to Sigrid's code analysis during generation. The agent checks its own output as it works — security vulnerabilities and quality issues get caught before they land in a commit.

For installation instructions, see the [MCP overview page](../integration-sigrid-mcp.md).

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

## Using Sigrid Quality Gates with AI Coding Agents

AI-generated code quality varies significantly based on the instructions given. The Sigrid MCP provides guardrails that notify agents when code doesn't meet quality standards without requiring the system to be published to Sigrid first.

We recommend combining two elements:
1. **Code principles**: brief guidelines that help the agent write good code upfront
2. **Quality gate**: a mandatory check using Sigrid before completing any task

### Recommended prompt

Add this to your agent instructions (see [where to place these instructions](#where-to-place-these-instructions)):

```
## Code Principles

Write maintainable code: single responsibility, small focused functions, clear naming, avoid duplication, simple control flow.
Write secure code.

## MANDATORY: Quality Gate

Before reporting ANY task as complete:

1. Run the Sigrid Code Quality Guardrails tool on all changed production code
2. Maintainability findings: accept if principles were followed, otherwise refactor
3. Security findings: fix if straightforward, otherwise flag to user

Do not skip this step.
```

For stricter workflows, add a rescan step: "If fixes were made, rescan to verify no new issues were introduced."

### Where to place these instructions

Most AI coding agents respect instruction files in your repository. Refer to your agent's documentation for specifics.

| File | Supported by |
|------|--------------|
| `.cursor/rules/` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.windsurfrules` | Windsurf |
| `CLAUDE.md` | Claude Code |
| `AGENTS.md` | OpenCode, emerging convention (check agent support) |

For tools that support both global and project-level rules, prefer project-level to keep instructions versioned with your code.

### Customizing for your codebase

The prompt above is a starting point. Consider these adjustments:

- **Framework conventions**: If your codebase follows specific design patterns (e.g., hexagonal architecture, Redux patterns), add them to the code principles section.
- **Check frequency**: You may prefer to run the quality gate with a different frequency, e.g. only before commits rather than after every task.
- **Direct invocation**: You can also ask the agent directly: "Run Sigrid on these files: ..."
- **Iterate from experience**: When the agent makes recurring mistakes, add a principle that addresses the pattern.

> **Tip**: Start with concise principles. Add explicit guidance only if the model struggles.

Pair the MCP with Sigrid CI to also catch architecture issues, vulnerable dependencies, and cross-file metrics.

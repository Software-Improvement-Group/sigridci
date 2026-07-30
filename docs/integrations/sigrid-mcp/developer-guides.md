# Developer guides

Each of these guides follows one job through on a real codebase: what to configure, what a session looks like, and how to check what the agent actually did. For the tools underneath them, with their parameters and the finding statuses, see [Guardrails](guardrails.md) and [auto-fix agents](autofix-agents.md).

- [Building with an AI coding agent and Sigrid Guardrails](developer-guides/building-with-guardrails.md) puts Guardrails in the feature loop, so the agent checks each file it writes before you ever see the diff.
- [Reducing technical debt with auto-fix agents](developer-guides/reducing-technical-debt.md) works through the refactoring candidates for your weakest maintainability property.
- [Triaging security and reliability findings](developer-guides/triaging-security-reliability.md) assesses a finding backlog in context and records each decision with a rationale.
- [Remediating open source risk](developer-guides/remediating-open-source-risk.md) runs unattended when new dependency risk appears, and opens a merge request for you to review.

These four are workflows we run ourselves, and they are a good place to start: try one out on your own codebase and you will learn quickly what these agents are good at and where you want something different.

They do not cover everything that Sigrid MCP can do. The [Sigrid MCP doc](../integration-sigrid-mcp.md) lists every tool available, so start there for a workflow that is not on this page.
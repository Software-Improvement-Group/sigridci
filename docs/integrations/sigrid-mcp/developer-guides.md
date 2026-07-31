# Developer guides

Each of these guides follows one job through on a real codebase: what to configure, what a session looks like, and how to check what the agent actually did. For the tools underneath them, with their parameters and the finding statuses, see [Guardrails](guardrails.md) and [auto-fix agents](autofix-agents.md).

- [Building with an AI coding agent and Sigrid Guardrails](developer-guides/building-with-guardrails.md) puts Guardrails in the feature loop, so the agent checks each file it writes before you ever see the diff.
- [Reducing technical debt with auto-fix agents](developer-guides/reducing-technical-debt.md) works through the refactoring candidates for your weakest maintainability property.
- [Triaging security and reliability findings](developer-guides/triaging-security-reliability.md) assesses a finding backlog in context and records each decision with a rationale.

These three are workflows we run ourselves, and they are a good place to start: try one out on your own codebase and you will learn quickly what these agents are good at and where you want something different.

They also do not cover everything that Sigrid MCP can do. The [Sigrid MCP doc](../integration-sigrid-mcp.md) lists every tool available, so start there for a workflow that is not on this page.

## Where Sigrid fits in an agentic workflow

{% include sigrid-mcp/lifecycle-circle.md %}

An agent that writes code in your repository needs to know what the system looks like, what is worth working on, and whether the change it just made is safe. Sigrid answers those from analysis of your own codebase.

That gives four steps of an agentic development cycle where Sigrid does something for you:

- **Grounding:** Sigrid gives your agents a continuous, accurate map of your architecture, so they act with full context and spend fewer tokens getting there.
- **Plan:** Sigrid surfaces current and emerging risks, and writes the plan to fix them.
- **Prevent:** Sigrid checks every agent change against your architecture, security, and quality standards, so architecture drift and new vulnerabilities do not get in.
- **Improve:** Sigrid refactors technical debt and security risks autonomously.

The guides above cover parts of this cycle, and the tools enable more than the guides describe. We are working on more guides, skills, and tools.
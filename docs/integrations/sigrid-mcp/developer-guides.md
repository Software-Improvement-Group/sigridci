# Developer guides

The [Guardrails](guardrails.md) and [auto-fix agent](autofix-agents.md) pages describe the tools: the MCP tools, the skills, the parameters, the statuses. These guides describe the work. Each one covers a single job on a real codebase, with the setup, one worked session, and how to tell a good run from a bad one.

| Guide | What it covers |
| --- | --- |
| [Building with an AI coding agent and Sigrid Guardrails](developer-guides/building-with-guardrails.md) | Checking maintainability and security on code as the agent writes it, before you see the diff |
| [Reducing technical debt with auto-fix agents](developer-guides/reducing-technical-debt.md) | Working the refactoring candidates for your weakest maintainability property |
| [Triaging security and reliability findings](developer-guides/triaging-security-reliability.md) | Assessing findings in context and recording a decision with a rationale |
| [Remediating open source risk](developer-guides/remediating-open-source-risk.md) | Running unattended when new dependency risk appears, and reviewing the merge request it opens |

Start with Guardrails. It needs the least setup, it applies to every session in which an agent writes code, and it stops the debt the other three guides are about clearing. The other three each need a system published to Sigrid, and you can read them in any order.

Every guide is readable on its own, so there is some repetition between them, mostly in the setup steps.

The concepts apply to any agentic CLI. The worked configuration examples use Claude Code, since that is the only CLI we ship a plugin for, and each guide names the generic equivalent of whatever it configures.

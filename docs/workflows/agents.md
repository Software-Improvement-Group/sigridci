# For using agents

Each of these guides follows one job through on a real codebase: what to configure, what a session looks like, and how to check what the agent actually did. For the tools underneath them, with their parameters and the finding statuses, see [Guardrails](../integrations/sigrid-mcp/guardrails.md) and [auto-fix agents](../integrations/sigrid-mcp/autofix-agents.md).

- [Building with an AI coding agent and Sigrid Guardrails](agents/building-with-guardrails.md) puts Guardrails in the feature loop, so the agent checks each file it writes before you ever see the diff.
- [Reducing technical debt with auto-fix agents](agents/reducing-technical-debt.md) works through the refactoring candidates for your weakest maintainability property.
- [Triaging security and reliability findings](agents/triaging-security-reliability.md) assesses a finding backlog in context and records each decision with a rationale.

These three are workflows we run ourselves, and they are a good place to start: try one out on your own codebase and you will learn quickly what these agents are good at and where you want something different.

They also do not cover everything that Sigrid MCP can do. The [Sigrid MCP doc](../integrations/integration-sigrid-mcp.md) lists every tool available, so start there for a workflow that is not on this page.

## Where Sigrid fits in an agentic workflow

{% include sigrid-mcp/lifecycle-circle.md %}

An agent that writes code in your repository needs to know what the system looks like, what is worth working on, and whether the change it just made is safe. Sigrid answers those from analysis of your own codebase.

That gives four steps of an agentic development cycle where Sigrid does something for you:

- **Grounding:** Sigrid gives your agents a continuous, accurate map of your architecture, so they act with full context and spend fewer tokens getting there.
- **Plan:** Sigrid surfaces current and emerging risks, and writes the plan to fix them.
- **Prevent:** Sigrid checks every agent change against your architecture, security, and quality standards, so architecture drift and new vulnerabilities do not get in.
- **Improve:** Sigrid refactors technical debt and security risks autonomously.

The guides above cover parts of this cycle, and the tools enable more than the guides describe. We are working on more guides, skills, and tools.

## LLM model selection

Which LLM model you want depends on how much of the work is judgment, and you cannot switch models mid-session. One model runs your session from the first prompt, and starting a subagent is the only way to get a second one involved. So there are two decisions here: which model runs the session, and whether any step is worth handing off.

Three tiers cover the work in these guides, and every vendor ships some version of the same ladder:

| What the step needs | Claude | OpenAI | Gemini |
|---|---|---|---|
| **Small.** Retrieving findings, recording statuses, summarizing a batch | Haiku | GPT mini | Flash-Lite |
| **Mid-sized.** Following a written procedure, editing code to a known pattern | Sonnet | GPT | Flash |
| **Reasoning.** Assessing a finding against how your system actually works | Opus | GPT at high reasoning | Pro |

Reasoning effort is the second dial. It earns its cost on the mid-sized and reasoning tiers, and does nothing for retrieval. Some vendors expose the top rung as an effort setting on one model, so for them the two dials are one. A single model runs your whole session, so pick for the hardest step in the loop.

Hand a step to a subagent only when it is self-contained. A subagent starts with an empty context and returns a summary, so a step that depends on what your session has already read comes back weaker and burns more tokens getting there. The `osh-researcher` agent we ship works this way: it looks up published advisories for one dependency over the web, with no access to your files and none to Sigrid. We pin it to a mid-sized model.

Every guide carries its own recommendation, in a block marked like this one.
{: .model }
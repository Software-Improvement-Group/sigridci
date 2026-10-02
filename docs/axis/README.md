---
permalink: /axis/
---

# Sigrid Axis

Sigrid Axis gives your AI coding agents Sigrid's analysis of your own system while they work, so they can anchor each change in your measured architecture, plan what is worth fixing, catch problems before they merge, and improve the code that is already there.

An agent optimizes for the task you gave it, and it can only check part of that task by itself. It can run the tests. It cannot measure whether a unit is too complex, see a dependency on a file it never opened, or tell a real vulnerability from a false alarm without knowing how your system is deployed. Those answers need the whole system, measured the same way every time, and a model's opinion of its own output is not that.

Sigrid Core already has those answers. Sigrid Axis puts them inside the agent's loop.

## Sigrid Core and Sigrid Axis

Sigrid Core is the analysis platform you may already know: it measures maintainability, architecture, security, reliability, and open source health, and it keeps the findings, ratings, and dependency graphs you see in the Sigrid dashboards and in [Sigrid CI](../sigridci-integration/using-sigridci.md).

Sigrid Axis brings that analysis to AI coding agents. It consists of the Sigrid Axis MCP server, which gives an agent tools that read from Sigrid Core and write triage decisions back to it, and a set of skills, which give the agent procedures for using those tools. MCP and skills are open standards, so Axis works in any agentic tool that supports them. Axis does not analyze anything on its own. Every rating, finding, and graph edge an agent sees through Axis comes from Sigrid Core, and every status it writes back shows up in Sigrid Core.

Axis works with Sigrid On-Premise too, through the [on-premise Sigrid Axis MCP server](../organization-integration/onpremise-mcp.md).

## The agentic lifecycle

{% include axis/lifecycle-circle.md %}

We think of agentic development as a cycle of four phases, and Sigrid Axis does something different in each one:

- **Ground:** the agent learns how your system is actually wired from Sigrid Core's dependency graph, so it acts on the real structure and spends fewer tokens getting there.
- **Plan:** Axis reads the current state of the system and the open findings, decides what is worth fixing, and writes that plan down.
- **Prevent:** Axis checks every change the agent makes against your quality, security, and architecture standards, before it reaches a commit or a merge.
- **Improve:** Axis fixes what the plan named, one reviewable commit at a time.

## Two capabilities

Sigrid Axis has two capabilities today.

[Guardrails](guardrails.md) covers the Prevent phase. It checks the code an agent writes while the agent is still working on it, and it checks a local change against Sigrid before you push. It consists of the `guardrails.quality_check` MCP tool, a standing instruction that gets the agent to run that check, and the [`change-feedback`](skills.md#change-feedback) skill.

[Auto-fix Agents](autofix-agents.md) covers the other three phases, for the problems Sigrid Core has already found:

- Ground: the [`explore-architecture`](skills.md#explore-architecture) skill and the `architecture-explorer` agent.
- Plan: the [`diagnose`](skills.md#diagnose) skill for maintainability and architecture, and the [`triage-findings`](skills.md#triage-findings) skill for security, reliability, and open source findings.
- Improve: the [`autofix`](skills.md#autofix) skill.

The [`setup`](skills.md#setup) skill sits outside both. It records which Sigrid system a repository belongs to, and every other skill reads that.

## Get started

Start with [installing Sigrid Axis](installation.md): connect the MCP server, install the skills, and add the Guardrails instruction, which the Claude Code plugin does for you.

Then pick the [guide](../workflows/agents/README.md) for the job in front of you. Each one follows that job through on a real codebase: what to configure, what a session looks like, and how to check what the agent did.

## LLM model selection

Which LLM you want depends on how much of the work is judgment, and you cannot switch models mid-session. One model runs your session from the first prompt, and starting a subagent is the only way to get a second one involved. So there are two decisions here: which model runs the session, and whether any step is worth handing off.

Three tiers cover the work in these guides, and every vendor ships some version of the same ladder:

| What the step needs                                                           | Claude | OpenAI | Gemini |
|-------------------------------------------------------------------------------|---|---|---|
| **Small:** Retrieving findings, recording statuses, summarizing a batch       | Haiku | Luna | Flash-Lite |
| **Mid-sized:** Following a written procedure, editing code to a known pattern | Sonnet | Sol | Flash |
| **Reasoning:** Assessing a finding against how your system actually works     | Opus or Fable | Astra | Pro |

Reasoning effort is the second dial. It earns its cost on the mid-sized and reasoning tiers, and does nothing for retrieval. Some vendors expose the top rung as an effort setting on one model, so for them the two dials are one. A single model runs your whole session, so pick for the hardest step in the loop.

Hand a step to a subagent only when it is self-contained. A subagent starts with an empty context and returns a summary, so a step that depends on what your session has already read comes back weaker and burns more tokens getting there. The two agents we ship work this way. The `osh-researcher` looks up published advisories for one dependency over the web, with no access to your files and none to Sigrid, and we pin it to a mid-sized model. The `architecture-explorer` answers one structural question from Sigrid's graph and your files, and we pin it to a small one.

Every guide carries its own recommendation, in a block marked like this one.
{: .model }

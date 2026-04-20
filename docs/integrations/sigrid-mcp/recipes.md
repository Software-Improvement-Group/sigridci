# Sigrid Modernization Recipes MCP

Modernization Recipes gives AI agents a prioritized list of refactoring targets from Sigrid. The agent works through the list, makes fixes, and marks each finding as resolved.

For installation instructions, see the [MCP overview page](../integration-sigrid-mcp.md).

## Before you start

You need:

- A Sigrid account with at least one system that has maintainability results
- The Sigrid MCP server connected to your AI coding agent (see [installation](../integration-sigrid-mcp.md))
- A local checkout of the system's repository
- Your Sigrid customer and system identifiers — the agent needs these to query the right system. You can pass them in your prompt or add them to your agent's context file (e.g. `CLAUDE.md`, `.cursor/rules/`)

## Tools

Two MCP tools make up the workflow:

**`sigrid_refactoring_candidates`** retrieves a ranked list of refactoring candidates from Sigrid for a given [maintainability property](../../reference/sig-quality-models.md). You can filter by technology and limit the number of results.

**`edit_sigrid_finding_status`** updates the status of a finding. Use it to mark findings as planned for fixing, accepted as-is, or resolved — so Sigrid reflects the decisions the agent made.

## Workflow

The basic loop:

1. The agent fetches refactoring candidates for a maintainability property
2. It reads the code, assesses the findings, and decides what to do — fix, refactor, or accept the risk
3. For findings it can fix, it implements the change
4. It updates the finding status in Sigrid to reflect what happened

The agent doesn't have to fix everything blindly. It can prioritize based on impact, spot patterns across findings, group related issues into a single refactoring, or accept findings where the current code is justified. Think of it as a developer working through a backlog — some items get fixed, some get triaged.

> **Beta:** Modernization Recipes is in early access. The current tools cover the core refactoring workflow — we're actively adding more tools and workflows.

## Getting started

Here are a few example prompts to try. Adapt them to your codebase.

**Direct fix:**
```
Get unit size findings for [customer]/[system] in Java. Refactor the longest methods. Update each finding status when done.
```

**Architectural refactoring:**
```
Get module coupling findings for [customer]/[system]. For each module, check whether it follows single responsibility. If it doesn't, split it into focused files. If it already has a clear single purpose and is small, mark as accepted. Update finding statuses to reflect your decisions.
```

**Triage:**
```
Get the top 100 duplication findings for [customer]/[system]. We accept duplication in boilerplate configuration between microservices — mark those as accepted. Mark the rest as will-fix.
```

**Execute after triage:**
```
Get duplication findings for [customer]/[system] with status will-fix. Fix them and update the status.
```

**Explore:**
```
Get maintainability findings for [customer]/[system]. What patterns do you see? Suggest a refactoring strategy before making changes.
```

## Workflows

The prompts above are a starting point. You can combine approaches, adjust the level of autonomy, or come up with entirely different workflows.

### Autonomous fixing

Give the agent a target property, your decision criteria, and let it work through findings in a loop. This works when you can spell out what "good" looks like before it starts.

What to include in your prompt:
- Which maintainability property and technology to target
- Your coding principles and framework conventions (e.g. "methods should have a single responsibility", "we use the repository pattern for data access")
- When to fix vs. when to accept (e.g. "if the module is small and already follows single responsibility, mark as accepted")
- That it should update finding statuses as it goes

### Discovery and prioritization

The agent fetches findings, reads the surrounding code, and reports back without changing anything. Good for getting an overview, finding patterns, or building a shortlist for ticket creation.

What to include in your prompt:
- Which property to analyze
- What you're looking for (worst offenders, clusters of related issues, recurring patterns)
- How to present the results (ranked list, grouped by module, with suggested actions)

### Execute pre-triaged work

Tell the agent to pick up findings already marked as will-fix in Sigrid, from a previous triage, a discovery run, or manual review, and fix them.

What to include in your prompt:
- That it should only work on findings with status will-fix
- How to handle edge cases (e.g. if a fix is too complex or risky, flag it instead of changing code)

These compose: run discovery first, triage the results, then execute on the will-fix items. Or skip to autonomous fixing if you trust the criteria.

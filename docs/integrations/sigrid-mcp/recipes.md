# Sigrid Modernization Recipes MCP

Modernization Recipes gives AI agents a prioritized list of refactoring targets from Sigrid. The agent works through the list, fixes what it can, and marks each finding as resolved.

For installation instructions, see the [MCP overview page](../integration-sigrid-mcp.md).

## Before you start

You need:

- A Sigrid account with at least one system that has maintainability results
- The Sigrid MCP server connected to your AI coding agent (see [installation](../integration-sigrid-mcp.md))
- A local checkout of the system's repository
- Your Sigrid customer and system identifiers. Pass them in your prompt or add them to your agent's context file (e.g. `CLAUDE.md`, `.cursor/rules/`)

## Tools

Two MCP tools drive the workflow:

**`sigrid_refactoring_candidates`** retrieves a ranked list of refactoring candidates from Sigrid for a given [maintainability property](../../reference/sig-quality-models.md). You can filter by technology and limit the number of results.

**`edit_sigrid_finding_status`** updates the status of a finding. Use it to mark findings as planned for fixing, accepted as-is, or resolved, so Sigrid reflects the decisions the agent made.

## Workflow

The basic loop:

1. The agent fetches refactoring candidates for a maintainability property
2. It reads the code, assesses each finding, and decides what to do: fix, refactor, or accept the risk
3. For findings it can fix, it implements the change
4. It updates the finding status in Sigrid to reflect what happened

The agent doesn't have to fix everything blindly. It can prioritize by impact, spot patterns across findings, group related issues into one refactoring, or accept findings where the current code is justified. Think of it as working through a backlog: some items get fixed, some get triaged.

> **Beta:** Modernization Recipes is in early access. The current tools cover the core refactoring workflow. We're actively adding more.

## Getting started

A few workflows to try. Adapt the prompts to your codebase, combine them, or do something different entirely.

### Autonomous fixing

Give the agent a target property and your decision criteria, and let it work through findings in a loop. Works best when you can spell out what "good" looks like before it starts.

What to include in your prompt:
- Which maintainability property and technology to target
- Your coding principles and framework conventions (e.g. "methods should have a single responsibility", "we use the repository pattern for data access")
- When to fix vs. when to accept (e.g. "if the module is small and follows single responsibility, mark as accepted")
- That it should update finding statuses as it goes

**Example — direct fix:**
```
Get unit size findings for [customer]/[system] in Java. Refactor the longest methods. Update each finding status when done.
```

**Example — architectural refactoring:**
```
Get module coupling findings for [customer]/[system]. For each module, check whether it follows single responsibility. If it doesn't, split it into focused files. If it already has a clear single purpose and is small, mark as accepted. Update finding statuses to reflect your decisions.
```

### Discovery and prioritization

The agent fetches findings, reads the surrounding code, and reports back without changing anything. Useful when you want an overview or a shortlist for ticket creation.

What to include in your prompt:
- Which property to analyze
- What you're looking for (worst offenders, clusters of related issues, recurring patterns)
- How to present the results (ranked list, grouped by module, suggested next steps)

**Example:**
```
Get maintainability findings for [customer]/[system]. What patterns do you see? Suggest a refactoring strategy before making changes.
```

### Triage and execute

Split the work into two steps: triage findings first (mark as will-fix or accepted), then pick up the will-fix items and fix them. Both steps can happen in one session, or you triage now and execute later.

**Example — triage:**
```
Get the top 100 duplication findings for [customer]/[system]. We accept duplication in boilerplate configuration between microservices — mark those as accepted. Mark the rest as will-fix.
```

**Example — execute after triage:**
```
Get duplication findings for [customer]/[system] with status will-fix. Fix them and update the status.
```

These compose: run discovery first, triage the results, then execute on the will-fix items. Or skip to autonomous fixing if you trust the criteria.

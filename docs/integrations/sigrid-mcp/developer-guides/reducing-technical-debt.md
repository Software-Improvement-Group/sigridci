# Reducing technical debt with auto-fix agents

This guide walks through using an [auto-fix agent](../autofix-agents.md) to work down the maintainability debt Sigrid already found in your codebase, taking the ranked refactoring candidates in the order that actually moves your rating.

That order is not the obvious one. A hundred medium-severity findings routinely outweigh a handful of very high ones, because Sigrid's ratings are LOC-weighted: what a finding contributes is the amount of code it puts in a bad risk bracket, measured against the size of the whole system. Sorting by severity and starting at the top is why a week of refactoring can leave a rating exactly where it was.

The `sigrid-diagnose` skill decides what to work on, and `sigrid-improve` does the work, verifying each change with Guardrails before it moves on.

You would run this deliberately, with time set aside: a debt-reduction day, the slack at the end of a sprint, or the week before you start work in a module you know is bad. Pick a stretch where you can review and merge a series of refactors without a release waiting on them. It suits diffuse debt, dozens of long units or duplication spread across a package.

This covers maintainability only. Security and reliability findings behave differently and have their own guide: [triaging security and reliability findings](triaging-security-reliability.md).

## Prerequisites

- A system published to Sigrid.
- An agentic CLI that can call MCP tools, with the `sigrid-diagnose` and `sigrid-improve` skills available. The configuration below uses Claude Code.
- A [Sigrid API token](../../../organization-integration/authentication-tokens.md) for the MCP server, which the plugin installer asks for once.

## Why the agent needs help

Ask an agent to "improve maintainability in this repository" and it will do something reasonable that barely moves your rating. The instruction sounds actionable but is not, because two of the things it needs are missing from the code it can read.

It cannot see the whole system. An agent picks targets from whatever it read into context, and ten files it happened to open are not the ten files that matter. On a large codebase the ratio of read to unread is not close.

It also has no model of impact. Without the LOC weighting it judges severity by eye, so it optimizes the number of findings closed and not the rating. Closing eleven small findings and reporting a successful run is a plausible outcome that moves nothing.

Sigrid supplies the global view: which property is weakest, which candidates carry the most rated code, and which candidates appear under several properties at once, where a single fix moves more than one rating. You supply what no rating can express: the conventions of your own codebase, and how much change you are willing to review in one go.

## Set up the agent

{% include sigrid-mcp/primitives.md %}

This workflow leans on the third one, since the two skills carry most of the procedure.

### 1. Install the plugin and record your profile

{% include sigrid-mcp/plugin-install.md setup=true %}

The first two commands configure the MCP server and the skills together. `/sigrid:setup` is easy to skip, and it is the one that matters most here: it records which Sigrid system this repository maps to, which branch Sigrid analyzes, and how your team handles branches and change requests. The skills read it at the start of every run, so you answer these questions once instead of every session. See [plugin configuration](../configuration.md) for what it stores and where.

On another CLI, take the skills from the [sigrid-ai-toolkit](https://github.com/Software-Improvement-Group/sigrid-ai-toolkit) and adapt them. See [before you start](../autofix-agents.md#before-you-start) for the identifiers Sigrid needs and where to put them.

### 2. Work on a branch

An ordinary git precaution, not a Sigrid requirement. A run produces a series of independent commits, so start from a clean tree on a fresh branch, and you can drop one refactor out of ten without redoing the other nine.

## What a session looks like

Two commands, and the order is not optional. The first diagnoses:

```
/sigrid:sigrid-diagnose
```

The skill fetches the current ratings, pulls the top candidates for all seven maintainability properties, and reasons across them. On a system whose duplication is weakest, what comes back is not "duplication is 1.3 stars" but which risk tier carries that score, and whether it is a few enormous clones or a long tail of medium ones. Those call for different work. Candidates that appear under two or more properties come first, since a 300-line method that is also a duplication finding fixes two ratings at once. And it reads the shape of the problem: a cluster of near-identical DAO classes is one structural fix, not eleven separate ones.

Nothing changes on disk yet. Read the diagnosis and disagree with it where you have context it lacks, such as knowing which module is being replaced next quarter. Then:

```
/sigrid:sigrid-improve
```

It asks which mode you want:

| Mode | What it does | When |
|---|---|---|
| **Interactive** | Presents the candidate list, you pick the order, it shows each diff and asks before continuing | First run on a codebase, or any module you do not know well |
| **Autonomous** | Works the full list from the diagnosis, you review the diffs at the end | Once you have seen the kind of change it makes and written down the limits you care about |

We would start interactive. You are calibrating whether the agent's idea of a good refactor matches yours, and that is much cheaper to find out one diff at a time. Calibrate per codebase, not once: a repository with unusual conventions needs the interactive run again.

Per candidate it reads the whole file before touching anything, makes the change, updates every call site of a changed signature, runs Guardrails to confirm no new findings appeared, and runs your formatter and type check. If a change introduces a new finding or breaks the build, it tries once more and then reverts that candidate instead of digging.

Two behaviors are worth knowing before you start. It does not touch code for the three architecture-level properties (`moduleCoupling`, `componentIndependence`, `componentEntanglement`); for those it explains the problem and proposes a restructuring plan for you to decide on. We think that is the right call, because those fixes are design decisions and not extractions. It also does not update finding statuses on its own. If you want Sigrid to reflect what happened, ask in the same session, while the finding UUIDs are still in context:

```
Update the status of the candidates we just fixed to WILL_FIX, with a remark
naming the commit. Mark the ones we agreed to leave as ACCEPTED, with the reason.
```

Make that request before the session ends. An accepted finding with a written reason is a decision your team keeps. An unrecorded one is a finding you re-triage next quarter, and the UUIDs are gone once the session is.

It will also stop and ask about context it cannot get from the code: serialization constraints, callers outside the repository, a migration window. In autonomous mode it skips those and logs them. That is the right trade, and it does mean the skipped list is part of the output you need to read.

## Check that the work was real

Start with behavior. The tests pass and the diff contains no new behavior. If a refactor needed a test changed, then more than the structure moved: either the test was asserting the old structure, or the behavior itself changed. Both need your judgment.

Ratings come last, and the dashboard will not show movement yet. Sigrid rates the branch it is configured to analyze, so your refactors only reach the ratings once they are merged and that branch has been analyzed again. Two things answer the question before then:

- Push the branch and open a merge request. Your [Sigrid CI](../../../sigridci-integration/using-sigridci.md) step reports Sigrid's verdict on the changed code in the pipeline, before anyone merges.
- Call the `/sigrid-ci-feedback` skill with the `maintainability` capability. It analyzes your working tree locally and returns the same maintainability feedback, publishing nothing to Sigrid. It reads a `SIGRID_CI_TOKEN` from your environment, separate from the token the plugin stored in your keychain.

We should be honest about expectations here, because ratings are measured against total system size, so a handful of refactors on a large codebase will not move a star rating. Clusters move ratings. If nothing moved after a substantial run, you worked the long tail instead of the mass, so go back to the diagnosis and ask which candidates carry the most LOC in a bad risk bracket.

## Turn what you rejected into a rule

Rejecting a diff usually means the agent hit something specific to your codebase that it had no way to know, and it will hit the same thing next run unless you write it down. The ones worth writing read like this: behavior-preserving only, and ask before changing a public API or a serialization format; new units follow the naming and layering conventions of the file they came out of; one candidate per commit, naming the finding it addresses.

Rules like these go in your agent's context file, such as `AGENTS.md` or `CLAUDE.md`. Once the set settles, move it to a file of its own, such as `REFACTORING_RULES.md`, and point to that from your context file.

Code that should never be a candidate is a different problem and has a better home. For anything you do not want rated, such as generated sources that live under your source root, add an `exclude` pattern to your [analysis scope configuration](../../../reference/analysis-scope-configuration.md). Then those candidates stop arriving at all.

## Where to go next

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) to stop new debt while you clear the old
- [Triaging security and reliability findings](triaging-security-reliability.md) for different findings and a different loop
- [Auto-fix agents MCP reference](../autofix-agents.md) for the full tool and status reference

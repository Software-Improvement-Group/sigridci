# Reducing technical debt with auto-fix agents

<div><a href="{% link axis/README.md %}#the-agentic-lifecycle">{% include axis/lifecycle-strip.md active="plan,improve" %}</a></div>

This guide walks through using [Auto-fix Agents](../../axis/autofix-agents.md) to work down the maintainability debt Sigrid already found in your codebase, taking the ranked refactoring candidates in the order that actually moves your rating.

That order is not the obvious one. A hundred medium-severity findings routinely outweigh a handful of very high ones, because Sigrid's ratings are LOC-weighted: what a finding contributes is the amount of code it puts in a bad risk bracket, measured against the size of the whole system. Sorting by severity and starting at the top is why a week of refactoring can leave a rating exactly where it was.

The `diagnose` skill decides what to work on, and `autofix` does the work, verifying each change with your tests and Guardrails before it moves on.

You would run this deliberately, with time set aside: a debt-reduction day, the slack at the end of a sprint, or the week before you start work in a module you know is bad. Pick a stretch where you can review and merge a series of refactors without a release waiting on them. It suits diffuse debt, dozens of long units or duplication spread across a package.

This guide covers maintainability. Security and reliability findings work differently and have their own guide, [triaging security and reliability findings](triaging-security-and-reliability-findings.md).

## Prerequisites

You need the following before you start:

- A system published to Sigrid, so Sigrid Core has rated it.
- The [Claude Code plugin](../../axis/installation.md#install-the-claude-code-plugin), or another agentic tool with the skills and the Sigrid Axis MCP server.
- A local checkout of the repository, with commands to build it and run its tests.

## Why the agent needs help

Ask an agent to "improve maintainability in this repository" and it will do something reasonable. Your rating will barely move.

An agent picks its targets from the files it has read. On a large codebase, that is a handful out of thousands, and nothing says those are the ones that matter.

It also does not know what counts. Sigrid's rating is based on how much of your code is in bad shape, so one enormous method can weigh more than twenty small ones. An agent judging by eye goes for the findings that look worst, or the ones that are quickest to close. It can close eleven small findings, report a successful run, and leave the rating exactly where it was.

Sigrid knows which property is weakest, which code carries the most weight, and which pieces show up under several properties at once, where one fix improves more than one rating. You know what no rating can tell it: the conventions of your codebase, and how much change you are willing to review in one go.

## Set up the agent

{% include axis/primitives.md %}

This workflow leans on the third row, since the two skills carry most of the procedure.

### 1. Install the plugin and record your profile

Install the plugin, then run `setup` in the repository:

{% include axis/plugin-install.md setup=true %}

`setup` is easy to skip, and it is the step that matters most here. It writes `.sigrid/profile.md`, which records the Sigrid system this repository maps to, the baseline branch Sigrid analyzes, and how your team names branches. The skills read it at the start of every run, so you answer these questions once instead of every session. Commit the file, so your team shares it. See [configuration](../../axis/configuration.md#the-sigrid-profile) for what it contains.

In another agentic tool, [install the skills and connect the MCP server](../../axis/installation.md#use-the-skills-in-other-agentic-tools) instead.

### 2. Know which branch you end up on

`autofix` needs a clean working tree, or it asks. When you start on the baseline branch, it creates a new branch for the run. When you start on a branch that already contains the baseline, it stays there, and otherwise it asks. It never fetches or pulls.

Each candidate becomes a commit of its own, so you can drop one refactor out of ten without redoing the other nine.

A mid-sized model handles most of what follows, since extracting a method and updating its call sites is procedural work. See [LLM model selection](../../axis/README.md#llm-model-selection).
{: .model }

## What a session looks like

The session takes two commands, and the order matters. The first one plans:

```
/diagnose maintainability
```

The skill fetches the ratings of all seven maintainability properties, pulls the top candidates for each, and reasons across them. On a system whose duplication is weakest, what comes back is not just "duplication is 1.3 stars" but the shape behind it: a concentrated cluster of a few enormous clones, or a long tail of medium ones. Those call for different work. A cluster of near-identical DAO classes is one structural fix, not eleven separate ones. Candidates that appear under two or more properties come first, since a 300-line method that is also a duplication finding improves two ratings at once.

The report names one primary candidate and the runner-ups, each as a problem and a solution in terms of the code. It also lists the candidates it rejected and the rule that removed each one: generated or test code, a finding your team already marked `ACCEPTED`, a fix that would make another property worse, or a fix that needs a change to a public API or a serialized format.

Nothing changes on disk yet. Read the diagnosis and disagree with it where you have context it lacks, such as knowing which module is being replaced next quarter. At the end, the skill writes a [handover](../../axis/skills.md#handovers) and offers to fix it now, save it for later, or stop. After a long diagnosis, save it and start the fix in a fresh session:

```
/autofix maintainability
```

`autofix` picks up the handover and works through it, primary candidate first. For each candidate, it:

1. Reads the whole file before touching anything.
2. Runs the tests that cover the code, so a failure afterwards is known to be its own. If nothing covers it, it adds a test for the behavior it is about to move.
3. Makes the change, and updates every call site of a changed signature.
4. Runs the tests again, runs Guardrails on every changed file, and runs your formatter.
5. Commits the candidate on its own.

If a change breaks the build or the tests, introduces a new Guardrails finding, or does not improve the metric, it tries one different approach. If that fails too, it reverts the candidate, logs why, and moves on.

The skills ask only at real decision points you have not already answered. A refactor that runs into context the code does not show, such as a serialization constraint, callers outside the repository, or a migration window, is such a point. If you told the skill not to ask, it skips that candidate and logs it. Either way, the skipped list is part of the output you need to read. See [how the skills interact with you](../../axis/skills.md#how-the-skills-interact-with-you).

`autofix` handles `unitSize`, `unitComplexity`, `unitInterfacing`, `duplication`, and `moduleCoupling`. It does not change code for the two component-level properties, `componentIndependence` and `componentEntanglement`. Those fixes are design decisions and not extractions, so it points you to `/diagnose architecture` instead. See [improving architecture](improving-architecture.md).

It stops at local commits. Review the branch, then push it and open the merge request or pull request yourself.

## Record what you decided

`autofix` does not change the status of maintainability findings. If you want Sigrid to reflect what happened, ask for it. The handover keeps the Sigrid finding IDs, so this works in the same session or a later one:

```
Set the candidates we fixed to WILL_FIX, with a remark naming the commit.
Mark the ones we agreed to leave as ACCEPTED, with the reason.
```

An accepted finding with a written reason is a decision your team keeps. An unrecorded one is a finding you triage again next quarter.

## Check that the work was real

Start with behavior. The tests pass and the diff contains no new behavior. If a refactor needed a test changed, then more than the structure moved: either the test was asserting the old structure, or the behavior itself changed. Both need your judgment.

Ratings come last, and the dashboard will not show movement yet. Sigrid rates the branch it is configured to analyze, so your refactors only reach the ratings once they are merged and that branch has been analyzed again. Two things answer the question before then:

- Run `/change-feedback maintainability`. It runs Sigrid CI on your working tree and returns Sigrid's maintainability feedback, publishing nothing to Sigrid. It needs your token in a `SIGRID_CI_TOKEN` or `SIGRID_TOKEN` environment variable, separate from the token the plugin stored in your keychain.
- Push the branch and open a merge request. Your [Sigrid CI](../../sigridci-integration/using-sigridci.md) step reports the same verdict in the pipeline, before anyone merges.

Ratings are measured against total system size, so a handful of refactors on a large codebase will not move a star rating. Clusters move ratings. If nothing moved after a substantial run, you worked the long tail instead of the mass, so go back to the diagnosis and ask which candidates carry the most LOC in a bad risk bracket.

## Turn what you rejected into a rule

Rejecting a diff usually means the agent hit something specific to your codebase that it had no way to know, and it will hit the same thing next run unless you write it down. The rules worth writing read like this: new units follow the naming and layering conventions of the file they came out of, never touch the `legacy` package, ask before splitting a class that is serialized.

Put rules like these in the **Customizing behavior** section of your [Sigrid profile](../../axis/configuration.md#customize-how-the-skills-behave). Every skill reads it, and because the profile is committed, the rules apply to everyone who runs the skills in that repository.

Code that should never be a candidate is a different problem and has a better home. For anything you do not want rated, such as generated sources under your source root, add an `exclude` pattern to your [analysis scope configuration](../../reference/analysis-scope-configuration.md). Then those candidates stop arriving at all.

## Where to go next

For the guides and references around this one, see:

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) to stop new debt while you clear the old
- [Preventing architecture drift](preventing-architecture-drift.md) for the structural changes a refactor can introduce
- [Improving architecture](improving-architecture.md) for the component-level properties this guide leaves out
- [Triaging security and reliability findings](triaging-security-and-reliability-findings.md) for different findings and a different loop
- [Skills reference](../../axis/skills.md) for everything `diagnose` and `autofix` do

# Reducing technical debt with auto-fix agents

A hundred medium-severity maintainability findings routinely outweigh a handful of very high ones. Sigrid's ratings are LOC-weighted: what a finding contributes is the amount of code it puts in a bad risk bracket, measured against the size of the whole system. So the intuitive move, sorting by severity and starting at the top, is usually the wrong one. It is also why a week of refactoring can leave a rating exactly where it was.

An [auto-fix agent](../autofix-agents.md) works from that weighting. The `sigrid-diagnose` skill decides what to work on, and `sigrid-improve` does the work, verifying each change with Guardrails before it moves on.

You would run this deliberately, with time set aside: a debt-reduction day, the slack at the end of a sprint, or the week before you start work in a module you know is bad. It suits diffuse debt, dozens of long units or duplication spread across a package. If you already know a module needs to be split differently, do that part yourself and hand the agent the mechanical work afterwards. Sigrid ranks candidates by how much rated code they carry, and it has no opinion on whether your design is right.

This covers maintainability only. Security and reliability findings behave differently and have their own guide: [triaging security and reliability findings](triaging-security-reliability.md). It also needs a published system, because refactoring candidates come from Sigrid's analysis of the branch it last analyzed. [Guardrails](building-with-guardrails.md) is the one that reads your working tree.

## Why the agent needs help

Ask an agent to "improve maintainability in this repository" and it will do something reasonable and nearly worthless. The instruction sounds actionable and is not, because three of the things it needs are missing from the code it can read.

The first is the whole system. An agent picks targets from whatever it read into context, and ten files it happened to open are not the ten files that matter. On a large codebase the ratio of read to unread is not close.

Second, it has no model of impact. Without the LOC weighting it judges severity by eye, so it optimizes the number of findings closed and not the rating. Closing eleven small findings and reporting a successful run is a plausible outcome that moves nothing.

Third, it has no definition of done. Splitting a 200-line method into five 40-line methods that only ever run in sequence satisfies the metric and helps nobody. An agent with no way to tell "done" from "moved" takes the metric literally, because the metric is the only part of the goal it can check.

Sigrid supplies the global view: which property is weakest, which candidates carry the most rated code, and which candidates appear under several properties at once, where a single fix moves more than one rating. Your context file supplies the definition of done, in the form of the rules you are not willing to see broken.

## Setting it up

{% include sigrid-mcp/primitives.md %}

This workflow leans on the third one, since the two skills carry most of the procedure.

### 1. Install the plugin and record your profile

{% include sigrid-mcp/plugin-install.md setup=true %}

The first two commands configure the MCP server and the skills together. `/sigrid:setup` is the one people skip, and it is the one that matters here: it records which Sigrid system this repository maps to, which branch Sigrid analyzes, and how your team handles branches and change requests. The skills read it at the start of every run, so you answer these questions once instead of every session. See [plugin configuration](../configuration.md) for what it stores and where.

On another CLI, configure the MCP server with the [installation instructions](../../integration-sigrid-mcp.md#manual-configuration-other-ides) and put your customer and system identifiers in your context file, since there is no profile to read:

```
## Sigrid

Customer: acme
System: payment-platform
Sigrid analyzes the `main` branch.
```

Your identifiers are in the Sigrid URL: `sigrid-says.com/<customer>/<system>`.

### 2. Tell the agent what you will not accept

Debt reduction goes wrong in predictable ways, and standing rules in your context file prevent most of it. These four lines are the ones worth having before the first run:

```
## Refactoring rules

- Behavior-preserving only. If a refactor requires a behavior change, stop and ask.
- Never change a public API or a serialization format without asking first.
- One candidate per commit, with the finding it addresses named in the message.
- Off limits: `src/generated/`, `src/legacy/billing/` (rewrite scheduled Q4).
```

The off-limits paths earn their two minutes. Generated code and modules already scheduled for replacement score as excellent candidates by every metric Sigrid has, and refactoring them is pure waste. The one-candidate-per-commit rule matters for a reason you will meet later, which is that you will want to drop one refactor out of ten without redoing the other nine.

### 3. Work on a branch

An ordinary git precaution, not a Sigrid requirement. A run produces a series of independent commits, so start from a clean tree on a fresh branch and `git diff` will mean something when you come to review.

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
| **Autonomous** | Works the full list from the diagnosis, you review the diffs at the end | Once you have seen the kind of change it makes and trust the rules in your context file |

Start interactive. You are calibrating whether the agent's idea of a good refactor matches yours, and that is much cheaper to find out one diff at a time. Calibrate per codebase, not once: a repository with unusual conventions needs the interactive run again.

Per candidate it reads the whole file before touching anything, makes the change, updates every call site of a changed signature, runs Guardrails to confirm no new findings appeared, and runs your formatter and type check. If a change introduces a new finding or breaks the build, it tries once more and then reverts that candidate instead of digging.

Two behaviors are worth knowing before you start. It does not touch code for the three architecture-level properties (`moduleCoupling`, `componentIndependence`, `componentEntanglement`); for those it explains the problem and proposes a restructuring plan for you to decide on. That is the right call, because those fixes are design decisions and not extractions. It also does not update finding statuses on its own. If you want Sigrid to reflect what happened, ask in the same session, while the finding UUIDs are still in context:

```
Update the status of the candidates we just fixed to WILL_FIX, with a remark
naming the commit. Mark the ones we agreed to leave as ACCEPTED, with the reason.
```

Make that request before the session ends. An accepted finding with a written reason is a decision your team keeps. An unrecorded one is a finding you re-triage next quarter, and the UUIDs are gone once the session is.

It will also stop and ask about context it cannot get from the code: serialization constraints, callers outside the repository, a migration window. In autonomous mode it skips those and logs them, which is the right trade, and it does mean the skipped list is part of the output you need to read.

## Checking that the work was real

Verify per candidate. It takes about a minute each.

Start with behavior. The tests pass and the diff contains no new behavior. A refactor that needed a test changed is not a refactor: either the test was asserting the old structure, or the behavior moved. Both need your judgment.

Then read the extracted units and ask whether you can name what each one does. If the answer is "the first half of the other method", the metric improved and the code did not. Ask for the responsibility of each unit before the next edit:

```
Why is this structure better? Name what each extracted unit is responsible for.
```

Guardrails backs this up mechanically, and the skill runs the check itself, so look for the call in the session and confirm it covers the file that changed. No new findings introduced matters as much as the old one closed.

At the end of the run, check movement at the system level:

```
Show the maintainability ratings again. Which property moved, and by how much?
```

Set your expectations honestly here, because the LOC weighting cuts both ways. Ratings are measured against total system size, so a handful of refactors on a large codebase will not move a star. Clusters move ratings. If nothing moved after a substantial run, you worked the long tail instead of the mass, so go back to the diagnosis and ask which candidates carry the most LOC in a bad risk bracket.

If the candidates themselves look stale, pointing at code that has changed or no longer exists, Sigrid analyzed a different branch or analyzed before your last merge. Check which branch is analyzed in [configuration](../configuration.md), and run the `sigrid-ci-feedback` skill for a local picture of the current tree.

## Where to go next

Debt reduction on the old code and prevention on the new code are the same project. Running only the first is how you arrive back here next quarter.

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) to stop new debt while you clear the old
- [Triaging security and reliability findings](triaging-security-reliability.md) for different findings and a different loop
- [Auto-fix agents MCP reference](../autofix-agents.md) for the full tool and status reference

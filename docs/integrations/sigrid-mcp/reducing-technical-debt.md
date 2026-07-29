# Reducing technical debt with auto-fix agents

An [auto-fix agent](autofix-agents.md) works through Sigrid's ranked refactoring candidates to lower the maintainability debt already in your codebase. The `sigrid-diagnose` skill decides what to work on, and `sigrid-improve` does the work.

This covers maintainability only. Security and reliability findings behave differently and have their own guide: [triaging security and reliability findings](triaging-security-reliability.md).

Everything here applies to any agentic CLI. The worked configuration uses Claude Code, since that is the only CLI we ship a plugin for.

## When you'd do this, and who's at the keyboard

You, on purpose, with time set aside: a debt-reduction day, the slack at the end of a sprint, or the week before you start work in a module you know is bad. You are at the keyboard, but supervising rather than typing. The agent proposes, you decide, and you review the diffs.

Use it when:

- Sigrid already analyses the system, so there are ratings and ranked candidates to work from.
- You can review and merge a series of refactors without blocking a release.
- The debt is diffuse, such as dozens of long units or widespread duplication, rather than one design problem you already know how to solve.

Do not use it when the answer is a redesign. Sigrid ranks candidates by how much rated code they carry, not by whether the design is right. If you already know a module needs to be split differently, do that yourself and use the agent for the mechanical work afterwards.

This needs a published system. [Guardrails](building-with-guardrails.md) analyses your working tree, but refactoring candidates come from Sigrid's analysis of the branch it last analysed.

## Why the agent needs help here

Ask an agent to "improve maintainability in this repository" and it will do something reasonable and nearly worthless, for three reasons.

- **It cannot see the whole system.** It picks targets from whatever it read into context. Ten files it happened to open are not the ten files that matter, and on a large codebase the ratio of read to unread is not close.
- **It has no impact model.** Sigrid's ratings are LOC-weighted: a finding's contribution is the amount of code it puts in a bad risk bracket, relative to system size. A hundred medium findings routinely outweigh a handful of very high ones. An agent judging severity by eye gets this backwards and optimises the number of findings closed instead of the rating.
- **It cannot tell "done" from "moved".** Splitting a 200-line method into five 40-line methods that only ever run in sequence satisfies the metric and helps nobody. Without a definition of done, an agent takes the metric literally.

Sigrid supplies the global view: which property is weakest, which candidates carry the most rated code, and which candidates appear under several properties at once, where one fix moves more than one rating. `sigrid-diagnose` does that reasoning. `sigrid-improve` acts on it and verifies each change with Guardrails before moving on.

## Setup

The same four primitives, with the reusable procedures doing most of the work this time:

{% include sigrid-mcp-primitives.md %}

### 1. Install the plugin and record your profile

```
/plugin marketplace add Software-Improvement-Group/sigrid-ai-toolkit
/plugin install sigrid@sigrid-ai-toolkit
/sigrid:setup
```

The first two commands configure the MCP server and the skills. `/sigrid:setup` is the one people skip, and it is the one that matters here: it records which Sigrid system this repository maps to, which branch Sigrid analyses, and how your team handles branches and change requests. The skills read it at the start of every run, so you answer these questions once instead of every session. See [plugin configuration](configuration.md) for what it stores and where.

On another CLI, configure the MCP server with the [installation instructions](../integration-sigrid-mcp.md#manual-configuration-other-ides) and put your customer and system identifiers in your context file, since there is no profile to read:

```
## Sigrid

Customer: acme
System: payment-platform
Sigrid analyses the `main` branch.
```

Your identifiers are in the Sigrid URL: `sigrid-says.com/<customer>/<system>`.

### 2. Tell the agent what you will not accept

Put your standing rules in the context file. Debt reduction goes wrong in predictable ways, and these four lines prevent most of it:

```
## Refactoring rules

- Behaviour-preserving only. If a refactor requires a behaviour change, stop and ask.
- Never change a public API or a serialization format without asking first.
- One candidate per commit, with the finding it addresses named in the message.
- Off limits: `src/generated/`, `src/legacy/billing/` (rewrite scheduled Q4).
```

The off-limits paths are worth the two minutes. Generated code and modules already scheduled for replacement score as excellent candidates by every metric Sigrid has, and refactoring them is pure waste.

### 3. Work on a branch

This is an ordinary git precaution rather than a Sigrid requirement. A debt-reduction run produces a series of independent commits, some of which you will want to drop. Start from a clean tree on a fresh branch so `git diff` means something and reverting one refactor does not take the others with it.

## The session, walked through

Two commands. The first diagnoses, the second acts.

### Diagnose

```
/sigrid:sigrid-diagnose
```

The skill fetches the current ratings, pulls the top candidates for all seven maintainability properties, and reasons across them. On a system whose duplication is weakest, it comes back with:

- **The weakest property, and what is driving it.** Not only "duplication is 1.3 stars", but which risk tier carries the score, and whether that is a few enormous clones or a long tail of medium ones. Those call for different work.
- **Ranked candidates, with a reason for the ranking.** Candidates that appear under two or more properties come first, since a 300-line method that is also a duplication finding fixes two ratings at once.
- **A read on the shape of the problem.** A cluster of near-identical DAO classes is one structural fix, not eleven separate ones.

Diagnosis changes nothing on disk. Read it, and disagree with it where you have context it lacks, such as knowing which module is being replaced next quarter.

### Improve

```
/sigrid:sigrid-improve
```

It asks which mode you want:

| Mode | What it does | When |
|---|---|---|
| **Interactive** | Presents the candidate list, you pick the order, it shows each diff and asks before continuing | First run on a codebase, or any module you do not know well |
| **Autonomous** | Works the full list from the diagnosis, you review the diffs at the end | Once you have seen the kind of change it makes and trust the rules in your context file |

Start interactive. You are calibrating whether the agent's idea of a good refactor matches yours, and that is much cheaper to find out one diff at a time.

Per candidate, it reads the whole file before touching anything, makes the change, updates every call site of a changed signature, runs Guardrails to confirm no new findings appeared, and runs your formatter and type check. If a change introduces a new finding or breaks the build, it tries once more and then reverts that candidate rather than digging.

Two behaviours are worth knowing before you start.

It does not touch code for the three architecture-level properties (`moduleCoupling`, `componentIndependence`, `componentEntanglement`). For those it explains the problem and proposes a restructuring plan for you to decide on, which is the right call: those fixes are design decisions, not extractions.

It also does not update finding statuses on its own. If you want Sigrid to reflect what happened, ask for it in the same session, while the finding UUIDs are still in context:

```
Update the status of the candidates we just fixed to WILL_FIX, with a remark
naming the commit. Mark the ones we agreed to leave as ACCEPTED, with the reason.
```

It will also stop and ask about context it cannot get from the code: serialization constraints, callers outside the repository, a migration window. In autonomous mode it skips those and logs them instead, which is the right trade, but it does mean the skipped list is part of the output you need to read.

## What good looks like, and how you verify it in the session

Verify per candidate, in this order. It takes about a minute each, and it is the difference between debt reduction and churn.

**Behaviour is unchanged.** The tests pass, and the diff contains no new behaviour. A refactor that needed a test changed is not a refactor: either the test was asserting the old structure, or the behaviour moved. Both need your judgement.

**The structure is genuinely better.** Read the extracted units and ask whether you can name what each one does. If the answer is "the first half of the other method", the metric improved and the code did not. Push back:

```
Why is this structure better? Name what each extracted unit is responsible for.
```

**Guardrails confirms it.** The skill runs the check itself, so look for the call in the session and check that it covers the file that changed. No new findings introduced matters as much as the old one closed.

**The finding status was updated.** You have to ask for this, since the skill does not do it by itself. Sigrid should reflect the decision, so the next run does not re-propose work you already did and your team can see what happened. This is also what makes an accepted finding stick.

At the end of the run, check movement at the system level instead of counting closed findings:

```
Show the maintainability ratings again. Which property moved, and by how much?
```

Set your expectations honestly here. Ratings are LOC-weighted against total system size, so a handful of refactors on a large codebase will not move a star. Clusters move ratings. If nothing moved after a substantial run, you worked the long tail instead of the mass, so go back to the diagnosis and pick the clusters.

## When it goes wrong, and the recovery move

| What you see | What is happening | What to do |
|---|---|---|
| It refactors files you did not want touched | Off-limits paths are not in the context file | Add them, and restate the scope in the prompt for this run |
| A refactor changes behaviour | The candidate was not a mechanical fix | Revert that commit. Feed it back: "this needs a behaviour change, skip it and tell me why". Those candidates are for a human |
| Metric closed, code no better | Mechanical extraction with no cohesion | Revert. Ask for the responsibility of each unit before it edits, not after |
| It stalls on one hard candidate | Guardrails keeps flagging the result, so it keeps trying | Stop it and skip that candidate. Very high findings in tangled code are often a redesign in disguise |
| Ratings did not move | You worked the tail, not the mass | Re-read the diagnosis for clusters. Ask: "which candidates carry the most LOC in a bad risk bracket?" |
| Candidates look stale | Sigrid analysed a different branch, or analysed before your last merge | Check which branch is analysed in [configuration](configuration.md), and run the `sigrid-ci-feedback` skill for a local picture of the current tree |
| It asks for context you do not have either | Genuinely ambiguous, such as an external caller or a serialization contract | Skip it and write down the question. This is a real finding about your codebase, not an agent failure |

## Habits worth keeping

- **Diagnose, then improve. Never improve first.** The diagnosis is where the impact reasoning happens. Skipping it turns a targeted run into whatever the agent read first.
- **One candidate, one commit.** You will want to drop one of them without redoing the other nine.
- **Stay interactive until the agent earns autonomous.** Per codebase, not per career. A repository with unusual conventions needs the calibration run again.
- **Ask for status updates before the session ends.** An accepted finding with a written reason is a decision your team keeps. An unrecorded one is a finding you re-triage next quarter, and the UUIDs are gone once the session is.
- **Chase clusters, not counts.** Eleven near-identical classes are one fix. Eleven unrelated long methods are eleven fixes and roughly the same rating.
- **Prevent while you repair.** Debt reduction on the old code and [Guardrails](building-with-guardrails.md) on the new code are the same project.

## Next

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) to stop new debt while you clear the old
- [Triaging security and reliability findings](triaging-security-reliability.md) for different findings and a different loop
- [Auto-fix agents MCP reference](autofix-agents.md) for the full tool and status reference

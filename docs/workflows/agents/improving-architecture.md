# Improving architecture with auto-fix agents

<div><a href="{% link axis/README.md %}#the-agentic-lifecycle">{% include axis/lifecycle-strip.md active="ground,plan,improve" %}</a></div>

This guide walks through using [Auto-fix Agents](../../axis/autofix-agents.md) to find the directory with the worst structure in your system, agree on how to fix it, and have an agent make the fix as local commits you review.

You run two commands. `/diagnose architecture` uses Sigrid's dependency graph of your whole codebase to name the directory most worth fixing, what is wrong with it, and what to change. `/autofix architecture` makes that change and checks the result against the numbers the diagnosis predicted.

Run this when you have time to review a structural change: a restructuring you keep putting off, the start of work in a part of the system that has become hard to change, or a low architecture rating you want to understand. To keep new changes from making the structure worse, see [preventing architecture drift](preventing-architecture-drift.md). For long units, complexity, and duplication inside the code, see [reducing technical debt](reducing-technical-debt.md).

## Prerequisites

You need the following before you start:

- A system published to Sigrid, so Sigrid Core has analyzed its architecture.
- The [Claude Code plugin](../../axis/installation.md#install-the-claude-code-plugin), or another agentic tool with the skills and the Sigrid Axis MCP server.
- A local checkout of the repository, with commands to build it and run its tests.

## Why the agent needs help

Ask an agent where your architecture is worst, and it will give you an answer. The answer is based on the dozen files it happened to open, not on your architecture.

Whether a directory is well structured depends on what calls into it and what it calls, from anywhere in the codebase. On a large system, one widely used file can have more than a thousand other files calling it. An agent cannot read all of that, so it guesses from what it has seen, and it has no way to tell how good the guess is.

Reading more would not fix this. To know that one file really depends on another, you have to follow every call to the code it actually runs, and that is a job for a static analyzer. An agent falls back on searching for imports, which is a rough proxy: some imports are never used, and some calls need no import at all.

Say the agent did get the numbers right. It still would not know whether they are bad. Are 40 calls across a boundary a lot? Is it good that 60% of the calls stay inside a directory? You only find out by comparing with other systems. Sigrid rates every directory against a benchmark of real systems, so it can tell you that a directory is below the market average, and that it matters more than the others because it is large.

Knowing a directory is bad does not tell you what to do about it either. It can be bad because files sit loose at its root, because it mixes two unrelated jobs, or because the rest of the system reaches straight into its internals. Each of those has a different fix. Sigrid's metrics tell them apart, so the plan can say what is wrong, what to change, and which number should move. That number is how you check afterwards whether the fix worked.

Sigrid does not see everything. For example, it cannot tell a boundary you designed from one that grew by accident. Reading the code fills those gaps, and the agent is good at that. So the work is split three ways. Sigrid points at where the structure is bad and why. The agent reads the code to confirm it and makes the change. You add what neither of them knows, such as which code is about to be replaced.

## Set up the skills

{% include axis/primitives.md %}

### 1. Install the plugin and record your profile

Install the plugin, then run `setup` in the repository:

{% include axis/plugin-install.md setup=true %}

`setup` writes `.sigrid/profile.md` with your Sigrid system and the baseline branch, so you do not have to name them on every run. Commit it, so your team shares it. In another agentic tool, [install the skills and connect the MCP server](../../axis/installation.md#use-the-skills-in-other-agentic-tools) instead.

### 2. Start from a clean branch with working tests

`autofix` builds and runs your tests after every step, and reverts a step that stays red, so the tests are your safety net. A restructuring touches every caller of what it moves, so we would not run it on a repository whose tests you do not trust.

Start with a clean working tree, up to date with the baseline branch. If you start on the baseline branch, `autofix` creates a new branch for the run.

Run the diagnosis on a reasoning model, since deciding whether a boundary is in the right place is judgment about how your system is meant to work. `autofix` can run on a mid-sized model when the plan is a move or a reroute, because it works from the numbers in the plan. See [LLM model selection](../../axis/README.md#llm-model-selection).
{: .model }

## What a session looks like

### Diagnose

Ask for the diagnosis:

```
/diagnose architecture
```

Add a directory, as in `/diagnose architecture of src/backend`, when you already know which part of the system bothers you.

The report names one directory and describes the problem and the fix in terms of your code, with any runner-ups after it. The problem is one of three kinds:

- **Breakdown:** files sit loose at the root of the directory and belong in a subdirectory.
- **Boundary:** the directory mixes two unrelated jobs, or part of it belongs next door. The fix is to move, split, or merge.
- **Enforcement:** the rest of the system reaches into the directory's internals. The fix is a facade, or rerouting callers to one that already exists.

The directory it names is often not the one with the lowest rating. The report lists what it set aside and why, such as test code, a utility directory whose coupling Sigrid does not score, or a parent whose rating mostly reflects its children. If nothing qualifies, it says so, and that is a useful answer too.

### Discuss the plan

Read the diagnosis as someone who knows the code. You should recognize the problem it describes. Before you accept it, talk it through in the same session, while the agent still has the graph and the code it read in context. These are the kinds of questions we would ask:

```
Why this directory and not src/backend?
Which files would move, and does the directory they move into get worse?
The pricing module is being replaced next quarter. Leave it out and plan again.
```

Say so when you know something the graph cannot show, such as a boundary that is deliberate, code that is about to be deleted, or paths other teams depend on. The agent adjusts the plan, and your decisions go into the [handover](../../axis/skills.md#handovers), the file in `.sigrid/handovers/` that carries the plan to `autofix`, so the next session does not reopen them.

When the plan is right, the skill asks whether to fix it now, save it for later, or stop. After a long discussion, save it and run the fix in a fresh session.

### Fix

Run the fix, in the same session or a new one:

```
/autofix architecture
```

It picks up the handover and makes one commit per step, building and testing after each. Most of the time it runs without you. It stops and asks when a step would change behavior, when it finds a reference it cannot keep working, such as a class name in a configuration file outside your control, or when the plan turns out not to match the code.

When it is done, you have a local branch and a report.

## Where to go next

For the guides and references around this one, see:

- [Preventing architecture drift](preventing-architecture-drift.md) to keep new changes from undoing the fix
- [Reducing technical debt](reducing-technical-debt.md) for maintainability problems inside the code
- [Skills reference](../../axis/skills.md#diagnose) for everything `diagnose` and `autofix` do
- [MCP tools reference](../../axis/tools.md#architecture) for the architecture tools behind them

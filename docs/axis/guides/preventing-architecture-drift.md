---
redirect_from:
  - /workflows/agents/preventing-architecture-drift.html
---

# Preventing architecture drift with an AI coding agent

<div><a href="{% link axis/README.md %}#the-agentic-lifecycle">{% include axis/lifecycle-strip.md active="ground,prevent" %}</a></div>

This guide walks through checking an agent's diff for architecture drift before it merges: a new call across a directory boundary, a facade bypassed on the way to a database, a dependency cycle the change would close. The `change-feedback architecture` skill grounds that check in Sigrid's measured dependency graph, so the verdict comes from how your system is actually wired today and not from the few files the agent happened to open.

Run it when a change touches more than one directory, on your own work or on a branch you are about to merge for someone else. It checks the diff and nothing more. [Guardrails](building-with-guardrails.md) covers each file as the agent writes it, and structure is exactly what a per-file check cannot see. For an audit of the coupling across the whole system, see [reducing technical debt](reducing-technical-debt.md), and you can always open the graph yourself in the [architecture explorer](../../capabilities/architecture-quality.md).

## Prerequisites

You need the following before you start:

- A system published to Sigrid, so Sigrid Core has analyzed its architecture.
- The [Claude Code plugin](../installation.md#install-the-claude-code-plugin), or another agentic tool with the skills and the Sigrid Axis MCP server. The check uses `architecture.get_external_dependencies`.
- A [Sigrid profile](../configuration.md#the-sigrid-profile) in the repository, with your baseline branch.
- A feature branch, or a staged or unstaged change, to check.

## Why the agent needs help

An agent checks its work against the task you gave it. The code runs, the test goes green, the task closes, and nothing anywhere in that loop holds an opinion about which parts of your system are allowed to talk to each other.

Picture a small reporting change that needs a total out of the orders table. Everything in your codebase reaches persistence through a repository interface, which is also where the query logging and the read replica routing live. The agent read the reporting package and the entity classes. It never opened the repository layer, so from where it sits, importing the order DAO into the report class and querying it there is an unremarkable way to get a number out of a database. In most codebases it would be. Here it costs you a query that never reaches the query log and a connection that skips the read replica, and the feature ships without one signal that anything is wrong.

The import is plausible, and plausibility is what the agent is good at: the same line appears in a million repositories, most of them fine. What makes it wrong is a fact about your system, and that fact was in code the agent had no reason to read. The next session starts from a clean context and reasons its way to the same place on a different file. A shortcut like this, once, is a review comment. A steady supply of them is how the structure you designed stops describing the code you have.

We've made this argument before: [our post on architectural debt](https://www.softwareimprovementgroup.com/blog/architectural-debt-ai/) describes an agent as a very fast, very clever intern, good at a bounded task like writing one function, and out of its depth on an unbounded one like deciding how a new component should connect to the rest of a system. Skipping the repository layer is the second kind of decision, wearing the costume of the first.

Sigrid already has the map that no amount of reading will produce. We build a dependency graph of your codebase down to the calls between individual files, rolled up per directory and per component, the same graphs you can browse yourself. Grounding a diff check in that graph turns a judgment call into a lookup: this reference is new, and here is everything that reaches this directory today.

## Set up the check

{% include axis/primitives.md %}

Running the check needs the second and third rows, the tools and the skill. The fourth is what gets it run on the day nobody thinks to ask for it.

### Install the plugin and record your profile

Install the plugin, then run `setup` in the repository:

{% include axis/plugin-install.md setup=true %}

`setup` writes `.sigrid/profile.md`, which records the Sigrid system this repository maps to and its baseline branch. The check diffs against that branch, and looks up your system in the graph without you naming a customer and a system every time. See [configuration](../configuration.md#the-sigrid-profile) for what the profile contains.

### Ground the agent before it writes

The check catches drift after the fact. The `architecture-explorer` agent can keep it from happening, because it answers structural questions from the same graph while the agent is still planning. Ask it where something is used, or what a directory depends on, before a change that crosses a boundary:

```
/explore-architecture How does the reporting package reach the database today?
```

The plugin nudges your agent to use `architecture-explorer` for questions like that one by itself. See [`explore-architecture`](../skills.md#explore-architecture).

## What a session looks like

Say an agent has just finished a `checkout` feature, part of which writes a ledger entry. It got there by importing `billing.internal.LedgerWriter` straight into `checkout`, around the `BillingGateway` facade that everything else uses to reach billing. Check the branch before you push it:

```
/change-feedback architecture
```

By default, the skill diffs `<baseline>...HEAD`, where the baseline is the branch in your profile. Ask for the staged or unstaged changes instead if you have not committed yet. It reads the added lines for new imports, calls, and type references that cross into another directory, spots the import, and takes it to the graph:

```
architecture.get_external_dependencies(acme, payment-platform,
    path="billing/internal", direction="all")
```

Back comes everything that calls into `billing/internal` today, and everything it calls, one hop out. `BillingGateway` is on that list, and so is billing's own package. `checkout` is not.

The skill reports every new reference as one of two verdicts:

- **Clean:** the reference matches an edge that already exists in the graph, between the same directories, through the same files. That is normal evolution.
- **Drift:** the reference adds an edge the graph does not have, closes a cycle, or goes around a gateway file. The report gives the file and line, what it violates, and the existing file it should route through instead.

Here, the import is drift: it bypasses `BillingGateway`, and the report suggests routing the ledger write through it.

The skill checks at most about five top-level directories per run, starting with the ones the change touches most. It lists any directories it skipped, so you can run it again scoped to those.

## Run it without being asked

Typing the command catches this once. An instruction in your agent's context file, next to the [conventions you add for Guardrails](building-with-guardrails.md#2-add-your-own-conventions-optional-on-claude-code), catches it in every session where the agent remembers to check:

```
Before reporting a task that touches more than one directory as complete, run /change-feedback architecture.
If it reports drift, either fix it or explain why the new reference is fine.
```

An instruction is followed most of the time, and the agent is the one deciding whether it applies here, so treat this as your everyday check and not your only one.

## Where to go next

For the checks and tools around this one, see:

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) for the file-level check that runs alongside this one
- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for the coupling across the whole system, which this check does not replace
- [MCP tools reference](../tools.md#architecture) for the architecture tools used here

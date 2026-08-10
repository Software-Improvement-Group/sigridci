# Preventing architecture drift with an AI coding agent

<div><a href="{% link workflows/agents.md %}#where-sigrid-fits-in-an-agentic-workflow">{% include sigrid-mcp/lifecycle-strip.md active="grounding,prevent" %}</a></div>

This guide walks through checking an agent's diff for architecture drift before it merges: a new call across a directory boundary, a facade bypassed on the way to a database, a dependency cycle the change would close. The `architecture-drift` skill grounds that check in Sigrid's measured dependency graph, so the verdict comes from how your system is actually wired today and not from the few files the agent happened to open.

Run it when a change touches more than one directory, on your own work or on a branch you are about to merge for someone else. It is a diff check and nothing more. [Guardrails](building-with-guardrails.md) covers each file as the agent writes it, and structure is exactly what a per-file check cannot see. If what you want instead is a coupling and cohesion audit of the whole system, that is [reducing technical debt](reducing-technical-debt.md), and you can always open the graph yourself in the [architecture explorer](../../capabilities/architecture-quality.md).

## Prerequisites

- A system published to Sigrid, so its architecture has been analyzed.
- An agentic CLI that can call MCP tools, with `architecture:get_internal`, `architecture:get_external_dependencies`, and the `architecture-drift` skill available. The configuration below uses Claude Code.
- A [Sigrid API token](../../organization-integration/authentication-tokens.md) for the MCP server, which the plugin installer asks for once.
- A diff, a staged change, or a feature branch to check.

## Why the agent needs help

An agent checks its work against the task you gave it. The code runs, the test goes green, the task closes, and nothing anywhere in that loop holds an opinion about which parts of your system are allowed to talk to each other.

Picture a small reporting change that needs a total out of the orders table. Everything in your codebase reaches persistence through a repository interface, which is also where the query logging and the read replica routing live. The agent read the reporting package and the entity classes. It never opened the repository layer, so from where it sits, importing the order DAO into the report class and querying it there is an unremarkable way to get a number out of a database. In most codebases it would be. Here it costs you a query that never reaches the query log and a connection that skips the read replica, and the feature ships without one signal that anything is wrong.

That is not carelessness. Plausibility is what the agent is good at, and that import is plausible: the same line appears in a million repositories, most of them fine. What makes it wrong is a fact about your system, and that fact was in code the agent had no reason to read. So it commits to the shortcut with real confidence and nothing available to contradict it, and the next session starts from a clean context and reasons its way to the same place on a different file. A shortcut like this, once, is a review comment. A steady supply of them is how the structure you designed stops describing the code you have.

We've made this same argument elsewhere: [our post on architectural debt](https://www.softwareimprovementgroup.com/blog/architectural-debt-ai/) describes an agent as a very fast, very clever intern, good at a bounded task like writing one function, and out of its depth on an unbounded one like deciding how a new component should connect to the rest of a system. Skipping the repository layer is the second kind of decision, wearing the costume of the first. Nobody decided to go around it. Nobody told the agent it was there to go around.

Sigrid already has the map that no amount of reading will produce. We build a dependency graph of your codebase down to the calls between individual files, rolled up per directory and per component, the same graphs you can browse yourself. Grounding a diff check in that graph turns a judgment call into a lookup: this reference is new, and here is everything that reaches this directory today.

## Set up the check

{% include sigrid-mcp/primitives.md %}

Running the check needs the second and third rows, the tools and the skill. The fourth is what gets it run on the day nobody thinks to ask for it.

### Install the plugin and record your profile

{% include sigrid-mcp/plugin-install.md setup=true %}

`/sigrid:setup` records which Sigrid system this repository maps to, so `architecture:get_internal` and `architecture:get_external_dependencies` know where to look without you naming a customer and a system every time you ask. See [plugin configuration](../../integrations/sigrid-mcp/configuration.md) for what it stores.

## What a session looks like

Say an agent has just finished a `checkout` feature, part of which writes a ledger entry. It got there by importing `billing.internal.LedgerWriter` straight into `checkout`, around the `BillingGateway` facade that everything else uses to reach billing. Check the diff sitting in your working tree:

```
/sigrid:architecture-drift
```

The skill pulls the new cross-directory references out of the diff, spots the import, and takes it to the graph:

```
architecture:get_external_dependencies(acme, payment-platform,
    path="billing/internal", direction="incoming")
```

Back comes everything that calls into `billing/internal` today, one hop out. `BillingGateway` is on that list, and so is billing's own package. `checkout` is not. The skill reports the new reference as drift, names the facade it goes around, and suggests routing the ledger write through `BillingGateway`.

## Run it without being asked

Typing the command catches this once. An instruction in your agent's context file, the same gate [Guardrails](building-with-guardrails.md#2-add-the-quality-gate) uses for maintainability and security, catches it in every session where the agent remembers to check:

```
Before reporting any task complete run the architecture-drift skill.
If it flags something, either fix it or explain why the new reference is fine.
```

An instruction is followed most of the time, and the agent is the one deciding whether it applies here, which makes this your everyday check and not your only one.

## Where to go next

- [Building with an AI coding agent and Sigrid Guardrails](building-with-guardrails.md) for the file-level check that runs alongside this one
- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for the full-system coupling and cohesion audit this check does not replace
- [Auto-fix agents MCP reference](../../integrations/sigrid-mcp/autofix-agents.md#architecture-exploration) for the architecture tools used here

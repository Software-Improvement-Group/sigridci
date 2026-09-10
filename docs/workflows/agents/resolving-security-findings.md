# Triaging and resolving security findings with auto-fix agents

<div><a href="{% link workflows/agents.md %}#where-sigrid-fits-in-an-agentic-workflow">{% include sigrid-mcp/lifecycle-strip.md active="plan" %}</a></div>

Somewhere in your backlog there is a command injection finding on a deployment script. You already know it is fine. The
script only runs from CI, the value it interpolates comes from a pipeline variable you control, and there is no route to
it from outside the network. Deciding that takes you about four seconds.

Sigrid cannot decide it at all, because none of those three facts are in the code. It sees a shell call built from a
variable and reports exactly what it sees, correctly.

Now multiply by two hundred findings. The work is not difficult, it is repetitive, and the fact that settles each case
is usually not on the screen. That is why security backlogs sit.

The `resolve-security-findings` skill works through that backlog with you: it reads each finding at its file and line,
proposes a classification, writes the decision back to Sigrid with the evidence attached, and fixes the code where a fix
is mechanical. This guide covers the part the skill itself does not: what you need to give it, what a real session looks
like, and how to tell afterward whether you can trust what it did.

## Prerequisites

- A system published to Sigrid, with security findings waiting on it.
- The Sigrid Claude Code Plugin installed, with the `resolve-security-findings` skill available. On a different agentic
  CLI, configure the Sigrid MCP server by hand using
  the [installation instructions](../../integrations/integration-sigrid-mcp.md#manual-configuration-other-ides), then
  take the skill definition from
  the [sigrid-ai-toolkit](https://github.com/Software-Improvement-Group/sigrid-ai-toolkit) and adapt it to whatever that
  CLI calls a skill or a rules file.
- Your Sigrid profile set up with `/sigrid:setup`, so you are not naming the customer and system on every invocation.
- A [Sigrid API token](../../organization-integration/authentication-tokens.md) for the MCP server. The plugin installer
  asks for it once.
- A clean working tree. The skill writes fixes to disk as it goes, and commits them by default, so start from a state
  you are happy to see change.

## Why this is worth doing

Triage is not a code reading problem. It is a context problem. Sigrid can find the sink; it cannot see that the endpoint
sits behind an internal load balancer, or that the input was already validated two layers up.

For as long as we have been shipping findings to customers, that has meant a human reading all two hundred of them in
order to apply about five facts. Most of the reading is wasted. You are not learning anything at finding 140 that you
did not know at finding 12, you are just checking the same handful of conditions again with worse attention than the
first time.

An agent inverts the labor. It does the reading, at full attention, on all two hundred. You supply the five facts. Your
job stops being "triage the backlog" and becomes "state my system's security context precisely enough that someone else
can triage it for me." Which is something you should be able to do anyway, and if you sit down to try it you will
probably find you cannot, at least not without checking a few things.

There is a second benefit that shows up later. Every decision the agent makes lands in Sigrid with a remark: the file
and line it relied on, and one sentence of reasoning. Manual triage almost never leaves that behind. Six months on,
"someone marked this accepted in March" is not an answer you can defend to an auditor or to the next developer.
"Internal-only admin endpoint, no external route, see `routes.py:80`" is.

## Set up the skill

{% include sigrid-mcp/primitives.md %}

### 1. Install the plugin

{% include sigrid-mcp/plugin-install.md setup=true %}

The plugin only works in Claude Code. Decide which security model you are resolving against before you start, because it
changes the finding list. The skill reads the model from the "Security findings triage" section of your profile and
falls back to OWASP Top 10 (`ow10`) when that field is empty. To use `sigsec`, `5055sec`,
`c25`, `pci4`, `owasvs4c`, `owasvs4s` or `lcnc10` instead, instruct the agent using the `/sigrid:setup` command.

### 2. Giving the agent your security context

By default the skill runs interactively and asks you about context as it goes. That is fine for a handful of findings
and tedious for a hundred, and it is the thing standing between you and an unattended run. So write the facts down once.

We recommend a `SECURITY-CONTEXT.md` file in the repo, next to the code it describes. Keeping it in the repo means it is
reviewable in a merge request, it diffs when the architecture changes, and it rots visibly rather than quietly. If you
would rather not add a file, the same content works in `CLAUDE.md` or `AGENTS.md`, which the agent already reads.

```markdown
# Security context

## Externally reachable

- `src/api/public/` - unauthenticated REST API, internet-facing via ALB
- `src/web/checkout/` - authenticated user session, internet-facing

## Internal-only

- `src/admin/` - enforced by network policy, only reachable from the ops VPC (see `infra/network/admin-policy.tf`)
- `scripts/deploy/` - runs from CI runners only, no HTTP surface

## Input already validated

- Everything under `src/api/public/` passes the schema validator in
  `src/api/middleware/validate.ts` before reaching a handler

## Accepted risks

- Legacy XML parser in `src/import/` accepted by the platform team, 2026-02, until
  the importer is retired in Q4
```

Every line in that file is a claim the agent will suppress findings on. Treat it that way. "Internal-only" has to name
the thing that enforces it, not the thing you intend. A route that is internal because no one has published the URL is
not internal, and an agent has no way to tell the difference between that and a network policy unless you say so.

The other input worth deciding up front is the severity ceiling: the level above which nothing gets suppressed
automatically, and findings go to `REFINED` for a human instead. We recommend `HIGH`. Not because HIGH findings are more
often real, but because they are the ones where being wrong is expensive.

## What a session looks like

Start small and scoped because a first run is really a calibration run: you are checking whether the agent's judgment
matches yours on code you know well.

```
/sigrid:resolve-security-findings Triage the security findings under src/import/
```

The agent pulls the findings in that path, reads each one at its file and line, and comes back with a proposal per
finding: false positive, accepted risk, needs human review, or will fix. Each proposal carries a file, a line, and one
sentence. Your job is to say no to the ones that are wrong, and to notice *why* they were wrong. Usually it is a missing
fact rather than bad reasoning, and the fix goes in `SECURITY-CONTEXT.md`. Expect to reject something because the
context was incomplete.

Once the context file has survived a couple of rounds like that, the same scope can run unattended:

```
/sigrid:resolve-security-findings Work through the security backlog under src/import/
in autonomous mode. Security context is in SECURITY-CONTEXT.md, severity ceiling HIGH.
```

Autonomous mode writes classifications and commits fixes without stopping to ask. It only runs when you ask for it
explicitly, and it will refuse to start until it has reachability facts, a severity ceiling, and your acknowledgement
that the risks it accepts still need a human to look at them afterwards. Autonomous mode moves the review to the end.

## Checking that it holds up

Four checks, in order of how much they matter.

1. **Audit the suppressions first.** Pull everything the run marked `FALSE_POSITIVE` or `ACCEPTED` out of Sigrid and read
   each remark against the code it cites.
2. **Review the diff normally.** The agent's commits are one per finding with the finding ID in the message. They go through
   your merge request process like anyone else's.
3. **Drain the `REFINED` list.** Everything the agent could not settle mechanically is sitting there with a named blocker.
4. **Compare against yourself.** On a first run, triage ten findings by hand before you look at what the agent did. If it
   disagrees with you on more than one or two, the context file is the problem.

## Things to watch out for

1. Ensure you are working on a branch that is up-to-date with Sigrid
2. If you instruct the agent to promote to `FIXED`, set them back to `WILL_FIX` if the branch is abandoned
3. Agree with your security owner up front which categories you are allowed to accept on their behalf and which come to
   them.

## Where to go next

- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for maintainability, where the agent refactors as well as diagnoses
- [Auto-fix agents MCP reference](../../integrations/sigrid-mcp/autofix-agents.md#security-and-reliability-triage) for
  the manual reliability loop, and for tools, models and statuses
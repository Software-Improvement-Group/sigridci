---
redirect_from:
  - /workflows/agents/resolving-security-findings.html
---

# Triaging security and reliability findings with auto-fix agents

<div><a href="{% link axis/README.md %}#the-agentic-lifecycle">{% include axis/lifecycle-strip.md active="plan,improve" %}</a></div>

Somewhere in your backlog there is a command injection finding on a deployment script. You already know it is fine. The script only runs from CI, the value it interpolates comes from a pipeline variable you control, and there is no route to it from outside the network. Deciding that takes you about four seconds.

Sigrid cannot decide it at all, because none of those three facts are in the code. It sees a shell call built from a variable and reports exactly what it sees, correctly.

Now multiply by two hundred findings. The work is repetitive more than difficult, and the fact that settles each case is usually not on the screen. That is why security backlogs sit.

This guide walks through working down that backlog with two skills. `triage-findings` reads each finding at its file and line, decides what to do with it, and writes the decision back to Sigrid with the evidence attached. `autofix` then fixes the findings triage decided to fix, as local commits. The guide covers what the skills cannot do alone: what you need to give them, what a session looks like, and how to tell afterwards whether you can trust the result.

## Prerequisites

You need the following before you start:

- A system published to Sigrid, with security or reliability findings waiting on it.
- The [Claude Code plugin](../../axis/installation.md#install-the-claude-code-plugin), or another agentic tool with the skills and the Sigrid Axis MCP server.
- A [Sigrid profile](../../axis/configuration.md#the-sigrid-profile) in the repository, written with `/setup`, so you are not naming the customer and system on every run.

## Why this is worth doing

Triage is a context problem more than a code reading problem. Sigrid can find the sink. It cannot see that the endpoint sits behind an internal load balancer, or that the input was already validated two layers up.

For as long as we have been shipping findings to customers, that has meant a person reading all two hundred of them to apply about five facts. Most of the reading is wasted. You learn nothing at finding 140 that you did not know at finding 12. You are checking the same handful of conditions again, with worse attention than the first time.

An agent inverts the labor. It does the reading, at full attention, on all two hundred, and you supply the five facts. Your job becomes stating your system's security context precisely enough that someone else can triage for you. You should be able to do that anyway, and if you sit down to try it, you will probably find you cannot without checking a few things.

A second benefit shows up later. Every decision lands in Sigrid with a remark, prefixed "Sigrid Auto-fix Agent:": the file and line it relied on, and one sentence of reasoning. Manual triage almost never leaves that behind. Six months on, "someone marked this accepted in March" is not an answer you can defend to an auditor or to the next developer. "Internal-only admin endpoint, no external route, see `routes.py:80`" is.

## Set up the skills

{% include axis/primitives.md %}

### 1. Install the plugin and record your profile

Install the plugin, then run `setup` in the repository:

{% include axis/plugin-install.md setup=true %}

Decide which security model you triage against before you start, because it changes the finding list. `setup` records it in the **Security model** field of your profile, and the **Reliability model** field for reliability. Leave the field empty to use your organization's default. The security models are `ow10`, `sigsec`, `5055sec`, `c25`, `pci4`, `owasvs4c`, `owasvs4s`, and `lcnc10`, and the reliability models are `sigrel` and `5055rel`.

### 2. Write down your security context

The skill asks you about context it cannot find in the code. That works for a handful of findings and gets tedious for a hundred, so write the facts down once.

We recommend a `SECURITY-CONTEXT.md` file in the repository, next to the code it describes. That way it is reviewable in a merge request, it changes along with the architecture, and it goes stale where you can see it. Point to it from the **Customizing behavior** section of your [profile](../../axis/configuration.md#customize-how-the-skills-behave), or put the same content in `CLAUDE.md` or `AGENTS.md`, which the agent already reads. Here is an example:

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

Every line in that file is a claim the agent will suppress findings on, so treat it that way. "Internal-only" has to name the thing that enforces it, not the thing you intend. A route that is internal because no one has published the URL is not internal, and an agent cannot tell that apart from a network policy unless you say so.

## What a session looks like

Start small and scoped, because a first run is really a calibration run: you are checking whether the agent's judgment matches yours on code you know well.

```
/triage-findings security under src/import/
```

The skill fetches the open findings under that path, with status `RAW`, `REFINED`, or `WILL_FIX`. Findings your team already accepted stay out, unless you ask to revisit them. With more than one finding, it hands each one to a subagent of its own, about eight at a time. You can also give it a single finding ID, or paste a finding from Sigrid.

Each finding gets read at its file and line and put through the same sequence of checks:

- **False positive:** the check itself is wrong, and the best fix would be to the check, not to the flagged code. If the fix you would reach for is a code change, it is not a false positive.
- **Accepted risk:** the issue is real, but the risk is acceptable at Sigrid's original severity, and the evidence names the context that mitigates it.
- **Needs a person** (`REFINED`): neither of the above has evidence, and something blocks a mechanical fix. The blockers are a design or product decision, a change to the access control decision itself, an action outside the working tree such as rotating a secret, code the analysis could not locate, or a fix that changes an exported signature or touches more than three files.
- **Will fix:** the default, when nothing above applies.

A false positive or an accepted risk needs evidence: a file, a line, and one sentence. Without it, the finding falls through to one of the last two. The checks are mechanical, with a named trigger for each, and none of them rests on how confident the agent feels.

The skill writes `WILL_FIX` and `REFINED` to Sigrid straight away. It proposes each false positive and accepted risk to you with its evidence, and writes it only after you confirm. Your job is to say no to the wrong ones, and to notice why they were wrong. Usually it is a missing fact rather than bad reasoning, and the fix goes in `SECURITY-CONTEXT.md`. Expect to reject something on a first run because the context was incomplete.

At the end, the skill lists every finding that needs a person, with its blocker, and offers a [handover](../../axis/skills.md#handovers) for the findings to fix. Take it, and fix them:

```
/autofix security
```

For each finding, `autofix` checks that the code still matches the finding, writes the fix, runs Guardrails on the changed code, and commits it on its own, with the message `Fix: <title> (Sigrid <id>)`. A fix that turns out to hit one of the blockers above is reverted, and the finding goes to `REFINED` with the blocker as its remark.

### Skip the confirmations

Once the context file has survived a couple of rounds, you can let the same scope run without the confirmations. Only you can waive them, by asking explicitly. The skill never assumes a waiver because a run is unattended or scripted:

```
/triage-findings security under src/import/. Don't ask me to confirm false positives
and accepted risks. Security context is in SECURITY-CONTEXT.md, severity ceiling HIGH.
I'll review the accepted risks afterwards.
```

A waived run still needs three things before it suppresses anything: which parts of the system are reachable from outside, a severity ceiling, and your acknowledgement that the accepted risks need a human review afterwards. Without them, or for a finding above the ceiling, it writes `REFINED` with the proposed classification in the remark.

We recommend a ceiling of `HIGH`. HIGH findings are not more often real than others, but they are the ones where being wrong is expensive.

### Promote the fixes to FIXED

Triage never sets `FIXED`. Committed fixes stay on `WILL_FIX`, and at the end of the run, `autofix` lists them and asks whether to set them to `FIXED` now. Consider the trade-off. On `WILL_FIX`, a triage run before the branch is merged picks them up again. On `FIXED`, you have to set them back to `WILL_FIX` if the branch is never merged. If your profile records a preference, `autofix` follows it and does not ask.

## Reliability findings

Reliability findings go through the same loop, with `/triage-findings reliability` and `/autofix reliability`. Three things differ:

- An accepted risk is about impact, not attack surface. The evidence names why the failure cannot occur or is harmless here, such as "the collection is never empty, built from a constant list at `config.py:12`".
- A waived run needs a severity ceiling and your acknowledgement, but no reachability facts.
- A fix that would change behavior callers may rely on, such as error types or retry and timeout semantics, is one more blocker, so the finding goes to `REFINED`.

## Check that it holds up

Here are four checks, in order of how much they matter:

1. **Audit the suppressions first.** Pull everything the run marked `FALSE_POSITIVE` or `ACCEPTED` out of Sigrid, and read each remark against the code it cites.
2. **Review the diff normally.** There is one commit per finding, with the finding ID in the message. It goes through your merge request process like anyone else's.
3. **Drain the `REFINED` list.** Everything the agent could not settle mechanically is there, with a named blocker.
4. **Compare against yourself.** On a first run, triage ten findings by hand before you look at what the agent did. If it disagrees with you on more than one or two, the context file is the problem.

## Things to watch out for

Keep these in mind across runs:

- Work on a branch that is up to date with the branch Sigrid analyzes, so the findings match your code.
- If you promoted findings to `FIXED` and the branch is abandoned, set them back to `WILL_FIX`.
- Agree with your security owner up front which categories you may accept on their behalf, and which go to them.

## Where to go next

For the guides and references around this one, see:

- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for maintainability, where the plan comes from ratings instead of a list
- [Skills reference](../../axis/skills.md#triage-findings) for `triage-findings`, including open source findings
- [MCP tools reference](../../axis/tools.md#findings) for the finding statuses and the tools behind the skills

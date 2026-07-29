# Building with an AI coding agent and Sigrid Guardrails

[Sigrid Guardrails](guardrails.md) checks maintainability and security on code as it is written. Your AI coding agent runs that check on its own output and fixes what it finds, before the code reaches your review or your commit.

The setup below covers the feature loop: you are building something ordinary, and you want the code the agent leaves behind to be code you would have accepted from a colleague.

Everything here applies to any agentic CLI. The worked configuration examples use Claude Code, since that is the only CLI we ship a plugin for. The "Generic" column in the table below tells you what to look for in yours.

## When you'd do this, and who's at the keyboard

You, a developer, working on a feature or a bug fix in a repository you know. You stay in the loop: you describe the change, the agent writes it, you read the diff, you commit. Nothing runs unattended.

Use this loop when:

- The change is normal product work, such as a new endpoint or a bug fix.
- You will review the diff yourself before it goes anywhere.
- You care about the state the code is left in, not only whether the feature works.

For clearing existing technical debt in bulk, use [reducing technical debt with auto-fix agents](reducing-technical-debt.md) instead. That is a different job with a different setup.

Guardrails works on the code in your working tree. You do not have to publish the system to Sigrid first, and the code does not have to be committed.

## Why the agent needs help here

A coding agent optimises for the goal you gave it, and "the feature works" is the only part of that goal it can verify by itself. It runs the code, reads the error, and tries again. It has no comparable signal for whether the code is maintainable, so it stops when the tests pass.

Three consequences you will recognise:

- **It adds rather than restructures.** Extending an existing method is a smaller, safer-looking edit than splitting it, so units grow across sessions until they are the worst units in the file.
- **It repeats itself.** Copying a nearby block that already works is more reliable than generalising it, so duplication accumulates fastest in the files an agent touches most.
- **It has no memory of your standards.** A rule you gave it yesterday is gone today unless it is written down somewhere the agent reads.

Guardrails gives the agent a quality signal it can act on: the same analysis Sigrid runs, on the files it just changed. For the third problem you need your context file, not a tool.

## Setup

Four primitives do the work. Every agentic CLI has some version of them, under some name:

{% include sigrid-mcp-primitives.md %}

This guide needs the first two. The fourth is optional and covered at the end.

### 1. Tool access

Install the plugin, which configures the Sigrid MCP server and the skills together:

```
/plugin marketplace add Software-Improvement-Group/sigrid-ai-toolkit
/plugin install sigrid@sigrid-ai-toolkit
```

The installer asks for your Sigrid API token once and stores it in your system keychain. See [authentication tokens](../../organization-integration/authentication-tokens.md) for how to obtain one, and [plugin configuration](configuration.md) for where it ends up.

On any other CLI, configure the MCP server by hand using the [installation instructions](../integration-sigrid-mcp.md#manual-configuration-other-ides). You need at least the `guardrails:quality_check` tool.

Verify it before you rely on it. Ask the agent:

```
Run the Sigrid quality check on <a file you changed recently>.
```

The tool takes one file at a time: the agent passes the code and the filename, and gets back the maintainability guidelines that file violates, with a severity and a line range per unit, plus a separate list of security findings. A clean file returns both lists empty, so an empty result is a pass rather than a failure to run. Note that the security list judges the file as a whole, so it can flag something the code inside your units did not cause, such as a Java class in the default package.

If the agent reports the tool as unavailable, fix that now. An agent that silently cannot check its work looks exactly like an agent whose work is clean.

### 2. Persistent instructions

Put the quality gate in your project's context file so it applies to every session without you asking. In Claude Code that is `CLAUDE.md` in the repository root. For the equivalent in other tools, see [where to place these instructions](guardrails.md#where-to-place-these-instructions).

```
## Code Principles

Write maintainable, self-documenting code: single responsibility, small focused
functions, clear naming, avoid duplication, simple control flow.

## MANDATORY: Quality Gate

Before reporting ANY task as complete:

1. Run the Sigrid guardrails:quality_check MCP tool on all files you changed
2. Maintainability findings: fix every finding in files you touched, new or
   pre-existing, judged against the principles above. Leave one only if the code
   already honors the principles, or the fix cascades outside task scope
   (don't get stuck). Say which, and why.
3. Security findings: fix if contained, otherwise flag to user

Only skip if the tool is unavailable and say so if you do.
```

Two details in that text are easy to lose when you reword it. The instruction names the tool, so the outcome is verifiable: "check code quality" is advice, while "run `guardrails:quality_check` on all files you changed" is an instruction you can confirm was followed. And it is tied to task completion, because an agent decides for itself when it is finished, and that moment is the only placement that fires reliably.

Add your own conventions under Code Principles: the framework patterns your codebase actually uses, plus a line for every recurring mistake you find yourself correcting. Your context file is where a correction becomes permanent.

## The session, walked through

Take a repository with a `PaymentService` and this request:

```
Add support for partial refunds. A refund can now be for less than the
original amount, and we need to reject refunds that exceed what's left.
```

What happens, in order:

1. **The agent reads before it writes.** It opens `PaymentService`, finds the existing `refund` method, and finds the call sites.
2. **It implements.** The straightforward change adds the remaining-amount check to `refund`, which grows from 30 lines to about 50 and picks up two new branches.
3. **It runs the tests.** They pass. Left alone, this is where it would report done.
4. **The gate fires.** It calls `guardrails:quality_check` on the changed file. The response flags `refund` under "Write Short Units of Code" and "Write Simple Units of Code", at HIGH severity, with the line range of the method.
5. **It refactors in response.** It extracts the validation into a `validateRefundable` helper and the amount arithmetic into a small value method, leaving `refund` as the orchestration.
6. **It re-checks.** A second `quality_check` call on the same file: findings gone, tests still passing.
7. **It reports** what it changed, that the gate passed, and anything it deliberately left alone.

The screenshot below shows the loop on a real change:

<a href="../../images/mcp/guardrails/guardrails-refactoring-loop.png" target="_blank"><img src="../../images/mcp/guardrails/guardrails-refactoring-loop.png" width="800" alt="Claude Code implementing a method, running Sigrid guardrails that flag maintainability issues, then refactoring by extracting a helper method" /></a>

Step 5 is where the value is. The agent did not need you to name the problem, and it did not have to guess what "too complex" means in your codebase. It got a finding with a location and a metric, and it had a principle to fix it against.

## What good looks like, and how you verify it in the session

Do not take "quality gate passed" as evidence. Check it the way you would check a claim about tests.

**Confirm the tool actually ran.** Your CLI shows tool calls. There should be at least one `guardrails:quality_check` call after the last edit. A check that ran before the final edit tells you nothing about the code you are about to commit.

**Confirm the file list.** The tool checks one file per call, so four changed files means four calls. If you changed four files and the check covers one, the gate ran on a quarter of your change. Ask:

```
Which files did you run the quality check on? List them against the files you changed.
```

**Read what it left behind.** The gate lets the agent leave a finding when the fix would cascade outside the task. That escape hatch is deliberate, and it stops a small feature from turning into a three-hour refactor. It is only acceptable if the agent says so. If findings were left silently, tighten the instruction rather than trusting the next run.

**Then read the diff.** Guardrails tells you the code is well structured. Whether it is correct, and whether it does what you asked, is still your call.

A clean run looks like this: tests pass, the quality check ran on every changed file after the last edit, no new findings, and any remaining finding is named with a reason.

## When it goes wrong, and the recovery move

| What you see | What is happening | What to do |
|---|---|---|
| The agent reports done without calling the tool | The gate is in the wrong file, or the context file is not being read | Ask it directly: "which instruction files did you load?" Move the gate to the project-level context file and make sure it is committed |
| It calls the tool, reports findings, and fixes nothing | The instruction reads as informational | Keep the imperative wording: *fix every finding in files you touched* |
| It fixes findings by moving code around without improving it | Extracting a 40-line block into a 40-line helper satisfies unit size and helps nobody | Ask for the reasoning: "why is this a better structure, in terms of the code principles?" Then add a principle that names the pattern |
| It gets stuck in a check-fix-check loop | Each fix introduces a new finding elsewhere | Stop it, ask what the remaining findings are, and decide yourself. The gate has an explicit "don't get stuck" clause for this. If that is not firing, the finding is probably structural and belongs in a separate change |
| It refactors far beyond the task | The gate says "files you touched", and it touched more than the task needed | Scope the request: "only fix findings in the methods you changed" |
| The tool is unavailable | Token, MCP connection, or an unsupported technology | See [troubleshooting](../integration-sigrid-mcp.md#troubleshooting) and the list of [supported technologies](guardrails.md#supported-technologies) |
| The check errors on a Java file | The analyzer compiles the snippet, so a bare method does not work | Have the agent pass the complete class, exactly as written to disk |

The failure worth watching for is the quiet one, where an agent has stopped calling the tool and reports success anyway. Check the tool calls, not the summary.

## Habits worth keeping

- **Put every correction in the context file.** If you tell the agent something twice, you should have written it down after the first time.
- **Check the tool calls, not the summary.** Once per session is enough, and it takes seconds.
- **Keep changes small enough to review.** The gate improves the code the agent writes. It cannot make a 900-line diff reviewable.
- **Let the agent leave things alone.** A finding consciously left with a reason beats a feature branch that grew a refactor.
- **Pair it with CI.** Guardrails sees the files in front of it. Architecture drift, vulnerable dependencies, and cross-file duplication need the full analysis, which is what [Sigrid CI](../../sigridci-integration/using-sigridci.md) does. The `sigrid-ci-feedback` skill runs it locally before you push.

### Optional: make the check automatic

Instructions are followed most of the time, which is not the same as always. If you want the reminder to fire mechanically, there are two places to put it.

**A hook in the CLI.** Claude Code can run a command after every file edit. A hook cannot call an MCP tool itself, but a `PostToolUse` hook can inject text into the agent's context, so it can remind reliably. Put this in `.claude/settings.json` in your repository, so your whole team gets it:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Reminder: run guardrails:quality_check on the files you changed before reporting this task complete.\"}}'"
          }
        ]
      }
    ]
  }
}
```

The JSON wrapper matters. Plain output from a `PostToolUse` hook goes to the debug log, and only `additionalContext` reaches the agent. This makes the reminder mechanical instead of remembered, but it is still a reminder rather than enforcement.

**A git pre-commit hook.** For actual enforcement, put the check where the code leaves your machine and run [Sigrid CI](../../sigridci-integration/using-sigridci.md) rather than the MCP tool. Sigrid CI is a command line tool, so a hook can call it directly, and it sees the whole system instead of a handful of files. This blocks a bad commit regardless of which agent, or which human, produced it.

## Next

- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for the debt that is already there
- [Triaging security and reliability findings](triaging-security-reliability.md) for the findings Sigrid already knows about
- [Guardrails MCP reference](guardrails.md) for supported technologies and the tool itself

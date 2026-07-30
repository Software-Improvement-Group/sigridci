# Building with an AI coding agent and Sigrid Guardrails

We built the same system 20 times with Claude Sonnet 4.6. One group of runs got a written set of code principles and nothing else. The other group also had Sigrid Guardrails in the build loop, checking each file as the agent wrote it. The guided runs came out with roughly 97% fewer high-risk security findings and a maintainability score roughly 24% higher, and the separation was clean: every guided run scored better on maintainability than every unguided one. The [experiment write-up](https://www.softwareimprovementgroup.com/blog/claude-sonnet-4-6-guardrails-experiment/) has the method and the full results.

[Sigrid Guardrails](../guardrails.md) gives your coding agent the same analysis Sigrid runs, on the files it just changed, while it is still working on them. The agent sees what it broke and fixes it before it presents you with anything. The checks are deterministic: the same metrics against the same thresholds every time, decided by Sigrid's quality model and not by a model's opinion of its own output.

When should you use it? Whenever an agent writes code. How closely you read the result is a separate question from whether the code has to be secure and maintainable: anything you deploy, or come back to and change in six months, has to be both. If you are reading every diff, Guardrails saves you the review comments you were about to write. If you are vibe coding and only checking that the thing runs, it is the only thing between you and whatever the agent happened to produce, which is when it matters most.

Guardrails reads the code you are working on, so the system does not have to be published to Sigrid first and the code does not have to be committed. For clearing out technical debt that is already there, which is a different job with a different setup, see [reducing technical debt with auto-fix agents](reducing-technical-debt.md).

## Why the agent needs help

An agent optimizes for the goal you gave it, and it can only verify part of that goal by itself. "The feature works" is testable: run the code, read the error, try again. "The code is good" is not, so the agent stops when the tests pass, and what it leaves behind is whatever satisfied the test.

That plays out in three ways you will recognize. Extending an existing method is a smaller and safer-looking edit than splitting it, so units grow across sessions until the worst unit in the file is the one the agent has touched most often.

Security is the second. An agent reproduces the patterns it has seen most, and insecure idioms are well represented among them: a query assembled by string concatenation, a permissive default, a check that runs after the work instead of before it. Nothing in the task tells it to look, and a vulnerability does not announce itself the way a failing assertion does.

Then there is the problem we built Sigrid to solve. "Maintainable" is not something an agent can measure by reading. Unit size, complexity, parameter counts, and duplication all have thresholds and a rating behind them, and without those numbers the agent is aiming at a standard it cannot see.

Guardrails makes the missing half of the goal testable too. It returns which guidelines a file violates, where, at what severity, and the thresholds behind each finding, so the agent knows what "too long" means instead of guessing. Your context file covers the rest, recording the conventions particular to your team.

## Setting it up

{% include sigrid-mcp/primitives.md %}

You need the first two to get started.

### 1. Tool access

Install the plugin, which configures the Sigrid MCP server and the skills together:

{% include sigrid-mcp/plugin-install.md %}

The installer asks for your Sigrid API token once and stores it in your system keychain. See [authentication tokens](../../../organization-integration/authentication-tokens.md) for how to get one. On any other CLI, configure the MCP server by hand using the [installation instructions](../../integration-sigrid-mcp.md#manual-configuration-other-ides); you need at least the `guardrails:quality_check` tool, and your language has to be one of the [supported technologies](../guardrails.md#supported-technologies).

Check it works before you rely on it:

```
Run the Sigrid quality check on <a file you changed recently>.
```

The tool takes one file at a time. The agent passes the code and the filename, and gets back the maintainability guidelines that file violates, with a severity and a line range per unit, plus a separate list of security findings. A clean file returns both lists empty, so an empty result is a pass and not a failure to run. For Java, the analyzer compiles what it is given, so the agent has to pass a complete class and not a bare method. If the tool comes back unavailable, fix that now and see [troubleshooting](../../integration-sigrid-mcp.md#troubleshooting) if you need it.

### 2. The quality gate

Tool access alone changes nothing, because the agent has no reason to call the tool. What makes it fire is an instruction in your project's context file, so it applies to every session without you asking for it. In Claude Code that file is `CLAUDE.md` in the repository root; for the equivalent elsewhere, see [where to place these instructions](../guardrails.md#where-to-place-these-instructions).

{% include sigrid-mcp/quality-gate-prompt.md %}

Two details in that text do the work, and both are easy to lose when you reword it. It names the tool, which makes the outcome verifiable: "check code quality" is advice, while "run `guardrails:quality_check` on all files you changed" is an instruction you can confirm was followed. And it is tied to task completion, which is the only placement that fires reliably, because an agent decides for itself when it is finished.

Then add your own conventions under Code Principles: the framework patterns your codebase actually uses, and a line for every recurring mistake you find yourself correcting. That file is where a correction becomes permanent.

## What a session looks like

Say you are adding partial refunds to a `PaymentService`, and you ask for it like this:

```
Add support for partial refunds. A refund can now be for less than the
original amount, and we need to reject refunds that exceed what's left.
```

The agent opens the file, finds the existing `refund` method and its call sites, and makes the obvious change. The remaining-amount check goes into `refund`, which grows from about 30 lines to about 50 and picks up two new branches. The tests pass. Without the gate, this is where it would report done.

Instead it calls `guardrails:quality_check` on the file it changed, and the response flags `refund` under "Write Short Units of Code" and "Write Simple Units of Code" at HIGH severity, with the line range of the method. So it refactors: the validation moves into a `validateRefundable` helper, the amount arithmetic into a small value method, and `refund` is left doing the orchestration. A second call on the same file comes back clean, the tests still pass, and the summary you get says what changed, that the gate passed, and anything it deliberately left alone.

<a href="../../../images/mcp/guardrails/guardrails-refactoring-loop.png" target="_blank"><img src="../../../images/mcp/guardrails/guardrails-refactoring-loop.png" width="800" alt="Claude Code implementing a method, running Sigrid guardrails that flag maintainability issues, then refactoring by extracting a helper method" /></a>

The refactor is the part that matters. You did not have to name the problem, and the agent did not have to guess what "too complex" means in your codebase. It got a location, a metric, and a threshold, and it had your code principles to fix against.

## Checking that the gate fired

"Quality gate passed" is a claim, and it deserves the same skepticism as a claim about tests. We would check it properly for the first few sessions in a new repository, to confirm the setup does what you think it does. Your CLI shows tool calls, so look for at least one `guardrails:quality_check` call after the last edit. A check that ran before the final edit tells you nothing about the code you are about to commit. Look at the file list too: the tool takes one file per call, so a four-file change means four calls, and if only one shows up then the gate covered a quarter of your work. Asking directly is enough:

```
Which files did you run the quality check on? List them against the files you changed.
```

The gate deliberately lets the agent leave a finding alone when the fix would cascade outside the task, and that clause is what stops a small feature from turning into a three-hour refactor. It is fine as long as the agent says so. If findings were left behind silently, tighten the wording rather than trusting the next run. Then read the diff: Guardrails tells you the code is well structured, not that it does what you asked.

The failure worth watching for is the quiet one, where an agent has stopped calling the tool and reports success anyway. Check the calls, not the summary.

Which points at the honest limit of a context file. An instruction is followed most of the time, and that is not the same as always. The less of the output you read, the more that gap costs you, so back the instruction with something mechanical: [Sigrid CI](../../../sigridci-integration/using-sigridci.md) in a pre-commit hook or in your pipeline runs the same deterministic checks where the code leaves your machine, whatever produced it.

## Where to go next

There is also a limit to what Guardrails can see, since it only ever looks at the files in front of it. Architecture drift, vulnerable dependencies, and duplication spread across files need the analysis of the whole system, which is the other reason to run Sigrid CI; the `sigrid-ci-feedback` skill does it locally before you push. From there:

- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for the debt that is already there
- [Triaging security and reliability findings](triaging-security-reliability.md) for the findings Sigrid already knows about
- [Guardrails MCP reference](../guardrails.md) for supported technologies and the tool itself

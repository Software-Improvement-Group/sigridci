# Sigrid Axis skills reference

The Sigrid Axis skills run a Sigrid job end to end in your agent: record your Sigrid system, check a change before you push it, explore the structure of the code, plan what to fix, and fix it as local commits.

The skills come with the [Claude Code plugin](installation.md#install-the-claude-code-plugin). Other agentic tools that read `SKILL.md` files can use them too; see [use the skills in other agentic tools](installation.md#use-the-skills-in-other-agentic-tools). Every skill reads [the Sigrid profile](configuration.md#the-sigrid-profile) for your customer, system, and conventions, so run `setup` first.

## Call a skill

Type the skill as a slash command. Most skills take an argument that picks the Sigrid model to work on:

```
/diagnose maintainability
/triage-findings security under src/payments/
/autofix security
```

The phrasing is flexible, and `/change-feedback for security problems` works as well as `/change-feedback security`. If you name no model, the skill asks, except for `change-feedback`, which has a default. Name the wrong kind of model, such as `/diagnose security`, and the skill explains the difference in one line and hands over to the right one.

Claude Code also accepts the skills with the plugin prefix, as in `/axis:diagnose`.

## The skills at a glance

Here are the skills, grouped by the [lifecycle phase](README.md#the-agentic-lifecycle) they belong to:

| Skill | Phase | Models |
|-------|-------|--------|
| `setup` | None | None |
| `change-feedback` | Prevent | maintainability, architecture, open-source, security |
| `explore-architecture` | Ground | None |
| `diagnose` | Plan | maintainability, architecture |
| `triage-findings` | Plan | security, reliability, open-source |
| `autofix` | Improve | maintainability, architecture, security, reliability, open-source |

The plan skills and `autofix` work as a pair. You plan with `diagnose` or `triage-findings`, and the plan is saved as a [handover](#handovers). Then `autofix` fixes what the plan named, straight away or later.

### `setup`

Writes the [Sigrid profile](configuration.md#the-sigrid-profile) for the repository, `.sigrid/profile.md`. It detects your Sigrid system from a `sigrid.yaml` file or a Sigrid CI pipeline, asks for what it cannot tell, and asks whether you want to customize how the skills behave. Run it once in each repository, and commit the file it writes.

Setup only reads the repository and writes the profile. It never changes your code, never calls the MCP server, and never stores your token.

### `change-feedback`

```
/change-feedback [maintainability|architecture|open-source|security]
```

Gives you Sigrid's verdict on your local changes before you commit or push, without starting a remote pipeline or publishing anything to Sigrid. With no argument, it runs maintainability, open-source, and security.

- **Maintainability, open-source, and security** run [Sigrid CI](../sigridci-integration/using-sigridci.md) on your working tree, in one run for all three. This needs Python 3.7 or later, network access to `github.com` to fetch the Sigrid CI scripts, and your token in a `SIGRID_CI_TOKEN` or `SIGRID_TOKEN` environment variable. A run can take up to 30 minutes.
- **Architecture** finds the new references across directories in your diff, by default against the baseline branch, and checks each one against Sigrid's measured dependency graph. A reference that matches an existing dependency is clean. One that adds a dependency, closes a cycle, or goes around a facade is drift, and the report names the file it should route through instead. See [preventing architecture drift](guides/preventing-architecture-drift.md).

### `explore-architecture`

```
/explore-architecture [question about the codebase structure]
```

Hands your question to the `architecture-explorer` agent and relays its answer. With no question, it gives an overview of the codebase structure.

The `architecture-explorer` agent combines Sigrid's measured dependency graph with reading files. It uses the graph for structural questions, such as which directories depend on which or what calls into a module, and it reads the files for what a directory is responsible for or where a symbol is used. The graph describes the baseline branch as Sigrid last analyzed it, so local changes are not in it. Calls Sigrid could not resolve to one definition, such as dynamic dispatch or dependency injection, are missing from it as well, and a missing edge means unmeasured rather than independent.

The agent also starts on its own when you ask a structural question in plain words, such as "where is this used" or "what does this directory depend on". The **Nudge to use architecture-explorer** [plugin option](configuration.md#plugin-options) makes that more likely.

### `diagnose`

```
/diagnose [maintainability|architecture]
```

Reads the current state of your system for a metrics-based model and names the one fix most worth making. It never changes code.

- **Maintainability** finds the property most worth fixing and the code driving it. It reports one primary candidate, the runner-ups, and the candidates it rejected with the rule that removed them, such as generated code, a finding your team already accepted, or a fix that would change a public API. See [reducing technical debt](guides/reducing-technical-debt.md).
- **Architecture** finds the directory whose structure is most worth fixing, based on Sigrid's measured dependency graph, and names the concrete fix.

If nothing qualifies, it says so and stops. Otherwise it writes a handover and offers to fix it.

### `triage-findings`

```
/triage-findings [security|reliability|open-source]
```

Goes through a list of findings for a findings-based model and decides each one: false positive, accepted risk, needs a person, or will fix. It never changes code and never opens issues. You can give it a finding ID, a finding pasted from Sigrid, or a scope such as a directory, and it works through the backlog in that scope.

- **Security and reliability** read the flagged code at its file and line before classifying it. A false positive or an accepted risk needs a file, a line, and one sentence of evidence. The decisions go back to Sigrid as finding statuses, and you confirm false positives and accepted risks before they are written. See [triaging security and reliability findings](guides/triaging-security-and-reliability-findings.md).
- **Open-source** groups the findings per dependency, because one version bump can clear several of them. For dependencies that need research, it starts the `osh-researcher` agent, which looks up advisories and versions in public registries and has no access to your files or to Sigrid. Open Source Health findings have no status in Sigrid, so the decisions live in the handover and the report.

At the end, it lists every finding that needs a person, with what is blocking it, and offers a handover for the findings to fix.

For open-source triage, the research agent queries package registries and advisory databases. You can pre-allow these hosts in `.claude/settings.json`, so it does not stop to ask: `pypi.org`, `npmjs.com`, `mvnrepository.com`, `central.sonatype.com`, `crates.io`, `nuget.org`, `github.com`, and `rustsec.org`.

### `autofix`

```
/autofix [maintainability|architecture|open-source|security|reliability] [handover path]
```

Fixes what a plan named, as commits on a local branch.

- **Maintainability** refactors the candidates from the plan one at a time, runs your tests before and after each change, and checks every changed file with Guardrails.
- **Architecture** moves or splits files, adds a facade, or reroutes calls, then recounts the call sites against the numbers `diagnose` predicted.
- **Security and reliability** fix the will-fix findings, one commit each. At the end, `autofix` asks whether to set them to `FIXED` in Sigrid.
- **Open-source** makes one commit per dependency, verified with `change-feedback open-source`. A dependency that turns out to need a person goes in the report with the options the research found.

It needs a clean working tree, or it asks. On the baseline branch it creates a new branch, on a branch that contains the baseline it stays there, and otherwise it asks. It never fetches or pulls. Every commit message ends with the trailer `Generated-by: Sigrid Axis autofix`.

It needs build and test commands for your repository, and it works from a handover. Pass a handover path, or it picks the handover for the model itself. With no handover, it runs the plan skill for the model first.

## How the skills interact with you

The skills ask only at real decision points that you have not already answered, in your prompt, in the handover, or by telling the skill not to ask. Choosing between two upgrade paths for a dependency is such a point, and so is a refactoring that runs into a constraint the code does not show, such as a serialization format.

When a skill cannot ask, or you told it not to, it takes the conservative default: the smaller change, or skipping the item and logging why. Every choice it made that way is in its final report, so read the report for more than the successes.

There are no separate interactive and autonomous modes. The usual flow is to plan interactively, then fix from the handover.

One exception: `triage-findings` always asks before it writes a false positive or an accepted risk to Sigrid, unless you explicitly tell it not to ask for that. It never assumes this from the run being unattended or scripted.

## Handovers

A handover carries a plan from `diagnose` or `triage-findings` to `autofix`, across sessions, worktrees, and people. It is written for an agent that has none of your session's context, so it has to stand on its own.

At the end of a plan run with something to fix, the skill writes the handover and offers three choices:

- **Fix now**, the default, continues in the same session with `/autofix <model>` on this handover.
- **Save for later** leaves the handover for you to read and edit. Run `/autofix <model>` whenever you like, in this session or a new one. The skill recommends this after a long run.
- **Stop** ends the run.

Handovers are written to `.sigrid/handovers/<model>-<timestamp>.md`, for example `.sigrid/handovers/security-20261001-141500.md`. A new plan never overwrites an existing handover. Handovers are personal, so the skill adds a `.gitignore` to that directory and they are never committed.

A handover contains:

- The model, the timestamp, and the target as concrete file paths.
- The chosen fix and why, in terms you can check against the code.
- The alternatives that were rejected and the decisions you made, so the next session does not reopen them.
- A status per item: done, skipped with the reason, or remaining.
- Pointers back to the sources: Sigrid finding IDs, metric values, files, and lines.

`autofix` picks its input in this order: the handover a plan run just wrote in the same session, a handover path you pass, or the only open handover for the model. If there are several, it asks which one, newest first. Before acting on an item, it checks the item still matches the code, and it marks an item that moved or was already fixed as skipped. It updates the status per item as it goes. When nothing is left, it renames the file to `<model>-<timestamp>.done.md`. That file stays as the record of the run and your decisions, and `autofix` never picks it again.

## What the skills never do

The skills stop at local commits and Sigrid statuses. They never:

- Push a branch.
- Open a merge request or a pull request.
- Open an issue.

Pushing, change requests, and issues are up to you or your pipeline. The report at the end of each run lists what needs a person, so you have what you need to open an issue yourself.

The plan skills go further than that: `diagnose` and `triage-findings` never change code at all, and `setup` only writes the profile.

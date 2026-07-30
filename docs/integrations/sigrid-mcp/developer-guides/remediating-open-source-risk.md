# Remediating open source risk with auto-fix agents

This guide walks through running an [auto-fix agent](../autofix-agents.md) on a schedule so new dependency risk gets researched, fixed, and verified without anyone watching, and arrives as a merge request you review like any other.

Dependency risk is different from the other work an auto-fix agent does. A new critical CVE in a library you use appears without anyone touching your code, the fix is usually a one-line version bump, and the value of fixing it decays by the day. That combination makes it the one workflow worth running unattended.

What comes out is a merge request or an issue, one per dependency, reviewed through whatever process you already have. The agent never merges anything, and your existing review and CI rules apply unchanged.

If you are clearing an existing backlog of dependency risk for the first time, run it interactively for that pass. It tells you which of your dependencies are pinned for a reason, and that is much cheaper to learn in one session than from eleven merge requests.

## Prerequisites

- A repository with real dependencies, analyzed by Sigrid [Open Source Health](../../../capabilities/system-open-source-health.md).
- A connected git-host MCP server. The skill refuses to run without one, and there is deliberately no local-only fallback.
- A profile recorded with `/sigrid:setup`, because an unattended run cannot stop to ask you anything.
- A test suite good enough that a green build after a version bump means something.
- An environment that can run [Sigrid CI](../../../sigridci-integration/using-sigridci.md), which is how the agent verifies a risk is actually cleared.
- A team where a merge request opened by a bot is normal, so someone will actually look at it.

## Why the agent needs help

The bump is easy. Knowing which bump is not, and the gap between those two is where an unsupervised agent produces confident nonsense.

The version that fixes the CVE is not in the advisory in a usable form. Advisories give affected ranges. What you need is the lowest version that clears every risk on that dependency, does not break the API you use, and does not drag in a conflicting transitive. That takes research across advisory databases and the package registry.

Nor can "fixed" be established by editing a manifest. Only re-running the analysis confirms the risk is gone, so an agent that bumps a version and reports success has reported an intention.

Then there is the fact that half the risk types have no version bump at all. Sigrid flags freshness, legal, activity, stability, and management risks alongside vulnerabilities. An abandoned library is not fixed by upgrading it, and a missing license declaration is not a code change.

Unattended operation adds a fourth requirement on top of those three: failure has to be safe. Nobody reads the reasoning as it happens, so the run has to end in a reviewable artifact whether it succeeded or not.

The `fix-osh-risk` skill is built around those four facts. It groups findings by dependency, because one bump usually clears several CVEs. It researches the upgrade path with a separate subagent that has web access only, no repository files and no Sigrid context. It verifies with Sigrid CI before it will open a merge request. And when it cannot fix something confidently it takes an off-ramp and opens a researched issue, which is why a run can never end in a local change nobody sees.

## Set up the automation

{% include sigrid-mcp/primitives.md %}

The fourth one carries this workflow, since the trigger is what makes it unattended.

### 1. Install the plugin and connect a git host

{% include sigrid-mcp/plugin-install.md setup=true %}

Connect a git-host MCP server for GitLab, GitHub, or whichever forge you use. The skill is forge-agnostic, and it needs to be able to create a branch, a merge request, and an issue.

`/sigrid:setup` then asks for the baseline branch, your branch naming, whether merge requests open as drafts, and who reviews them. Take the time to get these right, because an unattended run cannot stop to ask, and anything missing either aborts the run or comes out wrong. See [plugin configuration](../configuration.md) for what it stores.

### 2. Set the boundaries

The context file is where you put the things a bot must not decide on its own:

```
## Dependency remediation rules

- Patch and minor bumps: open a merge request. Major bumps: open an issue instead.
- Never touch these pins, they are deliberate: `torch==2.1.0` (CUDA build),
  `protobuf<4` (breaks the generated clients).
- Vulnerability and freshness risks: remediate. Activity, stability, and legal
  risks: issue only, we decide those ourselves.
- One dependency per merge request.
- Tests must pass and Sigrid CI must confirm the risk is cleared. Otherwise
  open an issue with what you tried.
```

Deliberate pins are the entry that saves you the most annoyance, since a version pinned for a reason invisible in the manifest looks exactly like neglect to any tool. Write the reason next to it, and consider a comment in the manifest too, for the humans. Revisit the routing rules every quarter or so, because what they encode is last quarter's tolerance for risk.

### 3. Clear the backlog first, interactively

Before you automate anything, do one supervised pass:

```
/sigrid:fix-osh-risk
```

It asks what to work on and walks through dependencies one at a time. Upgrade choices come framed in terms of what they cost you, such as "patch bump, no code changes" versus "minor bump, one deprecated call to update", so you are not picking version numbers.

We think this pass is worth a morning, for two reasons. It empties the queue, so the automated runs afterwards only ever see genuinely new risk. And it shows you where your rules are wrong before a scheduled job starts acting on them.

### 4. Add the trigger

The trigger's job is to notice new risk and start a headless run. A scheduled CI job is the simplest version that works: a nightly pipeline that asks for current risks and remediates them.

```
osh-remediation:
  rule: scheduled, nightly
  steps:
    - claude -p "Fix the open source health risks with severity HIGH or
      CRITICAL for acme/payment-platform. Work autonomously, following the
      dependency remediation rules. One merge request per dependency; open an
      issue where you cannot fix confidently."
```

Treat that as a sketch to adapt to your CI system, not a working pipeline file. What matters is what it is made of:

- **A schedule, not a code push.** New dependency risk appears when an advisory is published, which has nothing to do with your commits. We find nightly is usually right, and hourly buys you very little.
- **A severity floor.** Without one you get merge requests for every low-severity freshness notice, and the whole thing gets muted within a week.
- **A prompt that reaches the skill.** Phrase it in the terms the skill triggers on, such as fixing open source risks or dependency vulnerabilities, without naming the skill. That also works on a CLI where the procedure is a plain instruction in your context file.
- **A non-interactive run** (`claude -p` in Claude Code, the equivalent flag elsewhere). In this mode the skill takes its defaults, never asks, and downgrades to an issue when it is uncertain instead of blocking. That is what makes unattended runs safe. It also means a missing profile value aborts the run rather than prompting, which is why step 1 matters.
- **Credentials with the right scope.** The job needs a Sigrid token and git-host credentials that can push a branch and open a merge request, and nothing more. It must not be able to merge, approve, or push to your baseline branch. Verify that once, when you set the job up.

If you would rather trigger on a signal than on a clock, the [Sigrid REST API](../../sigrid-api-documentation.md) exposes the same open source health data, so a job can check for new risk and only start an agent when there is something to do.

## What comes out

The artifact is the deliverable, so it is what to look at.

A **merge request** appears when the agent was confident and Sigrid CI confirmed the risk is gone. It contains:

- The dependency, by package URL, and the risks it clears, whether CVEs or Sigrid risk dimensions.
- Old version to new, and whether the dependency is direct, transitive, or an override.
- Links to the advisories the research was based on, so you can check the claim.
- Residual risk, and explicitly what was not verified.
- A branch off your baseline branch, following your naming convention, with the description opened by a banner marking it as agent-generated.

An **issue** appears when the agent could not fix the risk confidently: an abandoned library, a major bump, no version that clears every CVE at once, or tests that failed. The issue carries the research, the options with their trade-offs, source links, and the diff it tried before backing out, which is enough for a human to make the call in one sitting. Getting an issue where you expected a fix is usually the skill working as intended, since activity, stability, and most legal risks have no bump available. If a whole category always comes out as an issue and always gets the same answer from you, write that answer into your rules.

If a merge request or issue already exists for that dependency, the agent comments on it with what is new instead of opening a second one.

## Review what it opens

We hold these to the same standard as a colleague's dependency bump.

Check that Sigrid CI confirmed the fix, meaning the analysis re-ran and the finding is gone, not that the version was bumped. The description says so, and if it does not, that is your signal: the verification step did not run, so look for the `sigrid-ci-feedback` step in the CI job log. This is also the case the skill is supposed to off-ramp on, when tests pass but the bumped version does not clear every CVE on that dependency.

Open one of the linked advisories and check that the new version is outside the affected range. Worth doing properly on the first few merge requests from a new setup, then spot-checking. The diff should be the bump and nothing else: a manifest change, a lock file change, and the call sites if the API changed, with anything beyond that explained in the description. And your own CI has to be green, because the agent's verification does not replace your pipeline.

Two things are worth watching across a few weeks. Issues should outnumber merge requests on the hard risk types, and if everything comes out as a merge request then the off-ramp is not firing and confidence is being manufactured somewhere. The queue should also drain: if new risk arrives faster than it clears, the trigger is working and the review is not. That is where we usually see this kind of automation stall, and the fix is an owner or a rotation, not a change to the job. An unreviewed merge request looks like the risk is handled when it is not.

If a run returns no risks at all, check with `opensourcehealth:get_risks` at a lower `risk_min` before concluding you are clean. If it opens dozens of merge requests at once, the backlog was never cleared and the floor is too low; the skill consolidates into a single issue past roughly five unrelated dependencies, so seeing dozens means it was invoked per dependency.

## Where to go next

Dependencies are one source of risk arriving without anyone changing your code. The findings in the code you wrote need a different loop:

- [Triaging security and reliability findings](triaging-security-reliability.md) for the findings in your own code
- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for maintainability debt
- [Open Source Health](../../../capabilities/system-open-source-health.md) for the risk dimensions Sigrid reports
- [Auto-fix agents MCP reference](../autofix-agents.md) for tools and parameters

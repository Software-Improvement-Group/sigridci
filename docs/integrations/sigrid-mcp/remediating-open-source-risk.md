# Remediating open source risk with auto-fix agents

Dependency risk is different from the other work an [auto-fix agent](autofix-agents.md) does. A new critical CVE in a library you use appears without anyone touching your code, the fix is usually a one-line version bump, and the value of fixing it decays by the day. That combination makes it the one workflow worth running unattended.

So this guide covers the trigger that starts the run and the merge request that comes out of it, rather than a chat transcript. When this works, nobody is watching the middle.

Everything here applies to any agentic CLI. The worked configuration uses Claude Code, since that is the only CLI we ship a plugin for.

## When you'd do this, and who's at the keyboard

Nobody, at the moment it runs. That is the design. Somebody set it up, and somebody reviews the merge request it opens, usually the team that owns the repository, through their normal review process.

Set it up when:

- The repository has real dependencies and Sigrid [Open Source Health](../../capabilities/system-open-source-health.md) analyses it.
- You have a test suite good enough that a green build after a version bump means something.
- A merge request opened by a bot is normal in your team, and someone will look at it.

Run it interactively instead when you are clearing an existing backlog of dependency risk for the first time. That first pass tells you which of your dependencies are pinned for a reason, and it is much cheaper to learn that in a session than from eleven merge requests.

The agent never merges anything. Its output is a merge request or an issue, and your existing review and CI rules apply unchanged.

## Why the agent needs help here

Dependency remediation looks trivial and is not. The bump is easy. Knowing which bump is not.

- **The version that fixes the CVE is not in the advisory in a usable form.** Advisories give affected ranges. What you need is the lowest version that clears every risk on that dependency, does not break the API you use, and does not drag in a conflicting transitive. That takes research across advisory databases and the package registry.
- **You cannot establish "fixed" by editing a manifest.** Only re-running the analysis confirms the risk is gone. An agent that bumps a version and reports success has reported an intention.
- **Half of the risk types have no version bump at all.** Sigrid flags freshness, legal, activity, stability, and management risks alongside vulnerabilities. An abandoned library is not fixed by upgrading it, and a missing license declaration is not a code change. An agent that treats every risk as a bump produces confident nonsense on those.
- **Unattended means failure has to be safe.** Nobody reads the reasoning as it happens, so the run has to end in a reviewable artefact whether it succeeded or not.

The `fix-osh-risk` skill is built around those four facts. It groups findings by dependency, because one bump usually clears several CVEs. It researches the upgrade path with a separate subagent that has web access only, with no repository files and no Sigrid context. It verifies with Sigrid CI before it will open a merge request. And when it cannot fix something confidently, it takes an off-ramp and opens a researched issue instead. Every run ends in a merge request or an issue, one per dependency, and never in a local change nobody sees.

## Setup

The four primitives, with the trigger doing the work this time:

{% include sigrid-mcp-primitives.md %}

### 1. Tool access, plus a git host

```
/plugin marketplace add Software-Improvement-Group/sigrid-ai-toolkit
/plugin install sigrid@sigrid-ai-toolkit
/sigrid:setup
```

Two prerequisites go beyond the other guides, and the skill refuses to run without either.

- **A connected git-host MCP server**, for GitLab, GitHub, or whichever forge you use. The skill is forge-agnostic, but it must be able to create a branch, a merge request, and an issue. There is deliberately no local-only fallback.
- **A profile with your conventions recorded.** `/sigrid:setup` asks for the baseline branch, your branch naming, whether merge requests open as drafts, and who reviews them. Unattended runs cannot ask, so anything missing here either stops the run or comes out wrong. See [plugin configuration](configuration.md).

The skill also uses [Sigrid CI](../../sigridci-integration/using-sigridci.md) through the `sigrid-ci-feedback` skill for verification, so the environment needs to be able to run it.

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

Deliberate pins are the entry that saves you the most annoyance. A version pinned for a reason invisible in the manifest looks exactly like neglect to any tool.

### 3. Clear the backlog first, interactively

Before you automate anything, do one supervised pass:

```
/sigrid:fix-osh-risk
```

It asks what to work on and walks through dependencies one at a time. It frames upgrade choices in terms of what they cost you, such as "patch bump, no code changes" versus "minor bump, one deprecated call to update", instead of asking you to pick version numbers.

Two reasons this pass is worth a morning. It empties the queue, so the automated runs afterwards only ever see genuinely new risk. And it shows you where your rules are wrong before a scheduled job acts on them.

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

Treat that as a sketch to adapt to your CI system rather than a working pipeline file. What matters is what it is made of:

- **A schedule, not a code push.** New dependency risk appears when an advisory is published, which has nothing to do with your commits. Nightly is usually right, and hourly buys you very little.
- **A severity floor.** Without one you get merge requests for every low-severity freshness notice, and the whole thing gets muted within a week.
- **A prompt that reaches the skill.** Phrase it in the terms the skill triggers on, such as fixing open source risks or dependency vulnerabilities, rather than naming the skill. That also works on a CLI where the procedure is a plain instruction in your context file.
- **A non-interactive run** (`claude -p` in Claude Code, the equivalent flag elsewhere). In this mode the skill takes its defaults, never asks, and downgrades to an issue when it is uncertain instead of blocking. That is what makes unattended runs safe. It also means a missing profile value aborts the run rather than prompting, which is why step 1 matters.
- **Credentials with the right scope.** The job needs a Sigrid token and git-host credentials that can push a branch and open a merge request, and nothing more. It must not be able to merge, approve, or push to your baseline branch.

If you would rather trigger on a signal than on a clock, the [Sigrid REST API](../sigrid-api-documentation.md) exposes the same open source health data, so a job can check for new risk and only start an agent when there is something to do.

## What comes out

The artefact is the deliverable, so this is what to look at.

**A merge request**, when the agent was confident and Sigrid CI confirmed the risk is gone. It contains:

- The dependency, by package URL, and the risks it clears, whether CVEs or Sigrid risk dimensions.
- Old version to new, and whether the dependency is direct, transitive, or an override.
- Links to the advisories the research was based on, so you can check the claim rather than take it.
- Residual risk, and explicitly what was not verified.
- A branch off your baseline branch, following your naming convention, with the description opened by a banner marking it as agent-generated.

**An issue**, when it could not fix the risk confidently: an abandoned library, a major bump, no version that clears every CVE at once, or tests that failed. The issue carries the research, the options with their trade-offs, source links, and the diff it tried before backing out. That is enough for a human to make the call in one sitting.

If a merge request or issue already exists for that dependency, the agent comments on it with what is new instead of opening a second one.

## What good looks like, and how you verify it

For the setup, once:

- **A supervised run happened first**, and you agreed with its choices.
- **Every risk type routes where you want it.** Trigger one issue-only risk deliberately and confirm it comes out as an issue.
- **The credentials cannot merge.** Verify this rather than assume it.

For each merge request, as a reviewer:

- **Sigrid CI confirmed the fix.** Not that the version was bumped, but that the analysis re-ran and the finding is gone. The description says so, and if it does not, that is your signal.
- **The advisory matches the claim.** Open one of the linked advisories and check that the new version is outside the affected range. Do this on the first few merge requests from a new setup, then spot-check.
- **The diff is the bump and nothing else.** A manifest change, a lock file change, and the call sites if the API changed. Anything beyond that needs an explanation in the description.
- **Your own CI is green.** The agent's verification does not replace your pipeline.

Across a few weeks:

- **Issues outnumber merge requests on the hard risk types.** That is correct. If everything comes out as a merge request, the off-ramp is not firing and confidence is being manufactured.
- **The queue drains.** If new risk arrives faster than it clears, the trigger is working and the review is not.

## When it goes wrong, and the recovery move

| What you see | What is happening | What to do |
|---|---|---|
| The run aborts immediately | A prerequisite is missing, such as no git-host MCP or a profile value an unattended run cannot ask for | Read the error, run `/sigrid:setup`, and confirm the git-host server is connected in the CI environment too |
| A merge request per dependency, dozens of them | The backlog was never cleared, and the floor is too low | Close them, do a supervised pass, and raise the severity floor. The skill consolidates into one issue past roughly five unrelated dependencies |
| It bumped a deliberate pin | The pin's reason exists only in someone's head | Add it to the context file with the reason. Consider a comment in the manifest too, for the humans |
| Tests pass, Sigrid CI still flags the risk | The version bumped does not clear every CVE on that dependency | This is the case the skill off-ramps on. If it opened a merge request anyway, the verification step did not run, so check the CI job log for the `sigrid-ci-feedback` step |
| Merge requests for risks you do not act on | Routing rules are missing | Put the risk-type routing in the context file: which dimensions get a merge request, and which get an issue |
| An issue where you expected a fix | Working as intended, since activity, stability, and most legal risks have no bump | Read the research and decide. If a whole category is always issues and always the same answer, write that answer into your rules |
| Nobody reviews the merge requests | The bottleneck moved to review, which is where automation usually stalls | Assign an owner or a rotation. An unreviewed merge request looks like the risk is handled when it is not |
| No risks returned | The severity floor or dimension filter is too narrow, or the system is genuinely clean | Check with `opensourcehealth:get_risks` at a lower `risk_min` before concluding you are clean |

## Habits worth keeping

- **Clear the backlog by hand, then automate.** Automation on top of a backlog produces noise, and noise gets muted.
- **Keep credentials minimal.** Push a branch and open a merge request, with nothing that can merge.
- **Review as you would a colleague's dependency bump.** Same standard. Check the advisory link on the first few, then trust the pattern and spot-check.
- **Keep the deliberate pins written down.** Every pin with an invisible reason is a merge request you will reject twice.
- **Let the agent open issues.** A researched issue on an abandoned library is the correct output.
- **Review the routing quarterly.** Your rules encode last quarter's tolerance for risk.

## Next

- [Triaging security and reliability findings](triaging-security-reliability.md) for the findings in your own code
- [Reducing technical debt with auto-fix agents](reducing-technical-debt.md) for maintainability debt
- [Open Source Health](../../capabilities/system-open-source-health.md) for the risk dimensions Sigrid reports
- [Auto-fix agents MCP reference](autofix-agents.md) for tools and parameters

# Using Sigrid CI

This page is about interacting with Sigrid CI from a user perspective. If you're looking for instructions on how to
integrate Sigrid CI in your development platform, locate the *"Sigrid CI: Pipeline integration"* in the menu. See the
[option reference](../reference/client-script-usage.md) if you want to know which configuration options are available. 
{: .attention }

Sigrid CI does two things:

1. Sigrid CI **publishes code to Sigrid**. This integration makes it easier to keep your Sigrid up-to-date, since
   changes to your code are automatically reflected in Sigrid.
2. Sigrid CI **provides feedback on your changes**. This allows development teams to consume this feedback as part
   of the normal development process.

In a typical development process, step 1 would take place whenever you merge something into your main/master branch,
and step 2 would apply to your [pull requests](https://www.atlassian.com/git/tutorials/making-a-pull-request).
If you're using a different process, this documentation contains guidelines on where and how Sigrid CI can be used
in [different development processes](development-workflows.md).

The remainder of this page is about **how** Sigrid CI gives feedback.

## What does Sigrid CI give feedback on?

Sigrid CI gives software quality feedback for multiple quality aspects. Which aspects depends on your Sigrid license:

- [Maintainability feedback](#maintainability-feedback)
- [Open Source Health feedback](#open-source-health-feedback)

If you do *not* want feedback for one of these aspects, you can explicitly define the `--capability` option in
the [Sigrid CI configuration](../reference/client-script-usage.md).

## How does Sigrid CI give feedback?

Sigrid CI gives you feedback on different quality aspects. You can find more information on our feedback for
[Maintainability](#maintainability-feedback) and [Open Source Health](#open-source-health-feedback) in the sections
below. However, there are also some shared principles we apply across Sigrid CI:

- **Focus on objectives:** All Sigrid CI feedback relates your changes to the
  [objectives](../capabilities/portfolio-objectives.md) you've defined in Sigrid. Objectives provide *context*.
  It's not reasonable to expect the same level of quality for a legacy system as for a brand new mission-critical
  system. Objectives allow you to provide this context, so that every system gets a target that is both reasonable
  and achievable. Using objectives also means there is a common thread between what you see in your pipeline versus
  what you see in the [management dashboard](../capabilities/management-dashboard.md), which helps to make different
  stakeholders in the IT organization have a shared perspective.
- **Strive for good, not for perfection:** It's not realistic to expect teams, who often already have a high workload,
  to be able to fix every single issue right away. This is another area where defining objectives help you to set a
  baseline on what you consider good-enough quality.
- **Don't forget about positive feedback:** Sigrid CI feedback is split into categories that should be familiar to
  anyone who has participated in an [agile retrospective](https://www.atlassian.com/agile/scrum/retrospectives):
  *What went well* and *What could be better*. We intentionally start with the positive feedback, to put the emphasis
  on how people improved technical debt. This helps to create a culture of quality awareness, and helps to point out
  that we see and appreciate people's efforts, and that we don't just want to flood them with endless lists of stuff
  they need to work on.

### Maintainability feedback

Maintainability feedback follows the [feedback structure](#how-do-you-deal-with-feedback-from-sigrid-ci) introduced
in the previous section. When it comes to your objective, Sigrid CI will let you pass as long as you're moving
*towards* your objective. As long as you keep making incremental improvements in the right direction, you'll get
there eventually. This approach means Sigrid CI is generally "nicer" than tools that require you to fix every single
issue right away.

<img src="../images/ci/maintainability-feedback.png" width="350" />

The reason Sigrid CI is "nice" is to encourage refactoring during normal development. Let's say you're working on
a normal, functional ticket. You find the file you're changing is full of technical debt. Ideally, you would try
to perform some minor refactorings while implementing your ticket. Obviously, we don't expect you to fix *everything*,
that would not be reasonable. The behavior we're going for is known as 
[the boy scout rule](https://deviq.com/principles/boy-scout-rule), where you should leave your code (or your campsite)
cleaner than you found it. 

### Open Source Health feedback

Sigrid CI gives feedback on security vulnerabilities and license risks in open source libraries. Sigrid also
checks other aspects of using open source libraries, such as freshness (i.e. how often you update), but those
are not part of Sigrid CI.

So why not give feedback on *all* aspects? In a word: Urgency. People generally security vulnerabilities or
license issues much more urgent than those other aspects. Updating a library can wait (but please not too long), fixing a vulnerability cannot
wait. Obviously, you should still manage those other aspects, as explained in our
[guidelines for healthy use of open source libraries](../workflows/best-practices-osh.md).

Sigrid CI does not require you to update every single open source library to address every single issues.
Which vulnerabilities and licenses are "allowed" versus "not allowed" is decided based on your
[objectives](../capabilities/portfolio-objectives.md). This means you can use a different objectives dependent on
the (type of) system. For example, you can decide to prevent high or critical severity vulnerabilities in public-facing 
systems, but only prevent critical vulnerabilities for internal systems.

<img src="../images/ci/osh-feedback.png" width="350" />

Unlike the [feedback for maintainability](#maintainability-feedback), you really do need to address every single
vulnerability and every single license issue that's blocking your objective. This is because of a difference in
urgency between maintainability and security: Maintainability is more of a "chronic" problem, while security
threats are "acute" and really do need to be mitigated right away.

Sigrid CI separates vulnerable open source libraries into two categories:

- **Vulnerable libraries for which a fix is available:** These have a straightforward mitigation: Update the open
  source library, ideally to the latest version, but at minimum to a version that is no longer vulnerable.
- **Vulnerable libraries for which no fix is available:** These cases are more difficult to manage, since there
  is no obvious solution or mitigation. These cases typically require more discussion on the exact details of the
  vulnerability and possible follow-up actions. This is explained in more detail, also from a process perspective,
  in our [guidelines on using open source](../workflows/best-practices-osh.md#how-to-remediate-vulnerabilities).

#### Adding Open Source Health feedback to an existing Sigrid CI configuration

If your Sigrid license includes Open Source Health, Sigrid CI will automatically give feedback on both Maintainability
and Open Source Health. If you do *not* want feedback on Open Source Health, even though you have a license for it,
you can explicitly add `--capability maintainability` to *only* receive feedback for Maintainability.

**If you use GitHub** you need one extra step: In your pipeline configuration, look for the
line `message-path: sigrid-ci-output/feedback.md`, and change this to `message-path: sigrid-ci-output/*feedback.md`.
Adding the asterisk allows you to get feedback on *all* Sigrid capabilities, not just maintainability.

### Security feedback (Beta)

Sigrid CI provides security feedback based on your [objectives](../capabilities/portfolio-objectives.md).
As with [open source vulnerabilities](#open-source-health-feedback-beta), you do need to fix every single
security finding that does not meet your objective.

<img src="../images/ci/security-feedback.png" width="350" />

When you encounter security findings during code reviews, there are three ways how you can deal with them:

- **Address the finding in the pull request:** It's always the best course of action to just address the finding
  within the pull request. This prevents the finding from ever going into the main/master branch, which is generally
  considered a best practice in [shift-left thinking](https://en.wikipedia.org/wiki/Shift-left_testing). 
- **Merge the pull request, manage the finding via Sigrid:** In some cases, the pull request author and reviewer might
  agree it's not feasible to address the finding right now. In those situations, it's OK to merge the pull request.
  This will cause the security finding to appear in Sigrid's
  [Security dashboard](../capabilities/portfolio-security.md), where it can be tracked.
- **Merge the pull request, mark the finding as a false positive in Sigrid:** Like any automated check, Sigrid can
  produce findings that are false positives. In those situations, if the pull request author and reviewer agree the
  finding is *actually* a false positive, it's OK to merge the pull request. You can then mark the finding as a false
  positive in Sigrid's [security page](../capabilities/system-security.md). False positives are automatically excluded
  from future Sigrid CI feedback. 

#### Adding Security feedback to an existing Sigrid CI configuration

- **All platforms:** You need to add the option `--capability maintainability,osh,security` to the Sigrid CI step in
  your pipeline configuration.
- **GitHub:** In addition to the above, you need one extra step: In your pipeline configuration, look for the
  line `message-path: sigrid-ci-output/feedback.md`, and change this to `message-path: sigrid-ci-output/*feedback.md`.
  Adding the asterisk allows you to get feedback on *all* Sigrid capabilities, not just maintainability.

## How do you deal with feedback from Sigrid CI?

Feedback from Sigrid CI is intended to be used in the context of a
[pull request](https://www.atlassian.com/git/tutorials/making-a-pull-request). Pull requests typically involve
two participants, the author and the reviewer, and both can use this feedback. When working on the pull request,
the author can use the feedback to make some corrections before asking for a review. When the pull request enters
the [code review](https://about.gitlab.com/topics/version-control/what-is-code-review/), the reviewer can use the
feedback as part of his or her review.

### Should you block your pipeline?

If you ask us: No. Any form of automated feedback will occasionally lead to results that are unfair, and Sigrid is
no  different. As explained above, we ideally want Sigrid CI feedback be used as input for a code review, with the
reviewer making the final call on whether to approve the review.

Still, we concede there are situations and organizations where you really do want to make Sigrid CI a mandatory check.
Therefore, we do provide the option to fail the pipeline if Sigrid objectives are not met. You can configure this
to make the pipeline fail on *any* Sigrid objective, but you can also make this behavior more nuanced by failing the
pipeline on certain types of objectives. The latter is configured using exit codes,
[as explained here](../reference/client-script-usage.md#letting-sigrid-ci-fail-your-pipeline).

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

Sigrid CI: Frequently Asked Questions
=====================================

## Table of contents

- [Which technologies do you support?](#which0technologies-do-you-support)
- [Where can I find more information about your metrics?](#where-can-i-find-more-information-about-your-metrics)
- [What is the maximum upload size?](#what-is-the-maximum-supported-upload-size)
- [Can I exclude certain files from being uploaded?](#can-i-exclude-certain-files-from-being-uploaded)
- [Do Sigrid CI uploads get added to the Sigrid dashboard?](#do-sigrid-ci-uploads-get-added-to-the-sigrid-dashboard)
- [What branch or commit does Sigrid CI compare against?](#what-branch-or-commit-does-sigrid-ci-compare-against)
- [Why am I being penalized for problems that were already there?](#why-am-i-being-penalized-for-problems-that-were-already-there)
- [Should we fail the build if the Sigrid CI check fails?](#should-we-fail-the-build-if-the-sigrid-ci-check-fails)
- [Why doesn't deleted code influence the rating?](#why-doesnt-deleted-code-influence-the-rating)

---

**Sigrid CI is currently in beta. Please [contact us](mailto:support@softwareimprovementgroup.com) if you have suggestions on how to make it more useful to you and your team.**

---

### Which technologies do you support?

Sigrid supports almost 300 different technologies, so we are pretty confident that we are able to support most projects out-of-the-box. Moreover, we are constantly adding support for new technologies, and extending our support for existing ones. This even includes some pretty specific technologies with a focused group of target users, such as proprietary programming languages developed in-house at our clients. 

If you are using a technology that you believe we do not support, please contact us using the contact information below, and we'll see what we can do.

### Where can I find more information about your metrics?

Sigrid itself includes a brief explanation of all metrics in the "refactoring candidates" page. If you need more information, you can find the [Guidance for producers](https://www.softwareimprovementgroup.com/wp-content/uploads/2019/11/20190919-SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability.pdf) on our website, which provides more details on what is measured and why.

For training purposes, SIG also published a book on [building maintainable software](https://www.amazon.com/Building-Maintainable-Software-Java-Future-Proof/dp/1491953527/ref=sr_1_7?dchild=1&qid=1610456817&refinements=p_27%3AJoost+Visser&s=books&sr=1-7&text=Joost+Visser), which contains detailed explanations on the metrics. It is not necessary to read the book to use Sigrid, but having training material available can be useful when training new or junior developers.

### What is the maximum upload size?

Sigrid CI is limited to uploads of 500 MB. This is mainly for performance reasons, since uploading and unpacking huge files takes some time, which endangers Sigrid CI's goal of providing quick feedback. Note that based on our experience 99% of repositories easily fit within this limit. Also, Sigrid will only measure the actual source code maintained by your development team. Other artifacts, such as libraries, binaries, or other non-source files are excluded.

### Can I exclude certain files from being uploaded?

Yes. In general, we only need to receive the actual source code, configuration and data is not required to perform the analysis and can be excluded from the upload.

Some files and directories are already excluded by default, based on common conventions for common technologies. For example, the following would be excluded automatically:

- The `node_modules` directory is excluded by default as it contains [NPM](https://www.npmjs.com) libraries
- The `target` directory is excluded as it contains build output from [Maven](https://maven.apache.org)

In addition to that, you can also exclude files and directories specifically for your project. This is done using the `--exclude` parameter, which is explained in the [configuration documentation](integration.md) page.

### Do Sigrid CI uploads get added to the Sigrid dashboard?

No. This is intentional: Sigrid CI tends to operate on pull requests, which are often branches that are a work-in-progress and still need to be reviewed. Adding every single build to the Sigrid dashboard would create a lot of noise, which makes it harder to use the dashboard for spotting trends and reporting. This is why there are two separate streams of uploads: one used for Sigrid CI (based on branches/pull requests), and one used to feed the Sigrid dashboard (based on a relatively stable branch, such as main).

Of course, one size doesn't fit all. Post-beta versions of Sigrid CI will at least give the *option* to also publish uploads to the Sigrid dashboard, so that every team can decide for themselves which uploads should be visible in the dashboard and which should not.

### What branch or commit does Sigrid CI compare against?

Feedback is based on comparing the source code against the current baseline in Sigrid. In other words, this depends on the branch you're using to populate the Sigrid dashboard. This would typically be the main branch, though for some teams the baseline could also be based on a release branch, the development branch, or an improvement branch. The baseline therefore depends on the team's way of working and branching strategy. 

### Why am I being penalized for problems that were already there?

We created Sigrid CI to be used during code reviews, so the feedback is based on only the files you touched during your pull request, not the whole system. 

However, we do consider the *entire* contents of those files, not only the lines that you personally wrote. This is because of the [boy scout rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html): *"Always leave the campground cleaner than you found it."*. Refactoring and regular work are not two separate activities, they belong together. Having separate tickets to refactor certain areas is OK, but it indicates that something went wrong earlier in the process, that led to those issues being introduced in the first place. Ideally, small refactorings should be done *during* regular tickets. That means that any tickets affecting existing files should not *only* consist of implementing the new behavior. You should also strive to make small refactorings that relate to the code you're currently working on. You have the files open anyway! 

Obviously, there are still limits to the amount of refactoring you can do in the context of a single ticket. It's probably not a good idea to change the entire architecture while working on a bug fix. This is why Sigrid CI reports on a subset of [SIG's maintainability quality model](https://www.softwareimprovementgroup.com/methodologies/iso-iec-25010-2011-standard/): the code-level metrics are in scope, but the architecture-level metrics are not. This is due to the difference in *local* versus *global* refactorings. Making some changes in the context of a file tend to be fairly local, in that they don't affect a lot of other people. This is why those types of refactoring are fine to work on during regular development work. In contrast, architectural refactoring will have a big impact on a lot of people, so this is something that needs more consideration and needs to be planned separately.

### Should we fail the build if the Sigrid CI check fails?

That's obviously your decision and something that depends on your development process. However, if you're asking our advice, we would say a failing Sigrid CI check should produce a warning rather than an error. That might seem like ridiculous advice coming from a company that creates software quality tooling, but we can explain.

One of Sigrid's key goals is making software quality advice *reasonable*. It's easy to invent a thousand quality checks and making them all mandatory, failing the build as soon as a single violation is found. It's obviously possible to fix every single issue, but it's probably not worth it considering what you get in return. Sigrid focuses on a relatively limited set of metrics, to avoid overloading developers with tons of instructions. Moreover, a small amount of non-conformities is tolerated, as long as the overall quality doesn't drop below a certain level. 

We therefore believe in a comply-or-explain model. Obviously, you should still strive to pass the Sigrid CI check in the overwhelming majority of cases. However, in the rare cases the check fails, it's perfectly OK for the reviewer to overrule the check and accept the pull request, as long as the reviewer finds that the author had good reasons for deviating from the best practice in that particular case.

## Why doesn't deleted code influence the rating?

In general, deleting code improves maintainability. The less code you have, the less you have to maintain. Having less code also makes it easier to make structural changes, since such changes will require less effort.

So why does Sigrid CI only give ratings based on new and changed code, but doesn't reward you for deleting code? This is mostly to keep the rating simple: combining code quality and deleted code into a single metric would make it hard to understand. Also, the majority of pull requests are about adding new code or changing existing code, deleting code is less common, so we have chosen to not optimize for that scenario.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

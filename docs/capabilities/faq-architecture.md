Architecture Quality: Frequently Asked Questions
================================================

This FAQ specifically covers Sigrid's Architecture Quality functionality. Also check the [Sigrid FAQ](faq.md) for more information about Sigrid in general.

### How do I enable Architecture Quality for my project?

Architecture Quality is available by default. Once you've published your system, you will automatically see an "Architecture" tab appear when you view your system in Sigrid.

You can us the [scope documentation](../reference/analysis-scope-configuration.md) to customize the Architecture Quality analysis for this system, if necessary.
  
### How do I enable the change history analysis?

This will happen automatically if you use Sigrid CI, assuming the change history is available.

### What information does SIG use for the change history analysis? 

Sigrid uses your anonymized repository history to calculate metrics on which code has been changed, and when those changes were made. These statistics do not contain personal information. In fact, if you use Sigrid CI, the developer names will be anonymized client-side, so *before* anything is published to Sigrid. 
You can find more information on Sigrid data usage in our [Privacy Statement](https://www.softwareimprovementgroup.com/wp-content/uploads/SIG_Sigrid_Privacy_Statement.pdf).

### Which version control systems does SIG support for analyzing the change history?

Git, which has over 95 percent market share. Supporting other version control systems would require an unreasonable
amount of effort for the SIG infrastructure. However, clients can convert their repository to Git during their
pipeline. Examples:

  - [Subversion](https://learn.microsoft.com/en-us/azure/devops/repos/git/perform-migration-from-svn-to-git?view=azure-devops)
  - [Mercurial](https://markheath.net/post/how-to-convert-mercurial-repository-to)
  - [Microsoft TFS](https://github.com/git-tfs/git-tfs)
  
### Does Architecture Quality support self-service configuration?

Yes, and the options are explained in the [scope documentation](../reference/analysis-scope-configuration.md).

### Do we support change history analysis for multi-repo systems?

Yes. If you use [multi-repo systems](../organization-integration/systems.md), each repository's change history will be used, and the results will be combined into the overall system.

### Are Git submodules supported?

Yes. This does require you to initialize the submodules as part of your build pipeline, but this is done automatically by basically all mainstream development platforms. If you are manually cloning your repository in your pipeline, use `git clone --recurse-submodules` to clone both the "main" repository as well as its submodules.

### How does the change history analysis process merge commits versus squashing commits?

Teams working with Git will often use slightly different workflows:
[merge commits or squashing commits](https://blog.mergify.com/what-is-the-difference-between-a-merge-commit-a-squash/).
We support both as part of our analysis. When using merge commits, we only count the "original commit" and not the
merge commit itself, to avoid counting every change twice. When squashing commits, we analyze the squashed commit 
instead of the original commits, for the practical reason that we no longer have access to the original commits after
they have been squashed.

### Do we support shallow clones?

No, as the shallow clone will only download the code and will *not* download the change history.

### Can I exclude my repository from the upload to Sigrid altogether?

Yes. Sigrid CI generates a log file called `git.log`, and you can exclude this file from being uploaded. You can use the `--exclude` [option in Sigrid CI](../reference/client-script-usage.md), for example `--exclude git.log`. 

### Troubleshooting issues when manually publishing your repository history

When you use Sigrid CI, your repository history is automatically anonymized and published to Sigrid. But it's also possible to *manually* export your repository history and publish it to Sigrid, as explained [here](../organization-integration/upload-instructions.md#creating-a-zip-file-for-your-system). If you run into a situation where you believe you correctly published your repository to Sigrid, yet you're not seeing the results in Sigrid, you can use the steps below to assist you in troubleshooting the issue:

- Make sure you are pushing a `git.log` file to Sigrid. This file contains your repository history, and should be located in the same directory as the source code for that repository.
- Open the file and count the commits. Every commit uses a `@@@` prefix to make this easier to count. If you are only exporting a single commit, you might have accidentally published a [shallow clone](https://git-scm.com/docs/git-clone). A shallow clone does not include the Git history.
- Open the file and make sure it uses the UTF-8 character encoding. 
- Check the dates for each commit, which you can check in the lines with the `@@@` prefix. By default, Sigrid will only analyze commits from the last year, so any commits older than that will be ignored. You can change [the history period used by Sigrid in the configuration](../reference/analysis-scope-configuration.md#analyzing-your-repository-history), in case you want to use a longer period.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

Architecture Quality: Frequently Asked Questions
================================================

This FAQ specifically covers Sigrid's Architecture Quality functionality. Also check the [Sigrid FAQ](faq.md) for more information about Sigrid in general.

### How do I enable Architecture Quality for my project?

Architecture Quality is available by default. Once you've published your system, you will automatically see an "Architecture" tab appear when you view your system in Sigrid.

You can us the [scope documentation](../reference/analysis-scope-configuration.md) to customize the Architecture Quality analysis for this system, if necessary.
  
### How do I enable the change history analysis?

This will happen automatically, assuming that you enabled Architecture Quality in the scope file and the change history is available.

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

### When should I use the history_enabled option?

The scope configuration file has an option called `history_enabled`. You normally don't need to use this option, the
analysis will automatically detect whether the upload contains the project's change history. However, if the  upload
*does* contain the change history, but you do *not* want to use the change history in the analysis, you can add the
configuration option `history_enabled: false`.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

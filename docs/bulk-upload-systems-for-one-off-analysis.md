Bulk-uploading systems for a one-off analysis
=============================================

Both [Sigrid](https://sigrid-says.com) and Sigrid CI target *continuous* software assurance. Analyzing software quality, identifying risks, and then defining improvement actions is not something you do once and call it a day. It's something you do both frequently and structurally, embedded in your organization's software development process.

However, in some rare cases it can be necessary to perform a one-off analysis on a large software landscape. This article describes the steps on how you can use Sigrid to perform such an analysis. 

Once the initial analysis has been completed, you can decide to integrate Sigrid into your development process. The [Sigrid CI documentation](../README.md) provides steps on embedding these analyses in your development pipeline and continuous integration process.

## Prerequisites

- Bulk analysis is supported for GitHub and GitLab.
  - The "regular" Sigrid CI also supports other platforms (see [the documentation](../README.md) for details).
- Bulk analysis is performed from a Linux or Mac OS command line. On Windows, you can use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install).
- The following software needs to be available:
  - Python 3.7 
  - Git
- You have a GitHub/GitLab API token that is authorized to access the projects you want to analyze.

## Bulk-uploading GitLab projects

### Step 1: Download Sigrid CI

Clone this repository so that you can run the scripts locally:

    git clone https://github.com/Software-Improvement-Group/sigridci.git ~/sigridci
    
### Step 3: Obtain a Sigrid CI token

You will need a token to authenticate with Sigrid. Follow [these instructions](authentication-tokens.md) to create a token if you don't have one already.

Once you have a token, you need to define an environment variable called `SIGRID_CI_TOKEN` which will be used by the script.

### Step 4: Download ghorg

*ghorg* is an open source tool that bulk-downloads every project in your account. Download the latest release for your operating system from [ghorg's project page](https://github.com/gabrie30/ghorg/releases).
 
### Step 5: Create a YAML configuration file for ghorg

If not sure, you can use the following example for a reasonable default configuration:

    GHORG_PRESERVE_DIRECTORY_STRUCTURE: false
    GHORG_SCM_TYPE: gitlab
    GHORG_CLONE_PROTOCOL: https
    GHORG_CLONE_TYPE: org
    GHORG_CONCURRENCY: 25
    GHORG_NO_CLEAN: false
    GHORG_CLONE_WIKI: false
    GHORG_DRY_RUN: false
    GHORG_PRUNE: false
    GHORG_PRUNE_NO_CONFIRM: false
    GHORG_FETCH_ALL: false
    GHORG_QUIET: false
    GHORG_EXIT_CODE_ON_CLONE_INFOS: 0
    GHORG_EXIT_CODE_ON_CLONE_ISSUES: 1
    
Refer to the [ghorg documentation](https://github.com/gabrie30/ghorg) for an overview and description of all available configuration options.
    
### Step 6: Run ghorg to download all GitLab projects
    
    ghorg clone <group> --token=<gitlab-token> --base-url=<your-gitlab-url> --path=<output-dir> --config=<config.yaml>
    
The value of `<group>` should match the name of the GitLab group for which you want to download projects. If you want to upload every project in a subgroup, you need to specify the group name, for example `parentgroupname/childgroupname`.

This will download the default branch for every repository. This behavior is intentional, many organizations now contain a mixture of repositories where the default branch is `main` and repositories where the default branch is `master`. As such, it is no longer safe to rely on a specific branch name, so using the project's default branch is the safest choice.

### Step 7: Bulk-analyze all projects using Sigrid CI

You can now use the Sigrid CI client script to analyze the projects you downloaded in the previous step:

    find . -type d -iname .git -exec bash -c 'echo ~/sigridci/sigridci/sigridci.py --customer <sigrid-account-name> --system $(basename $(dirname "$1"))  --source $(dirname "$1")  --publishonly' sh {} \;
    
Note we're starting the analysis asynchronously (this is done by adding the `--publishonly` option). In other words, we're not waiting for each analysis is done before starting the next one. Your organization might have dozens or even hundreds of projects, so it's not practical to wait for every single one.

One of the parameters in the script refers to your Sigrid account name. You should have received this name when you initially received your Sigrid account from SIG. If you're not sure, you can also retrieved your Sigrid account name from the URL after you sign in to Sigrid, since every URL in Sigrid will follow the pattern `https://sigrid-says.com/your-sigrid-account-name/...`.

### Step 8: Inspect analysis results in Sigrid

You're done! The actual analysis is asynchronous. Sign in to [Sigrid](https://sigrid-says.com) and you will see the analysis results for each project as soon as they're ready.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

Using the Sigrid CI client scripts
==================================

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid to support two different kinds of development process integration:

- To *publish* your code to Sigrid after every change. Publishing makes results available at https://sigrid-says.com for users who have access to the system.
- To *provide feedback* on your changes, which can be used when reviewing pull requests. Results are visible in your development environment (e.g. GitHub, Azure DevOps, GitLab), but are not published and are hence not visible at [sigrid-says.com](https://sigrid-says.com).

<img src="../images/sigridci-architecture.png" width="750" />

The [general Sigrid CI documentation](../sigridci-integration/development-workflows.html) contains instructions on how and when to use these scripts available within various development platforms. There are multiple options for making the Sigrid CI client scripts available to the pipeline, which are explained in the instructions for each respective development platform.

## Environment requirements

- Docker
- If you are *not* using Docker
  - Python 3.7 or higher
  - Git
  - To support custom runners and on-premise installations, the Sigrid CI client script intentionally does not require any [PIP](https://pypi.org/project/pip/) dependencies.

## Command line options

The script takes a limited number of mandatory arguments. However, Sigrid CI's behavior can be configured and customized using a large number of optional arguments that can be used to align Sigrid CI's behavior to your development team's workflow. The following arguments are available:

| Argument          | Required | Example value       | Description                                                                                                                       |
|-------------------|----------|---------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| `--customer`      | Yes      | examplecustomername | Name of your organization's Sigrid account. Contact SIG support if you're not sure about this. [1]                                |
| `--system`        | Yes      | examplesystemname   | Name of your system in Sigrid. Contact SIG support if you're not sure about this. [2]                                             |
| `--subsystem `    | No       | frontend            | Used to map between repository directory structure versus the one known by Sigrid. [5]                                            |
| `--source`        | Yes      | .                   | Path of your project's source code. Use "." for current directory.                                                                |
| `--publish`       | No       | N/A                 | Automatically publishes analysis results to Sigrid. [1]                                                                           |
| `--publishonly`   | No       | N/A                 | Publishes analysis results to Sigrid, but *does not* provide feedback in the CI environment itself. [3]                           |
| `--exclude`       | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be excluded from the upload. [4, 7]                               |
| `--include`       | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be included in the upload. [6, 7]                                 |
| `--targetquality` | No       | 3.5                 | See [defining quality objectives](#defining-quality-objectives).                                                                  |
| `--showupload`    | No       | N/A                 | Logs the contents of the upload before submitting it to Sigrid.                                                                   |
| `--convert`       | No       | beinformed          | Used for some technologies. See [technology conversion configuration](technology-support.md#technology-conversion-configuration). |

Notes:

1. Customer names can only contain lowercase letters and numbers.
2. System names can only contain lowercase letters, numbers, and hyphens.
3. Typically, you would use the `--publish` option when committing to the main/master branch, and you would *not* use it for pull requests. See below for more information.  
4. These files and directories are excluded *on top of* Sigrid's default excludes. By default, Sigrid excludes things like third party libraries (e.g. `/node_modules/` for NPM libraries, build output (e.g. `/target/` for Maven builds), and generated code. 
5. The `--subsystem` option can be used to map multiple repositories to the same Sigrid system. Refer to the [documentation on mapping repositories to systems](../organization-integration/systems.md) for more information.
6. Include can be used to narrow down the upload to specific folders and/or files. In addition, exclude can be used to exclude files and folders from the included folders.
7. Folders should always be surrounded by '/' characters

## What's the difference between `--publish` and `--publishonly`?

Sigrid CI can run in different "modes", depending on your [development process and workflow](../sigridci-integration/development-workflows.md). The following table shows what happens depending on the values of these options:

|                                  | **Publish to Sigrid** | **Do not publish to Sigrid** |
|----------------------------------|-----------------------|------------------------------|
| **Feedback on new/changed code** | `--publish`           | (normal)                     |
| **No feedback**                  | `--publishonly`       | (doesn't make sense)         |

So when to use these options:

- If you want feedback on your new/changed code, *without* publishing your code to Sigrid, run the script without the publish options. This is suitable for a workflow with pull requests, as you can use it to receive feedback on your pull request.
- If you want to publish your code to Sigrid, *and* you want Sigrid CI to give your feedback on your new/changed code, use the `--publish` option. This is suitable for people who use a workflow without pull requests where everyone is making changes to the main/master branch.
- If you want to publish your code to Sigrid, but do *not* want feedback on your new/changed code, use the `--publishonly` option.
  - This is suitable for merge commits to the main/master branch. In that situation, you don't need feedback, since you *already had* your feedback in the pull request and there is no reason to receive the same feedback again when merging your changes. 
  - Moreover, this publishes your code to Sigrid in a fire-and-forget fashion, which is faster since the script will not wait for the analysis to complete and will immediately exit. This is suitable for the main/master branch scenario described above, but can also be used in other situations where the fire-and-forget behavior is preferred.

## Defining quality objectives

Sigrid CI compares the quality of the new/changed code against the configured target quality level. The target is always relative to the thousands of other systems in the SIG benchmark. This means you don't need to fix every single minor issue, as long as the overall quality is OK you're still allowed to proceed.

### Option 1: Use Sigrid's maintainability target for your system (default)

By default, Sigrid CI will use the maintainability target you've defined for your system in Sigrid. This is the same target that's depicted in the "system objectives" list you see in Sigrid. See below:

<img src="../images/sigrid-objectives.png" width="500" />

* **Default setting:** If you do not set any objective, Sigrid CI will use a default target of 3.5 stars. This is the lower threshold of the better-than-average 4-star range. Four-star code quality is the level that SIG recommends for systems with modern technologies in active development.

### Option 2: Use a maintainability target in Sigrid CI that is different from the target in Sigrid

Using the `--targetquality` parameter allows you to override the maintainability target defined in Sigrid. For example, `--targetquality 4.0` will require pull requests to be 4.0 stars even if the system-level maintainability target defined in Sigrid is 3.5 stars. You would normally use the same target in both, but in some situations, you might want to be more strict or more lenient for pull requests. 

### Additional information on configuring Sigrid CI

You can find more details on how to configure Sigrid CI [here](../sigridci-integration/github-actions.md).

To see how Sigrid CI provides feedback directly in your pull request, review [these instructions](../sigridci-integration/github-actions.md#usage).

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

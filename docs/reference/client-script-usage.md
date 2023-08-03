Using the Sigrid CI client script
=================================

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to the CI environment, in order to call the scripts *from* the CI pipeline. The [general Sigrid CI documentation](../README.md) contain instructions on how to make this script available within various CI environments. 

Once the `sigridci.py` script is available within your CI environment, you can call the script to start the Sigrid CI run. 

## Environment requirements

- Docker
- If you're *not* using Docker and instead use your own environment:
  - Python 3.7 or higher
  - Git
  - To support custom runners and on-premise installations, the Sigrid CI client script intentionally does not have any [PIP](https://pypi.org/project/pip/) dependencies.

## Command line options

The script takes a limited number of mandatory arguments. However, Sigrid CI's behavior can be configured and customized using a large number of optional arguments that can be used to align Sigrid CI's behavior to your development team's workflow. The following arguments are available:

| Argument            | Required | Example value       | Description                                                                                              |
|---------------------|----------|---------------------|----------------------------------------------------------------------------------------------------------|
| `--customer`        | Yes      | examplecustomername | Name of your organization's Sigrid account. Contact SIG support if you're not sure about this. [1]       |
| `--system`          | Yes      | examplesystemname   | Name of your system in Sigrid. Contact SIG support if you're not sure about this. [2]                    |
| `--source`          | Yes      | .                   | Path of your project's source code. Use "." for current directory.                                       |
| `--targetquality`   | No       | 3.5                 | See [defining quality targets](#defining-quality-targets). Used to decide if the CI step should fail.    |
| `--publish`         | No       | N/A                 | Automatically publishes analysis results to Sigrid. [1]                                                  |
| `--publishonly`     | No       | N/A                 | Publishes analysis results to Sigrid, but *does not* provide feedback in the CI environment itself. [3]  |
| `--exclude`         | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be excluded from the upload. [4]         |
| `--subsystem `      | No       | frontend            | Used to map between repository directory structure versus the one known by Sigrid. [5]                   |
| `--include-history` | No       | N/A                 | See [publishing your repository history](#publishing-your-repository-history).                           |
| `--showupload`      | No       | N/A                 | Logs the contents of the upload before submitting it to Sigrid.                                          |

Notes:

1. Customer names can only contain lowercase letters and numbers.
2. System names can only contain lowercase letters, numbers, and hyphens.
3. Typically, you would use the `--publish` option when committing to the main/master branch, and you would *not* use it for pull requests. See below for more information.  
4. These files and directories are excluded *on top of* Sigrid's default excludes. By default, Sigrid excludes things like third party libraries (e.g. `/node_modules/` for NPM libraries, build output (e.g. `/target/` for Maven builds), and generated code. 
5. The `--subsystem` option can be used to map multiple repositories to the same Sigrid system. Refer to the [documentation on mapping repositories to systems](../organization-integration/systems.md) for more information.

## What's the difference between `--publish` and `--publishonly`?

Sigrid CI can run in different "modes", depending on your [development process and workflow](../sigridci-integration/development-workflows.md). The following table shows what happens depending on the values of these options:

|                                  | **Publish to Sigrid** | **Do not publish to Sigrid** |
|----------------------------------|-----------------------|------------------------------|
| **Feedback on new/changed code** | `--publish`           | (normal)                     |
| **No feedback**                  | `--publishonly`       | (doesn't make sense)         |

So when to use these options:

- If you want feedback on your new/changed code, *without* publishing your code to Sigrid, run the script without the publish options. This is suitable for a workflow with pull requests, as you can use it to receive feedback on your pull request.
- If you want to publish your code to Sigrid, *and* you want Sigrid CI to give your feedback on your new/changed code, use the `--publish` option. This is suitable for people that use a workflow without pull requests where everyone is making changes to the main/master branch.
- If you want to publish your code to Sigrid, but you do *not* want feedback on your new/changed code, use the `--publishonly` option.
  - This is suitable for merge commits to the main/master branch. In that situation you don't need feedback, since you *already had* your feedback in the pull request and there is no reason to receive the same feedback again when merging your changes. 
  - Moreover, this publishes your code to Sigrid in a fire-and-forget fashion, which is faster since the script will not wait for the analysis to complete and will immediately exit. This is suitable for the main/master branch scenario described above, but can also be used in other situation where the fire-and-forget behavior is preferred.

## Defining quality targets

Sigrid CI compares the quality of the new/changed code against the configured target quality level. The target is always relative to the thousands of other systems in the SIG benchmark. This means you don't need to fix every single minor issue, as long as the overall quality is OK you're still allowed to proceed.

### Option 1: Use Sigrid's maintainability target for your system (default)

By default, Sigrid CI will use the maintainability target you've defined for your system in Sigrid. This is the same target that's depicted in the "system objectives" list you see in Sigrid. See below:

<img src="../images/sigrid-objectives.png" width="500" />

* **Default setting:** If you do not set any objective, Sigrid CI will use a default target of 3.5 stars. This is the lower threshold of the better-than-average 4-star range. Four star code quality is the level that SIG recommends for systems with modern technologies in active development.
* **Specific objective for new- and changed code**: If you have set a specific objective for new- and changed code, that objective will automatically be used for Sigrid CI (since Sigrid CI focuses on giving feedback on new/changed code specifically). Given that you may expect 4 star quality for modern system development, that could be a target for newly added code.
* **Same objective for system/new/changed code quality**: If you have set a maintainability rating objective, but not specifically one for new- and changed code, your "normal" maintainability objective will be used.

You can find more information on how to define, track, and use Sigrid objectives in the [objectives section](../capabilities/objectives.md).

### Option 2: Use a maintainability target in Sigrid CI that is different from the target in Sigrid

Using the `--targetquality` parameter allows you to override the maintainability target defined in Sigrid. For example, `--targetquality 4.0` will require pull requests to be 4.0 stars even if the system-level maintainability target defined in Sigrid is 3.5 stars. You would normally use the same target in both, but in some situations you might want to be more strict or more lenient for pull requests. 

## Option 3: Advanced per-metric targets

The advanced approach requires you to add a section to the `sigrid.yaml` [configuration file](analysis-scope-configuration.md). This approach allows you to specify a target quality level for both the overall maintainability level and every system property. You can use different targets for different metrics, so this allows you to both have an overall target, but also be more strict (or more lenient) for some of the underlying system properties. Using the configuration file provides more flexibility and more control, but it also makes the feedback more complicated. In general, it is recommended to use the overall target quality level, and only start defining specific thresholds for specific system properties when there are structural quality issues that cannot be addressed otherwise.

Adding the following section to `sigrid.yaml` will configure a target for the overall maintainability rating, but also sets more lenient targets for certain system properties:

```
sigridci:
  target:
    maintainability: 3.5
    duplication: 3.5
    unit_size: 3.5
    unit_complexity: 3.5
    unit_interfacing: 2.5
    module_coupling: 3.0
```

## Publishing your repository history

The `--include-history` option lets Sigrid CI publish your repository history to Sigrid. When enabled, this will export your Git history and publish it to Sigrid along with your source code. This information is then used in Sigrid's Architecture Quality feature to show evolution and knowledge metrics. Note that Sigrid will never report on the activities of individual developers, all data is aggregated to team level.

- [The Architecture Quality feature usage documentation](../capabilities/architecture-quality.md) for information on how to utilize this information in Sigrid.
- See the [Architecture Quality configuration](analysis-scope-configuration.md#architecture-quality) for more information on the available options.
- The [Architecture Quality FAQ](../capabilities/faq-architecture.md) covers common questions regarding this feature, including support for specific (Git) features. 
- This option is only supported for Git repositories, as [Git is now used by 97% of the market](https://survey.stackoverflow.co/2023/). If you don't use Git, you can still enable this option but it will have no effect.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

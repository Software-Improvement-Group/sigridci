Using the Sigrid CI client script
=================================

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to the CI environment, in order to call the scripts *from* the CI pipeline. The [general Sigrid CI documentation](../README.md) contain instructions on how to make this script available within various CI environments. 

Once the `sigridci.py` script is available within your CI environment, you can call the script to start the Sigrid CI run. 

## Environment requirements

- Python 3.7 or higher
- Git

Sigrid CI is used in a wide variety of environments, including custom runners and on-premise installations. For this reason, the script intentionally does not have any dependencies, since [PIP](https://pypi.org/project/pip/) is not always available in the environments where Sigrid CI is used. This is also the reason why the client script is provided as a script that runs locally: Sigrid CI is used by many organizations that are unable to run [Docker](https://www.docker.com) containers in their environment. 

## Command line options

The script takes a limited number of mandatory arguments. However, Sigrid CI's behavior can be configured and customized using a large number of optional arguments that can be used to align Sigrid CI's behavior to your development team's workflow. The following arguments are available:

| Argument            | Required | Example value       | Description                                                                                              |
|---------------------|----------|---------------------|----------------------------------------------------------------------------------------------------------|
| `--customer`        | Yes      | examplecustomername | Name of your organization's Sigrid account. Contact SIG support if you're not sure on this. [1]          |
| `--system`          | Yes      | examplesystemname   | Name of your system in Sigrid. Contact SIG support if you're not sure on this. [2]                       |
| `--source`          | Yes      | .                   | Path of your project's source code. Use "." for current directory.                                       |
| `--targetquality`   | No       | 3.5                 | Target quality level, not meeting this target will cause the CI step to fail. Default is 3.5 stars.      |
| `--publish`         | No       | N/A                 | Automatically publishes analysis results to Sigrid. [1]                                                  |
| `--publishonly`     | No       | N/A                 | Publishes analysis results to Sigrid, but *does not* provide feedback in the CI environment itself. [3]  |
| `--exclude`         | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be excluded from the upload. [4]         |
| `--pathprefix`      | No       | frontend            | Used to map between repository directory structure versus the one known by Sigrid. [5]                   |
| `--include-history` | No       | N/A                 | When enabled, includes the repository history in the upload. Required for architecture quality analysis. |
| `--showupload`      | No       | N/A                 | Logs the contents of the upload before submitting it to Sigrid.                                          |

Notes:

1. Customer names can only contain lowercase letters and numbers.
2. System names can only contain lowercase letters, numbers, and hyphens.
3. Typically, you would use the `--publish` option when committing to the main/master branch, and you would *not* use it for pull requests.  
4. These files and directories are excluded *on top of* Sigrid's default excludes. By default, Sigrid excludes things like third party libraries (e.g. `/node_modules/` for NPM libraries, build output (e.g. `/target/` for Maven builds), and generated code. 
5. The `--pathprefix` option can be used in cases where your repository used a different directory structure from the one that is known to Sigrid. For example, you might have combined your back-end and front-end repositories within a single system in Sigrid, so that in Sigrid there are two top-level folders: `backend` and `frontend` containing the contents of your two repositories. However, you still want to get specific feedback for your front-end repository in Sigrid CI. In this case you would use `--pathprefix frontend` so that Sigrid CI knows the location of your repository within the larger directory structure. Note that you cannot use this option if you're already using `--publish`.  

## Specifying a quality target

Sigrid CI compares the quality of the new/changed code against the configured target quality level. The simplest and recommended way to configure the target is by using the `--targetquality` command line argument. This will check the overall quality maintainability rating against the target. 

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

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

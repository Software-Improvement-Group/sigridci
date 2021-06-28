Using the Sigrid CI client script
=================================

This guide explains the command line interface for the Sigrid CI client script. Make sure you have also read the [general Sigrid CI documentation](README.md) before starting this guide.

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to the CI environment, in order to call the scripts *from* the CI pipeline. The [general Sigrid CI documentation](README.md) contain instructions on how to make this script available within various CI environments. 

Once the `sigridci.py` script is available within your CI environment, you can call the script to start the Sigrid CI run. The script can be configured by using a number of command line arguments:

| Argument        | Required | Example value       | Description                                                                                                                              |
|-----------------|----------|---------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| --customer      | Yes      | examplecustomername | Name of your organization's Sigrid account. Contact SIG support if you're not sure on this. Value should be lowercase.                   |
| --system        | Yes      | examplesystemname   | Name of your system in Sigrid. Contact SIG support if you're not sure on this. Value should be lowercase.                                |
| --source        | Yes      | .                   | Path of your project's source code. Use "." for current directory.                                                                       |
| --targetquality | No       | 3.5                 | Target quality level, not meeting this target will cause the CI step to fail. Default is 3.5 stars.                                      |
| --exclude       | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be excluded from the upload, on top of files already excluded by Sigrid. [1] |
| --pathprefix    | No       | frontend            | Used to map between repository directory structure versus the one known by Sigrid. [2]                                                       |

[1] By default, Sigrid already excludes a number of files and directories from being analyzed. This includes third party libraries (for example `/node_modules/` for NPM libraries, build output (for example `/target/` for Maven builds), and generated code. Using the `--exclude` option will exclude additional files and directories *on top of* the ones that were already excluded.

[2] The `--pathprefix` option can be used in cases where your repository used a different directory structure from the one that is known to Sigrid. For example, you might have combined your back-end and front-end repositories within a single system in Sigrid, so that in Sigrid there are two top-level folders: `backend` and `frontend` containing the contents of your two repositories. However, you still want to get specific feedback for your front-end repository in Sigrid CI. In this case you would use `--pathprefix frontend` so that Sigrid CI knows the location of your repository within the larger directory structure.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

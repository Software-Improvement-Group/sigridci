Integrating Sigrid CI with GitHub Actions
=========================================

This guide explains how to integrate Sigrid into your GitHub continuous integration pipeline. Make sure you have also read the [general Sigrid CI documentation](README.md) before starting this guide.

---

**Sigrid CI is currently in beta. Please [contact us](mailto:support@softwareimprovementgroup.com) if you have suggestions on how to make it more useful to you and your team.**

---

## Prerequisites

- You have credentials to submit your code to Sigrid. [Request a Sigrid CI account](mailto:support@softwareimprovementgroup.com) if this is not the case.
- You have on-boarded your system, i.e. your system is available in Sigrid. [Request your system to be added](mailto:support@softwareimprovementgroup.com) if this is not yet the case.
- [Python 3](https://www.python.org) needs to be available in the CI environment. The client scripts for Sigrid CI are based on Python.

## Configuration

**Step 1: Configure Sigrid credentials to environment variables**

Sigrid CI reads your Sigrid account credentials from two environment variables, called `SIGRID_CI_ACCOUNT` and `SIGRID_CI_TOKEN`. You can either define these environment variables in the CI user's `~/.bashrc`, though some platforms also allow you to define environment variables using a graphical interface.

You can make these environment variables available using the following steps:

- Open your project settings in GitHub
- Select "Environments" in the settings menu
- If no environment is available yet, click "New environment"
- Give the environment a name (can be anything) and select "Configure environment"
- Click "Add secret"
- Add an environment variable `SIGRID_CI_ACCOUNT` with the account name you have received

<img src="images/github-env.png" width="400" />

- Add another environment variable `SIGRID_CI_TOKEN` with the token you have received.
- Your environment secrets should now look like this:

<img src="images/github-env-secrets.png" width="400" />

**Step 2: Download the Sigrid CI client scripts and make them available to your Sigrid CI environment**

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to the CI environment, in order to call the scripts *from* the CI pipeline. You can configure your GitHub Actions to both download the Sigrid CI client scripts and then run Sigrid CI. 

In your GitHub repository, create a file `.github/workflows/sigridci.yml` and give it the following conents:

```
name: sigridci
on: [push]
jobs:
  sigridci:
    runs-on: ubuntu-latest
    steps:
      - run: "echo Sigrid CI example"
      - run: "git clone X sigridci"
      - run: "./sigridci/sigridci.py --customer opensource --system junit --source . --targetquality 3.5" 
```

**Security note:** This example downlaods the Sigrid CI client scripts directly from GitHub. That might be acceptable for some projects, and is in fact increasingly common. However, some projects might not allow this as part of their security policy. In those cases, you can simply download the `sigridci` directory in this repository, and make it available to your runners (either by placing the scripts in a known location, or packaging them into a Docker container). 

Refer to the [GitHub Actions documentation](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions) for more information on when and how these actions should be performed.

The relevant command that starts Sigrid CI is the call to the `sigridci.py` script, which will call Sigrid CI. The script takes the following arguments:

| Argument        | Required | Example value | Description                                                                                         |
|-----------------|----------|---------------|-----------------------------------------------------------------------------------------------------|
| --customer      | Yes      | mycompany     | Name of your organization's Sigrid account. Contact SIG support if you're not sure on this.         |
| --system        | Yes      | junit         | Name of your system in Sigrid. Contact SIG support if you're not sure on this.                      |
| --source        | Yes      | .             | Path of your project's source code. Use "." for current directory.                                  |
| --targetquality | No       | 3.5           | Target quality level, not meeting this target will cause the CI step to fail. Default is 3.5 stars. |
| --exclude       | No       | /build/,.png  | Comma-separated list of file and/or directory names that should be excluded from the upload.        |

Finally, note that you need to perform this step for every project where you wish to use Sigrid CI. Be aware that you can set a project-specific target quality, you don't necessarily have to use the same target for every project.

## Usage

To view all Sigrid CI results, check the "Actions" tab in your GitHub repository. Select "Sigrid CI" from the available actions in the menu on the left. This will give you a central overview of all Sigrid CI analyses:

<img src="images/github-actions.png" width="500" />

The check will succeed if the code quality meets the specified target, and will fail otherwise. In addition to this central overview, you can also find the Sigrid CI indicator next to all commits:

<img src="images/github-commits.png" width="300" />

Clicking the small indicator will show a pop-up with some more information:

<img src="images/github-details.png" width="300" />

Select "Details" to see the output from the Sigrid CI check:

Sigrid CI provides multiple levels of feedback. The first and fastest type of feedback is directly produced in the CI output, as shown in the following screenshot:

<img src="images/feedback-ci-environment.png" width="600" />

The output consists of the following:

- A list of refactoring candidates that were introduced in your merge request. This allows you to understand what quality issues you caused, which in turn allows you to fix them quickly. Note that quality is obviously important, but you are not expected to always fix every single issue. As long as you meet the target, it's fine.
- An overview of all ratings, compared against the system as a whole. This allows you to check if your changes improved the system, or accidentally made things worse.
- The final conclusion on whether your changes and merge request meet the quality target.

In addition to the textual output, Sigrid CI also generates a static HTML file that shows the results in a more graphical form. This is similar to test coverage tools, which also tend to produce a HTML report. The information in the HTML report is based on the aforementioned list, though it includes slightly more detail.

<img src="images/feedback-report.png" width="600" />

Finally, if you want to have more information on the system as a whole, you can also access [Sigrid](http://sigrid-says.com/), which gives you ore information on the overall quality of the system, its architecture, and more.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

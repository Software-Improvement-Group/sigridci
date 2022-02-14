Integrating Sigrid CI with Azure DevOps
=======================================

This guide explains how to integrate Sigrid into your Azure DevOps continuous integration pipeline. Make sure you have also read the [general Sigrid CI documentation](README.md) before starting this guide.

## Prerequisites

- You have a [Sigrid](https://sigrid-says.com) user account. 
- You have created an [authentication token for using Sigrid CI](authentication-tokens.md).
- [Python 3.7 or higher](https://www.python.org) needs to be available in the CI environment. The client script for Sigrid CI is based on Python.

## On-boarding your system to Sigrid

On-boarding is done automatically when you first run Sigrid CI. As long as you have a valid token, and that token is authorized to on-board systems, you will receive the message *system has been on-boarded to Sigrid*. Subsequent runs will then be visible in both your CI environment and [sigrid-says.com](https://sigrid-says.com). 

## Configuration

**Step 1: Create pipeline configuration file**

We will create a pipeline that consists of two jobs:

- One job that will publish the main/master branch to [sigrid-says.com](https://sigrid-says.com) after every commit.
- One job to provide feedback on pull requests, which can be used as input for code reviews.

In the root of your repository, create a file `azure-devops-pipeline.yaml` and add the following contents:

```
stages:
  - stage: Report
    jobs:
    - job: SigridCI
      pool:
        vmImage: 'ubuntu-latest' #https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/hosted?view=azure-devops&tabs=yaml#software
      continueOnError: true
      condition: "ne(variables['Build.SourceBranch'], 'refs/heads/main')"
      steps:
      - bash: "git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci"
        displayName: Clone SigridCI from Github
      - task: UsePythonVersion@0
        displayName: Get PythonTools 3.7
        inputs:
          versionSpec: '3.7'
          addToPath: false
      - bash: "./sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --targetquality 3.5"
        env:
          SIGRID_CI_ACCOUNT: $(SIGRID_CI_ACCOUNT)
          SIGRID_CI_TOKEN: $(SIGRID_CI_TOKEN)
        continueOnError: true
      - publish: sigrid-ci-output
        artifact: sigrid-ci-output
    - job: SigridPublish
      pool:
        vmImage: 'ubuntu-latest'
      continueOnError: true
      condition: "eq(variables['Build.SourceBranch'], 'refs/heads/main')"
      steps:
      - bash: "git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci"
        displayName: Clone SigridCI from Github
      - task: UsePythonVersion@0
        displayName: Get PythonTools 3.7
        inputs:
          versionSpec: '3.7'
          addToPath: false
      - bash: "./sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --publish"
        env:
          SIGRID_CI_ACCOUNT: $(SIGRID_CI_ACCOUNT)
          SIGRID_CI_TOKEN: $(SIGRID_CI_TOKEN)
        continueOnError: true
```

Note the name of the branch, which is `main` in the example but might be different for your repository. In general, most older projects will use `master` as their main branch, while more recent projects will use `main`. 

The example uses the Docker container `python:3.9-buster`, but any Docker container that contains Python 3 will do.

The relevant command that starts Sigrid CI is the call to the `sigridci.py` script, which starts the Sigrid CI analysis. The scripts supports a number of arguments that you can use to configure your Sigrid CI run. The scripts and its command line interface are explained in [using the Sigrid CI client script](client-script-usage.md).

Finally, note that you need to perform this step for every project where you wish to use Sigrid CI. Be aware that you can set a project-specific target quality, you don't necessarily have to use the same target for every project.

**Security note:** This example downloads the Sigrid CI client scripts directly from GitHub. That might be acceptable for some projects, and is in fact increasingly common. However, some projects might not allow this as part of their security policy. In those cases, you can simply download the `sigridci` directory in this repository, and make it available to your runners (either by placing the scripts in a known location, or packaging them into a Docker container). 

Commit and push this file to the repository, so that Azure DevOps can use this configuration file for your pipeline. If you already have an existing pipeline configuration, simply add these steps to it.

**Step 2: Create your Azure DevOps pipeline**

In Azure DevOps, access the section "Pipelines" from the main menu. In this example we assume you are using a YAML file to configure your pipeline:

<img src="images/azure-configurepipeline.png" width="500" />

Select the YAML file you created in the previous step:

<img src="images/azure-selectyaml.png" width="500" />

This will display the contents of the YAML file in the next screen. The final step is to add your account credentials to the pipeline. Click "Variables" in the top right corner. Create a secret named `SIGRID_CI_ACCOUNT` with the account name you have received:

<img src="images/azure-variables.png" width="500" />

When done, add another variables named `SIGRID_CI_TOKEN` with the authentication token you have received.

From this point, Sigrid CI will run as part of the pipeline. When the pipeline is triggered depends on the configuration: by default it will run after every commit, but you can also trigger it periodically or run it manually.

<img src="images/azure-build-status.png" width="700" />

# Usage

To obtain feedback on your commit, click on the "Sigrid CI" step in the pipeline results screen shown above. 

<img src="images/azure-indicator.png" width="300" />

The check will succeed if the code quality meets the specified target, and will fail otherwise. In addition to the simple success/failure indicator, Sigrid CI provides multiple levels of feedback. The first and fastest type of feedback is directly produced in the CI output, as shown in the following screenshot:

<img src="images/azure-feedback.png" width="600" />

The output consists of the following:

- A list of refactoring candidates that were introduced in your merge request. This allows you to understand what quality issues you caused, which in turn allows you to fix them quickly. Note that quality is obviously important, but you are not expected to always fix every single issue. As long as you meet the target, it's fine.
- An overview of all ratings, compared against the system as a whole. This allows you to check if your changes improved the system, or accidentally made things worse.
- The final conclusion on whether your changes and merge request meet the quality target.

In addition to the textual output, Sigrid CI also generates a static HTML file that shows the results in a more graphical form. This is similar to test coverage tools, which also tend to produce a HTML report. You can access the HTML report from the "published" section in the build summary.

<img src="images/azure-artifacts.png" width="500" />

In the list of published artifacts, expand the "sigrid-ci-output" section and download the index.html file to view the report.

<img src="images/azure-artifact-download.png" width="600" />

The information in the HTML report is similar to the command line output, though it includes slightly more detail.

<img src="images/feedback-report.png" width="600" />

Finally, if you want to have more information on the system as a whole, you can also access [Sigrid](http://sigrid-says.com/), which gives you more information on the overall quality of the system, its architecture, and more.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

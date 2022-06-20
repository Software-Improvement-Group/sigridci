Integrating Sigrid CI with GitLab
=================================

## Prerequisites

- You have a [Sigrid](https://sigrid-says.com) user account. 
- You have created an [authentication token for using Sigrid CI](authentication-tokens.md).
- [Python 3.7 or higher](https://www.python.org) needs to be available in the CI environment. The client scripts for Sigrid CI are based on Python.

## On-boarding your system to Sigrid

On-boarding is done automatically when you first run Sigrid CI. As long as you have a valid token, and that token is authorized to on-board systems, you will receive the message *system has been on-boarded to Sigrid*. Subsequent runs will then be visible in both your CI environment and [sigrid-says.com](https://sigrid-says.com). 

## Configuration

**Step 1: Configure Sigrid credentials to environment variables**

Sigrid CI reads your Sigrid account credentials from an environment variable called `SIGRID_CI_TOKEN`. To add it to your GitLab CI pipeline, follow these steps:

- Select "Settings" in your GitLab project's menu
- Select "CI/CD" in the settings menu
- Locate the section named "Variables"
- Click the "Add variable" button
- Add an environment variable `SIGRID_CI_TOKEN` and use your [Sigrid authentication token](authentication-tokens.md) as the value.

<img src="images/gitlab-env.png" width="400" />

These instructions describe how to configure a single GitLab project, but you can follow the same steps to configure the entire GitLab group, which will make the environment variables available to all projects within that group.

**Step 2: Download the Sigrid CI client scripts and make them available to your Sigrid CI environment**

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to your GitLab runners, in order to call the scripts *from* the CI pipeline. 

The scripts can be obtained by either cloning or downloading this repository, and moving the `sigridci` directory to a location that is available to the GitLab runners. 

**Step 3: Add Sigrid CI to your project's CI pipeline**

Next, you need to edit your project's CI configuration, in order to add Sigrid CI as an extra step. Open `.gitlab-ci.yml` in your project's root directory and add the following:

```
stages:  
- report

sigridci:
  stage: report
  script:
    - git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci
    - ./sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --targetquality 3.5
  allow_failure: true
  artifacts:
    paths:
      - "sigrid-ci-output/*"
    reports:
      junit: "sigrid-ci-output/sigridci-junit-format-report.xml"
    expire_in: 1 week
    when: always
  except:
    - master
    
sigridpublish:
  stage: report
  script:
    - git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci
    - ./sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --targetquality 3.5 --publish
  allow_failure: true
  artifacts:
    paths:
      - "sigrid-ci-output/*"
    expire_in: 1 week
    when: always
  only:
    - master
```

This configures two additional build steps:

- The `sigridci` step provides Sigrid feedback for pull request. This step is configured to run for every branch *except* the main/master branch.
- The `sigridpublish` step publishes project snapshots to [sigrid-says.com](https://sigrid-says.com). This step only runs for the main/master branch.

**Security note:** This example downloads the Sigrid CI client scripts directly from GitHub. That might be acceptable for some projects, and is in fact increasingly common. However, some projects might not allow this as part of their security policy. In those cases, you can simply download the `sigridci` directory in this repository, and make it available to your runners (either by placing the scripts in a known location, or packaging them into a Docker container). 

The relevant command that starts Sigrid CI is the call to the `sigridci.py` script, which starts the Sigrid CI analysis. The scripts supports a number of arguments that you can use to configure your Sigrid CI run. The scripts and its command line interface are explained in [using the Sigrid CI client script](client-script-usage.md).

Finally, note that you need to perform this step for every project where you wish to use Sigrid CI. Be aware that you can set a project-specific target quality, you don't necessarily have to use the same target for every project.

## Optional: change the analysis scope configuration

Sigrid will try to automatically detect the technologies you use, the component structure, and files/directories that should be excluded from the analysis. You can override the default configuration by creating a file called `sigrid.yaml` and adding it to the root of your repository. You can read more about the various options for custom configuration in the [configuration file documentation](analysis-scope-configuration.md).

## Usage

Once you have configured the integration, Sigrid CI will show up as a new step in your GitLab CI pipeline. The step will succeed if the code quality meets the specified target, and will fail otherwise. 

<img src="images/ci-pipeline.png" width="300" />

Sigrid CI provides multiple levels of feedback. The first and fastest type of feedback is directly produced in the CI output, as shown in the following screenshot:

<img src="images/feedback-ci-environment.png" width="600" />

The output consists of the following:

- A list of refactoring candidates that were introduced in your merge request. This allows you to understand what quality issues you caused, which in turn allows you to fix them quickly. Note that quality is obviously important, but you are not expected to always fix every single issue. As long as you meet the target, it's fine.
- An overview of all ratings, compared against the system as a whole. This allows you to check if your changes improved the system, or accidentally made things worse.
- The final conclusion on whether your changes and merge request meet the quality target.

In addition to the textual output, Sigrid CI also generates a static HTML file that shows the results in a more graphical form. This is similar to test coverage tools, which also tend to produce a HTML report. You can download this report form GitLab using the "download" button on the right side of the CI results view:

<img src="images/gitlab-download.png" width="300" />

The information in the HTML report is based on the aforementioned list, though it includes slightly more detail.

<img src="images/feedback-report.png" width="600" />

Sigrid CI output is also included in GitLab's CI/CD pipeline page, which contains a *Tests* tab. The *View details* button will show the same list of refactoring candidates that is shown in the aforementioned textual output and HTML report.

<img src="images/gitlab-ci-details.png" width="700" />

Finally, if you want to have more information on the system as a whole, you can also access [Sigrid](http://sigrid-says.com/), which gives you more information on the overall quality of the system, its architecture, and more.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

Integrating Sigrid CI into your Jenkins pipeline
================================================

This guide explains how to integrate Sigrid into your Jenkins continuous integration pipeline. Make sure you have also read the [general Sigrid CI documentation](README.md) before starting this guide. 

---

**Sigrid CI is currently in beta. Please [contact us](mailto:support@softwareimprovementgroup.com) if you have suggestions on how to make it more useful to you and your team.**

---

## Prerequisites

- You have a Sigrid user account. Sigrid CI requires Sigrid, it is currently not supported to *only* use the CI integration without using Sigrid itself.
- You have on-boarded your system, i.e. your system is available in Sigrid. [Request your system to be added](mailto:support@softwareimprovementgroup.com) if this is not yet the case.
- [Python 3](https://www.python.org) needs to be available to your Jenkins runners. The client scripts for Sigrid CI are based on Python.

## Request a Sigrid CI account

The account you use to submit code to Sigrid CI is different from your normal Sigrid user account. The account consists of an account name and a token, which you add to your CI environment's configuration in the next step. 

You can obtain a Sigrid CI account by requesting one from [support@softwareimprovementgroup.com](mailto:support@softwareimprovementgroup.com). Support for creating Sigrid CI accounts yourself will be added in a future version.

Once the account has been created, you can use Sigrid's user management feature to control which systems it is allowed to access. Similar to normal Sigrid user accounts, Sigrid CI accounts can either serve a specific system, a group of systems, or all systems in your portfolio.

## Configuration

**Step 1: Configure Sigrid credentials to environment variables**

Sigrid CI reads your Sigrid account credentials from two environment variables, called `SIGRID_CI_ACCOUNT` and `SIGRID_CI_TOKEN`. You need to make these two environment variables available Jenkins. To do this, navigate to the "Credentials" settings in your Jenkins setting page. Then select "Add credentials" with the type "secret text". You can then use this page to add `SIGRID_CI_ACCOUNT`:

<img src="images/jenkins-credentials.png" width="600" />

After saving, do the same for the `SIGRID_CI_TOKEN`. Note that you should have received both your account name and the token when your account was created, as described in the prerequisites section. After you've added both secrets they should be visible in the list:

<img src="images/jenkins-credentials-list.png" width="500" />

This example assumes a default configuration for Jenkins. Your configuration might be different, refer to the [Jenkins documentation](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#secret-text) for more information on how to make secrets available to Jenkins pipelines.

**Step 2: Add SigridCI to your Jenkins configuration**

In the root of your repository, add a file named `Jenkinsfile`. Use the following contents:

```
pipeline {
    agent {
        docker {
            image 'python:3.9-buster'
        }
    }
    
    environment {
        SIGRID_CI_ACCOUNT = credentials('SIGRID_CI_ACCOUNT')
        SIGRID_CI_TOKEN = credentials('SIGRID_CI_TOKEN')
    }

    stages {
        stage('build') {
            steps {
                sh 'git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci'
                sh './sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --targetquality 3.5'
            }
        }
    }
}
```

The previous example uses a Docker image to run the pipeline. While recommended, this is *not* a requirement for using Sigrid CI. It is also possible to use Sigrid CI with a local agent, which is shown in the following example:

```
pipeline {
    agent any

    environment {
        SIGRID_CI_ACCOUNT = credentials('SIGRID_CI_ACCOUNT')
        SIGRID_CI_TOKEN = credentials('SIGRID_CI_TOKEN')
    }

    stages {
        stage('build') {
            steps {
                sh 'git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci'
                sh './sigridci/sigridci/sigridci.py --customer examplecustomername --system examplesystemname --source . --targetquality 3.5'
            }
        }
    }
}
```

**Security note:** This example downloads the Sigrid CI client scripts directly from GitHub. That might be acceptable for some projects, and is in fact increasingly common. However, some projects might not allow this as part of their security policy. In those cases, you can simply download the `sigridci` directory in this repository, and make it available to your runners (either by placing the scripts in a known location, or packaging them into a Docker container). 

In this example we're assuming you don't have a Jenkins configuration yet, hence we create it from scratch. If you already have an existing Jenkins configuration, simply add the contents of the example to your configuration.

Sigrid CI consists of a number of Python-based client scripts, that interact with Sigrid in order to analyze your project's source code and provide feedback based on the results. These client scripts need to be available to the CI environment, in order to call the scripts *from* the CI pipeline. The script takes the following arguments:

| Argument        | Required | Example value       | Description                                                                                         |
|-----------------|----------|---------------------|-----------------------------------------------------------------------------------------------------|
| --customer      | Yes      | examplecustomername | Name of your organization's Sigrid account. Contact SIG support if you're not sure on this.         |
| --system        | Yes      | examplesystemname   | Name of your system in Sigrid. Contact SIG support if you're not sure on this.                      |
| --source        | Yes      | .                   | Path of your project's source code. Use "." for current directory.                                  |
| --targetquality | No       | 3.5                 | Target quality level, not meeting this target will cause the CI step to fail. Default is 3.5 stars. |
| --exclude       | No       | /build/,.png        | Comma-separated list of file and/or directory names that should be excluded from the upload.        |

**Step 3: Configure your Jenkins pipeline**

Create a new pipeline in Jenkins by selecting "New item" in the menu. Select the type "pipeline" from the list of options presented to you, and enter a name for your new build pipeline.

<img src="images/jenkins-new-pipeline.png" width="600" />

Next, navigate to the section "Pipeline", and select the option "Pipeline script from SCM". This will make Jenkins use the `Jenkinsfile` configuration you created earlier. This means you only need to enter the location and credentials for your repository, and Jenkins will then pick up the rest of the configuration from the `Jenkinsfile`.

<img src="images/jenkins-scm-config.png" width="600" />

Again, these instructions assume that you needed to create a new Jenkins pipeline from scratch. If you already had an existing pipeline, simply add the required steps to it.

The Sigrid CI output uses color to communicate whether the ratings meet the target: system properties that meet the target are shown in green, while ratings below the target are shown in red. Jenkins does not support colored text by default, meaning this information is lost. Using the [Jenkins ANSI color plugin](https://plugins.jenkins.io/ansicolor/) will allow Jenkins to show colored text.

## Usage

You can schedule your Jenkins pipeline to indicate *when* it should run: the typical strategy is to run it automatically after every commit, but you can also schedule it to run periodically. You can also start your pipeline manually using the "Build now" button.

<img src="images/jenkins-build-now.png" width="200" />

Once you have configured the integration, Sigrid CI will show up as a new step in your CI pipeline. The step will succeed if the code quality meets the specified target, and will fail otherwise.. Your can access the build status from the "build history" section in the menu:

<img src="images/jenkins-build-history.png" width="300" />

Clicking on the build output will provide more information. Sigrid CI provides multiple levels of feedback. The first and fastest type of feedback is directly produced in the CI output, as shown in the following screenshot:

<img src="images/jenkins-feedback.png" width="600" />

The output consists of the following:

- A list of refactoring candidates that were introduced in your merge request. This allows you to understand what quality issues you caused, which in turn allows you to fix them quickly. Note that quality is obviously important, but you are not expected to always fix every single issue. As long as you meet the target, it's fine.
- An overview of all ratings, compared against the system as a whole. This allows you to check if your changes improved the system, or accidentally made things worse.
- The final conclusion on whether your changes and merge request meet the quality target.

In addition to the textual output, Sigrid CI also generates a static HTML file that shows the results in a more graphical form. This is similar to test coverage tools, which also tend to produce a HTML report. The information in the HTML report is based on the aforementioned list, though it includes slightly more detail.

<img src="images/feedback-report.png" width="600" />

Finally, if you want to have more information on the system as a whole, you can also access [Sigrid](http://sigrid-says.com/), which gives you more information on the overall quality of the system, its architecture, and more.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

Integrating Sigrid CI with Mendix QSM on a GitLab server
========================================================

Please note: `QSM` is the brand name used by Mendix, in this manual we will use `Sigrid`.

This documentation covers cloud-based Sigrid. For on-premise Sigrid, refer to the section about [on-premise analysis configuration](../organization-integration/onpremise-analysis.md).
{: .attention }

## Prerequisites

- You are not using the default Mendix teamserver, but you are using your own Git server for version control of your projects.
- You would like to trigger the Sigrid analysis from within your own pipeline in Git.
- Your runners are able to pull this [public docker image](https://hub.docker.com/r/softwareimprovementgroup/mendixpreprocessor), the image is used to preprocess the Mendix code before uploading it to Sigrid.
- You have a [Sigrid](https://qsm.mendix.com) user account. 
- You have created an [authentication token using Sigrid](../organization-integration/authentication-tokens.md).
- You have created a Personal access (PAT) token using the [Mendix user settings](https://user-settings.mendix.com/link/developersettings)

## On-boarding your system to Sigrid

On-boarding is done automatically when you first run Sigrid CI. As long as you have a valid token, you will receive the message *system has been on-boarded to Sigrid*. Subsequent runs will then be visible in both your CI environment and [sigrid-says.com](https://sigrid-says.com). 

## Configuration

**Step 1: Configure both the Sigrid credential and the Mendix PAT to environment variables**

Sigrid CI reads your credentials from 2 environment variables called `SIGRID_CI_TOKEN` and `MENDIX_TOKEN`. 
To add these to your GitLab CI pipeline, follow these steps:

- Select "Settings" in your GitLab project's menu
- Select "CI/CD" in the settings menu
- Locate the section named "Variables"
- Click the "Add variable" button
- Add an first environment variable `SIGRID_CI_TOKEN` and use your [Sigrid authentication token](../organization-integration/authentication-tokens.md) as the value.
- Add an second environment variable `MENDIX_TOKEN` and use the [Mendix user settings](https://user-settings.mendix.com/link/developersettings) to create a PAT with 'mx:modelrepository:repo:read' access only.

<img src="../images/gitlab-env.png" width="400" />

<img src="../images/mendix-credentials.png" width="600" />

These instructions describe how to configure a single GitLab project, but you can follow the same steps to configure the entire GitLab group, which will make the environment variables available to all projects within that group.

**Step 2: Create pipeline configuration file for Gitlab**

We will create a pipeline that consists of two jobs:

- One job that will publish the main branch to [sigrid-says.com](https://sigrid-says.com) after every commit to main.
- One job to provide feedback on pull requests, which can be used as input for code reviews.


In the root of your repository, create a file `.gitlab-ci.yml` and add the following contents:

```yaml
stages:
 - report

variables:
  SIGRID_CI_CUSTOMER: '<example_customer_name>'
  SIGRID_CI_SYSTEM: '<example_system_name>'

sigridci:
  image: 
    name: softwareimprovementgroup/mendixpreprocessor:latest
    entrypoint: [""]
  stage: report
  script: 
    - /usr/local/bin/entrypoint.sh
  artifacts:
    paths:
      - "sigrid-ci-output/*"
    reports:
      junit: "sigrid-ci-output/sigridci-junit-format-report.xml"
    expire_in: 1 week
    when: always
  rules:
    - if: $CI_COMMIT_REF_NAME != $CI_DEFAULT_BRANCH

sigridpublish:
  image: 
    name: softwareimprovementgroup/mendixpreprocessor:latest
    entrypoint: [""]
  variables:
    SIGRID_CI_PUBLISH: 'publish'
  stage: report
  script:
    - /usr/local/bin/entrypoint.sh
  artifacts:
    paths:
      - "sigrid-ci-output/*"
    reports:
      junit: "sigrid-ci-output/sigridci-junit-format-report.xml"
    expire_in: 1 week
    when: always
  rules:
    - if: $CI_COMMIT_REF_NAME == $CI_DEFAULT_BRANCH
```

Note the name of the branch, which is `main` in the example but might be different for your repository. In general, most older projects will use `master` as their main branch, while more recent projects will use `main`.

The docker image allows a few optional environment variables to be set, that are equivalent to [client script options](../reference/client-script-usage.md#command-line-options) of the full Sigrid CI script.
Optional variables are:
- `SIGRID_CI_TARGET_QUALITY`: Equivalent to `--target-quality`
- `INCLUDE`: Equivalent to `--include`
- `EXCLUDE`: Equivalent to `--exclude`

Finally, note that you need to perform this step for every project where you wish to use Sigrid CI.

The output consists of the following:

- A list of refactoring candidates that were introduced in your merge request. This allows you to understand what quality issues you caused, which in turn allows you to fix them quickly. Note that quality is obviously important, but you are not expected to always fix every single issue. As long as you meet the target, it's fine.
- An overview of all ratings, compared against the system as a whole. This allows you to check if your changes improved the system, or accidentally made things worse.
- The final conclusion on whether your changes and merge request meet the quality target.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.


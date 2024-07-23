# Post security findings to Slack

This directory contains a 

At the highest level, this script carries out 3 steps and then finishes:
1. Use the [appropriate endpoint](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html#security-and-reliability-findings) in Sigrid's REST API to get the current open findings for the 
   given system.
2. Compose a message listing the latest 5 findings, ordered by decreasing severity.
3. Send this message to Slack by making an HTTP POST request to a Slack webhook.

## Usage

The idea is to use this script for instance once per day as a scheduled job. The obvious 
scheduler would be your CI/CD environment (e.g., Gitlab, Github or Azure DevOps).

Prerequisites:
- You need an [authentication token](https://docs.sigrid-says.com/organization-integration/authentication-tokens.html)
  to access Sigrid's REST API. The token should represent a user with access to the system you 
  want to get findings for.
- You need to create an [incoming webhook](https://api.slack.com/messaging/webhooks) for your 
  Slack workspace.

Both the authentication token and the webhook URL need to be treated as secrets. The script 
reads both from environment variables. We assume (and recommend!) that these environment 
variables are set by your CI/CD environment.

In addition, you need to have the example script available in your CI/CD environment. There are 
two ways to do so:
- (A) Download the script as published in this repository on the fly for each job. We'll 
  illustrate this for Gitlab below. This is the easiest way, but keep in mind that SIG may 
  change the script at any moment.
- (B) Manually download the script once and add it to your own codebase. This allows adapting 
  the script to your needs.

### Example usage: Gitlab

To use the script from Gitlab, proceed as follows. First, [create an environment variable that 
will hold the Sigrid authentication token]
(https://docs.sigrid-says.
com/sigridci-integration/gitlab.html#step-1-configure-sigrid-credentials-to-environment
-variables). If you're also using Sigrid CI, you already have this variable.

Second, create an [incoming webhook](https://api.slack.com/messaging/webhooks) for your
Slack workspace and store the webhook URL thus obtained in a second CI/CD variable named ``.``.

Finally, add a pipeline job like so:
```yaml
stages:
  - report

send_daily_findings:
  stage: report
  image: python:alpine3.20
  script:
    - wget https://raw.githubusercontent.com/Software-Improvement-Group/sigridci/main/sigridci/sigridci.py
    - python daily-findings --customer sig --system sigrid-backend
  allow_failure: true
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

## Frequently Asked Questions

Q: What is the support status of this script?

A: The script uses the Sigrid REST API, which is fully supported as a feature of Sigrid. The 
script in this directory is just an example of how the REST API can be used. The script is not 
part of Sigrid and is not supported.

Q: Can you add feature X? Where can I file feature requests?

A: We welcome feedback; the "issues" section of this repository is the most convenient channel 
for that. Keep in mind that the script is primarily meant as an illustration of how Sigrid's 
REST API can be used. 

Q: Why Python?

A: We've chosen Python for this example because the Python standard library provides everything 
we need and because we think that Python source code is easy to read, even for people with 
little to know experience with Python.


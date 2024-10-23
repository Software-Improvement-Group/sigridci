# Post security findings to Slack

This directory contains a Python script illustrating how Sigrid's REST API can be used to send a 
daily report about new security findings to Slack.

At the highest level, this script carries out 3 steps and then finishes:
1. Use the [appropriate endpoint](https://docs.sigrid-says.com/integrations/sigrid-api-documentation.html#security-and-reliability-findings) in Sigrid's REST API to get the current open findings for the 
   given system.
2. Compose a message listing the latest 5 findings, ordered by decreasing severity.
3. Send this message to Slack by making an HTTP POST request to a Slack webhook.

## Usage

The idea is to use this script for instance once per day as a scheduled job. The obvious 
scheduler would be your CI/CD environment (e.g., GitLab, GitHub or Azure DevOps).

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
  illustrate this for GitLab below. This is the easiest way, but keep in mind that SIG may 
  change the script at any moment.
- (B) Manually download the script once and add it to your own codebase. This allows adapting 
  the script to your needs.

### Example usage: GitLab

To use the script from GitLab, proceed as follows. First, [create an environment variable that 
will hold the Sigrid authentication token]
(https://docs.sigrid-says.
com/sigridci-integration/gitlab.html#step-1-configure-sigrid-credentials-to-environment
-variables). It should be named `SIGRID_CI_TOKEN`. If you're also using Sigrid CI, you already have this 
variable.

Second, create an [incoming webhook](https://api.slack.com/messaging/webhooks) for your
Slack workspace and store the webhook URL thus obtained in a second CI/CD variable named `SECURITY_FINDINGS_WEBHOOK`.

Finally, add a pipeline job like so:
```yaml
stages:
  - report

post-daily-findings:
  stage: report
  image: python:alpine3.20
  script:
    - wget https://raw.githubusercontent.com/Software-Improvement-Group/sigridci/main/examples/slack-security-findings/daily_findings.py
    - python daily_findings.py --customer sig --system sigrid-backend
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

This example pipeline job assumes you're using GitLab's Docker-based runners. The `script`, 
which runs inside the `python:alpine3.20` container, first uses `wget` to download the example 
script from GitHub. It then runs it using the Python interpreter provided by the `python:alpine3.
20` image. It assumes environment variables `` and `` have been set. 

## Frequently Asked Questions

Q: What is the support status of this script?

A: The script uses the Sigrid REST API, which is fully supported as a feature of Sigrid. The 
script in this directory is just an example of how the REST API can be used. The script is not 
part of Sigrid and is not supported.

Q: What does it take to use this for another messaging platform, e.g. Microsoft Teams?

A: At SIG, we understand that the concept would be the same: you'd need to create an [incoming 
webhook](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to
/add-incoming-webhook?tabs=newteams%2Cdotnet) and format a message in the way Teams expect. 
However, the script would need to be changed a bit because some details differ. 

Q: Can you add feature X? Where can I file feature requests?

A: We welcome feedback; the "issues" section of this repository is the most convenient channel 
for that. Keep in mind that the script is primarily meant as an illustration of how Sigrid's 
REST API can be used.

Q: In the description and examples provided here, the script is run once per day. Wouldn't it be 
better to trigger it after every Sigrid CI job?

A: This would only make sense for Sigrid CI jobs that publish their results, as the Sigrid REST 
API endpoint we use only has access to published results. Sigrid CI publish jobs are 
asynchronous: they finish after _triggering_ an analysis at SIG. Consequently, running the daily 
findings script presented in this directory immediately after will almost for sure NOT provide 
new findings. Polling SIG to find out whether there are new results fail whenever two 
overlapping Sigrid CI jobs run for the same system.

Q: The script provides a list of new findings in the last 7 days. I'd like a different period.

A: We deliberately did not make this configurable to keep the script simple. The idea is that 
you copy it and adapt it to your needs.

Q: The script reports on one system only. I would like to get a similar daily report for my 
entire portfolio.

A: That's not currently possible, as the Sigrid REST API has no endpoint that provides security 
findings for an entire portfolio. We also think it is best if development teams take responsibility 
for handling security findings (as opposed to a centralized office); no team would be 
responsible for all systems in a portfolio, hence we don't think there's a proper use case for 
portfolio-wide daily findings reports.

Q: Why Python?

A: We've chosen Python for this example because the Python standard library provides everything 
we need and because we think that Python source code is easy to read, even for people with 
little to no experience with Python. We also deliberately kept the entire script in one file and 
we're not using anything else than the standard library, so it is easy to run the script (no 
need to install dependencies or create virtual environments).

## License

Copyright Software Improvement Group

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
    
    


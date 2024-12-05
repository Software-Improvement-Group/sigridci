#!/usr/bin/env python3

# Copyright Software Improvement Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from sigridci.command_line_helper import getFeedbackPublishOptions, parseFeedbackCommandLineArguments, checkEnvironment
from sigridci.reports.azure_pull_request_report import AzurePullRequestReport
from sigridci.reports.gitlab_pull_request_report import GitLabPullRequestReport
from sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci_runner import SigridCiRunner


if __name__ == "__main__":
    checkEnvironment()
    args = parseFeedbackCommandLineArguments("Open Source Health")
    options = getFeedbackPublishOptions(args)

    apiClient = SigridApiClient(options)
    objective = apiClient.fetchObjectives().get("OSH_MAX_SEVERITY", "CRITICAL")

    with open(args.analysisresults, mode="r", encoding="utf-8") as f:
        analysisId = "local"
        feedback = json.load(f)

    markdownReport = OpenSourceHealthMarkdownReport()
    additionalReports = [GitLabPullRequestReport(markdownReport), AzurePullRequestReport(markdownReport)]

    runner = SigridCiRunner(options, apiClient)
    runner.provideFeedbackOnly(analysisId, feedback, markdownReport, additionalReports)

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
import os

from .capability import MAINTAINABILITY, Capability
from .objective import Objective
from .publish_options import PublishOptions
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.bitbucket_pull_request_report import BitBucketPullRequestReport
from .reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from .reports.combined_text_report import CombinedTextReport
from .reports.github_pull_request_report import GitHubPullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.inline_results_report import InlineResultsReport
from .reports.junit_format_report import JUnitFormatReport
from .reports.report import Report
from .reports.static_html_report import StaticHtmlReport


class FeedbackProvider:
    def __init__(self, analysisId: str, options: PublishOptions, objectives: dict):
        self.analysisId = analysisId
        self.options = options
        self.objectives = self.prepareObjectives(objectives)
        self.capabilityFeedback: dict[Capability, dict] = {}
        self.previousCapabilityFeedback: dict[Capability, dict] = {}

    def prepareObjectives(self, original: dict) -> dict:
        objectives = original.copy()

        hasMaintainabilityObjective = any(metric for metric in objectives if metric.startswith("MAINTAINABILITY"))
        if not hasMaintainabilityObjective:
            objectives["MAINTAINABILITY"] = Objective.DEFAULT_RATING_OBJECTIVE

        for defaultObjective in ["OSH_MAX_SEVERITY", "SECURITY_MAX_SEVERITY"]:
            if not objectives.get(defaultObjective):
                objectives[defaultObjective] = Objective.DEFAULT_FINDING_OBJECTIVE

        if not objectives.get("ARCHITECTURE_QUALITY"):
            objectives["ARCHITECTURE_QUALITY"] = Objective.DEFAULT_RATING_OBJECTIVE

        return objectives

    def registerFeedback(self, capability: Capability, feedback: dict) -> None:
        self.capabilityFeedback[capability] = feedback

    def registerPreviousFeedback(self, capability: Capability, feedback: dict) -> None:
        self.previousCapabilityFeedback[capability] = feedback

    def generateReports(self) -> int:
        if not os.path.exists(self.options.outputDir):
            os.mkdir(self.options.outputDir)

        if not self.options.inlineResults:
            for capability in self.capabilityFeedback:
                with open(f"{self.options.outputDir}/{capability.shortName}.json", mode="w", encoding="utf-8") as f:
                    json.dump(self.capabilityFeedback[capability], f, sort_keys=False, indent=4)

            # We have some legacy reports that are maintainability-only,
            # which we keep for backward compatibility.
            if MAINTAINABILITY in self.options.capabilities:
                for maintainabilityReport in [JUnitFormatReport(), StaticHtmlReport(self.objectives)]:
                    maintainabilityReport.generate(self.analysisId, self.capabilityFeedback[MAINTAINABILITY], self.options)

        masterReport = CombinedMarkdownFeedbackReport(self.objectives)

        for report in self.getCrossCapabilityReports(masterReport):
            report.previousFeedback = self.previousCapabilityFeedback
            report.generate(self.analysisId, self.capabilityFeedback, self.options)

        return masterReport.getExitCode(self.capabilityFeedback, self.options)

    def getCrossCapabilityReports(self, masterReport: CombinedMarkdownFeedbackReport) -> list[Report]:
        if self.options.inlineResults:
            return [InlineResultsReport(self.objectives)]

        return [
            masterReport,
            GitHubPullRequestReport(masterReport),
            GitLabPullRequestReport(masterReport),
            AzurePullRequestReport(masterReport),
            BitBucketPullRequestReport(masterReport),
            # The plain text output always goes last, so that the last thing
            # you see in the command line output is the summary.
            CombinedTextReport(masterReport)
        ]

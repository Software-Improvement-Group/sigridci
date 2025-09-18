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

from .publish_options import Capability
from .reports.ascii_art_report import AsciiArtReport
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.junit_format_report import JUnitFormatReport
from .reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from .reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from .reports.pipeline_summary_report import PipelineSummaryReport
from .reports.security_markdown_report import SecurityMarkdownReport


class FeedbackProvider:
    def __init__(self, capability, options, objectives):
        self.capability = capability
        self.objectives = objectives
        self.options = options
        self.analysisId = "local"
        self.feedback = None
        self.previousFeedback = None

    def loadLocalAnalysisResults(self, analysisResultsFile):
        with open(analysisResultsFile, mode="r", encoding="utf-8") as f:
            self.analysisId = "local"
            self.feedback = json.load(f)

    def loadPreviousAnalysisResults(self, analysisResultsFile):
        with open(analysisResultsFile, mode="r", encoding="utf-8") as f:
            self.previousFeedback = json.load(f)

    def generateReports(self):
        if self.feedback is None:
            raise Exception("No feedback provided")

        if not os.path.exists(self.options.outputDir):
            os.mkdir(self.options.outputDir)

        markdownReport = self.prepareMarkdownReport()
        reports = self.prepareAdditionalReports(markdownReport)

        for report in reports:
            report.previousFeedback = self.previousFeedback
            report.generate(self.analysisId, self.feedback, self.options)

        print(f"Sigrid CI feedback is available from {markdownReport.getMarkdownFile(self.options)}")
        print(f"View this system in Sigrid: {markdownReport.getSigridUrl(self.options)}")
        return markdownReport.isObjectiveSuccess(self.feedback, self.options)

    def prepareMarkdownReport(self):
        if self.capability == Capability.MAINTAINABILITY:
            objective = self.objectives.get("MAINTAINABILITY", 3.5)
            return MaintainabilityMarkdownReport(objective)
        elif self.capability == Capability.OPEN_SOURCE_HEALTH:
            objective = self.objectives.get("OSH_MAX_SEVERITY", "CRITICAL")
            return OpenSourceHealthMarkdownReport(objective)
        elif self.capability == Capability.SECURITY:
            objective = self.objectives.get("SECURITY_MAX_SEVERITY", "CRITICAL")
            return SecurityMarkdownReport(objective)
        else:
            raise Exception(f"Unknown capability: {self.capability}")

    def prepareAdditionalReports(self, markdownReport):
        reports = [markdownReport, GitLabPullRequestReport(markdownReport), AzurePullRequestReport(markdownReport)]
        if self.capability == Capability.MAINTAINABILITY:
            reports += [AsciiArtReport(), JUnitFormatReport()]
        reports.append(PipelineSummaryReport(markdownReport))
        return reports

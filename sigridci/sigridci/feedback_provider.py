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

import os

from .capability import ARCHITECTURE, MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY, Capability
from .objective import Objective
from .publish_options import PublishOptions
from .reports.ascii_art_report import AsciiArtReport
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.bitbucket_pull_request_report import BitBucketPullRequestReport
from .reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from .reports.combined_text_report import CombinedTextReport
from .reports.github_pull_request_report import GitHubPullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.inline_results_report import ArchitectureInlineResultsReport, MaintainabilityInlineResultsReport, \
    OpenSourceHealthInlineResultsReport, SecurityInlineResultsReport
from .reports.junit_format_report import JUnitFormatReport
from .reports.report import Report
from .reports.static_html_report import StaticHtmlReport


class FeedbackProvider:
    def __init__(self, analysisId: str, options: PublishOptions, objectives: dict):
        self.analysisId = analysisId
        self.options = options
        self.objectives = self.prepareObjectives(objectives)
        self.analysisId = "local"
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

        for capability, reports in self.getCapabilityReports().items():
            for report in reports:
                report.previousFeedback = self.previousCapabilityFeedback.get(capability)
                report.generate(self.analysisId, self.capabilityFeedback[capability], self.options)

        masterReport = CombinedMarkdownFeedbackReport(self.objectives)

        for report in self.getCrossCapabilityReports(masterReport):
            report.previousFeedback = self.previousCapabilityFeedback
            report.generate(self.analysisId, self.capabilityFeedback, self.options)

        return masterReport.getExitCode(self.capabilityFeedback, self.options)

    def getCrossCapabilityReports(self, masterReport: CombinedMarkdownFeedbackReport) -> list[Report]:
        if self.options.inlineResults:
            return []

        return [
            masterReport,
            GitHubPullRequestReport(masterReport),
            GitLabPullRequestReport(masterReport),
            AzurePullRequestReport(masterReport),
            BitBucketPullRequestReport(masterReport),
            # Always goes last, so that the last thing you see
            # in the command line output is the summary.
            CombinedTextReport(masterReport)
        ]

    def getCapabilityReports(self) -> dict[Capability, list[Report]]:
        if self.options.inlineResults:
            return {cap : [self.prepareInlineResultsReport(cap)] for cap in self.options.capabilities}
        elif MAINTAINABILITY in self.options.capabilities:
            reports = [AsciiArtReport(), JUnitFormatReport(), StaticHtmlReport(self.objectives)]
            return {MAINTAINABILITY : reports}
        else:
            return {}

    def prepareInlineResultsReport(self, capability) -> Report:
        if capability == MAINTAINABILITY:
            return MaintainabilityInlineResultsReport(self.objectives)
        elif capability == OPEN_SOURCE_HEALTH:
            vulnerabilityObjective = self.objectives["OSH_MAX_SEVERITY"]
            licenseObjective = self.objectives["OSH_MAX_LICENSE_RISK"]
            return OpenSourceHealthInlineResultsReport(self.options, vulnerabilityObjective, licenseObjective)
        elif capability == SECURITY:
            return SecurityInlineResultsReport(self.options, self.objectives["SECURITY_MAX_SEVERITY"])
        elif capability == ARCHITECTURE:
            return ArchitectureInlineResultsReport()
        else:
            raise Exception(f"Unknown capability: {capability}")

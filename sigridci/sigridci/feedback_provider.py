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
import uuid

from .capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY
from .objective import Objective
from .reports.ascii_art_report import AsciiArtReport
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.junit_format_report import JUnitFormatReport
from .reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from .reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from .reports.osh_text_report import OpenSourceHealthTextReport
from .reports.pipeline_summary_report import PipelineSummaryReport
from .reports.security_markdown_report import SecurityMarkdownReport
from .reports.static_html_report import StaticHtmlReport


class FeedbackProvider:
    def __init__(self, capability, options, objectives):
        self.capability = capability
        self.options = options
        self.objectives = self.prepareObjectives(objectives)
        self.analysisId = "local"
        self.feedback = None
        self.previousFeedback = None

    def prepareObjectives(self, objectives):
        if self.capability == MAINTAINABILITY:
            return self.prepareMaintainabilityObjectives(objectives)
        elif self.capability == OPEN_SOURCE_HEALTH:
            return self.prepareOpenSourceHealthObjectives(objectives)
        elif self.capability == SECURITY:
            return {
                "SECURITY_MAX_SEVERITY" : objectives.get("SECURITY_MAX_SEVERITY", Objective.DEFAULT_FINDING_OBJECTIVE)
            }
        else:
            raise Exception(f"Unknown capability: {self.capability}")

    def prepareMaintainabilityObjectives(self, objectives):
        maintainabilityObjectives = {}

        for metric in Objective.MAINTAINABILITY_METRICS:
            if metric in objectives:
                maintainabilityObjectives[metric] = objectives[metric]
            elif f"MAINTAINABILITY_{metric}" in objectives:
                maintainabilityObjectives[metric] = objectives[f"MAINTAINABILITY_{metric}"]

        if len(maintainabilityObjectives) == 0:
            maintainabilityObjectives["MAINTAINABILITY"] = Objective.DEFAULT_RATING_OBJECTIVE

        return maintainabilityObjectives

    def prepareOpenSourceHealthObjectives(self, objectives):
        return {
            "OSH_MAX_SEVERITY" : objectives.get("OSH_MAX_SEVERITY", Objective.DEFAULT_FINDING_OBJECTIVE),
            "OSH_MAX_LICENSE_RISK" : objectives.get("OSH_MAX_LICENSE_RISK", None)
        }

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

        rawFeedbackFile = f"{self.options.outputDir}/{self.capability.shortName}-{uuid.uuid4()}.json"
        with open(rawFeedbackFile, mode="w", encoding="utf-8") as f:
            json.dump(self.feedback, f, sort_keys=False, indent=4)

        markdownReport = self.prepareMarkdownReport()
        reports = self.prepareAdditionalReports(markdownReport)

        for report in reports:
            report.previousFeedback = self.previousFeedback
            report.generate(self.analysisId, self.feedback, self.options)

        return markdownReport.isObjectiveSuccess(self.feedback, self.options)

    def prepareMarkdownReport(self):
        if self.capability == MAINTAINABILITY:
            return MaintainabilityMarkdownReport(self.objectives)
        elif self.capability == OPEN_SOURCE_HEALTH:
            vulnerabilityObjective = self.objectives["OSH_MAX_SEVERITY"]
            licenseObjective = self.objectives["OSH_MAX_LICENSE_RISK"]
            return OpenSourceHealthMarkdownReport(self.options, vulnerabilityObjective, licenseObjective)
        elif self.capability == SECURITY:
            return SecurityMarkdownReport(self.objectives["SECURITY_MAX_SEVERITY"])
        else:
            raise Exception(f"Unknown capability: {self.capability}")

    def prepareAdditionalReports(self, markdownReport):
        reports = [markdownReport, GitLabPullRequestReport(markdownReport), AzurePullRequestReport(markdownReport)]
        if self.capability == MAINTAINABILITY:
            reports += [AsciiArtReport(), JUnitFormatReport(), StaticHtmlReport(self.objectives)]
        elif self.capability == OPEN_SOURCE_HEALTH:
            reports += [OpenSourceHealthTextReport(markdownReport)]
        reports.append(PipelineSummaryReport(markdownReport))
        return reports

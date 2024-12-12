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
from enum import Enum

from .publish_options import PublishOptions
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from .reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from .reports.security_markdown_report import SecurityMarkdownReport


class Capability(Enum):
    MAINTAINABILITY = "maintainability"
    OPEN_SOURCE_HEALTH = "osh"
    SECURITY = "security"


class FeedbackProvider:
    def __init__(self, capability, options, objectives):
        self.options = options
        self.markdownReport = self.prepareMarkdownReport(capability, objectives)
        self.additionalReports = [
            GitLabPullRequestReport(self.markdownReport),
            AzurePullRequestReport(self.markdownReport)
        ]

    def prepareMarkdownReport(self, capability, objectives):
        if capability == Capability.MAINTAINABILITY:
            self.options.targetRating = objectives.get("MAINTAINABILITY", PublishOptions.DEFAULT_TARGET)
            return MaintainabilityMarkdownReport()
        elif capability == Capability.OPEN_SOURCE_HEALTH:
            objective = objectives.get("OSH_MAX_SEVERITY", PublishOptions.DEFAULT_FINDINGS_OBJECTIVE)
            return OpenSourceHealthMarkdownReport(objective)
        elif capability == Capability.SECURITY:
            objective = objectives.get("SECURITY_MAX_SEVERITY", PublishOptions.DEFAULT_FINDINGS_OBJECTIVE)
            return SecurityMarkdownReport(objective)
        else:
            raise Exception(f"Unknown capability: {capability}")

    def loadLocalAnalysisResults(self, analysisResultsFile):
        with open(analysisResultsFile, mode="r", encoding="utf-8") as f:
            self.analysisId = "local"
            self.feedback = json.load(f)

    def generateReports(self):
        if self.feedback is None:
            raise Exception("No feedback provided")

        if not os.path.exists(self.options.outputDir):
            os.mkdir(self.options.outputDir)

        for report in [self.markdownReport] + self.additionalReports:
            report.generate(self.analysisId, self.feedback, self.options)

        print(f"Sigrid CI feedback is available from {self.markdownReport.getMarkdownFile(self.options)}")
        print(f"View this system in Sigrid: {self.markdownReport.getSigridUrl(self.options)}")

        return self.markdownReport.isObjectiveSuccess(self.feedback, self.options)

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

from .report import Report, MarkdownRenderer
from .security_markdown_report import SecurityMarkdownReport
from ..objective import Objective


class OpenSourceHealthMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = SecurityMarkdownReport.MAX_FINDINGS

    def __init__(self, objective = "CRITICAL"):
        super().__init__()
        self.objective = objective

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        includedVulnerabilities = list(self.getIncludedVulnerabilities(feedback))
        includedVulnerabilities.sort(key=lambda entry: entry[1]["severity"])

        details = self.generateFindingsTable(includedVulnerabilities)
        sigridLink = f"{self.getSigridUrl(options)}/-/open-source-health"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        objectiveDisplayName = f"{self.objective.lower()} open source vulnerabilities"
        if self.isObjectiveSuccess(feedback, options):
            return f"✅  You achieved your objective of having no {objectiveDisplayName}"
        else:
            return f"⚠️  You did not meet your objective of having no {objectiveDisplayName}"

    def generateFindingsTable(self, includedVulnerabilities):
        if len(includedVulnerabilities) == 0:
            return ""

        md = "| Risk | Dependency | Description |\n"
        md += "|------|------------|-------------|\n"

        for dependency, vulnerability in includedVulnerabilities[0:self.MAX_FINDINGS]:
            symbol = SecurityMarkdownReport.SEVERITY_SYMBOLS[vulnerability["severity"]]
            name = f"{dependency['name']}@{dependency['currentVersion']}"
            description = vulnerability["description"]
            md += f"| {symbol} | {name} | {description} |\n"

        if len(includedVulnerabilities) > self.MAX_FINDINGS:
            md += f"| | ... and {len(includedVulnerabilities) - self.MAX_FINDINGS} more vulnerabilities | |\n"

        return md

    def getIncludedVulnerabilities(self, feedback):
        for dependency in feedback["dependencies"]:
            for vulnerability in dependency["vulnerabilities"]:
                if Objective.isFindingIncluded(vulnerability["severity"], self.objective):
                    yield (dependency, vulnerability)

    def getCapability(self):
        return "Open Source Health"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/osh-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        includedVulnerabilities = list(self.getIncludedVulnerabilities(feedback))
        return len(includedVulnerabilities) == 0

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
from ..objective import Objective


class SecurityMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = 8
    SEVERITY_SYMBOLS = {
        "CRITICAL" : "🟣",
        "HIGH" : "🔴",
        "MEDIUM" : "🟠",
        "LOW" : "🟡",
        "UNKNOWN" : "⚪️"
    }

    def __init__(self, objective = "CRITICAL"):
        super().__init__()
        self.objective = objective

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        findings = list(self.getRelevantFindings(feedback))
        details = self.generateFindingsTable(findings, options)
        sigridLink = f"{self.getSigridUrl(options)}/-/security"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        if self.isObjectiveSuccess(feedback, options):
            return f"✅  You achieved your objective of having no {self.objective.lower()} security findings"
        else:
            return f"⚠️  You did not meet your objective of having no {self.objective.lower()} security findings"

    def generateFindingsTable(self, findings, options):
        if len(findings) == 0:
            return ""

        md = "| Risk | File | Finding |\n"
        md += "|------|------|---------|\n"

        for finding in findings[0:self.MAX_FINDINGS]:
            symbol = self.SEVERITY_SYMBOLS[self.getFindingSeverity(finding)]
            file = finding["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
            line = finding["locations"][0]["physicalLocation"]["region"]["startLine"]
            link = self.decorateLink(options, f"{file}:{line}", file, line)
            description = finding["message"]["text"]
            md += f"| {symbol} | {link} | {description} |\n"

        if len(findings) > self.MAX_FINDINGS:
            md += f"| | ... and {len(findings) - self.MAX_FINDINGS} more findings | |\n"

        return md

    def getRelevantFindings(self, feedback):
        for run in feedback["runs"]:
            for result in run["results"]:
                tags = result.get("properties", {}).get("tags", [])
                severity = self.getFindingSeverity(result)
                if len(tags) > 0:
                    if Objective.isFindingIncluded(severity, self.objective):
                        yield result

    def getFindingSeverity(self, result):
        return result.get("properties", {}).get("severity", "UNKNOWN")

    def getCapability(self):
        return "Security"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/security-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        findings = list(self.getRelevantFindings(feedback))
        return len(findings) == 0

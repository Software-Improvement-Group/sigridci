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
        self.previousFeedback = None

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        rules = list(self.getRules(feedback))
        introduced = list(self.getIntroducedFindings(feedback, rules))
        fixed = list(self.getFixedFindings(feedback))

        details = ""
        details += "## 👍 What went well?\n\n"
        details += f"> You fixed **{len(fixed)}** security findings.\n\n"
        details += self.generateFindingsTable(fixed, rules, options)
        details += "## 👎 What could be better?\n\n"
        if len(introduced) > 0:
            details += f"> Unfortunately, you introduced **{len(introduced)}** security findings.\n\n"
            details += self.generateFindingsTable(introduced, rules, options)
        else:
            details += "> You did not introduce any security findings during your changes, great job!\n\n"

        sigridLink = f"{self.getSigridUrl(options)}/-/security"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        if self.isObjectiveSuccess(feedback, options):
            return f"✅  You achieved your objective of having no {self.objective.lower()} security findings"
        else:
            return f"⚠️  You did not meet your objective of having no {self.objective.lower()} security findings"

    def generateFindingsTable(self, findings, rules, options):
        if len(findings) == 0:
            return ""

        md = "| Risk | File | Finding |\n"
        md += "|------|------|---------|\n"

        for finding in findings[0:self.MAX_FINDINGS]:
            symbol = self.SEVERITY_SYMBOLS[self.getFindingSeverity(finding, rules)]
            file = finding["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
            line = finding["locations"][0]["physicalLocation"]["region"]["startLine"]
            link = self.decorateLink(options, f"{file}:{line}", file, line)
            description = finding["message"]["text"]
            md += f"| {symbol} | {link} | {description} |\n"

        if len(findings) > self.MAX_FINDINGS:
            md += f"| | ... and {len(findings) - self.MAX_FINDINGS} more findings | |\n"

        return f"{md}\n"

    def getRules(self, feedback):
        for run in feedback["runs"]:
            for rule in run.get("rules", []):
                properties = rule.get("properties", {})
                if properties.get("severity"):
                    yield rule

    def getIntroducedFindings(self, feedback, rules):
        previousFingerprints = self.getFingerprints(self.previousFeedback) if self.previousFeedback else []

        for run in feedback["runs"]:
            for result in run.get("results", []):
                severity = self.getFindingSeverity(result, rules)
                fingerprint = result["fingerprints"]["sigFingerprint/v1"]
                if Objective.isFindingIncluded(severity, self.objective) and fingerprint not in previousFingerprints:
                    yield result

    def getFixedFindings(self, feedback):
        if not self.previousFeedback:
            return []

        fingerprints = list(self.getFingerprints(feedback))
        previousRules = list(self.getRules(self.previousFeedback))

        for run in self.previousFeedback["runs"]:
            for result in run.get("results", []):
                severity = self.getFindingSeverity(result, previousRules)
                fingerprint = result["fingerprints"]["sigFingerprint/v1"]
                if Objective.isFindingIncluded(severity, self.objective) and fingerprint not in fingerprints:
                    yield result

    def getFindingSeverity(self, result, rules):
        for rule in rules:
            if rule["id"] == result["ruleId"]:
                return rule["properties"]["severity"].upper()
        return "UNKNOWN"

    def getFingerprints(self, feedback):
        for run in feedback["runs"]:
            for result in run.get("results", []):
                yield result["fingerprints"]["sigFingerprint/v1"]

    def getCapability(self):
        return "Security"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/security-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        rules = list(self.getRules(feedback))
        findings = list(self.getIntroducedFindings(feedback, rules))
        return len(findings) == 0

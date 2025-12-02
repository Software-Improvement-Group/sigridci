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
from ..analysisresults.findings_processor import FindingsProcessor
from ..capability import SECURITY
from ..objective import Objective
from ..platform import SECURITY_EXCLUDE_RULE_DOCS, SECURITY_EXCLUDE_FILE_DOCS


class SecurityMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = 8
    SEVERITY_SYMBOLS = {
        "CRITICAL" : "🟣",
        "HIGH" : "🔴",
        "MEDIUM" : "🟠",
        "LOW" : "🟡",
        "NONE" : "🟢",
        "UNKNOWN" : "⚪️"
    }

    def __init__(self, objective = "HIGH"):
        super().__init__()
        self.objective = objective
        self.previousFeedback = None
        self.processor = FindingsProcessor()

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        findings = self.processor.extractRelevantFindings(feedback, self.objective)
        previousFindings = self.processor.extractRelevantFindings(self.previousFeedback, self.objective)

        introduced = list(self.getIntroducedFindings(findings, previousFindings))
        fixed = list(self.getFixedFindings(findings, previousFindings))

        details = ""
        details += "## 👍 What went well?\n\n"
        details += f"> You fixed **{len(fixed)}** security findings.\n\n"
        details += self.generateFindingsTable(fixed, options)
        details += "## 👎 What could be better?\n\n"
        if len(introduced) > 0:
            details += f"> Unfortunately, you introduced **{len(introduced)}** security findings.\n\n"
            details += self.generateFindingsTable(introduced, options)
            details += "If you believe these findings are false positives,\n"
            details += f"you can [exclude the rule]({SECURITY_EXCLUDE_RULE_DOCS}) in the Sigrid configuration.\n"
            details += "If you believe these findings are located in files that should not be scanned, you can also\n"
            details += f"[exclude the files and/or directories]({SECURITY_EXCLUDE_FILE_DOCS}) in the configuration.\n\n"
        else:
            details += "> You did not introduce any security findings during your changes, great job!\n\n"

        sigridLink = f"{self.getSigridUrl(options)}/-/security"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        objectiveLabel = Objective.getSeverityObjectiveLabel(self.objective)
        if self.isObjectiveSuccess(feedback, options):
            return f"✅  You achieved your objective of having {objectiveLabel} security findings"
        else:
            return f"⚠️  You did not meet your objective of having {objectiveLabel} security findings"

    def generateFindingsTable(self, findings, options):
        if len(findings) == 0:
            return ""

        md = "| Risk | File | Finding |\n"
        md += "|------|------|---------|\n"

        for finding in findings[0:self.MAX_FINDINGS]:
            symbol = self.SEVERITY_SYMBOLS[finding.risk]
            link = self.decorateLink(options, f"{finding.file}:{finding.line}", finding.file, finding.line)
            md += f"| {symbol} | {link} | {finding.description} |\n"

        if len(findings) > self.MAX_FINDINGS:
            md += f"| | ... and {len(findings) - self.MAX_FINDINGS} more findings | |\n"

        return f"{md}\n"

    def getIntroducedFindings(self, findings, previousFindings):
        previousFingerprints = [finding.fingerprint for finding in previousFindings]
        return [finding for finding in findings if finding.fingerprint not in previousFingerprints]

    def getFixedFindings(self, findings, previousFindings):
        fingerprints = [finding.fingerprint for finding in findings]
        return [finding for finding in previousFindings if finding.fingerprint not in fingerprints]

    def getCapability(self):
        return SECURITY

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/security-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        findings = self.processor.extractRelevantFindings(feedback, self.objective)
        return len(findings) == 0

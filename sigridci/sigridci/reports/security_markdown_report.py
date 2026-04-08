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
from ..analysisresults.sarif_processor import SarifProcessor, FindingStatus
from ..capability import SECURITY
from ..objective import Objective
from ..platform import SECURITY_EXCLUDE_RULE_DOCS, SECURITY_EXCLUDE_FILE_DOCS, SECURITY_BETA_DOCS


class SecurityMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = 8
    SEVERITY_SYMBOLS = {
        "CRITICAL" : "🟣",
        "HIGH" : "🔴",
        "MEDIUM" : "🟠",
        "LOW" : "🟡",
        "NONE" : "🟢",
        "INFORMATION" : "🔵",
        "UNKNOWN" : "⚪️"
    }

    def __init__(self, options, objective = "HIGH"):
        super().__init__()
        self.objective = objective
        self.processor = SarifProcessor(options, objective)
        self.previousFeedback = None

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        findings = self.extractFindings(feedback)
        introduced = self.processor.filterStatus(findings, FindingStatus.INTRODUCED, partOfObjective=False)
        fixed = self.processor.filterStatus(findings, FindingStatus.FIXED, partOfObjective=False)
        remaining = self.processor.filterStatus(findings, FindingStatus.REMAINING, partOfObjective=False)
        accepted = self.processor.filterStatus(findings, FindingStatus.ACCEPTED, partOfObjective=False)
        sigridLink = f"{self.getSigridUrl(options)}/-/security"

        details = f"> Sigrid CI for Security is currently in Beta. [The documentation]({SECURITY_BETA_DOCS}) "
        details += "contains more information on its current state and known limitations.\n\n"
        if feedback.get("baseline"):
            details += f"Sigrid compared your code against the baseline of {feedback['baseline']} UTC.\n\n"
        if len(introduced) + len(fixed) > 0:
            details += "- ❌ means this finding fails your objective.\n"
            details += "- ⚠️ means a finding exists, but is not severe enough to fail your objective.\n"
            details += "- ✅ means everything is fine.\n\n"
        details += "## 👍 What went well?\n\n"
        if len(introduced) == 0:
            details += "> You did not introduce any security findings during your changes, great job!\n\n"
        if len(fixed) > 0 or len(introduced) > 0:
            details += f"> You fixed **{len(fixed)}** security findings.\n\n"
            details += self.generateFindingsTable(fixed, options)
        if len(introduced) > 0:
            details += "## 👎 What could be better?\n\n"
            details += f"> Unfortunately, you introduced **{len(introduced)}** security findings.\n\n"
            details += self.generateFindingsTable(introduced, options)
            details += "If you believe these findings are false positives,\n"
            details += f"you can [exclude the rule]({SECURITY_EXCLUDE_RULE_DOCS}) in the Sigrid configuration.\n"
            details += "If you believe these findings are located in files that should not be scanned, you can also\n"
            details += f"[exclude the files and/or directories]({SECURITY_EXCLUDE_FILE_DOCS}) in the configuration.\n\n"
        if len(remaining) + len(accepted) > 0:
            details += "## 😑 You have remaining security findings\n\n"
            details += f"> You have **{len(remaining)}** open security findings"
            if len(accepted) > 0:
                details += f" and **{len(accepted)}** security findings for which you have previous accepted the risk"
            details += f".\n[You can view these findings in Sigrid]({sigridLink}).\n\n"

        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        objectiveLabel = Objective.getSeverityObjectiveLabel(self.objective)
        if self.isObjectiveSuccess(feedback, options):
            return [f"✅  You achieved your objective of having {objectiveLabel} security findings"]
        else:
            return [f"⚠️  You did not meet your objective of having {objectiveLabel} security findings"]

    def generateFindingsTable(self, findings, options):
        if len(findings) == 0:
            return ""

        md = "| Risk | Meets objective? | File | Finding |\n"
        md += "|----|----|----|----|\n"

        for finding in sorted(findings, key=lambda f: Objective.sortBySeverity(f.risk))[0:self.MAX_FINDINGS]:
            severitySymbol = self.SEVERITY_SYMBOLS[finding.risk]
            objectiveSymbol = self.formatObjectiveSymbol(finding)
            link = self.decorateLink(options, f"{finding.file}:{finding.line}", finding.file, finding.line)
            md += f"| {severitySymbol} | {objectiveSymbol} | {link} | {finding.description} |\n"

        if len(findings) > self.MAX_FINDINGS:
            md += f"| | ... and {len(findings) - self.MAX_FINDINGS} more findings | | |\n"

        return f"{md}\n"

    def formatObjectiveSymbol(self, finding):
        if finding.status == FindingStatus.FIXED:
            return "✅"
        elif finding.partOfObjective:
            return "❌"
        else:
            return "⚠️"

    def getCapability(self):
        return SECURITY

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/security-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        allFindings = self.extractFindings(feedback)
        relevantFindings = self.processor.filterStatus(allFindings, FindingStatus.INTRODUCED, partOfObjective=True)
        return len(relevantFindings) == 0

    def extractFindings(self, feedback):
        findings = list(self.processor.extractFindings(feedback))

        if self.previousFeedback is not None:
            # For on-premise Sigrid we need to check for new findings ourselves,
            # since we don't have an end point to perform that logic.
            previousFindings = list(self.processor.extractFindings(self.previousFeedback))
            previousFingerprints = [finding.fingerprint for finding in previousFindings]

            for finding in findings:
                if finding.status == FindingStatus.REMAINING and finding.fingerprint not in previousFingerprints:
                    finding.status = FindingStatus.INTRODUCED

        return findings

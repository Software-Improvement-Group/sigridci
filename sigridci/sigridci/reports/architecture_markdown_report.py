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
from ..capability import ARCHITECTURE
from ..platform import AQ_EXCLUDE_DOCS, Platform


class ArchitectureMarkdownReport(Report, MarkdownRenderer):
    FINDING_TYPES = {
        "UNDESIRABLE" : "🔴 Undesirable dependency",
        "CYCLIC" : "🟠 Cyclic dependency"
    }

    def __init__(self):
        super().__init__()
        self.tableLineSeparator = "<br />" if Platform.isHtmlMarkdownSupported() else " • "

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        positive = self.getPositiveFeedback(feedback)
        negative = self.getNegativeFeedback(feedback)
        remaining = self.getRemainingFeedback(feedback)
        sigridLink = f"{self.getSigridUrl(options)}/-/architecture-quality/explorer"

        md = f"Sigrid compared your code against the baseline of {feedback['baseline']}.\n\n"

        if len(positive) > 0 or len(negative) == 0:
            md += "## 👍 What went well?\n\n"
            if len(positive) > 0:
                md += f"> You improved **{len(positive)}** architecture issues.\n\n"
                md += f"{self.generateFindingsTable(positive, options)}\n"
            elif len(negative) == 0:
                md += "> You did not introduce any architecture issues during your changes, great job!\n\n"

        if len(negative) > 0:
            md += "## 👎 What could be better?\n\n"
            md += f"> Unfortunately, you introduced **{len(negative)}** architecture issues.\n\n"
            md += f"{self.generateFindingsTable(negative, options)}\n"
            md += "If you believe these findings are false positives,\n"
            md += f"you can [exclude the rule]({AQ_EXCLUDE_DOCS}) in the Sigrid configuration.\n"

        if remaining > 0:
            md += "## 📚 You have remaining technical debt\n\n"
            md += f"> You have **{remaining}** architecture issues.\n"
            md += f"[You can view these findings in Sigrid]({sigridLink}).\n\n"

        return self.renderMarkdownTemplate(feedback, options, md, sigridLink)

    def generateFindingsTable(self, findings, options):
        if len(findings) == 0:
            return ""

        md = "| Issue | Location |\n"
        md += "|---|---|\n"
        for finding in findings:
            type = self.FINDING_TYPES.get(finding["qualification"], finding["qualification"])
            activity = finding["activity"].title()
            source = self.formatDependencyLocation(finding["sourceHierarchy"], options)
            target = self.formatDependencyLocation(finding["targetHierarchy"], options)
            location = f"Source: {source}{self.tableLineSeparator}Target: {target}"
            md += f"| **{type}**{self.tableLineSeparator}({activity}) | {location} |\n"
        return md

    def formatDependencyLocation(self, hierarchy, options):
        topLevelComponent = hierarchy[0]
        file = next((se for se in hierarchy if se["type"] == "FILE"), None)

        location = topLevelComponent["shortName"]
        if file:
            location += f"▶ {self.decorateLink(options, file['shortName'], file['name'])}"
        return location

    def getSummary(self, feedback, options):
        if self.isObjectiveSuccess(feedback, options):
            return [f"✅  You achieved your objective of having no architecture issues"]
        else:
            return [f"⚠️  You did not meet your objective of having no architecture issues"]

    def getCapability(self):
        return ARCHITECTURE

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/architecture-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        return len(self.getNegativeFeedback(feedback)) == 0

    def getDependencyFeedback(self, feedback, activity):
        dependencyFeedback = feedback.get("dependencyFeedback", [])
        return [dep for dep in dependencyFeedback if dep["qualification"] != "NEW" and dep["activity"] in activity]

    def getPositiveFeedback(self, feedback):
        return self.getDependencyFeedback(feedback, ("REMOVED", "DECREASED"))

    def getNegativeFeedback(self, feedback):
        return self.getDependencyFeedback(feedback, ("INTRODUCED", "INCREASED"))

    def getRemainingFeedback(self, feedback):
        return sum(feedback["remaining"].values())

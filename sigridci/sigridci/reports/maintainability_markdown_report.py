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

import html
import os

from .report import Report, MarkdownRenderer
from ..objective import Objective, ObjectiveStatus
from ..platform import Platform


class MaintainabilityMarkdownReport(Report, MarkdownRenderer):
    MAX_SHOWN_FINDINGS = 8
    MAX_OCCURRENCES = 3

    RISK_CATEGORY_SYMBOLS = {
        "VERY_HIGH" : "🔴",
        "HIGH" : "🟠",
        "MODERATE" : "🟡",
        "MEDIUM" : "🟡",
        "LOW" : "🟢"
    }

    def __init__(self, objective=3.5):
        super().__init__()
        self.objective = objective

    def generate(self, analysisId, feedback, options):
        print(feedback)
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            markdown = self.renderMarkdown(analysisId, feedback, options)
            f.write(markdown)

    def renderMarkdown(self, analysisId, feedback, options):
        status = Objective.determineStatus(feedback, self.objective)
        sigridLink = self.getSigridUrl(options)

        md = f"# [Sigrid]({sigridLink}) maintainability feedback\n\n"
        md += f"{self.renderSummary(feedback, options)}\n\n"

        if status != ObjectiveStatus.UNKNOWN:
            if Platform.isHtmlMarkdownSupported():
                md += "<details><summary>Show details</summary>\n\n"
            md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"
            md += self.renderRefactoringCandidates(feedback, options)
            md += "## ⭐️ Sigrid ratings\n\n"
            md += self.renderRatingsTable(feedback)
            md += self.renderReactionSection(options)
            if Platform.isHtmlMarkdownSupported():
                md += "</details>\n"

        md += "\n----\n"
        md += f"[**View this system in Sigrid**]({sigridLink})"
        return md

    def renderSummary(self, feedback, options):
        return f"**{self.getSummary(feedback, options)}**"

    def getSummary(self, feedback, options):
        status = Objective.determineStatus(feedback, self.objective)
        targetText = f"{self.objective:.1f} stars"

        if status == ObjectiveStatus.ACHIEVED:
            return f"✅  You wrote maintainable code and achieved your objective of {targetText}"
        elif status == ObjectiveStatus.IMPROVED:
            return f"↗️  You improved the maintainability of the code towards your objective of {targetText}"
        elif status == ObjectiveStatus.UNCHANGED:
            return f"⏸️️  Your maintainability remains unchanged and is still below your objective of {targetText}"
        elif status == ObjectiveStatus.WORSENED:
            return f"⚠️  Your code did not improve maintainability towards your objective of {targetText}"
        else:
            return "💭️  You did not change any files that are measured by Sigrid"

    def renderRefactoringCandidates(self, feedback, options):
        good = self.filterRefactoringCandidates(feedback, self.GOOD_CATEGORIES)
        bad = self.filterRefactoringCandidates(feedback, self.BAD_CATEGORIES)
        unchanged = self.filterRefactoringCandidates(feedback, self.UNCHANGED_CATEGORIES)

        md = ""
        md += "## 👍 What went well?\n\n"
        md += f"> You fixed or improved **{len(good)}** refactoring candidates.\n\n"
        md += self.renderRefactoringCandidatesTable(good, options) + "\n"

        md += "## 👎 What could be better?\n\n"
        if len(bad) > 0:
            md += f"> Unfortunately, **{len(bad)}** refactoring candidates were introduced or got worse.\n\n"
            md += self.renderRefactoringCandidatesTable(bad, options) + "\n"
        else:
            md += "> You did not introduce any technical debt during your changes, great job!\n\n"

        md += "## 📚 Remaining technical debt\n\n"
        md += f"> **{len(unchanged)}** refactoring candidates didn't get better or worse, but are still present in the code you touched.\n\n"
        md += f"[View this system in Sigrid to explore your technical debt]({self.getSigridUrl(options)})\n\n"
        return md

    def renderRatingsTable(self, feedback):
        md = ""
        md += f"| System property | System on {self.formatBaseline(feedback)} | Before changes | New/changed code |\n"
        md += f"|-----------------|-------------------------------------------|----------------|------------------|\n"

        for metric in self.METRICS:
            fmt = "**" if metric == "MAINTAINABILITY" else ""
            metricName = self.formatMetricName(metric)
            baseline = self.formatRating(feedback["baselineRatings"], metric)
            newCode = self.formatRating(feedback["newCodeRatings"], metric)
            before = self.formatRating(feedback["changedCodeBeforeRatings"], metric)
            md += f"| {fmt}{metricName}{fmt} | {fmt}{baseline}{fmt} | {fmt}{before}{fmt} | {fmt}{newCode}{fmt} |\n"

        return md

    def renderRefactoringCandidatesTable(self, refactoringCandidates, options):
        if len(refactoringCandidates) == 0:
            return ""

        md = ""
        md += "| Risk | System property | Location |\n"
        md += "|------|-----------------|----------|\n"

        for rc in refactoringCandidates[0:self.MAX_SHOWN_FINDINGS]:
            symbol = self.RISK_CATEGORY_SYMBOLS[rc["riskCategory"]]
            metricName = self.formatMetricName(rc["metric"])
            metricInfo = f"**{metricName}**<br />({rc['category'].title()})"
            location = self.formatRefactoringCandidateLocation(rc, options)
            md += f"| {symbol} | {metricInfo} | {location} |\n"

        if len(refactoringCandidates) > self.MAX_SHOWN_FINDINGS:
            md += f"| ⚫️ | | + {len(refactoringCandidates) - self.MAX_SHOWN_FINDINGS} more |"

        return md + "\n"

    def formatRefactoringCandidateLocation(self, rc, options):
        label = html.escape(rc["subject"]).replace("::", "<br />")
        if not rc.get("occurrences"):
            return label
        occurrences = rc["occurrences"][0:self.MAX_OCCURRENCES]
        md = "<br />".join(self.formatRefactoringCandidateOccurrence(options, label, rc, occ) for occ in occurrences)
        if len(rc["occurrences"]) > self.MAX_OCCURRENCES:
            md += f"<br />+ {len(rc['occurrences']) - self.MAX_OCCURRENCES} occurrences"
        return md

    def formatRefactoringCandidateOccurrence(self, options, label, rc, occurrence):
        if rc["metric"] == "DUPLICATION":
            label = f"{occurrence['filePath']} line {occurrence['startLine']}-{occurrence['endLine']}"
        return self.decorateLink(options, label, occurrence["filePath"], occurrence.get("startLine", 0))

    def getCapability(self):
        return "Maintainability"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        status = Objective.determineStatus(feedback, self.objective)
        return status != ObjectiveStatus.WORSENED

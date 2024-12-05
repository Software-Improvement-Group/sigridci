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

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            markdown = self.renderMarkdown(analysisId, feedback, options)
            f.write(markdown)

    def renderMarkdown(self, analysisId, feedback, options):
        status = Objective.determineStatus(feedback, options)
        sigridLink = self.getSigridUrl(options)

        md = f"# [Sigrid]({sigridLink}) maintainability feedback\n\n"
        md += f"{self.renderSummary(feedback, options)}\n\n"

        if status != ObjectiveStatus.UNKNOWN:
            if Platform.isHtmlMarkdownSupported():
                md += "<details><summary>Show details</summary>\n\n"

            md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"
            md += self.renderRefactoringCandidates(feedback, sigridLink)
            md += "## ⭐️ Sigrid ratings\n\n"
            md += self.renderRatingsTable(feedback)

            if options.feedbackURL:
                md += "\n----\n\n"
                md += "## Did you find this feedback helpful?\n\n"
                md += "We would like to know your thoughts to make Sigrid better.\n"
                md += "Your username will remain confidential throughout the process.\n\n"
                md += f"- ✅ [Yes, these findings are useful]({self.getFeedbackLink(options, 'useful')})\n"
                md += f"- 🔸 [The findings are false positives]({self.getFeedbackLink(options, 'falsepositive')})\n"
                md += f"- 🔹 [These findings are not so important to me]({self.getFeedbackLink(options, 'unimportant')})\n"

            if Platform.isHtmlMarkdownSupported():
                md += "</details>\n"

        md += "\n----\n"
        md += f"[**View this system in Sigrid**]({sigridLink})"
        return md

    def renderSummary(self, feedback, options):
        return f"**{self.getSummaryText(feedback, options)}**"

    def renderRefactoringCandidates(self, feedback, sigridLink):
        good = self.filterRefactoringCandidates(feedback, ["improved"])
        bad = self.filterRefactoringCandidates(feedback, ["introduced", "worsened"])
        unchanged = self.filterRefactoringCandidates(feedback, ["unchanged"])

        md = ""
        md += "## 👍 What went well?\n\n"
        md += f"> You fixed or improved **{len(good)}** refactoring candidates.\n\n"
        md += self.renderRefactoringCandidatesTable(good) + "\n"

        md += "## 👎 What could be better?\n\n"
        if len(bad) > 0:
            md += f"> Unfortunately, **{len(bad)}** refactoring candidates were introduced or got worse.\n\n"
            md += self.renderRefactoringCandidatesTable(bad) + "\n"
        else:
            md += "> You did not introduce any technical debt during your changes, great job!\n\n"

        md += "## 📚 Remaining technical debt\n\n"
        md += f"> **{len(unchanged)}** refactoring candidates didn't get better or worse, but are still present in the code you touched.\n\n"
        md += f"[View this system in Sigrid** to explore your technical debt]({sigridLink})\n\n"
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

    def filterRefactoringCandidates(self, feedback, categories):
        return [rc for rc in feedback["refactoringCandidates"] if rc["category"] in categories]

    def renderRefactoringCandidatesTable(self, refactoringCandidates):
        if len(refactoringCandidates) == 0:
            return ""

        sortFunction = lambda rc: list(self.RISK_CATEGORY_SYMBOLS).index(rc["riskCategory"])
        sortedRefactoringCandidates = sorted(refactoringCandidates, key=sortFunction)

        md = ""
        md += "| Risk | System property | Location |\n"
        md += "|------|-----------------|----------|\n"

        for rc in sortedRefactoringCandidates[0:self.MAX_SHOWN_FINDINGS]:
            symbol = self.RISK_CATEGORY_SYMBOLS[rc["riskCategory"]]
            metricName = self.formatMetricName(rc["metric"])
            metricInfo = f"**{metricName}**<br />({rc['category'].title()})"
            location = self.formatRefactoringCandidateLocation(rc)
            md += f"| {symbol} | {metricInfo} | {location} |\n"

        if len(sortedRefactoringCandidates) > self.MAX_SHOWN_FINDINGS:
            md += f"| ⚫️ | | + {len(sortedRefactoringCandidates) - self.MAX_SHOWN_FINDINGS} more |"

        return md + "\n"

    def formatRefactoringCandidateLocation(self, rc):
        location = rc["subject"]

        if rc.get("occurrences") and len(rc["occurrences"]) > self.MAX_OCCURRENCES:
            formatOccurrence = lambda occ: f"{occ['filePath']} (line {occ['startLine']}-{occ['endLine']})"
            occurrences = [formatOccurrence(occ) for occ in rc["occurrences"][0:self.MAX_OCCURRENCES]]
            location = "\n".join(occurrences) + f"\n+ {len(rc['occurrences']) - self.MAX_OCCURRENCES} occurrences"

        return html.escape(location).replace("::", "<br />").replace("\n", "<br />")

    def getFeedbackLink(self, options, feedback):
        return f"{options.feedbackURL}?feature=sigridci.feedback&feedback={feedback}&system={options.getSystemId()}"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        status = Objective.determineStatus(feedback, options)
        return status != ObjectiveStatus.WORSENED

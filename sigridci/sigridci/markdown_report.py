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

from .objective import Objective, ObjectiveStatus
from .report import Report


class MarkdownReport(Report):

    RISK_CATEGORY_SYMBOLS = {
        "VERY_HIGH" : "🔴",
        "HIGH" : "🟠",
        "MODERATE" : "🟡",
        "MEDIUM" : "🟡",
        "LOW" : "🟢"
    }

    def generate(self, analysisId, feedback, options):
        with open(os.path.abspath(f"{self.outputDir}/feedback.md"), "w", encoding="utf-8") as f:
            markdown = self.renderMarkdown(analysisId, feedback, options)
            f.write(markdown)

    def renderMarkdown(self, analysisId, feedback, options):
        sigridLink = self.getSigridUrl(options)
        landingPage = self.getLandingPage(analysisId, options)
        good = self.filterRefactoringCandidates(feedback, ["improved"])
        bad = self.filterRefactoringCandidates(feedback, ["introduced", "worsened"])
        unchanged = self.filterRefactoringCandidates(feedback, ["unchanged"])

        md = "# Sigrid maintainability feedback\n\n"
        md += f"**{self.getSummaryText(feedback, options)}**\n\n"
        md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"

        md += "## 👍 What went well?\n\n"
        md += f"You fixed or improved **{len(good)}** refactoring candidates.\n\n"
        md += self.renderRefactoringCandidatesTable(good) + "\n"

        md += "## 👎 What could be better?\n\n"
        md += f"Unfortunately, **{len(bad)}** refactoring candidates were introduced or got worse.\n\n"
        md += self.renderRefactoringCandidatesTable(bad) + "\n"

        md += "## 📚 Remaining technical debt\n\n"
        md += f"**{len(unchanged)}** refactoring candidates didn't get better or worse, but are still in the code.\n\n"
        md += self.renderRefactoringCandidatesTable(unchanged) + "\n"

        md += "## Sigrid ratings\n\n"
        md += self.renderRatingsTable(feedback)
        md += "\n----\n\n"
        md += f"- [**View this system in Sigrid**]({sigridLink})\n"
        md += f"- [**View this Sigrid CI feedback in Sigrid**]({landingPage})\n"
        return md

    def renderSummary(self, feedback, options):
        return f"**{self.getSummaryText(feedback, options)}**"

    def renderRatingsTable(self, feedback):
        md = ""
        md += f"| System property | Baseline on {self.formatBaseline(feedback)} | New/changed code |\n"
        md += f"|-----------------|---------------------------------------------|------------------|\n"

        for metric in self.METRICS:
            fmt = "**" if metric == "MAINTAINABILITY" else ""
            baseline = "(" + self.formatRating(feedback["baselineRatings"], metric) + ")"
            newCode = self.formatRating(feedback["newCodeRatings"], metric)
            md += f"| {fmt}{self.formatMetricName(metric)}{fmt} | {fmt}{baseline}{fmt} | {fmt}{newCode}{fmt} |\n"

        return md

    def filterRefactoringCandidates(self, feedback, categories):
        return [rc for rc in feedback["refactoringCandidates"] if rc["category"] in categories]

    def sortRefactoringCandidates(self, rc):
        return list(self.RISK_CATEGORY_SYMBOLS).index(rc["riskCategory"])

    def renderRefactoringCandidatesTable(self, refactoringCandidates):
        if len(refactoringCandidates) == 0:
            return ""

        md = ""
        md += "| Risk | System property | Location |\n"
        md += "|------|-----------------|----------|\n"

        for rc in sorted(refactoringCandidates, key=self.sortRefactoringCandidates):
            symbol = self.RISK_CATEGORY_SYMBOLS[rc["riskCategory"]]
            metricName = self.formatMetricName(rc["metric"])
            metricInfo = f"**{metricName}**<br />({rc['category'].title()})"
            location = html.escape(rc["subject"]).replace("::", "<br />").replace("\n", "<br />")
            md += f"| {symbol} | {metricInfo} | {location} |\n"

        return md + "\n"

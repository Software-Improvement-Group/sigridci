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
        md += self.renderSummary(feedback, options)
        md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"

        md += "## 👍 What went well?\n\n"
        md += f"You fixed or improved **{len(good)}** refactoring candidates.\n\n"
        md += self.renderRefactoringCandidatesTable(good) + "\n"

        md += "## 👎 What could be better?\n\n"
        md += f"Unfortunately, **{len(bad)}** refactoring candidates were introduced or got worse.\n\n"
        md += self.renderRefactoringCandidatesTable(bad) + "\n"

        md += "## 📚 Remaining technical debt\n\n"
        md += f"**{len(unchanged)}** refactoring candidates didn't get any or worse, but are still in the code.\n\n"
        md += self.renderRefactoringCandidatesTable(unchanged) + "\n"

        md += "## Sigrid ratings\n\n"
        md += self.renderRatingsTable(feedback)
        md += "\n----\n\n"
        md += f"- [**View this system in Sigrid**]({sigridLink})\n"
        md += f"- [**View this Sigrid CI feedback in Sigrid**]({landingPage})\n"
        return md

    def renderSummary(self, feedback, options):
        target = f"{options.targetRating:.1f} stars"

        if not self.isFeedbackAvailable(feedback):
            return "** You did not change any files that are measured by Sigrid **\n\n"
        elif self.meetsObjectives(feedback, options):
            return f"**✅ You wrote maintainable code and passed your Sigrid objective of {target}**\n\n"
        else:
            return f"**❌ Your code failed to meet your Sigrid objective of {target}**\n\n"

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
        categoryOrder = list(self.RISK_CATEGORY_SYMBOLS).index(rc["riskCategory"])
        return categoryOrder

    def renderRefactoringCandidatesTable(self, refactoringCandidates):
        md = ""
        md += "| Risk | System property | Location |\n"
        md += "|------|-----------------|----------|\n"

        for rc in sorted(refactoringCandidates, key=self.sortRefactoringCandidates):
            symbol = self.RISK_CATEGORY_SYMBOLS[rc["riskCategory"]]
            metric = self.formatMetricName(rc["metric"])
            location = html.escape(rc["subject"]).replace("::", "<br />").replace("\n", "<br />")
            md += f"| {symbol} | {metric} | {location} |\n"

        return md + "\n"

    def formatRefactoringCandidateLink(self, rc):
        entries = rc["subject"].split("::")[-1].split("\n")
        codeLinkBase = os.environ.get("CODE_LINK_BASE", "")

        if codeLinkBase:
            extractLabel = lambda entry: entry.replace("(", "\\(").replace(")", "\\)").strip()
            extractPath = lambda entry: entry.split(":")[0].split("(")[0].strip()
            return ", ".join([f"[{extractLabel(entry)}]({codeLinkBase}/{extractPath(entry)})" for entry in entries])
        else:
            return ", ".join([entry for entry in entries])

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

from .report import Report


class MarkdownReport(Report):

    def generate(self, analysisId, feedback, options):
        with open(os.path.abspath("sigrid-ci-output/feedback.md"), "w", encoding="utf-8") as f:
            markdown = self.renderMarkdown(analysisId, feedback, options)
            f.write(markdown)

    def renderMarkdown(self, analysisId, feedback, options):
        sigridLink = self.getSigridUrl(options)
        landingPage = self.getLandingPage(analysisId, options)

        md = "# Sigrid maintainability feedback\n\n"
        md += self.renderSummary(feedback, options)
        md += "## Sigrid ratings\n\n"
        md += self.renderRatingsTable(feedback, options)
        if not self.meetsObjectives(feedback, options):
            md += "\n## Refactoring candidates\n\n"
            md += self.renderRefactoringCandidatesList(feedback)
        md += "\n----\n\n"
        md += f"- [**View this system in Sigrid**]({sigridLink})\n"
        md += f"- [**View this feedback in Sigrid**]({landingPage})\n"
        return md

    def renderSummary(self, feedback, options):
        targetRating = ("%.1f" % options.targetRating) + " stars"

        if not self.isFeedbackAvailable(feedback):
            return "** You did not change any files that are measured by Sigrid **\n\n"
        elif self.meetsObjectives(feedback, options):
            return f"**\u2705 You wrote maintainable code and passed your Sigrid objective of {targetRating}**\n\n"
        else:
            return f"**\u274C Your code failed to meet your Sigrid objective of {targetRating}**\n\n"

    def renderRatingsTable(self, feedback, options):
        md = ""
        md += f"| System property | Baseline on {self.formatBaseline(feedback)} | New/changed code |\n"
        md += f"|-----------------|---------------------------------------------|------------------|\n"

        for metric in self.METRICS:
            fmt = "**" if metric == "MAINTAINABILITY" else ""
            baseline = "(" + self.formatRating(feedback["baselineRatings"], metric) + ")"
            newCode = self.formatRating(feedback["newCodeRatings"], metric)
            md += f"| {fmt}{self.formatMetricName(metric)}{fmt} | {fmt}{baseline}{fmt} | {fmt}{newCode}{fmt} |\n"

        return md

    def renderRefactoringCandidatesList(self, feedback):
        md = ""

        for metric in self.REFACTORING_CANDIDATE_METRICS:
            relevantRefactoringCandidates = self.getRefactoringCandidates(feedback, metric)
            if len(relevantRefactoringCandidates) > 0:
                md += f"\n**{self.formatMetricName(metric)}**\n\n"
                for rc in relevantRefactoringCandidates:
                    md += f"- *({rc['category']})* {self.formatRefactoringCandidateLink(rc)}\n"

        return md

    def formatRefactoringCandidateLink(self, rc):
        entries = rc["subject"].split("::")[-1].split("\n")
        codeLinkBase = os.environ.get("CODE_LINK_BASE", "")

        if codeLinkBase:
            extractLabel = lambda entry: entry.replace("(", "\\(").replace(")", "\\)").strip()
            extractPath = lambda entry: entry.split(":")[0].split("(")[0].strip()
            return ", ".join([f"[{extractLabel(entry)}]({codeLinkBase}/{extractPath(entry)})" for entry in entries])
        else:
            return ", ".join([entry for entry in entries])

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

import urllib.parse
from datetime import datetime

from ..platform import Platform


class Report:
    REFACTORING_CANDIDATE_METRICS = [
        "DUPLICATION",
        "UNIT_SIZE",
        "UNIT_COMPLEXITY",
        "UNIT_INTERFACING",
        "MODULE_COUPLING"
    ]

    METRICS = [
        "VOLUME",
        *REFACTORING_CANDIDATE_METRICS,
        "COMPONENT_INDEPENDENCE",
        "COMPONENT_ENTANGLEMENT",
        "MAINTAINABILITY"
    ]

    def generate(self, analysisId, feedback, options):
        pass

    def formatMetricName(self, metric):
        return metric.replace("_PROP", "").title().replace("_", " ")

    def formatRating(self, ratings, metric, naText="N/A"):
        if ratings.get(metric, None) == None:
            return naText
        return "%.1f" % ratings[metric]

    def formatBaseline(self, feedback):
        if not feedback.get("baseline", None):
            return "N/A"
        snapshotDate = datetime.strptime(feedback["baseline"], "%Y%m%d")
        return snapshotDate.strftime("%Y-%m-%d")

    def getRefactoringCandidates(self, feedback, metric):
        refactoringCandidates = feedback.get("refactoringCandidates", [])
        return [rc for rc in refactoringCandidates if rc["metric"] == metric or metric == "MAINTAINABILITY"]

    def getSigridUrl(self, options):
        customer = urllib.parse.quote_plus(options.customer.lower())
        system = urllib.parse.quote_plus(options.system.lower())
        return f"{options.sigridURL}/{customer}/{system}"


class MarkdownRenderer:
    def renderMarkdown(self, analysisId, feedback, options):
        raise NotImplementedError()

    def renderMarkdownTemplate(self, feedback, options, details, sigridLink):
        md = f"# [Sigrid]({sigridLink}) {self.getCapability()} feedback\n\n"
        md += f"**{self.getSummary(feedback, options)}**\n\n"
        if len(details) > 0:
            if Platform.isHtmlMarkdownSupported():
                md += "<details><summary>Show details</summary>\n\n"
            md += details
            md += self.renderReactionSection(options)
            if Platform.isHtmlMarkdownSupported():
                md += "</details>\n"
        md += "\n----\n\n"
        md += f"[**View this system in Sigrid**]({sigridLink})"
        return md

    def renderReactionSection(self, options):
        if not options.feedbackURL:
            return ""

        md = "\n### 💬 Did you find this feedback helpful?\n\n"
        md += "We would like to know your thoughts to make Sigrid better.\n"
        md += "Your username will remain confidential throughout the process.\n\n"
        md += f"- ✅ [Yes, these findings are useful]({self.getReactionLink(options, 'useful')})\n"
        md += f"- 🔸 [The findings are false positives]({self.getReactionLink(options, 'falsepositive')})\n"
        md += f"- 🔹 [These findings are not important to me]({self.getReactionLink(options, 'unimportant')})\n"
        return md

    def getReactionLink(self, options, reaction):
        featureId = "sigridci." + self.getCapability().lower().replace(" ", "")
        return f"{options.feedbackURL}?feature={featureId}&feedback={reaction}&system={options.getSystemId()}"

    def getSummary(self, feedback, options):
        raise NotImplementedError()

    def getCapability(self):
        raise NotImplementedError()

    def getMarkdownFile(self, options):
        raise NotImplementedError()

    def isObjectiveSuccess(self, feedback, options):
        raise NotImplementedError()

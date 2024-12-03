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

from ..objective import Objective, ObjectiveStatus
from ..platform import Platform
from ..publish_options import PublishOptions


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

    def getSummaryText(self, feedback, options):
        status = Objective.determineStatus(feedback, options)
        targetRating = PublishOptions.DEFAULT_TARGET if isinstance(options.targetRating, str) else options.targetRating
        targetText = f"{targetRating:.1f} stars"

        if status == ObjectiveStatus.ACHIEVED:
            return f"✅  You wrote maintainable code and achieved your objective of {targetText}"
        elif status == ObjectiveStatus.IMPROVED:
            return f"↗️  You improved your code's maintainability towards your objective of {targetText}"
        elif status == ObjectiveStatus.UNCHANGED:
            return f"⏸️️  Your rating did not change and is still below your objective of {targetText}"
        elif status == ObjectiveStatus.WORSENED:
            return f"⚠️  Your code did not improve towards your objective of {targetText}"
        else:
            return "💭️  You did not change any files that are measured by Sigrid"


class MarkdownRenderer:
    def renderMarkdown(self, analysisId, feedback, options):
        return ""

    def renderMarkdownTemplate(self, capability, summary, details, sigridLink):
        md = f"# [Sigrid]({sigridLink}) {capability} feedback\n\n"
        md += f"**{summary}**\n\n"
        if len(details) > 0:
            if Platform.isHtmlMarkdownSupported():
                md += "<details><summary>Show details</summary>\n\n"
            md += details
            if Platform.isHtmlMarkdownSupported():
                md += "</details>\n"
        md += "\n----\n\n"
        md += f"[**View this system in Sigrid**]({sigridLink})"
        return md

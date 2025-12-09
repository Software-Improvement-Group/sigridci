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
from ..objective import Objective, ObjectiveStatus


class StaticHtmlReport(Report):
    HTML_STAR_FULL = "&#9733;"
    HTML_STAR_EMPTY = "&#9734;"

    def __init__(self, objectives):
        super().__init__()
        # This report exists only for backward compatibility and is not able to depict
        # the new fine-grained objectives.
        self.objective = objectives.get("MAINTAINABILITY", Objective.DEFAULT_RATING_OBJECTIVE)

    def generate(self, analysisId, feedback, options):
        with open(os.path.dirname(__file__) + "/sigridci-feedback-template.html", encoding="utf-8", mode="r") as f:
            template = f.read()
            template = self.renderHtmlFeedback(template, feedback, options)

        reportFile = os.path.abspath(f"{options.outputDir}/index.html")
        with open(reportFile, encoding="utf-8", mode="w") as f:
            f.write(template)

    def renderHtmlFeedback(self, template, feedback, options):
        placeholders = {
            "CUSTOMER" : html.escape(options.customer),
            "SYSTEM" : html.escape(options.system),
            "TARGET" : "%.1f" % self.objective,
            "LINES_OF_CODE_TOUCHED" : "%d" % feedback.get("newCodeLinesOfCode", 0),
            "BASELINE_DATE" : self.formatBaseline(feedback),
            "SIGRID_LINK" : self.getSigridUrl(options),
            "MAINTAINABILITY_PASSED" : self.formatPassed(feedback)
        }

        for metric in Objective.MAINTAINABILITY_METRICS:
            placeholders[f"{metric}_OVERALL"] = self.formatRating(feedback.get("baselineRatings", {}), metric)
            placeholders[f"{metric}_NEW"] = self.formatRating(feedback.get("newCodeRatings", {}), metric)
            placeholders[f"{metric}_STARS_OVERALL"] = self.formatHtmlStars(feedback.get("baselineRatings", {}), metric)
            placeholders[f"{metric}_STARS_NEW"] = self.formatHtmlStars(feedback.get("newCodeRatings", {}), metric)
            placeholders[f"{metric}_REFACTORING_CANDIDATES"] = self.formatRefactoringCandidates(feedback, metric)

        placeholders["MAINTAINABILITY_TARGET"] = "%.1f" % self.objective
        placeholders["MAINTAINABILITY_PASSED"] = self.formatPassed(feedback)

        return self.fillPlaceholders(template, placeholders)

    def fillPlaceholders(self, template, placeholders):
        for placeholder, value in placeholders.items():
            template = template.replace(f"@@@{placeholder}", value)
        return template

    def formatPassed(self, feedback):
        status = Objective.determineStatus(feedback, self.objective)
        return "failed" if status == ObjectiveStatus.WORSENED else "passed"

    def formatRefactoringCandidates(self, feedback, metric):
        refactoringCandidates = self.getRefactoringCandidates(feedback, metric)
        if len(refactoringCandidates) == 0:
            return "None"
        return "\n".join([self.formatRefactoringCandidate(rc) for rc in refactoringCandidates])

    def formatRefactoringCandidate(self, rc):
        subjectName = html.escape(rc["subject"]).replace("\n", "<br />").replace("::", "<br />")
        category = html.escape(rc["category"])
        return f"<span><em>({category})</em><div>{subjectName}</div></span>"

    def formatHtmlStars(self, ratings, metric):
        if ratings.get(metric, None) == None:
            return "N/A"
        stars = min(int(ratings[metric] + 0.5), 5)
        fullStars = stars * self.HTML_STAR_FULL
        emptyStars = (5 - stars) * self.HTML_STAR_EMPTY
        rating = self.formatRating(ratings, metric)
        return f"<strong class=\"stars{stars}\">{fullStars}{emptyStars}</strong> &nbsp; " + rating

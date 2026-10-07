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
from typing import Union, Iterator

from .markdown_fragment import MarkdownFragment, FeedbackFinding, Location, Summary
from .report import Report
from ..capability import MAINTAINABILITY, Capability
from ..objective import Objective, ObjectiveStatus
from ..publish_options import PublishOptions


class MaintainabilityMarkdownReport(MarkdownFragment, Report):
    def __init__(self, objectives: Union[None, dict[str, Union[float, None]]] = None):
        if objectives is None:
            objectives = {"MAINTAINABILITY" : Objective.DEFAULT_RATING_OBJECTIVE}
        self.objective = {title: value for title, value in objectives.items() if title.startswith("MAINTAINABILITY")}

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        # This is now a no-op, this class only implements Report
        # for backward compatibility.
        pass

    def getSummary(self, feedback: dict, options: PublishOptions) -> list[Summary]:
        return [self.getSummaryForObjective(metric, target or 0, feedback) for metric, target in self.objective.items()]

    def getSummaryForObjective(self, metric: str, target: float, feedback: dict) -> Summary:
        status = Objective.determineStatus(feedback, target, metric)
        targetText = f"{target:.1f} stars"

        objectiveName = f"{self.formatMetricName(metric)} objective"
        if len(self.objective) == 1 and metric == "MAINTAINABILITY":
            objectiveName = "objective"

        if status == ObjectiveStatus.ACHIEVED:
            return Summary("✅ ", f"You wrote maintainable code and achieved your {objectiveName} of {targetText}.")
        elif status == ObjectiveStatus.IMPROVED:
            return Summary("✅️ ", f"You improved your code towards your {objectiveName} of {targetText}.")
        elif status == ObjectiveStatus.UNCHANGED:
            return Summary("️⚠️️ ", f"You are still below your {objectiveName} of {targetText}.")
        elif status == ObjectiveStatus.WORSENED:
            return Summary("❌️", f"Your code did not improve towards your {objectiveName} of {targetText}.")
        else:
            return Summary("💭️ ", f"You did not change any files that are analyzed by Sigrid.")

    def renderRatingsTable(self, feedback: dict) -> str:
        md = f"| System property | System on {self.formatBaseline(feedback)} | Before changes | New/changed code |\n"
        md += f"|-----------------|-------------------------------------------|----------------|------------------|\n"

        for metric in Objective.SYSTEM_PROPERTIES + ["MAINTAINABILITY"]:
            fmt = "**" if metric == "MAINTAINABILITY" else ""
            metricName = self.formatMetricName(metric)
            baseline = self.formatRating(feedback["baselineRatings"], metric)
            newCode = self.formatRating(feedback["newCodeRatings"], metric)
            before = self.formatRating(feedback["changedCodeBeforeRatings"], metric)
            md += f"| {fmt}{metricName}{fmt} | {fmt}{baseline}{fmt} | {fmt}{before}{fmt} | {fmt}{newCode}{fmt} |\n"

        return f"{md}\n"

    def getCapability(self) -> Capability:
        return MAINTAINABILITY

    def getMarkdownFile(self, options: PublishOptions) -> str:
        return os.path.abspath(f"{options.outputDir}/feedback.md")

    def getObjectiveStatuses(self, feedback):
        return [
            Objective.checkMaintainabilityRating(feedback, metric, target or 0.0)
            for metric, target
            in self.objective.items()
        ]

    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        return not ObjectiveStatus.WORSENED in self.getObjectiveStatuses(feedback)

    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        return (self.toFinding(rc) for rc in self.filterRefactoringCandidates(feedback, self.BAD_CATEGORIES))

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        return (self.toFinding(rc) for rc in self.filterRefactoringCandidates(feedback, self.GOOD_CATEGORIES))

    def toFinding(self, rc: dict) -> FeedbackFinding:
        title = f"{self.formatMetricName(rc['metric'])} ({rc['category'].title()})"
        details = self.formatSubject(rc)
        locations = [Location(occ["filePath"], occ["startLine"]) for occ in rc["occurrences"]]
        return FeedbackFinding(rc["riskCategory"], MAINTAINABILITY, title, details, locations)

    def formatSubject(self, rc: dict) -> list[str]:
        getFileName = lambda filePath: filePath.split("/")[-1].split("\\")[-1]
        if rc["metric"] == "DUPLICATION":
            return [f"{int(rc['value'])} duplicated lines across {len(rc['occurrences'])} occurences"]
        elif "::" in rc["subject"]:
            return [rc["subject"].split("::")[-1].split("(")[0]]
        else:
            return [getFileName(rc["subject"])]

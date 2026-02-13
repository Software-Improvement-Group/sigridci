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

from enum import Enum


class ObjectiveStatus(Enum):
    ACHIEVED = 1
    IMPROVED = 2
    UNCHANGED = 3
    WORSENED = 4
    UNKNOWN = 5


class Objective:
    DEFAULT_RATING_OBJECTIVE = 3.5
    DEFAULT_FINDING_OBJECTIVE = "HIGH"
    SEVERITY_OBJECTIVE = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "NONE", "UNKNOWN"]
    REFACTORING_CANDIDATES = ["DUPLICATION", "UNIT_SIZE", "UNIT_COMPLEXITY", "UNIT_INTERFACING", "MODULE_COUPLING"]
    SYSTEM_PROPERTIES = ["VOLUME"] + REFACTORING_CANDIDATES + ["COMPONENT_INDEPENDENCE", "COMPONENT_ENTANGLEMENT"]
    MAINTAINABILITY_METRICS = ["MAINTAINABILITY"] + SYSTEM_PROPERTIES

    @staticmethod
    def checkMaintainabilityRating(feedback, metric, target):
        return Objective.determineStatus(feedback, target, metric)

    @staticmethod
    def determineStatus(feedback, objective, metric="MAINTAINABILITY"):
        newAndChangedAfter = feedback.get("newCodeRatings", {}).get(metric, None)
        baseline = feedback.get("baselineRatings", {}).get(metric, None)
        changedCodeBefore = feedback.get("changedCodeBeforeRatings", {}).get(metric, None)
        changedCodeAfter = feedback.get("changedCodeAfterRatings", {}).get(metric, None)

        if newAndChangedAfter is None or objective is None:
            return ObjectiveStatus.UNKNOWN

        # We're using a split norm. If you've achieved your objective, we let
        # you pass regardless of the trend. This is intentional to avoid being
        # unreasonably negative (i.e. failing people that drop from 4.5 to 4.3
        # stars). Only when you *don't* meet your objective do we start looking
        # at the trend and whether you're moving in the right direction.
        if newAndChangedAfter >= objective:
            return ObjectiveStatus.ACHIEVED

        hasChangedCode = changedCodeBefore != None and changedCodeAfter != None

        if hasChangedCode:
            return Objective.determineStatusBasedOnTrend(changedCodeBefore, changedCodeAfter)
        else:
            return Objective.determineStatusBasedOnTrend(baseline, newAndChangedAfter)

    @staticmethod
    def determineStatusBasedOnTrend(previous, current):
        if previous == None or current == None:
            return ObjectiveStatus.UNKNOWN
        elif current > previous:
            return ObjectiveStatus.IMPROVED
        elif current < previous:
            return ObjectiveStatus.WORSENED
        else:
            return ObjectiveStatus.UNCHANGED

    @staticmethod
    def meetsFindingObjective(findingSeverities, objective):
        matches = [severity for severity in findingSeverities if Objective.isFindingIncluded(severity, objective)]
        return len(matches) == 0

    @staticmethod
    def isFindingIncluded(severity, objective):
        if objective == "CRITICAL":
            return False
        elif objective == "HIGH":
            return severity in ("CRITICAL")
        elif objective == "MEDIUM":
            return severity in ("CRITICAL", "HIGH")
        elif objective == "LOW":
            return severity in ("CRITICAL", "HIGH", "MEDIUM")
        else:
            return severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW")

    @staticmethod
    def getSeverityObjectiveLabel(objective):
        # We phrase objectives for findings as the "worst" severity
        # that is still allowed. So an objective of HIGH means high-severity
        # findings are allowed, but critical-severity findings are not allowed.
        # In the feedback, we want to phrase this in terms of goal, i.e. the
        # "least-worst" severity that is *not* allowed.
        if objective == "CRITICAL" or objective not in Objective.SEVERITY_OBJECTIVE:
            return "any"
        if objective == "NONE":
            return "no"
        index = Objective.SEVERITY_OBJECTIVE.index(objective)
        return f"no {Objective.SEVERITY_OBJECTIVE[index - 1].lower()}-severity"

    @staticmethod
    def sortBySeverity(severity):
        if not severity in Objective.SEVERITY_OBJECTIVE:
            return 99
        return Objective.SEVERITY_OBJECTIVE.index(severity)

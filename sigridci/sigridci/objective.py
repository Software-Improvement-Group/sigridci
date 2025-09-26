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

    @staticmethod
    def determineStatus(feedback, objective):
        newAndChangedAfter = feedback.get("newCodeRatings", {}).get("MAINTAINABILITY", None)
        baseline = feedback.get("baselineRatings", {}).get("MAINTAINABILITY", None)
        changedCodeBefore = feedback.get("changedCodeBeforeRatings", {}).get("MAINTAINABILITY", None)
        changedCodeAfter = feedback.get("changedCodeAfterRatings", {}).get("MAINTAINABILITY", None)

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
            return severity in ("CRITICAL")
        elif objective == "HIGH":
            return severity in ("CRITICAL", "HIGH")
        elif objective == "MEDIUM":
            return severity in ("CRITICAL", "HIGH", "MEDIUM")
        else:
            return True

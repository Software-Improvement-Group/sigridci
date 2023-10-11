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
    WORSENED = 3
    UNKNOWN = 4


class Objective:

    @staticmethod
    def determineStatus(feedback, options):
        target = options.targetRating
        newAndChangedAfter = feedback["newCodeRatings"].get("MAINTAINABILITY", None)
        baseline = feedback["baselineRatings"].get("MAINTAINABILITY", None)
        changedCodeBefore = feedback.get("changedCodeBeforeRatings", {}).get("MAINTAINABILITY", None)
        changedCodeAfter = feedback.get("changedCodeAfterRatings", {}).get("MAINTAINABILITY", None)

        if newAndChangedAfter == None or target in (None, "sigrid"):
            return ObjectiveStatus.UNKNOWN
        elif newAndChangedAfter >= target:
            return ObjectiveStatus.ACHIEVED
        elif changedCodeBefore != None and changedCodeAfter != None and changedCodeAfter >= changedCodeBefore:
            return ObjectiveStatus.IMPROVED
        elif newAndChangedAfter >= baseline:
            return ObjectiveStatus.IMPROVED
        else:
            return ObjectiveStatus.WORSENED

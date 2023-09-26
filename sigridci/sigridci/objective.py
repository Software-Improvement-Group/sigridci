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
    STAGNANT = 3
    UNKNOWN = 4


class Objective:

    @staticmethod
    def determineStatus(feedback, options):
        rating = feedback["newCodeRatings"].get("MAINTAINABILITY", None)
        target = options.targetRating
        baseline = feedback["baselineRatings"].get("MAINTAINABILITY", None)
        before = feedback["changedCodeBeforeRatings"].get("MAINTAINABILITY", baseline)

        if rating == None or target in (None, "sigrid"):
            return ObjectiveStatus.UNKNOWN
        elif rating >= target:
            return ObjectiveStatus.ACHIEVED
        elif before != None and rating > before:
            return ObjectiveStatus.IMPROVED
        else:
            return ObjectiveStatus.STAGNANT

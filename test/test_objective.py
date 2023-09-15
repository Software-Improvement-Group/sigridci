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

from unittest import TestCase

from sigridci.sigridci.objective import Objective, ObjectiveStatus
from sigridci.sigridci.publish_options import PublishOptions, RunMode


class ObjectiveTest(TestCase):

    def setUp(self):
        self.options = PublishOptions(
            customer="aap",
            system="noot",
            runMode=RunMode.FEEDBACK_AND_PUBLISH,
            sourceDir="/tmp",
            targetRating=3.5,
            sigridURL="https://example-sigrid.com"
        )

    def testUnknownIfRatingIsNotAvailable(self):
        feedback = self.mockFeedback(4.0, None, None)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.UNKNOWN)

    def testObjectiveAchieved(self):
        feedback = self.mockFeedback(4.0, 3.0, 5.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.ACHIEVED)

    def testObjectiveFailedButStillImproved(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.3)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testImprovedComparedToBaseline(self):
        feedback = self.mockFeedback(3.2, None, 3.3)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testStagnantIfObjectiveNotMet(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.STAGNANT)

    def mockFeedback(self, baselineRating, beforeRating, newCodeRating):
        return {
            "baselineRatings" : {
                "MAINTAINABILITY" : baselineRating
            },
            "changedCodeBeforeRatings" : {
                "MAINTAINABILITY" : beforeRating
            },
            "newCodeRatings" : {
                "MAINTAINABILITY" : newCodeRating
            }
        }

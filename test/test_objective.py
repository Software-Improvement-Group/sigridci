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
        feedback = self.mockFeedback(4.0, None, None, None)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.UNKNOWN)

    def testObjectiveAchieved(self):
        feedback = self.mockFeedback(4.0, 3.0, 5.0, 5.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.ACHIEVED)

    def testObjectiveFailedButStillImproved(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.3, 3.3)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testImprovedChangedCode(self):
        feedback = self.mockFeedback(3.4, 3.2, 3.3, 3.3)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testWorsenedChangedCode(self):
        feedback = self.mockFeedback(4.0, 3.0, 2.8, 2.8)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.WORSENED)

    def testChangedCodeTheSameQuality(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.0, 3.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.UNCHANGED)

    def testNewCodeIsBetterButBelowObjectiveAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 3.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testNewCodeIsWorseAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 1.9)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.WORSENED)

    def testNewCodeAchievesTargetAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 4.5)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.ACHIEVED)

    def testUnknownIfOldRatingsAreNotAvailable(self):
        feedback = self.mockFeedback(None, None, None, 3.0)
        status = Objective.determineStatus(feedback, self.options)
        self.assertEqual(status, ObjectiveStatus.UNKNOWN)

    def testIsFindingIncluded(self):
        self.assertTrue(Objective.isFindingIncluded("CRITICAL", "CRITICAL"))
        self.assertFalse(Objective.isFindingIncluded("HIGH", "CRITICAL"))
        self.assertFalse(Objective.isFindingIncluded("MEDIUM", "CRITICAL"))
        self.assertFalse(Objective.isFindingIncluded("LOW", "CRITICAL"))

        self.assertTrue(Objective.isFindingIncluded("CRITICAL", "HIGH"))
        self.assertTrue(Objective.isFindingIncluded("HIGH", "HIGH"))
        self.assertFalse(Objective.isFindingIncluded("MEDIUM", "HIGH"))
        self.assertFalse(Objective.isFindingIncluded("LOW", "HIGH"))

        self.assertTrue(Objective.isFindingIncluded("CRITICAL", "MEDIUM"))
        self.assertTrue(Objective.isFindingIncluded("HIGH", "MEDIUM"))
        self.assertTrue(Objective.isFindingIncluded("MEDIUM", "MEDIUM"))
        self.assertFalse(Objective.isFindingIncluded("LOW", "MEDIUM"))

    def testMeetsFindingObjective(self):
        self.assertTrue(Objective.meetsFindingObjective([], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["HIGH"], "CRITICAL"))

        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "CRITICAL"))
        self.assertFalse(Objective.meetsFindingObjective(["HIGH", "CRITICAL"], "CRITICAL"))

        self.assertTrue(Objective.meetsFindingObjective([], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["MEDIUM"], "HIGH"))

        self.assertFalse(Objective.meetsFindingObjective(["HIGH"], "HIGH"))
        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "HIGH"))

    def testDoNotCountUnknownSeverityAgainstObjective(self):
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "MEDIUM"))

    def mockFeedback(self, baseline, changedBefore, changedAfter, newAndChanged):
        return {
            "baselineRatings" : {
                "MAINTAINABILITY" : baseline
            },
            "changedCodeBeforeRatings" : {
                "MAINTAINABILITY" : changedBefore
            },
            "changedCodeAfterRatings" : {
                "MAINTAINABILITY" : changedAfter
            },
            "newCodeRatings" : {
                "MAINTAINABILITY" : newAndChanged
            }
        }

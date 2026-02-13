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


class ObjectiveTest(TestCase):

    def testUnknownIfRatingIsNotAvailable(self):
        feedback = self.mockFeedback(4.0, None, None, None)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.UNKNOWN)

    def testObjectiveAchieved(self):
        feedback = self.mockFeedback(4.0, 3.0, 5.0, 5.0)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.ACHIEVED)

    def testObjectiveFailedButStillImproved(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.3, 3.3)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testImprovedChangedCode(self):
        feedback = self.mockFeedback(3.4, 3.2, 3.3, 3.3)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testWorsenedChangedCode(self):
        feedback = self.mockFeedback(4.0, 3.0, 2.8, 2.8)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.WORSENED)

    def testChangedCodeTheSameQuality(self):
        feedback = self.mockFeedback(4.0, 3.0, 3.0, 3.0)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.UNCHANGED)

    def testNewCodeIsBetterButBelowObjectiveAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 3.0)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.IMPROVED)

    def testNewCodeIsWorseAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 1.9)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.WORSENED)

    def testNewCodeAchievesTargetAndNoChangedCode(self):
        feedback = self.mockFeedback(2.0, None, None, 4.5)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.ACHIEVED)

    def testUnknownIfOldRatingsAreNotAvailable(self):
        feedback = self.mockFeedback(None, None, None, 3.0)
        status = Objective.determineStatus(feedback, 3.5)
        self.assertEqual(status, ObjectiveStatus.UNKNOWN)

    def testCriticalObjectiveMeansEverythingisFine(self):
        self.assertTrue(Objective.meetsFindingObjective(["CRITICAL"], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["HIGH"], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["MEDIUM"], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["LOW"], "CRITICAL"))

    def testHighObjectiveMeansCriticalFindingsAreNotAllowed(self):
        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["HIGH"], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["MEDIUM"], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["LOW"], "HIGH"))

    def testMediumObjectiveMeansCriticalAndHighAreNotAllowed(self):
        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "MEDIUM"))
        self.assertFalse(Objective.meetsFindingObjective(["HIGH"], "MEDIUM"))
        self.assertTrue(Objective.meetsFindingObjective(["MEDIUM"], "MEDIUM"))
        self.assertTrue(Objective.meetsFindingObjective(["LOW"], "MEDIUM"))

    def testLowObjectiveStillAllowsLowSeverity(self):
        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "LOW"))
        self.assertFalse(Objective.meetsFindingObjective(["HIGH"], "LOW"))
        self.assertTrue(Objective.meetsFindingObjective(["LOW"], "LOW"))
        self.assertTrue(Objective.meetsFindingObjective(["NONE"], "LOW"))

    def testNoneObjectiveMeansNothingIsAllowed(self):
        self.assertFalse(Objective.meetsFindingObjective(["CRITICAL"], "NONE"))
        self.assertFalse(Objective.meetsFindingObjective(["HIGH"], "NONE"))
        self.assertFalse(Objective.meetsFindingObjective(["LOW"], "NONE"))
        self.assertTrue(Objective.meetsFindingObjective(["NONE"], "NONE"))

    def testDoNotCountUnknownSeverityAgainstObjective(self):
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "CRITICAL"))
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "HIGH"))
        self.assertTrue(Objective.meetsFindingObjective(["UNKNOWN"], "MEDIUM"))

    def testSeverityObjectiveLabel(self):
        self.assertEqual("any", Objective.getSeverityObjectiveLabel("CRITICAL"))
        self.assertEqual("no critical-severity", Objective.getSeverityObjectiveLabel("HIGH"))
        self.assertEqual("no high-severity", Objective.getSeverityObjectiveLabel("MEDIUM"))
        self.assertEqual("no medium-severity", Objective.getSeverityObjectiveLabel("LOW"))
        self.assertEqual("no", Objective.getSeverityObjectiveLabel("NONE"))

    def testSortBySeverity(self):
        values = ["CRITICAL", "LOW", "HIGH", "AAP"]
        values.sort(key=Objective.sortBySeverity)

        self.assertEqual(["CRITICAL", "HIGH", "LOW", "AAP"], values)

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

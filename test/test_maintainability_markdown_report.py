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

import inspect
import os
import tempfile
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport


class MaintainabilityMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", feedbackURL="")

    def testShowFindings(self):
        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("noot", "worsened", "UNIT_SIZE", "MODERATE"),
            self.toRefactoringCandidate("mies", "unchanged", "UNIT_COMPLEXITY", "VERY_HIGH")
        ]

        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.4},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 2.0},
            "refactoringCandidates": refactoringCandidates
        }

        report = MaintainabilityMarkdownReport({"MAINTAINABILITY" : 5.0})
        summary = report.getSummary(feedback, self.options)
        negative = list(report.getFindings(feedback, self.options))

        self.assertEqual(summary[0].text, "Your code did not improve towards your objective of 5.0 stars.")
        self.assertEqual(len(negative), 2)
        self.assertEqual(negative[0].title, "Unit Size (Introduced)")
        self.assertEqual(negative[1].title, "Unit Size (Worsened)")

    def testShowFixedRefactoringCandidatesInWhatWentWellSection(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates" : [
                self.toRefactoringCandidate("aap", "improved", "UNIT_SIZE", "HIGH"),
                self.toRefactoringCandidate("noot", "fixed", "UNIT_SIZE", "VERY_HIGH")
            ]
        }

        report = MaintainabilityMarkdownReport()
        negative = list(report.getFindings(feedback, self.options))
        positive = list(report.getPositiveFindings(feedback, self.options))

        self.assertEqual(len(negative), 0)
        self.assertEqual(len(positive), 2)
        self.assertEqual(positive[0].title, "Unit Size (Fixed)")
        self.assertEqual(positive[1].title, "Unit Size (Improved)")

    def testPositiveSummaryIfObjectiveMet(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 3.8},
            "newCodeRatings": {"MAINTAINABILITY": 4.1},
            "overallRatings": {"MAINTAINABILITY": 4.1}
        }

        report = MaintainabilityMarkdownReport()
        summary = report.getSummary(feedback, self.options)

        self.assertEqual(summary[0].text, "You wrote maintainable code and achieved your objective of 3.5 stars.")

    def testCautiouslyPositiveSummaryWhenMovingTowardsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.9},
            "newCodeRatings": {"MAINTAINABILITY": 2.9},
            "overallRatings": {"MAINTAINABILITY": 3.1}
        }

        report = MaintainabilityMarkdownReport()
        summary = report.getSummary(feedback, self.options)

        self.assertEqual(summary[0].text, "You improved your code towards your objective of 3.5 stars.")

    def testNegativeSummaryWhenNoImprovement(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"MAINTAINABILITY": 2.8},
            "overallRatings": {"MAINTAINABILITY": 3.0}
        }

        report = MaintainabilityMarkdownReport()
        summary = report.getSummary(feedback, self.options)

        self.assertEqual(summary[0].text, "Your code did not improve towards your objective of 3.5 stars.")

    def testSummaryPositiveIfCodeGotWorseButStillMeetsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 4.2},
            "newCodeRatings": {"MAINTAINABILITY": 3.9},
            "overallRatings": {"MAINTAINABILITY": 3.9}
        }

        report = MaintainabilityMarkdownReport()
        summary = report.getSummary(feedback, self.options)

        self.assertEqual(summary[0].text, "You wrote maintainable code and achieved your objective of 3.5 stars.")

    def testSpecialStatusIfNewCodeIsTheSameQuality(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "newCodeRatings": {"MAINTAINABILITY": 3.0},
            "overallRatings": {"MAINTAINABILITY": 3.0}
        }

        report = MaintainabilityMarkdownReport()
        summary = report.getSummary(feedback, self.options)

        self.assertEqual(summary[0].text, "You are still below your objective of 3.5 stars.")

    def toRefactoringCandidate(self, subject, category, metric, riskCategory):
        return {
            "subject" : subject,
            "category" : category,
            "metric" : metric,
            "riskCategory" : riskCategory
        }

    def toOccurrence(self, file, startLine, endLine):
        return {
            "filePath" : file,
            "startLine" : startLine,
            "endLine" : endLine
        }

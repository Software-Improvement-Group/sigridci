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
import tempfile
from unittest import TestCase

from sigridci.sigridci.markdown_report import MarkdownReport
from sigridci.sigridci.publish_options import PublishOptions, RunMode


class MarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", targetRating=3.5)

    def testMarkdown(self):
        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("noot", "worsened", "UNIT_SIZE", "MODERATE"),
            self.toRefactoringCandidate("mies", "unchanged", "UNIT_COMPLEXITY", "VERY_HIGH")
        ]

        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": refactoringCandidates
        }

        report = MarkdownReport()
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # Sigrid maintainability feedback
            
            **↗️  You improved your code's maintainability towards your Sigrid objective of 3.5 stars**
            
            Sigrid compared your code against the baseline of 2022-01-10.
            
            ## 👍 What went well?
            
            You fixed or improved **0** refactoring candidates.
            
            
            ## 👎 What could be better?
            
            Unfortunately, **2** refactoring candidates were introduced or got worse.
            
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🟠 | **Unit Size**<br />(Introduced) | aap |
            | 🟡 | **Unit Size**<br />(Worsened) | noot |
            
            
            ## 📚 Remaining technical debt
            
            **1** refactoring candidates didn't get any or worse, but are still in the code.
            
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Complexity**<br />(Unchanged) | mies |
            
            
            ## Sigrid ratings
            
            | System property | Baseline on 2022-01-10 | New/changed code |
            |-----------------|---------------------------------------------|------------------|
            | Volume | (N/A) | N/A |
            | Duplication | (4.0) | 5.0 |
            | Unit Size | (4.0) | 2.0 |
            | Unit Complexity | (N/A) | N/A |
            | Unit Interfacing | (N/A) | N/A |
            | Module Coupling | (N/A) | N/A |
            | Component Independence | (N/A) | N/A |
            | Component Entanglement | (N/A) | N/A |
            | **Maintainability** | **(4.0)** | **3.0** |
            
            ----
            
            - [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
            - [**View this Sigrid CI feedback in Sigrid**](https://sigrid-says.com/aap/noot/-/sigrid-ci/1234?targetRating=3.5)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    def testCustomOuputDirectory(self):
        tempDir = tempfile.mkdtemp()

        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("noot", "worsened", "UNIT_SIZE", "MODERATE"),
            self.toRefactoringCandidate("mies", "unchanged", "UNIT_COMPLEXITY", "VERY_HIGH")
        ]

        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": refactoringCandidates
        }

        report = MarkdownReport()
        report.outputDir = tempDir
        report.generate("1234", feedback, self.options)
        markdown = report.renderMarkdown("1234", feedback, self.options)

        with open(f"{tempDir}/feedback.md", "r") as f:
            contents = f.read()
        self.assertEqual(contents.strip(), markdown.strip())

    def testSortRefactoringCandidatesTableBySeverity(self):
        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("noot", "introduced", "UNIT_SIZE", "MODERATE"),
            self.toRefactoringCandidate("mies", "introduced", "UNIT_COMPLEXITY", "VERY_HIGH")
        ]

        report = MarkdownReport()
        table = report.renderRefactoringCandidatesTable(refactoringCandidates)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Complexity**<br />(Introduced) | mies |
            | 🟠 | **Unit Size**<br />(Introduced) | aap |
            | 🟡 | **Unit Size**<br />(Introduced) | noot |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    def testNoRefactoringCanidatesTableWhenNoRefactoringCandidates(self):
        report = MarkdownReport()
        table = report.renderRefactoringCandidatesTable([])

        self.assertEqual(table, "")

    def testAvoidSummaryIfNothingHappened(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : None},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"MAINTAINABILITY": 4.0}
        }

        report = MarkdownReport()
        summary = report.renderSummary(feedback, self.options)
        expected = "**🟰  You did not change any files that are measured by Sigrid**"

        self.assertEqual(summary, expected)

    def testPositiveSummaryIfObjectiveMet(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 3.8},
            "newCodeRatings": {"MAINTAINABILITY": 4.1},
            "overallRatings": {"MAINTAINABILITY": 4.1}
        }

        report = MarkdownReport()
        summary = report.renderSummary(feedback, self.options)
        expected = "**✅  You wrote maintainable code and achieved your Sigrid objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testCautiouslyPositiveSummaryWhenMovingTowardsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"MAINTAINABILITY": 2.9},
            "overallRatings": {"MAINTAINABILITY": 3.1}
        }

        report = MarkdownReport()
        summary = report.renderSummary(feedback, self.options)
        expected = "**↗️  You improved your code's maintainability towards your Sigrid objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testNegativeSummaryWhenNoImprovement(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"MAINTAINABILITY": 2.8},
            "overallRatings": {"MAINTAINABILITY": 3.0}
        }

        report = MarkdownReport()
        summary = report.renderSummary(feedback, self.options)
        expected = "**❌  Your code did not manage to improve towards your Sigrid objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testSummaryPositiveIfCodeGotWorseButStillMeetsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 4.2},
            "newCodeRatings": {"MAINTAINABILITY": 3.9},
            "overallRatings": {"MAINTAINABILITY": 3.9}
        }

        report = MarkdownReport()
        summary = report.renderSummary(feedback, self.options)
        expected = "**✅  You wrote maintainable code and achieved your Sigrid objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def toRefactoringCandidate(self, subject, category, metric, riskCategory):
        return {
            "subject" : subject,
            "category" : category,
            "metric" : metric,
            "riskCategory" : riskCategory
        }

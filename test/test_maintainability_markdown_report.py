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


class MarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", targetRating=3.5, feedbackURL="")

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
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
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": refactoringCandidates
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback
            
            **↗️  You improved the maintainability of the code towards your objective of 3.5 stars**
            
            Sigrid compared your code against the baseline of 2022-01-10.
            
            ## 👍 What went well?
            
            > You fixed or improved **0** refactoring candidates.
            
            
            ## 👎 What could be better?
            
            > Unfortunately, **2** refactoring candidates were introduced or got worse.
            
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🟠 | **Unit Size**<br />(Introduced) | aap |
            | 🟡 | **Unit Size**<br />(Worsened) | noot |
            
            
            ## 📚 Remaining technical debt
            
            > **1** refactoring candidates didn't get better or worse, but are still present in the code you touched.
            
            [View this system in Sigrid to explore your technical debt](https://sigrid-says.com/aap/noot)
            
            ## ⭐️ Sigrid ratings
            
            | System property | System on 2022-01-10 | Before changes | New/changed code |
            |-----------------|-------------------------------------------|----------------|------------------|
            | Volume | N/A | N/A | N/A |
            | Duplication | 4.0 | N/A | 5.0 |
            | Unit Size | 4.0 | N/A | 2.0 |
            | Unit Complexity | N/A | N/A | N/A |
            | Unit Interfacing | N/A | N/A | N/A |
            | Module Coupling | N/A | N/A | N/A |
            | Component Independence | N/A | N/A | N/A |
            | Component Entanglement | N/A | N/A | N/A |
            | **Maintainability** | **4.0** | **2.6** | **3.0** |
            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    def testCustomOuputDirectory(self):
        tempDir = tempfile.mkdtemp()
        self.options.outputDir = tempDir

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

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        report.generate("1234", feedback, self.options)
        markdown = report.renderMarkdown("1234", feedback, self.options)

        with open(f"{tempDir}/feedback.md", "r") as f:
            contents = f.read()
        self.assertEqual(contents.strip(), markdown.strip())

    def testSortRefactoringCandidatesTableBySeverity(self):
        feedback = {
            "refactoringCandidates" : [
                self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
                self.toRefactoringCandidate("noot", "introduced", "UNIT_SIZE", "MODERATE"),
                self.toRefactoringCandidate("mies", "introduced", "UNIT_COMPLEXITY", "VERY_HIGH")
            ]
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        table = report.renderRefactoringCandidatesTable(
            report.filterRefactoringCandidates(feedback, ["introduced"]), self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Complexity**<br />(Introduced) | mies |
            | 🟠 | **Unit Size**<br />(Introduced) | aap |
            | 🟡 | **Unit Size**<br />(Introduced) | noot |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    def testShowFixedRefactoringCandidatesInWhatWentWellSection(self):
        feedback = {
            "refactoringCandidates" : [
                self.toRefactoringCandidate("aap", "improved", "UNIT_SIZE", "HIGH"),
                self.toRefactoringCandidate("noot", "fixed", "UNIT_SIZE", "VERY_HIGH")
            ]
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderRefactoringCandidates(feedback, self.options)

        expected = """
            ## 👍 What went well?
    
            > You fixed or improved **2** refactoring candidates.
            
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Size**<br />(Fixed) | noot |
            | 🟠 | **Unit Size**<br />(Improved) | aap |
            
            
            ## 👎 What could be better?
            
            > You did not introduce any technical debt during your changes, great job!
            
            ## 📚 Remaining technical debt
            
            > **0** refactoring candidates didn't get better or worse, but are still present in the code you touched.
            
            [View this system in Sigrid to explore your technical debt](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    def testLimitRefactoringCandidatesTableWhenThereAreTooMany(self):
        findings = [self.toRefactoringCandidate(f"aap-{i}", "introduced", "UNIT_SIZE", "HIGH") for i in range(1, 100)]

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        table = report.renderRefactoringCandidatesTable(findings, self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🟠 | **Unit Size**<br />(Introduced) | aap-1 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-2 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-3 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-4 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-5 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-6 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-7 |
            | 🟠 | **Unit Size**<br />(Introduced) | aap-8 |
            | ⚫️ | | + 91 more |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    def testLimitDuplicatesWithTooManyOccurrences(self):
        rc = self.toRefactoringCandidate(f"aap", "introduced", "DUPLICATION", "VERY_HIGH")
        rc["occurrences"] = [self.toOccurrence(f"aap-{i}", i, i) for i in range(1, 10)]

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        table = report.renderRefactoringCandidatesTable([rc], self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Duplication**<br />(Introduced) | aap-1 line 1-1<br />aap-2 line 2-2<br />aap-3 line 3-3<br />+ 6 occurrences |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    def testNoRefactoringCanidatesTableWhenNoRefactoringCandidates(self):
        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        table = report.renderRefactoringCandidatesTable([], self.options)

        self.assertEqual(table, "")

    def testAvoidSummaryIfNothingHappened(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : None},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"MAINTAINABILITY": 4.0}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**💭️  You did not change any files that are measured by Sigrid**"

        self.assertEqual(summary, expected)

    def testPositiveSummaryIfObjectiveMet(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 3.8},
            "newCodeRatings": {"MAINTAINABILITY": 4.1},
            "overallRatings": {"MAINTAINABILITY": 4.1}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**✅  You wrote maintainable code and achieved your objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testCautiouslyPositiveSummaryWhenMovingTowardsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.9},
            "newCodeRatings": {"MAINTAINABILITY": 2.9},
            "overallRatings": {"MAINTAINABILITY": 3.1}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**↗️  You improved the maintainability of the code towards your objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testNegativeSummaryWhenNoImprovement(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"MAINTAINABILITY": 2.8},
            "overallRatings": {"MAINTAINABILITY": 3.0}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**⚠️  Your code did not improve maintainability towards your objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testSummaryPositiveIfCodeGotWorseButStillMeetsObjective(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 4.2},
            "newCodeRatings": {"MAINTAINABILITY": 3.9},
            "overallRatings": {"MAINTAINABILITY": 3.9}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**✅  You wrote maintainable code and achieved your objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    def testSpecialStatusIfNewCodeIsTheSameQuality(self):
        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "newCodeRatings": {"MAINTAINABILITY": 3.0},
            "overallRatings": {"MAINTAINABILITY": 3.0}
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        summary = report.renderSummary(feedback, self.options)
        expected = "**⏸️️  Your maintainability remains unchanged and is still below your objective of 3.5 stars**"

        self.assertEqual(summary, expected)

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testWordsOfEncouragementWhenNoBadRefactoringCandidates(self):
        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "improved", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("mies", "unchanged", "UNIT_COMPLEXITY", "VERY_HIGH")
        ]

        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 3.1},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 4.0},
            "newCodeRatings": {"MAINTAINABILITY": 4.0},
            "overallRatings": {"MAINTAINABILITY": 4.0},
            "refactoringCandidates": refactoringCandidates
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback

            **✅  You wrote maintainable code and achieved your objective of 3.5 stars**
            
            Sigrid compared your code against the baseline of 2022-01-10.
            
            ## 👍 What went well?
            
            > You fixed or improved **1** refactoring candidates.
            
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🟠 | **Unit Size**<br />(Improved) | aap |
            
            
            ## 👎 What could be better?
            
            > You did not introduce any technical debt during your changes, great job!
            
            ## 📚 Remaining technical debt
            
            > **1** refactoring candidates didn't get better or worse, but are still present in the code you touched.
            
            [View this system in Sigrid to explore your technical debt](https://sigrid-says.com/aap/noot)
            
            ## ⭐️ Sigrid ratings
            
            | System property | System on 2022-01-10 | Before changes | New/changed code |
            |-----------------|-------------------------------------------|----------------|------------------|
            | Volume | N/A | N/A | N/A |
            | Duplication | N/A | N/A | N/A |
            | Unit Size | N/A | N/A | N/A |
            | Unit Complexity | N/A | N/A | N/A |
            | Unit Interfacing | N/A | N/A | N/A |
            | Module Coupling | N/A | N/A | N/A |
            | Component Independence | N/A | N/A | N/A |
            | Component Entanglement | N/A | N/A | N/A |
            | **Maintainability** | **3.0** | **3.1** | **4.0** |
            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    def testKeepMarkdownSimpleIfThereAreNoCodeChanges(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : None},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"MAINTAINABILITY": None},
            "refactoringCandidates": []
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback
    
            **💭️  You did not change any files that are measured by Sigrid**

            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testDoNotShowAnyRefactoringCandidatesIfTheBaselineIsUnknown(self):
        refactoringCandidates = [
            self.toRefactoringCandidate("aap", "introduced", "UNIT_SIZE", "HIGH"),
            self.toRefactoringCandidate("noot", "introduced", "UNIT_COMPLEXITY", "HIGH")
        ]

        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"MAINTAINABILITY": None},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : None},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"MAINTAINABILITY": 3.0},
            "overallRatings": {"MAINTAINABILITY": 3.4},
            "refactoringCandidates": refactoringCandidates
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback

            **💭️  You did not change any files that are measured by Sigrid**

            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testIncludeFeedbackLinks(self):
        self.options.feedbackURL = "https://example.com"

        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.9},
            "newCodeRatings": {"MAINTAINABILITY": 2.8},
            "overallRatings": {"MAINTAINABILITY": 3.0},
            "refactoringCandidates": []
        }

        report = MaintainabilityMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback

            **⚠️  Your code did not improve maintainability towards your objective of 3.5 stars**
            
            Sigrid compared your code against the baseline of N/A.
            
            ## 👍 What went well?

            > You fixed or improved **0** refactoring candidates.
            
            
            ## 👎 What could be better?
            
            > You did not introduce any technical debt during your changes, great job!
            
            ## 📚 Remaining technical debt
            
            > **0** refactoring candidates didn't get better or worse, but are still present in the code you touched.
            
            [View this system in Sigrid to explore your technical debt](https://sigrid-says.com/aap/noot)
            
            ## ⭐️ Sigrid ratings
            
            | System property | System on N/A | Before changes | New/changed code |
            |-----------------|-------------------------------------------|----------------|------------------|
            | Volume | N/A | N/A | N/A |
            | Duplication | N/A | N/A | N/A |
            | Unit Size | N/A | N/A | N/A |
            | Unit Complexity | N/A | N/A | N/A |
            | Unit Interfacing | N/A | N/A | N/A |
            | Module Coupling | N/A | N/A | N/A |
            | Component Independence | N/A | N/A | N/A |
            | Component Entanglement | N/A | N/A | N/A |
            | **Maintainability** | **3.0** | **2.9** | **2.8** |
            
            ### 💬 Did you find this feedback helpful?
            
            We would like to know your thoughts to make Sigrid better.
            Your username will remain confidential throughout the process.
            
            - ✅ [Yes, these findings are useful](https://example.com?feature=sigridci.maintainability&feedback=useful&system=sig-aap-noot)
            - 🔸 [The findings are false positives](https://example.com?feature=sigridci.maintainability&feedback=falsepositive&system=sig-aap-noot)
            - 🔹 [These findings are not important to me](https://example.com?feature=sigridci.maintainability&feedback=unimportant&system=sig-aap-noot)
            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"GITLAB_CI" : "aap/noot"})
    def testUseHtmlMarkdownOnSupportedPlatforms(self):
        self.options.feedbackURL = "https://example.com"

        feedback = {
            "baselineRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.9},
            "newCodeRatings": {"MAINTAINABILITY": 2.8},
            "overallRatings": {"MAINTAINABILITY": 3.0},
            "refactoringCandidates": []
        }

        report = MaintainabilityMarkdownReport()
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback

            **⚠️  Your code did not improve maintainability towards your objective of 3.5 stars**
            
            <details><summary>Show details</summary>
            
            Sigrid compared your code against the baseline of N/A.
            
            ## 👍 What went well?

            > You fixed or improved **0** refactoring candidates.
            
            
            ## 👎 What could be better?
            
            > You did not introduce any technical debt during your changes, great job!
            
            ## 📚 Remaining technical debt
            
            > **0** refactoring candidates didn't get better or worse, but are still present in the code you touched.
            
            [View this system in Sigrid to explore your technical debt](https://sigrid-says.com/aap/noot)
            
            ## ⭐️ Sigrid ratings
            
            | System property | System on N/A | Before changes | New/changed code |
            |-----------------|-------------------------------------------|----------------|------------------|
            | Volume | N/A | N/A | N/A |
            | Duplication | N/A | N/A | N/A |
            | Unit Size | N/A | N/A | N/A |
            | Unit Complexity | N/A | N/A | N/A |
            | Unit Interfacing | N/A | N/A | N/A |
            | Module Coupling | N/A | N/A | N/A |
            | Component Independence | N/A | N/A | N/A |
            | Component Entanglement | N/A | N/A | N/A |
            | **Maintainability** | **3.0** | **2.9** | **2.8** |
            
            ### 💬 Did you find this feedback helpful?
            
            We would like to know your thoughts to make Sigrid better.
            Your username will remain confidential throughout the process.
            
            - ✅ [Yes, these findings are useful](https://example.com?feature=sigridci.maintainability&feedback=useful&system=sig-aap-noot)
            - 🔸 [The findings are false positives](https://example.com?feature=sigridci.maintainability&feedback=falsepositive&system=sig-aap-noot)
            - 🔹 [These findings are not important to me](https://example.com?feature=sigridci.maintainability&feedback=unimportant&system=sig-aap-noot)
            </details>
            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testDoNotIncludeFeedbackLinksIfNothingHappened(self):
        feedback = {
            "baselineRatings": {},
            "changedCodeBeforeRatings" : {},
            "newCodeRatings": {},
            "overallRatings": {},
            "refactoringCandidates": []
        }

        report = MaintainabilityMarkdownReport()
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot) maintainability feedback
            
            **💭️  You did not change any files that are measured by Sigrid**

            
            ----
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {
        "CI_SERVER_URL" : "https://example.com",
        "CI_PROJECT_PATH" : "aap/noot",
        "CI_COMMIT_REF_NAME" : "mybranch"
    })
    def testMakeLinksForDuplicationOccurrences(self):
        rc = self.toRefactoringCandidate(f"aap", "introduced", "DUPLICATION", "VERY_HIGH")
        rc["occurrences"] = [self.toOccurrence(f"aap-{i}", i, i) for i in range(1, 3)]

        report = MaintainabilityMarkdownReport()
        table = report.renderRefactoringCandidatesTable([rc], self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Duplication**<br />(Introduced) | [aap-1 line 1-1](https://example.com/aap/noot/-/blob/mybranch/aap-1#L1)<br />[aap-2 line 2-2](https://example.com/aap/noot/-/blob/mybranch/aap-2#L2) |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {
        "CI_SERVER_URL" : "https://example.com",
        "CI_PROJECT_PATH" : "aap/noot",
        "CI_COMMIT_REF_NAME" : "mybranch"
    })
    def testMakeLinksForUnitMetrics(self):
        rc = self.toRefactoringCandidate(f"aap.py::noot", "introduced", "UNIT_SIZE", "VERY_HIGH")
        rc["occurrences"] = [self.toOccurrence(f"aap.py", 0, 0)]

        report = MaintainabilityMarkdownReport()
        table = report.renderRefactoringCandidatesTable([rc], self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Size**<br />(Introduced) | [aap.py<br />noot](https://example.com/aap/noot/-/blob/mybranch/aap.py#L0) |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {
        "CI_SERVER_URL" : "https://example.com",
        "CI_PROJECT_PATH" : "aap/noot",
        "CI_COMMIT_REF_NAME" : "mybranch"
    })
    def testNormalizeLinksForSubsystems(self):
        rc = self.toRefactoringCandidate(f"boom/aap.py::noot", "introduced", "UNIT_SIZE", "VERY_HIGH")
        rc["occurrences"] = [self.toOccurrence(f"boom/aap.py", 0, 0)]

        self.options.subsystem = "boom"

        report = MaintainabilityMarkdownReport()
        table = report.renderRefactoringCandidatesTable([rc], self.options)

        expected = """
            | Risk | System property | Location |
            |------|-----------------|----------|
            | 🔴 | **Unit Size**<br />(Introduced) | [boom/aap.py<br />noot](https://example.com/aap/noot/-/blob/mybranch/aap.py#L0) |
        """

        self.assertEqual(table.strip(), inspect.cleandoc(expected).strip())

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

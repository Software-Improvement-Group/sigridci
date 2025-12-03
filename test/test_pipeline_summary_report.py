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
from io import StringIO
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.pipeline_summary_report import PipelineSummaryReport


class PipelineSummaryReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_AND_PUBLISH, "/tmp",
                                      sigridURL="https://example-sigrid.com")

    def testDisplayLandingPageFromClient(self):
        feedback = {
            "baseline": "20220110",
            "changedCodeBeforeRatings" : {},
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.2},
            "refactoringCandidates": []
        }

        buffer = StringIO()
        report = PipelineSummaryReport(MaintainabilityMarkdownReport(), output=buffer, ansiColors=False)
        report.generate("1234", feedback, self.options)

        expected = """
            ** ⚠️  Your code did not improve towards your objective of 3.5 stars. **
        """

        self.assertEqual(buffer.getvalue().strip().split("\n")[0], inspect.cleandoc(expected))

    def testSigridLinkIsLowercase(self):
        self.options.customer = "Aap"
        self.options.system = "NOOT"

        buffer = StringIO()
        report = PipelineSummaryReport(MaintainabilityMarkdownReport(), output=buffer, ansiColors=False)

        self.assertEqual(report.getSigridUrl(self.options), "https://example-sigrid.com/aap/noot")

    def testSpecialTextIfNoCodeChanged(self):
        feedback = {
            "baseline": "20220110",
            "changedCodeBeforeRatings" : {},
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": []
        }

        buffer = StringIO()
        report = PipelineSummaryReport(MaintainabilityMarkdownReport(), output=buffer, ansiColors=False)
        report.generate("1234", feedback, self.options)

        expected = """
            ** 💭️  You did not change any files that are measured by Sigrid. **
        """

        self.assertEqual(buffer.getvalue().strip().split("\n")[0], inspect.cleandoc(expected).strip())

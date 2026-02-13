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

import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.static_html_report import StaticHtmlReport


class StaticHtmlReportTest(TestCase):

    def testGenerateHTML(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": []
        }

        with TemporaryDirectory() as tempDir:
            options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
            report = StaticHtmlReport({"MAINTAINABILITY" : 3.5})
            report.generate("test", feedback, options)

            self.assertTrue(os.path.exists(f"{tempDir}/index.html"))

    def testFeedbackTemplateOnlyContainsAsciiCharacters(self):
        with open("sigridci/sigridci/reports/sigridci-feedback-template.html", mode="r", encoding="ascii") as f:
            f.read()

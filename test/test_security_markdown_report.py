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

import json
import os
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport


class SecurityMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            self.feedback = json.load(f)

    def testGetFindings(self):
        report = SecurityMarkdownReport(self.options, {})
        summary = report.getSummary(self.feedback, self.options)
        negative = list(report.getFindings(self.feedback, self.options))
        nonurgent = list(report.getNonUrgentFindings(self.feedback, self.options))
        positive = list(report.getPositiveFindings(self.feedback, self.options))

        self.assertEqual(summary[0].text, "You did not meet your objective of having no critical security findings.")
        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0].details, ["Puma4"])
        self.assertEqual(len(nonurgent), 1)
        self.assertEqual(nonurgent[0].details, ["Puma2"])
        self.assertEqual(len(positive), 1)
        self.assertEqual(positive[0].details, ["Insecure_Randomness"])

    def testSpecialMessageWhenYouMeetObjective(self):
        with open(os.path.dirname(__file__) + "/testdata/security-nofindings.json", encoding="utf-8", mode="r") as f:
            noResults = json.load(f)
            noResults["baseline"] = "2026-03-20 12:00"

        report = SecurityMarkdownReport(self.options, {})
        summary = report.getSummary(noResults, self.options)

        self.assertEqual(summary[0].text, "You achieved your objective of having no critical security findings.")

    def testIgnoreFailedRun(self):
        with open(os.path.dirname(__file__) + "/testdata/security-failed-run.json", encoding="utf-8", mode="r") as f:
            noResults = json.load(f)

        report = SecurityMarkdownReport(self.options, {})
        summary = report.getSummary(noResults, self.options)
        negative = list(report.getFindings(noResults, self.options))

        self.assertEqual(summary[0].text, "You achieved your objective of having no critical security findings.")
        self.assertEqual(len(negative), 0)

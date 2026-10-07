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
import json
import os
from unittest import TestCase, mock

from sigridci.sigridci.capability import Capability, ALL_CAPABILITIES, SECURITY
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport


class CombinedMarkdownFeedbackReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions(
            customer="aap",
            system="noot",
            runMode=RunMode.FEEDBACK_ONLY,
            sourceDir="/tmp",
            capabilities=ALL_CAPABILITIES
        )

        self.defaultObjectives = {
            "MAINTAINABILITY" : 4.0,
            "ARCHITECTURE_QUALITY" : 4.0,
            "OSH_MAX_SEVERITY" : "LOW",
            "SECURITY_MAX_SEVERITY" : "HIGH"
        }

        self.feedback = {}
        for capability in ALL_CAPABILITIES:
            with open(f"test/testdata/examplesystem/{capability.shortName}.json", "r", encoding="utf8") as f:
                self.feedback[capability] = json.load(f)


    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testGenerateMarkdown(self):
        report = CombinedMarkdownFeedbackReport(self.defaultObjectives)
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        with open("test/testdata/expected-combined-markdown-report.md", "r", encoding="utf8") as f:
            expected = f.read()

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    def testExcludeCapabilitiesNotInScope(self):
        self.options.capabilities = [SECURITY]
        report = CombinedMarkdownFeedbackReport(self.defaultObjectives)
        fragments = list(report.prepareFragments(self.options))

        self.assertEqual(len(fragments), 1)
        self.assertEqual(fragments[0].getCapability(), SECURITY)

    def testPositiveFindings(self):
        self.options.capabilities = [SECURITY]

        with open("test/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            securityFeedback = {SECURITY : json.load(f)}

        report = CombinedMarkdownFeedbackReport(self.defaultObjectives)
        negative = report.getFindings(securityFeedback, self.options)
        positive = report.getPositiveFindings(securityFeedback, self.options)

        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0].details, ["Puma4"])

        self.assertEqual(len(positive), 1)
        self.assertEqual(positive[0].details, ["Insecure_Randomness"])

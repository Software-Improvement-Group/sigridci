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

import contextlib
import io
import json
import os
import tempfile
from unittest import TestCase

from sigridci.sigridci.capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY
from sigridci.sigridci.feedback_provider import FeedbackProvider
from sigridci.sigridci.publish_options import PublishOptions, RunMode, Capability
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport


class FeedbackProviderTest(TestCase):

    def testGenerateReportsBasedOnCapability(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        options.capabilities = [OPEN_SOURCE_HEALTH]

        oshFeedback = FeedbackProvider("1234", options, {})
        oshFeedback.registerFeedback(OPEN_SOURCE_HEALTH, {"components" : [], "metadata" : {"timestamp" : "2025-09-29"}})
        oshFeedback.generateReports()

        self.assertTrue(os.path.exists(f"{tempDir}/feedback.md"))

    def testInlineResultsPrintsJsonInsteadOfWritingFiles(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir, inlineResults=True)
        options.capabilities = [OPEN_SOURCE_HEALTH]

        oshFeedback = FeedbackProvider("1234", options, {})
        oshFeedback.registerFeedback(OPEN_SOURCE_HEALTH, {"components": [], "metadata": {"timestamp": "2025-09-29"}})

        with contextlib.redirect_stdout(io.StringIO()) as output:
            exitCode = oshFeedback.generateReports()

        self.assertEqual(exitCode, 0)
        self.assertFalse(os.path.exists(f"{tempDir}/feedback.md"))
        self.assertEqual(os.listdir(tempDir), [])

        lines = output.getvalue().splitlines()
        self.assertEqual(2, len(lines))
        self.assertEqual("Inline results: osh", lines[0])
        self.assertEqual("osh", json.loads(lines[1])["capability"])

    def testApplyDefaultObjectives(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        feedbackProvider = FeedbackProvider("1234", options, {"MAINTAINABILITY" : 4.0})

        expected = {
            "MAINTAINABILITY" : 4.0,
            "ARCHITECTURE_QUALITY" : 3.5,
            "OSH_MAX_SEVERITY" : "HIGH",
            "SECURITY_MAX_SEVERITY" : "HIGH"
        }

        self.assertEqual(feedbackProvider.objectives, expected)

    def testGetSystemPropertyObjectives(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        objectives = {"MAINTAINABILITY_UNIT_SIZE" : 4.0}
        feedbackProvider = FeedbackProvider("1234", options, objectives)

        expected = {
            "MAINTAINABILITY_UNIT_SIZE" : 4.0,
            "ARCHITECTURE_QUALITY" : 3.5,
            "OSH_MAX_SEVERITY" : "HIGH",
            "SECURITY_MAX_SEVERITY" : "HIGH"
        }

        self.assertEqual(feedbackProvider.objectives, expected)

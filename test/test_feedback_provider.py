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
import tempfile
from unittest import TestCase, mock

from sigridci.sigridci.feedback_provider import FeedbackProvider, Capability
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport


class FeedbackProviderTest(TestCase):

    def testConfigureReportsForCapability(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)

        maintainabilityFeedback = FeedbackProvider(Capability.MAINTAINABILITY, options, {})
        oshFeedback = FeedbackProvider(Capability.OPEN_SOURCE_HEALTH, options, {})
        securityFeedback = FeedbackProvider(Capability.SECURITY, options, {})

        self.assertEqual(MaintainabilityMarkdownReport, type(maintainabilityFeedback.markdownReport))
        self.assertEqual(OpenSourceHealthMarkdownReport, type(oshFeedback.markdownReport))
        self.assertEqual(SecurityMarkdownReport, type(securityFeedback.markdownReport))

    def testGenerateReportsBasedOnCapability(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)

        oshFeedback = FeedbackProvider(Capability.OPEN_SOURCE_HEALTH, options, {})
        oshFeedback.analysisId = "1234"
        oshFeedback.feedback = {"dependencies" : []}
        oshFeedback.generateReports()

        self.assertTrue(os.path.exists(f"{tempDir}/osh-feedback.md"))
        self.assertFalse(os.path.exists(f"{tempDir}/security-feedback.md"))

        securityFeedback = FeedbackProvider(Capability.SECURITY, options, {})
        securityFeedback.analysisId = "1234"
        securityFeedback.feedback = {"runs" : []}
        securityFeedback.generateReports()

        self.assertTrue(os.path.exists(f"{tempDir}/security-feedback.md"))

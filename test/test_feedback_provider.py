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
from unittest import TestCase

from sigridci.sigridci.capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY
from sigridci.sigridci.feedback_provider import FeedbackProvider
from sigridci.sigridci.publish_options import PublishOptions, RunMode, Capability
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport


class FeedbackProviderTest(TestCase):

    def testConfigureReportsForCapability(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)

        maintainabilityFeedback = FeedbackProvider(MAINTAINABILITY, options, {})
        oshFeedback = FeedbackProvider(OPEN_SOURCE_HEALTH, options, {})
        securityFeedback = FeedbackProvider(SECURITY, options, {})

        self.assertEqual(MaintainabilityMarkdownReport, type(maintainabilityFeedback.prepareMarkdownReport()))
        self.assertEqual(OpenSourceHealthMarkdownReport, type(oshFeedback.prepareMarkdownReport()))
        self.assertEqual(SecurityMarkdownReport, type(securityFeedback.prepareMarkdownReport()))

    def testGenerateReportsBasedOnCapability(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)

        oshFeedback = FeedbackProvider(OPEN_SOURCE_HEALTH, options, {})
        oshFeedback.analysisId = "1234"
        oshFeedback.feedback = {"components" : [], "metadata" : {"timestamp" : "2025-09-29"}}
        oshFeedback.generateReports()

        self.assertTrue(os.path.exists(f"{tempDir}/osh-feedback.md"))
        self.assertFalse(os.path.exists(f"{tempDir}/security-feedback.md"))

        securityFeedback = FeedbackProvider(SECURITY, options, {})
        securityFeedback.analysisId = "1234"
        securityFeedback.feedback = {"runs" : []}
        securityFeedback.generateReports()

        self.assertTrue(os.path.exists(f"{tempDir}/security-feedback.md"))

    def testGetMaintainabilityObjective(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        feedbackProvider = FeedbackProvider(MAINTAINABILITY, options, {"MAINTAINABILITY" : 4.0})

        self.assertEqual({"MAINTAINABILITY" : 4.0}, feedbackProvider.objectives)

    def testGetSystemPropertyObjectives(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        objectives = {"MAINTAINABILITY_UNIT_SIZE" : 4.0, "UNIT_COMPLEXITY" : 5.0}
        feedbackProvider = FeedbackProvider(MAINTAINABILITY, options, objectives)

        self.assertEqual({"UNIT_SIZE" : 4.0, "UNIT_COMPLEXITY" : 5.0}, feedbackProvider.objectives)

    def testDefaultMaintainabilityObjectiveIfNoneIsSet(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        feedbackProvider = FeedbackProvider(MAINTAINABILITY, options, {})

        self.assertEqual({"MAINTAINABILITY" : 3.5}, feedbackProvider.objectives)

    def testSetDefaultOshVulnerabilityObjective(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        feedbackProvider = FeedbackProvider(OPEN_SOURCE_HEALTH, options, {})

        self.assertEqual({"OSH_MAX_SEVERITY" : "HIGH", "OSH_MAX_LICENSE_RISK" : None}, feedbackProvider.objectives)

    def testUseOshLicenseObjectiveIfAvailable(self):
        tempDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=tempDir)
        feedbackProvider = FeedbackProvider(OPEN_SOURCE_HEALTH, options, {"OSH_MAX_LICENSE_RISK" : "LOW"})

        self.assertEqual({"OSH_MAX_SEVERITY" : "HIGH", "OSH_MAX_LICENSE_RISK" : "LOW"}, feedbackProvider.objectives)

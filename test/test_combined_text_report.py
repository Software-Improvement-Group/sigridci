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
from io import StringIO
from unittest import TestCase, mock

from sigridci.sigridci.capability import Capability, ALL_CAPABILITIES
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from sigridci.sigridci.reports.combined_text_report import CombinedTextReport


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

    def testPrintAsciiArt(self):
        buffer = StringIO()
        report = CombinedTextReport(CombinedMarkdownFeedbackReport(self.defaultObjectives), buffer)
        report.generate("1234", self.feedback, self.options)

        expected = """
        """

        self.assertEqual(inspect.cleandoc(expected), buffer.getvalue().strip())

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
from sigridci.sigridci.reports.architecture_markdown_report import ArchitectureMarkdownReport


class ArchitectureMarkdownReportTest(TestCase):
    maxDiff = None

    def testFeedbackBasedOnArchitectureFindings(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/architecture.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        report = ArchitectureMarkdownReport()
        summary = report.getSummary(feedback, options)
        negative = list(report.getFindings(feedback, options))

        self.assertEqual(summary[0].text, "Your changes introduced architecture issues.")
        self.assertEqual(len(negative), 2)
        self.assertEqual(negative[0].title, "Undesirable dependency (Increased)")
        self.assertEqual(negative[1].title, "Cyclic dependency (Introduced)")

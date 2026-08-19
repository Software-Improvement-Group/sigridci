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
from io import StringIO
from unittest import TestCase

from sigridci.sigridci.analysisresults.sarif_processor import Finding, FindingStatus
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.architecture_markdown_report import ArchitectureMarkdownReport
from sigridci.sigridci.reports.architecture_text_report import ArchitectureTextReport


class ArchitectureTextReportTest(TestCase):

    def testPrintFindings(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/aap", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/architecture.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        buffer = StringIO()
        report = ArchitectureTextReport(ArchitectureMarkdownReport(), output=buffer)
        report.generate("1234", feedback, options)

        expected = """
            Architecture findings
            
                🔴 Undesirable dependency
                    Source: sigdelivery-aqci ▶ b/b.ts
                    Target: sigdelivery-aqci ▶ c/c.ts
            
                🟠 Cyclic dependency
                    Source: sigdelivery-aqci ▶ b/b.ts
                    Target: sigdelivery-aqci ▶ a/a.ts
        """

        self.assertEqual(inspect.cleandoc(expected), buffer.getvalue().strip())

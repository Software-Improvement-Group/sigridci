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

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.architecture_markdown_report import ArchitectureMarkdownReport


class ArchitectureMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testFeedbackBasedOnArchitectureFindings(self):
        with open(os.path.dirname(__file__) + "/testdata/architecture.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        report = ArchitectureMarkdownReport()
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/architecture-quality/explorer) Architecture feedback *(Beta)*

            **⚠️  You did not meet your objective of having no architecture issues**
            
            Sigrid compared your code against the baseline of 2026-08-17 12:00 UTC.
            
            ## 👎 What could be better?
            
            > Unfortunately, you introduced **2** architecture issues.
            
            | Issue | Location |
            |---|---|
            | **🔴 Undesirable dependency** • (Increased) | Source: sigdelivery-aqci▶ b.ts • Target: sigdelivery-aqci▶ c.ts |
            | **🟠 Cyclic dependency** • (Introduced) | Source: sigdelivery-aqci▶ b.ts • Target: sigdelivery-aqci▶ a.ts |
            
            If you believe these findings are false positives,
            you can [exclude the rule](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#manually-removing-architecture-dependencies) in the Sigrid configuration.
            ## 📚 You have remaining technical debt
            
            > You have **1** architecture issues.
            [You can view these findings in Sigrid](https://sigrid-says.com/aap/noot/-/architecture-quality/explorer).
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/architecture-quality/explorer)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

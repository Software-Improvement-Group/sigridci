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
from sigridci.sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport


class OpenSourceHealthMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/osh.json", encoding="utf-8", mode="r") as f:
            self.feedback = json.load(f)

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testIncludeFindingsBasedOnObjectives(self):
        report = OpenSourceHealthMarkdownReport("CRITICAL")
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You did not meet your objective of having no critical open source vulnerabilities**
            
            | Risk | Dependency | Description |
            |------|------------|-------------|
            | 🟣 | requirejs@2.3.2 | This is a test. |
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testSortFindingsBasedOnSeverity(self):
        report = OpenSourceHealthMarkdownReport("HIGH")
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You did not meet your objective of having no high open source vulnerabilities**
            
            | Risk | Dependency | Description |
            |------|------------|-------------|
            | 🟣 | requirejs@2.3.2 | This is a test. |
            | 🔴 | node-fetch@1.6.3 | Another test. |
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testSpecialMessageWhenYouMeetObjective(self):
        report = OpenSourceHealthMarkdownReport()
        feedback = {"dependencies": []}
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **✅  You achieved your objective of having no critical open source vulnerabilities**
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testLimitFeedbackWhenTooManyVulnerabilities(self):
        with open(os.path.dirname(__file__) + "/testdata/osh-manyfindings.json", encoding="utf-8", mode="r") as f:
            manyFindings = json.load(f)

        report = OpenSourceHealthMarkdownReport("HIGH")
        markdown = report.renderMarkdown("1234", manyFindings, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You did not meet your objective of having no high open source vulnerabilities**
            
            | Risk | Dependency | Description |
            |------|------------|-------------|
            | 🟣 | requirejs@2.3.2 | This is a test. |
            | 🟣 | requirejs-2@2.3.2 | This is a test. |
            | 🟣 | requirejs-3@2.3.2 | This is a test. |
            | 🟣 | requirejs-4@2.3.2 | This is a test. |
            | 🟣 | requirejs-5@2.3.2 | This is a test. |
            | 🟣 | requirejs-6@2.3.2 | This is a test. |
            | 🟣 | requirejs-7@2.3.2 | This is a test. |
            | 🟣 | requirejs-8@2.3.2 | This is a test. |
            | | ... and 2 more vulnerabilities | |
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

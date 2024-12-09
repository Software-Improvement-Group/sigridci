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
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport


class SecurityMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/security.json", encoding="utf-8", mode="r") as f:
            self.feedback = json.load(f)

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testCreateTableFromFindings(self):
        report = SecurityMarkdownReport()
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/security) Security feedback
            
            **⚠️  You did not meet your objective of having no critical security findings**
            
            | Risk | File | Finding |
            |------|------|---------|
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/security)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testSpecialMessageWhenYouMeetObjective(self):
        with open(os.path.dirname(__file__) + "/testdata/security-nofindings.json", encoding="utf-8", mode="r") as f:
            noResults = json.load(f)

        report = SecurityMarkdownReport()
        markdown = report.renderMarkdown("1234", noResults, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/security) Security feedback
            
            **✅  You achieved your objective of having no critical security findings**
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/security)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testLimitFindingsIfThereAreTooMany(self):
        with open(os.path.dirname(__file__) + "/testdata/security-manyfindings.json", encoding="utf-8", mode="r") as f:
            manyResults = json.load(f)

        report = SecurityMarkdownReport()
        markdown = report.renderMarkdown("1234", manyResults, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/security) Security feedback
            
            **⚠️  You did not meet your objective of having no critical security findings**
            
            | Risk | File | Finding |
            |------|------|---------|
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | ⚪️ | Security.java:33 | Weak Hash algorithm used |
            | | ... and 3 more findings | |
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/security)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

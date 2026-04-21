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
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport
from sigridci.sigridci.reports.security_text_report import SecurityTextReport


class SecurityTextReportTest(TestCase):

    def testPrintFindings(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/aap", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        buffer = StringIO()
        report = SecurityTextReport(SecurityMarkdownReport(options, "HIGH"), output=buffer)
        report.generate("1234", feedback, options)

        expected = """
            Security findings
            
                🟣 Puma4
                    In neutron/neutron/db/sqlalchemytypes.py (line 51)
        """

        self.assertEqual(inspect.cleandoc(expected), buffer.getvalue().strip())

    def testLimitFindingsIfThereAreTooMany(self):
        findings = [
            Finding("1", "CRITICAL", "1", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("2", "CRITICAL", "2", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("3", "CRITICAL", "3", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("4", "CRITICAL", "4", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("5", "HIGH", "5", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("6", "CRITICAL", "6", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("7", "CRITICAL", "7", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("8", "LOW", "8", "aap.py", 1, False, FindingStatus.INTRODUCED),
            Finding("9", "CRITICAL", "9", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("10", "CRITICAL", "10", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("11", "CRITICAL", "11", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("12", "HIGH", "12", "aap.py", 1, True, FindingStatus.INTRODUCED),
            Finding("13", "HIGH", "13", "aap.py", 1, True, FindingStatus.INTRODUCED)
        ]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/aap", feedbackURL="")
        buffer = StringIO()

        report = SecurityTextReport(SecurityMarkdownReport(options, "MEDIUM"), output=buffer)
        report.printFindings(findings)

        expected = """
                Security findings
                
                    🟣 1
                        In aap.py (line 1)
                    🟣 2
                        In aap.py (line 1)
                    🟣 3
                        In aap.py (line 1)
                    🟣 4
                        In aap.py (line 1)
                    🟣 6
                        In aap.py (line 1)
                    🟣 7
                        In aap.py (line 1)
                    🟣 9
                        In aap.py (line 1)
                    🟣 10
                        In aap.py (line 1)
                    🟣 11
                        In aap.py (line 1)
                    🔴 5
                        In aap.py (line 1)
                    ... and 2 more findings
            """

        self.assertEqual(inspect.cleandoc(expected), buffer.getvalue().strip())

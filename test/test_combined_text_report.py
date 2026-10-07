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
import re
from io import StringIO
from unittest import TestCase

from sigridci.sigridci.capability import Capability, ALL_CAPABILITIES
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from sigridci.sigridci.reports.combined_text_report import CombinedTextReport


class CombinedMarkdownFeedbackReportTest(TestCase):
    maxDiff = None

    ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

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
            ----------------------------------------------------------------------
            Sigrid objectives check
            ----------------------------------------------------------------------
            
            
            Failed checks
            
                - 🟣 Security: A07:2025 - Authentication Failures
                     Hard coded password
                     Location: Example2.java (line 5)
            
                - 🟠 Architecture: Cyclic dependency (Introduced)
                     Source: sigdelivery-sigrid-ci-example-dennis ▶ c.ts
                     Target: sigdelivery-sigrid-ci-example-dennis ▶ b.ts
                     Location: c.ts
            
                - 🟠 Open Source Health: `log4j-core` 2.17.0 contains known vulnerabilities.
                     Vulnerabilities:
                     [GHSA-6hg6-v5c8-fphq](https://nvd.nist.gov/vuln/detail/CVE-2026-34477)
                     [GHSA-vc5p-v9hr-52mj](https://nvd.nist.gov/vuln/detail/CVE-2025-68161)
                     [GHSA-8489-44mv-ggj8](https://nvd.nist.gov/vuln/detail/CVE-2021-44832)
                     [GHSA-3pxv-7cmr-fjr4](https://nvd.nist.gov/vuln/detail/CVE-2026-34480)
                     Location: build.gradle
            
                - 🔴 Maintainability: Duplication (Introduced)
                     74 duplicated lines across 2 occurences
                     Location: Example.java (line 41)
                     Location: Example2.java (line 39)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     57 duplicated lines across 2 occurences
                     Location: Example.java (line 177)
                     Location: Example2.java (line 162)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     49 duplicated lines across 2 occurences
                     Location: Example.java (line 246)
                     Location: Example2.java (line 237)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     40 duplicated lines across 2 occurences
                     Location: Example.java (line 131)
                     Location: Example2.java (line 110)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     17 duplicated lines across 2 occurences
                     Location: Example.java (line 3)
                     Location: Example2.java (line 15)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     390 duplicated lines across 27 occurences
                     Location: Example2.java (line 318)
                     Location: Example2.java (line 129)
                     Location: Example.java (line 150)
            
                - 🔴 Maintainability: Duplication (Introduced)
                     300 duplicated lines across 26 occurences
                     Location: Example2.java (line 318)
                     Location: Example2.java (line 129)
                     Location: Example.java (line 150)
            
                - ⚪️ ... and 54 more findings
            
            
            Sigrid objectives: ❌ Failed
            
            - ️⚠️️  **Maintainability** You are still below your objective of 4.0 stars.
            - ⚠️  **Architecture** Your changes introduced architecture issues.
            - ❌️ **Open Source Health** You have no medium-severity open source vulnerabilities.
            - ❌️ **Security** You did not meet your objective of having no 🟣 critical security findings.
            
            
            View this system in Sigrid:
                https://sigrid-says.com/aap/noot
        """

        self.assertEqual(inspect.cleandoc(expected), self.ANSI_PATTERN.sub("", buffer.getvalue().strip()))

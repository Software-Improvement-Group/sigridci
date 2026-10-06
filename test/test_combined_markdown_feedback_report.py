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

from sigridci.sigridci.capability import Capability, ALL_CAPABILITIES
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport


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


    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testGenerateMarkdown(self):
        report = CombinedMarkdownFeedbackReport(self.defaultObjectives)
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com) objectives check: ❌ Failed

            - ✅ **Maintainability** ⏸️️  You are still below your objective of 4.0 stars.
            - ✅ **Architecture** ⚠️  Your changes introduced architecture issues
            - ❌ **Open Source Health** ❌️  You failed to meet your objective of having no medium-severity open source vulnerabilities.
            - ❌ **Security** ⚠️  You did not meet your objective of having no 🟣 critical security findings
            
            #### Failed checks
            
            | Risk | Finding | Details | Location | Actions |
            |------|---------|---------|----------|---------|
            | 🟣 | **Security** • ??? | Hard coded password | Example2.java | [Exclude file](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-files-and-directories-from-security-scanning) • [Exclude rule](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-security-rules) |
            | 🟠 | **Architecture** • Cyclic dependency | ??? |  | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#manually-removing-architecture-dependencies) |
            | 🟠 | **Open Source Health** • org.apache.logging.log4j:log4j-core 2.17.0 contains known vulnerabilities | [GHSA-6hg6-v5c8-fphq](https://nvd.nist.gov/vuln/detail/CVE-2026-34477), [GHSA-vc5p-v9hr-52mj](https://nvd.nist.gov/vuln/detail/CVE-2025-68161), [GHSA-8489-44mv-ggj8](https://nvd.nist.gov/vuln/detail/CVE-2021-44832), [GHSA-3pxv-7cmr-fjr4](https://nvd.nist.gov/vuln/detail/CVE-2026-34480). | build.gradle | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks) |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | 🔴 | **Maintainability** • Duplication (Introduced) |  |  |  |
            | ⚪️ | ... and 54 more findings | | | |
            
            ----
    
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
            
            ![© Software Improvement Group](https://sigrid-says.com/usage/matomo.php?idsite=6&rec=1&ca=1&e_c=sigridci.feedbackview&e_a=sigridci.feedbackview&e_n=sig-aap-noot)
        """

        print("\n\n\n\n\n" + markdown + "\n\n\n\n\n")

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testPassQualityCheck(self):
        pass

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testPositiveFindings(self):
        pass

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testExcludeCapabilitiesNotInScope(self):
        pass

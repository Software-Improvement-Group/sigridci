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

        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            self.feedback = json.load(f)

        with open(os.path.dirname(__file__) + "/testdata/osh-junit-previous.json", encoding="utf-8", mode="r") as f:
            self.previousFeedback = json.load(f)

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testIncludeFindingsBasedOnObjectives(self):
        report = OpenSourceHealthMarkdownReport(self.options, "HIGH")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **❌️  You failed to meet your objective of having no critical-severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            - ❌ means the library has issues that fail your objective.
            - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
            - ✅ means everything is fine.
            
            If you believe these findings are false positives, you can
            [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
            
            ## 👎 What could be better?
            
            > You have **4** open source libraries with issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | org.apache.logging.log4j:log4j-core 2.14.1 • *CVE-2021-45046, CVE-2021-45105, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), CVE-2021-44832.* | 2.25.1 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | commons-io:commons-io 2.9.0 • *CVE-2024-47554.* | 2.20.0 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | io.github.classgraph:classgraph 4.8.106 • *(Transitive) CVE-2021-47621.* | 4.8.181 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | junit:junit  • *CVE-2020-15250.* | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testSortFindingsBasedOnSeverity(self):
        report = OpenSourceHealthMarkdownReport(self.options, "MEDIUM")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **❌️  You failed to meet your objective of having no high-severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            - ❌ means the library has issues that fail your objective.
            - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
            - ✅ means everything is fine.
            
            If you believe these findings are false positives, you can
            [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
            
            ## 👎 What could be better?
            
            > You have **4** open source libraries with issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | org.apache.logging.log4j:log4j-core 2.14.1 • *CVE-2021-45046, CVE-2021-45105, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), CVE-2021-44832.* | 2.25.1 | gradle/libs.versions.toml |
            | ❌ | ✅ | commons-io:commons-io 2.9.0 • *CVE-2024-47554.* | 2.20.0 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | io.github.classgraph:classgraph 4.8.106 • *(Transitive) CVE-2021-47621.* | 4.8.181 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | junit:junit  • *CVE-2020-15250.* | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testLimitFeedbackWhenTooManyVulnerabilities(self):
        report = OpenSourceHealthMarkdownReport(self.options, "LOW")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **❌️  You failed to meet your objective of having no medium-severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            - ❌ means the library has issues that fail your objective.
            - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
            - ✅ means everything is fine.
            
            If you believe these findings are false positives, you can
            [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
            
            ## 👎 What could be better?
            
            > You have **4** open source libraries with issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | org.apache.logging.log4j:log4j-core 2.14.1 • *CVE-2021-45046, CVE-2021-45105, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), CVE-2021-44832.* | 2.25.1 | gradle/libs.versions.toml |
            | ❌ | ✅ | commons-io:commons-io 2.9.0 • *CVE-2024-47554.* | 2.20.0 | gradle/libs.versions.toml |
            | ❌ | ✅ | io.github.classgraph:classgraph 4.8.106 • *(Transitive) CVE-2021-47621.* | 4.8.181 | gradle/libs.versions.toml |
            | ❌ | ✅ | junit:junit  • *CVE-2020-15250.* | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testShowUpdatedLibraries(self):
        report = OpenSourceHealthMarkdownReport(self.options, "MEDIUM")
        report.decorateLinks = False
        report.previousFeedback = self.previousFeedback
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **❌️  You failed to meet your objective of having no high-severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-18.
            
            - ❌ means the library has issues that fail your objective.
            - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
            - ✅ means everything is fine.
            
            If you believe these findings are false positives, you can
            [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
            
            ## 👍 What went well?
            
            > You updated **1** open source libraries that previously had issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | commons-io:commons-other 1.99 | 3.0 | gradle/libs.versions.toml |
            
            ## 👎 What could be better?
            
            > You have **4** open source libraries with issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | org.apache.logging.log4j:log4j-core 2.14.1 • *CVE-2021-45046, CVE-2021-45105, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), CVE-2021-44832.* | 2.25.1 | gradle/libs.versions.toml |
            | ❌ | ✅ | commons-io:commons-io 2.9.0 • *CVE-2024-47554.* | 2.20.0 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | io.github.classgraph:classgraph 4.8.106 • *(Transitive) CVE-2021-47621.* | 4.8.181 | gradle/libs.versions.toml |
            | ⚠️ | ✅ | junit:junit  • *CVE-2020-15250.* | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testShowLegalRiskIfObjectiveIsSet(self):
        report = OpenSourceHealthMarkdownReport(self.options, "CRITICAL", "LOW")
        report.decorateLinks = False
        report.previousFeedback = self.previousFeedback
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
        # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback

        **✅  You achieved your objective of having any open source vulnerabilities.**
        
        **❌  You failed to meet your objective of having no open source libraries with license issues.**
        
        Sigrid compared your code against the baseline of 2025-09-18.
        
        - ❌ means the library has issues that fail your objective.
        - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
        - ✅ means everything is fine.
        
        If you believe these findings are false positives, you can
        [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
        
        ## 👍 What went well?
        
        > You updated **1** open source libraries that previously had issues.
        
        | Vulnerabilities | License | Library | Latest version | Location(s) |
        |----|----|----|----|----|
        | ⚠️ | ✅ | commons-io:commons-other 1.99 | 3.0 | gradle/libs.versions.toml |
        
        ## 👎 What could be better?
        
        > You have **5** open source libraries with issues.
        
        | Vulnerabilities | License | Library | Latest version | Location(s) |
        |----|----|----|----|----|
        | ⚠️ | ✅ | org.apache.logging.log4j:log4j-core 2.14.1 • *CVE-2021-45046, CVE-2021-45105, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228), CVE-2021-44832.* | 2.25.1 | gradle/libs.versions.toml |
        | ⚠️ | ✅ | commons-io:commons-io 2.9.0 • *CVE-2024-47554.* | 2.20.0 | gradle/libs.versions.toml |
        | ⚠️ | ✅ | io.github.classgraph:classgraph 4.8.106 • *(Transitive) CVE-2021-47621.* | 4.8.181 | gradle/libs.versions.toml |
        | ⚠️ | ✅ | junit:junit  • *CVE-2020-15250.* | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
        | ✅ | ❌ | org.mockito:mockito-junit-jupiter 3.10.0 • *License: The MIT License.* | 5.19.0 | gradle/libs.versions.toml |
        
        
        ----
        
        [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testSpecialStatusIfThereAreNoLibraries(self):
        emptyFeedback = {
            "metadata": {
                "timestamp": "2026-02-03"
            },
            "components": []
        }

        report = OpenSourceHealthMarkdownReport(self.options, "CRITICAL", "LOW")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", emptyFeedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
    
            **💭  Sigrid did not find any open source libraries.**
            
            Sigrid compared your code against the baseline of 2026-02-03.
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testGreenCheckmarkIfThereAreLibrariesButNoFindings(self):
        emptyFeedback = {
            "metadata": {
                "timestamp": "2026-02-03"
            },
            "components": [
                {
                    "name": "platform-browser-dynamic",
                    "purl": "pkg:npm/%40angular/platform-browser-dynamic@21.0.9",
                    "type": "library",
                    "group": "@angular",
                    "bom-ref": "pkg:npm/%40angular/platform-browser-dynamic@21.0.9?package-id=d540fd8750e7344a",
                    "version": "21.0.9",
                    "evidence": {},
                    "licenses": [],
                    "properties": [
                        {
                            "name": "sigrid:risk:vulnerability",
                            "value": "NONE"
                        },
                        {
                            "name": "sigrid:risk:legal",
                            "value": "NONE"
                        }
                    ]
                }
            ]
        }

        report = OpenSourceHealthMarkdownReport(self.options, "CRITICAL", "LOW")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", emptyFeedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
    
            **✅  You achieved your objective of having any open source vulnerabilities.**

            **✅  You achieved your objective of having no open source libraries with license issues.**
            
            Sigrid compared your code against the baseline of 2026-02-03.
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testOnlyReportIssuesRelevantToSubSystem(self):
        self.options.subsystem = "aap"

        with open(os.path.dirname(__file__) + "/testdata/osh-subsystem.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        report = OpenSourceHealthMarkdownReport(self.options, "HIGH")
        report.decorateLinks = False
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback

            **❌️  You failed to meet your objective of having no critical-severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            - ❌ means the library has issues that fail your objective.
            - ⚠️ means the library has issues, but they are not severe enough to fail your objective.
            - ✅ means everything is fine.
            
            If you believe these findings are false positives, you can
            [exclude them in the Sigrid configuration](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks).
            
            ## 👎 What could be better?
            
            > You have **1** open source libraries with issues.
            
            | Vulnerabilities | License | Library | Latest version | Location(s) |
            |----|----|----|----|----|
            | ❌ | ✅ | org.example:example-aap 1.0 • *CVE-2026-12345.* | 3.0 | aap/build.gradle |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

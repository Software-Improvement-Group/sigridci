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
        report = OpenSourceHealthMarkdownReport("CRITICAL")
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You failed your objective of having no critical severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            ## 👎 What could be better?
            
            > You have **1** vulnerable open source libraries with a fix available.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🟣 | org.apache.logging.log4j:log4j-core 2.14.1 | 2.25.1 | gradle/libs.versions.toml |
            
            
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
            
            **⚠️  You failed your objective of having no high severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            ## 👎 What could be better?
            
            > You have **2** vulnerable open source libraries with a fix available.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🟣 | org.apache.logging.log4j:log4j-core 2.14.1 | 2.25.1 | gradle/libs.versions.toml |
            | 🔴 | commons-io:commons-io 2.9.0 | 2.20.0 | gradle/libs.versions.toml |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testLimitFeedbackWhenTooManyVulnerabilities(self):
        report = OpenSourceHealthMarkdownReport("LOW")
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You failed your objective of having no low severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-19.
            
            ## 👎 What could be better?
            
            > You have **21** vulnerable open source libraries with a fix available.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🟣 | org.apache.logging.log4j:log4j-core 2.14.1 | 2.25.1 | gradle/libs.versions.toml |
            | 🔴 | commons-io:commons-io 2.9.0 | 2.20.0 | gradle/libs.versions.toml |
            | 🟠 | io.github.classgraph:classgraph 4.8.106 | 4.8.181 | gradle/libs.versions.toml |
            | 🟠 | junit:junit  | 4.13.2 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            | 🟢 | org.codehaus.groovy:groovy-bom 2.5.14 | 3.0.25 | gradle/libs.versions.toml |
            | 🟢 | org.opentest4j:opentest4j 1.2.0 | 1.3.0 | gradle/libs.versions.toml |
            | 🟢 | org.openjdk.jmh:jmh-core 1.32 | 1.37 | gradle/libs.versions.toml |
            | 🟢 | org.apache.logging.log4j:log4j-jul 2.14.1 | 2.25.1 | gradle/libs.versions.toml |
            | | ... 13 more vulnerable open source libraries | |
            
            ## 😑 You have findings that you cannot address right now

            > You have **13** vulnerable open source libraries without a fix available.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🟢 | org.gradle:test-retry-gradle-plugin 1.2.1 |  | buildSrc/build.gradle.kts |
            | 🟢 | HH:mm ss.SSSZ |  | build.gradle.kts |
            | 🟢 | Xdoclint:none  |  | documentation/documentation.gradle.kts |
            | 🟢 | -Xlint:-overrides  |  | buildSrc/src/main/kotlin/java-library-conventions.gradle.kts |
            | 🟢 | gradle.plugin.com.github.jengelman.gradle.plugins:shadow 7.0.0 |  | buildSrc/build.gradle.kts |
            | 🟢 | com.univocity:univocity-parsers 2.9.1 | 2.9.1 | gradle/libs.versions.toml |
            | 🟢 | org.apache.servicemix.bundles:org.apache.servicemix.bundles.junit 4.13.2_1 | 4.13.2_1 | buildSrc/src/main/kotlin/junit4-compatibility.gradle.kts |
            | 🟢 | org.apiguardian:apiguardian-api 1.1.2 | 1.1.2 | gradle/libs.versions.toml |
            | | ... 5 more vulnerable open source libraries | |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

    @mock.patch.dict(os.environ, {"SIGRID_CI_MARKDOWN_HTML" : "false"})
    def testShowUpdatedLibraries(self):
        report = OpenSourceHealthMarkdownReport("HIGH")
        report.previousFeedback = self.previousFeedback
        markdown = report.renderMarkdown("1234", self.feedback, self.options)

        expected = """
            # [Sigrid](https://sigrid-says.com/aap/noot/-/open-source-health) Open Source Health feedback
            
            **⚠️  You failed your objective of having no high severity open source vulnerabilities.**
            
            Sigrid compared your code against the baseline of 2025-09-18.
            
            ## 👍 What went well?
            
            > You updated **1** vulnerable open source libraries.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🔴 | commons-io:commons-other 1.99 | 3.0 | gradle/libs.versions.toml |
            
            ## 👎 What could be better?
            
            > You have **2** vulnerable open source libraries with a fix available.
            
            | Risk | Library | Latest version | Location(s) |
            |----|----|----|----|
            | 🟣 | org.apache.logging.log4j:log4j-core 2.14.1 | 2.25.1 | gradle/libs.versions.toml |
            | 🔴 | commons-io:commons-io 2.9.0 | 2.20.0 | gradle/libs.versions.toml |
            
            
            ----
            
            [**View this system in Sigrid**](https://sigrid-says.com/aap/noot/-/open-source-health)
        """

        self.assertEqual(markdown.strip(), inspect.cleandoc(expected).strip())

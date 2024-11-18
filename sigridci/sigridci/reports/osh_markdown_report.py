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

import os

from .report import Report
from .security_markdown_report import SecurityMarkdownReport
from ..platform import Platform


class OpenSourceHealthMarkdownReport(Report):

    def generate(self, analysisId, feedback, options):
        with open(os.path.abspath(f"{options.outputDir}/osh-feedback.md"), "w", encoding="utf-8") as f:
            f.write(self.generateMarkdown(feedback, options))

    def generateMarkdown(self, feedback, options):
        md = f"# [Sigrid]({self.getSigridUrl(options)}) Open Source Health feedback\n\n"

        if Platform.isHtmlMarkdownSupported():
            md += "<details><summary>Show findings</summary>\n\n"

        md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"
        md += self.generateFindingsTable(feedback)

        if Platform.isHtmlMarkdownSupported():
            md += "</details>\n\n"

        md += "----\n"
        md += f"[**View this system in Sigrid**]({self.getSigridUrl(options)}/-/open-source-health)"
        return md

    def generateFindingsTable(self, feedback):
        md = "| Risk | Dependency | Description |\n"
        md += "|------|------------|-------------|\n"

        for dependency in feedback["dependencies"]:
            for vulnerability in dependency["vulnerabilities"]:
                symbol = SecurityMarkdownReport.SEVERITY_SYMBOLS[vulnerability["severity"]]
                name = f"{dependency['name']}@{dependency['currentVersion']}"
                description = vulnerability["description"]
                md += f"| {symbol} | {name} | {description} |\n"

        return md

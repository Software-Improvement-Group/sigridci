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
from ..platform import Platform


class SecurityMarkdownReport(Report):
    SEVERITY_SYMBOLS = {
        "CRITICAL" : "🟣",
        "HIGH" : "🔴",
        "MEDIUM" : "🟠",
        "LOW" : "🟡"
    }

    def generate(self, analysisId, feedback, options):
        with open(os.path.abspath(f"{options.outputDir}/security-feedback.md"), "w", encoding="utf-8") as f:
            f.write(self.generateMarkdown(feedback, options))

    def generateMarkdown(self, feedback, options):
        md = f"# [Sigrid]({self.getSigridUrl(options)}) Security feedback\n\n"

        if Platform.isHtmlMarkdownSupported():
            md += "<details><summary>Show findings</summary>\n\n"

        md += f"Sigrid compared your code against the baseline of {self.formatBaseline(feedback)}.\n\n"
        md += self.generateFindingsTable(feedback)

        if Platform.isHtmlMarkdownSupported():
            md += "</details>\n\n"

        md += "----\n"
        md += f"[**View this system in Sigrid**]({self.getSigridUrl(options)}/-/security)"
        return md

    def generateFindingsTable(self, feedback):
        md = "| Risk | File | Finding |\n"
        md += "|------|------|---------|\n"

        for finding in self.getRelevantFindings(feedback):
            symbol = "⚪️"
            file = finding["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
            line = finding["locations"][0]["physicalLocation"]["region"]["startLine"]
            description = finding["message"]["text"]
            md += f"| {symbol} | {file}:{line} | {description} |\n"

        return md

    def getRelevantFindings(self, feedback):
        for run in feedback["runs"]:
            for result in run["results"]:
                if "tags" in result["properties"] and len(result["properties"]["tags"]) > 0:
                    yield result
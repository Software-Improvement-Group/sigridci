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

import sys

from .architecture_markdown_report import ArchitectureMarkdownReport
from .report import Report


class ArchitectureTextReport(Report):
    def __init__(self, markdownReport, *, output=sys.stdout):
        self.output = output
        self.markdownReport = markdownReport

    def generate(self, analysisId, feedback, options):
        findings = self.markdownReport.getNegativeFeedback(feedback)
        displayedFindings = findings[0:options.getMaxShownFindings()]

        if len(displayedFindings) > 0:
            print("", file=self.output)
            print("Architecture findings", file=self.output)
            print("", file=self.output)
            for finding in displayedFindings:
                title = ArchitectureMarkdownReport.FINDING_TYPES.get(finding["qualification"], finding["qualification"])
                print(f"    {title}", file=self.output)
                print(f"        Source: {self.formatDependencyLocation(finding['sourceHierarchy'])}", file=self.output)
                print(f"        Target: {self.formatDependencyLocation(finding['targetHierarchy'])}", file=self.output)
                print("", file=self.output)
            if len(findings) > len(displayedFindings):
                print(f"    ... and {len(findings) - len(displayedFindings)} more findings", file=self.output)
                print("", file=self.output)

    def formatDependencyLocation(self, hierarchy):
        topLevelComponent = hierarchy[0]
        file = next((se for se in hierarchy if se["type"] == "FILE"), None)

        location = topLevelComponent["shortName"]
        if file:
            location += f" ▶ {file['name']}"
        return location

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

from .report import Report
from .security_markdown_report import SecurityMarkdownReport
from ..analysisresults.sarif_processor import SarifProcessor, FindingStatus
from ..objective import Objective


class SecurityTextReport(Report):
    MAX_SHOWN = 10

    def __init__(self, markdownReport, *, output=sys.stdout):
        self.output = output
        self.markdownReport = markdownReport
        self.objective = markdownReport.objective

    def generate(self, analysisId, feedback, options):
        allFindings = self.markdownReport.extractFindings(feedback)
        self.printFindings(allFindings)

    def printFindings(self, allFindings):
        processor = self.markdownReport.processor
        relevantFindings = processor.filterStatus(allFindings, FindingStatus.INTRODUCED, partOfObjective=True)
        displayedFindings = sorted(relevantFindings, key=lambda f: Objective.sortBySeverity(f.risk))[0:self.MAX_SHOWN]

        if len(displayedFindings) > 0:
            print("", file=self.output)
            print("Security findings", file=self.output)
            print("", file=self.output)
            for finding in displayedFindings:
                symbol = SecurityMarkdownReport.SEVERITY_SYMBOLS[finding.risk]
                print(f"    {symbol} {finding.description}", file=self.output)
                print(f"        In {finding.file} (line {finding.line})", file=self.output)
            if len(relevantFindings) > len(displayedFindings):
                print(f"    ... and {len(relevantFindings) - len(displayedFindings)} more findings", file=self.output)
            print("", file=self.output)

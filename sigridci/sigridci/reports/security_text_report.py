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
from ..analysisresults.findings_processor import FindingsProcessor


class SecurityTextReport(Report):

    def __init__(self, objective, *, output=sys.stdout):
        self.output = output
        self.objective = objective

    def generate(self, analysisId, feedback, options):
        processor = FindingsProcessor()
        allFindings = list(processor.extractFindings(feedback, self.objective))
        relevantFindings = [finding for finding in allFindings if finding.partOfObjective]

        if len(relevantFindings) > 0:
            print("", file=self.output)
            print("Security findings", file=self.output)
            print("", file=self.output)
            for finding in relevantFindings:
                symbol = SecurityMarkdownReport.SEVERITY_SYMBOLS[finding.risk]
                print(f"    {symbol} {finding.description}", file=self.output)
                print(f"        In {finding.file} (line {finding.line})", file=self.output)
            print("", file=self.output)

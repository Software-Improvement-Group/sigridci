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
from ..analysisresults.cyclonedx_processor import CycloneDXProcessor


class OpenSourceHealthTextReport(Report):

    def __init__(self, objective, *, output=sys.stdout):
        self.output = output
        self.objective = objective

    def generate(self, analysisId, feedback, options):
        processor = CycloneDXProcessor()
        findings = [lib for lib in processor.extractLibraries(feedback, self.objective) if not lib.meetsObjectives()]

        if len(findings) > 0:
            print("", file=self.output)
            print("Vulnerable open source libraries", file=self.output)
            print("", file=self.output)
            for finding in findings:
                symbol = SecurityMarkdownReport.SEVERITY_SYMBOLS[finding.vulnerabilityRisk.severity]
                print(f"    {symbol} {finding.name} {finding.version}", file=self.output)
                for file in finding.files:
                    print(f"        Defined in {file}", file=self.output)
            print("", file=self.output)

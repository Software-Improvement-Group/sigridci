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
from typing import TextIO

from .combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from .markdown_fragment import FeedbackFinding
from .report import Report
from ..publish_options import PublishOptions


class CombinedTextReport(Report):
    ANSI_GREEN = "\033[1m\033[92m"
    ANSI_YELLOW = "\033[1m\033[33m"
    ANSI_RED = "\033[1m\033[91m"
    ANSI_BLUE = "\033[1m\033[96m"
    ANSI_END = "\033[0m"

    def __init__(self, masterReport: CombinedMarkdownFeedbackReport, output: TextIO = sys.stdout):
        self.masterReport = masterReport
        self.output = output

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        print("", file=self.output)
        print(f"{self.ANSI_BLUE}{'-' * 70}{self.ANSI_END}", file=self.output)
        print(f"{self.ANSI_BLUE}Sigrid objectives check{self.ANSI_END}", file=self.output)
        print(f"{self.ANSI_BLUE}{'-' * 70}{self.ANSI_END}", file=self.output)
        print("", file=self.output)

        self.printFindingsList(feedback, options)
        self.printConclusion(feedback, options)

        print(f"{self.ANSI_BLUE}View this system in Sigrid:{self.ANSI_END}", file=self.output)
        print(f"    {self.getSigridUrl(options)}", file=self.output)
        print("", file=self.output)

    def printConclusion(self, feedback: dict, options: PublishOptions) -> None:
        success = self.masterReport.getExitCode(feedback, options) == 0
        conclusion = self.masterReport.renderConclusion(feedback, options)

        if success:
            print(f"{self.ANSI_GREEN}Sigrid objectives: {conclusion}{self.ANSI_END}", file=self.output)
        else:
            print(f"{self.ANSI_RED}Sigrid objectives: {conclusion}{self.ANSI_END}", file=self.output)
        print("", file=self.output)
        print(self.masterReport.renderObjectiveSummary(feedback, options), file=self.output)

    def printFindingsList(self, feedback: dict, options: PublishOptions) -> None:
        findings = self.masterReport.getFindings(feedback, options)

        if len(findings) > 0:
            print("", file=self.output)
            print(f"{self.ANSI_BLUE}Failed checks{self.ANSI_END}", file=self.output)
            print("", file=self.output)

            for finding in findings[0:options.getMaxShownFindings()]:
                self.printFinding(finding)

            remainder = len(findings) - options.getMaxShownFindings()
            if remainder > 0:
                print(f"    - ⚪️ ... and {remainder} more findings", file=self.output)

            print("", file=self.output)

    def printFinding(self, finding: FeedbackFinding) -> None:
        symbol = self.masterReport.renderSeverity(finding)
        capabilityName = finding.capability.displayName

        print(f"    - {symbol} {self.ANSI_BLUE}{capabilityName}:{self.ANSI_END} {finding.title}", file=self.output)
        for detailLine in finding.details:
            print(f"         {detailLine}", file=self.output)
        for location in finding.locations[0:3]:
            print(f"         Location: {self.masterReport.formatLocationLabel(location)}", file=self.output)
        print("", file=self.output)

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
from .report import Report
from ..publish_options import PublishOptions


class CombinedTextReport(Report):
    ANSI_GREEN = "\033[1m\033[92m"
    ANSI_YELLOW = "\033[1m\033[33m"
    ANSI_RED = "\033[1m\033[91m"
    ANSI_END = "\033[0m"

    def __init__(self, masterReport: CombinedMarkdownFeedbackReport, output: TextIO = sys.stdout):
        self.masterReport = masterReport
        self.output = output

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        success = self.masterReport.getExitCode(feedback, options) == 0
        conclusion = self.masterReport.renderConclusion(feedback, options)

        if success:
            print(f"{self.ANSI_GREEN}{conclusion}{self.ANSI_END}", file=self.output)
        else:
            print(f"{self.ANSI_RED}{conclusion}{self.ANSI_END}", file=self.output)
        print("", file=self.output)
        print(self.masterReport.renderObjectiveSummary(feedback, options), file=self.output)
        print("", file=self.output)

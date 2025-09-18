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

from .ascii_art_report import AsciiArtReport
from .maintainability_markdown_report import MaintainabilityMarkdownReport
from .report import Report
from ..objective import Objective, ObjectiveStatus
from ..publish_options import RunMode


class PipelineSummaryReport(Report):

    def __init__(self, markdownReport, *, output=sys.stdout, ansiColors=True):
        self.markdownReport = markdownReport
        self.output = output
        self.ansiColors = ansiColors

    def generate(self, analysisId, feedback, options):
        success = self.markdownReport.isObjectiveSuccess(feedback, options)

        print("", file=self.output)
        self.printConclusionMessage(feedback, options)
        self.printLandingPage(analysisId, options)

        # If you publish(only) we never break the build
        # We can break the build when running on a branch or pull request.
        if options.runMode == RunMode.FEEDBACK_ONLY and not success:
            sys.exit(1)

    def printConclusionMessage(self, feedback, options):
        success = self.markdownReport.isObjectiveSuccess(feedback, options)
        # Use the same summary text as what we use in the Markdown report.
        message = self.markdownReport.getSummary(feedback, options)

        asciiArt = AsciiArtReport(self.output, self.ansiColors)
        color = asciiArt.ANSI_GREEN if success else asciiArt.ANSI_YELLOW
        asciiArt.printColor(f"** {message} **", asciiArt.ANSI_BOLD + color)

    def printLandingPage(self, analysisId, options):
        landingPage = self.getSigridUrl(options)

        print("", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("View this system in Sigrid:", file=self.output)
        print(f"    {landingPage}", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("", file=self.output)

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
from .report import Report
from ..objective import Objective, ObjectiveStatus
from ..publish_options import RunMode


class PipelineSummaryReport(Report):

    def __init__(self, output=sys.stdout, ansiColors=True):
        self.output = output
        self.ansiColors = ansiColors

    def generate(self, analysisId, feedback, options):
        status = Objective.determineStatus(feedback, options)

        print("", file=self.output)
        self.printConclusionMessage(feedback, options, status)
        self.printLandingPage(analysisId, options)

        # If you publish(only) we never break the build
        # We can break the build when running on a branch or pull request.
        if options.runMode == RunMode.FEEDBACK_ONLY and status == ObjectiveStatus.WORSENED:
            sys.exit(1)

    def printConclusionMessage(self, feedback, options, status):
        message = self.getSummaryText(feedback, options)

        asciiArt = AsciiArtReport(self.output, self.ansiColors)
        color = asciiArt.ANSI_YELLOW if status == ObjectiveStatus.WORSENED else asciiArt.ANSI_GREEN
        asciiArt.printColor(f"** {message} **", asciiArt.ANSI_BOLD + color)

    def printLandingPage(self, analysisId, options):
        landingPage = self.getSigridUrl(options)

        print("", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("View this system in Sigrid:", file=self.output)
        print(f"    {landingPage}", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("", file=self.output)

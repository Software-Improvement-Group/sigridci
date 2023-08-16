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
from .publish_options import RunMode
from .report import Report


class PipelineSummaryReport(Report):
    MESSAGE_NA = "\n** SIGRID CI RUN COMPLETE: NO FILES CONSIDERED FOR MAINTAINABILITY WERE CHANGED **\n"
    MESSAGE_PASS = "\n** SIGRID CI RUN COMPLETE: YOU WROTE MAINTAINABLE CODE AND REACHED THE TARGET **\n"
    MESSAGE_FAIL = "\n** SIGRID CI RUN COMPLETE: THE CODE YOU WROTE DID NOT MEET THE TARGET FOR MAINTAINABLE CODE **\n"

    def __init__(self, output=sys.stdout, ansiColors=True):
        super().__init__()
        self.output = output
        self.ansiColors = ansiColors

    def generate(self, analysisId, feedback, options):
        self.printConclusionMessage(feedback, options)
        self.printLandingPage(analysisId, options)
        # If you publish(only) we never break the build
        # We can break the build when running on a branch or pull request.
        if options.runMode == RunMode.FEEDBACK_ONLY and not self.meetsObjectives(feedback, options):
            sys.exit(1)

    def printConclusionMessage(self, feedback, options):
        asciiArt = AsciiArtReport(self.output, self.ansiColors)

        if not self.isFeedbackAvailable(feedback):
            asciiArt.printColor(self.MESSAGE_NA, asciiArt.ANSI_BOLD + asciiArt.ANSI_BLUE)
        elif self.meetsObjectives(feedback, options):
            asciiArt.printColor(self.MESSAGE_PASS, asciiArt.ANSI_BOLD + asciiArt.ANSI_GREEN)
        else:
            asciiArt.printColor(self.MESSAGE_FAIL, asciiArt.ANSI_BOLD + asciiArt.ANSI_YELLOW)

    def printLandingPage(self, analysisId, options):
        landingPage = self.getLandingPage(analysisId, options)
        if analysisId == "":
            landingPage = self.getSigridUrl(options)

        print("", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("View your analysis results in Sigrid:", file=self.output)
        print(f"    {landingPage}", file=self.output)
        print("-" * (len(landingPage) + 4), file=self.output)
        print("", file=self.output)

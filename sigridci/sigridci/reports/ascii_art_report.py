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


class AsciiArtReport(Report):
    ANSI_BOLD = "\033[1m"
    ANSI_GREEN = "\033[92m"
    ANSI_YELLOW = "\033[33m"
    ANSI_RED = "\033[91m"
    ANSI_BLUE = "\033[96m"
    LINE_WIDTH = 80

    def __init__(self, output=sys.stdout, ansiColors=True):
        self.output = output
        self.ansiColors = ansiColors

    def generate(self, analysisId, feedback, options):
        self.printHeader("Refactoring candidates")
        for metric in self.REFACTORING_CANDIDATE_METRICS:
            self.printMetric(feedback, metric)

        self.printRatingsTable(feedback)

    def printRatingsTable(self, feedback):
        self.printHeader("Maintainability ratings")

        self.printTableRow(
            "System property",
            f"System on {self.formatBaseline(feedback)}",
            "Before changes",
            "New/changed code"
        )

        for metric in self.METRICS:
            if metric == "MAINTAINABILITY":
                self.printSeparator()

            self.printTableRow(
                self.formatMetricName(metric),
                self.formatRating(feedback["baselineRatings"], metric),
                self.formatRating(feedback["changedCodeBeforeRatings"], metric),
                self.formatRating(feedback["newCodeRatings"], metric)
            )

    def printTableRow(self, *row):
        formattedRow = "%-25s%-22s%-17s%-22s" % tuple(row)
        print(formattedRow, file=self.output)

    def printHeader(self, header):
        print("", file=self.output)
        self.printSeparator()
        print(header, file=self.output)
        self.printSeparator()

    def printSeparator(self):
        print("-" * self.LINE_WIDTH, file=self.output)

    def printMetric(self, feedback, metric):
        print("", file=self.output)
        print(self.formatMetricName(metric), file=self.output)

        refactoringCandidates = self.getRefactoringCandidates(feedback, metric)
        if len(refactoringCandidates) == 0:
            print("    None", file=self.output)
        else:
            for rc in refactoringCandidates:
                print(self.formatRefactoringCandidate(rc), file=self.output)

    def formatRefactoringCandidate(self, rc):
        category = ("(" + rc["category"] + ")").ljust(14)
        subject = rc["subject"].replace("\n", "\n" + (" " * 21)).replace("::", "\n" + (" " * 21))
        return f"    - {category} {subject}"

    def printColor(self, message, ansiPrefix):
        if self.ansiColors:
            print(ansiPrefix + message + "\033[0m", file=self.output)
        else:
            print(message, file=self.output)

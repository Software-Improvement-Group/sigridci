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
    LINE_WIDTH = 79

    def __init__(self, output=sys.stdout, ansiColors=True):
        self.output = output
        self.ansiColors = ansiColors

    def generate(self, analysisId, feedback, options):
        self.printHeader("What went well?")
        self.printRefactoringCandidates(self.filterRefactoringCandidates(feedback, self.GOOD_CATEGORIES))

        self.printHeader("What could be better?")
        self.printRefactoringCandidates(self.filterRefactoringCandidates(feedback, self.BAD_CATEGORIES))

        self.printHeader("Remaining technical debt")
        unchanged = self.filterRefactoringCandidates(feedback, self.UNCHANGED_CATEGORIES)
        print(f"{len(unchanged)} refactoring candidates didn't get better or worse.", file=self.output)
        print("", file=self.output)

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
        formattedRow = "%-25s%-22s%-16s%-16s" % tuple(row)
        print(formattedRow, file=self.output)

    def printHeader(self, header):
        self.printSeparator()
        print(header, file=self.output)
        self.printSeparator()
        print("", file=self.output)

    def printSeparator(self):
        print("-" * self.LINE_WIDTH, file=self.output)

    def printRefactoringCandidates(self, refactoringCandidates):
        if len(refactoringCandidates) == 0:
            print("There are no refactoring candidates.", file=self.output)
            print("", file=self.output)
            return

        for rc in refactoringCandidates:
            print(self.formatRefactoringCandidate(rc), file=self.output)
            print("", file=self.output)

    def formatRefactoringCandidate(self, rc):
        title = f"{self.formatMetricName(rc['metric'])} ({rc['category']})"
        subject = rc["subject"].replace("\n", "\n  ").replace("::", "\n  ")
        return f"{title}\n  {subject}"

    def printColor(self, message, ansiPrefix):
        if self.ansiColors:
            print(ansiPrefix + message + "\033[0m", file=self.output)
        else:
            print(message, file=self.output)

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

from xml.dom.minidom import Document

from .objective import Objective, ObjectiveStatus
from .report import Report


class JUnitFormatReport(Report):

    def generate(self, analysisId, feedback, options):
        with open(f"{self.outputDir}/sigridci-junit-format-report.xml", "w") as fileRef:
            fileRef.write(self.generateXML(feedback, options))

    def generateXML(self, feedback, options):
        dom = Document()
        testSuite = dom.createElement("testsuite")
        testSuite.setAttribute("name", "Sigrid CI")
        dom.appendChild(testSuite)

        testCase = dom.createElement("testcase")
        testCase.setAttribute("classname", "Sigrid CI")
        testCase.setAttribute("name", "Maintainability")
        testSuite.appendChild(testCase)

        failures = self.getFailures(feedback, options)
        if len(failures) > 0:
            failure = dom.createElement("failure")
            failure.appendChild(dom.createTextNode("Refactoring candidates:\n\n" + "\n".join(failures)))
            testCase.appendChild(failure)

        return dom.toprettyxml(indent="    ")

    def getFailures(self, feedback, options):
        status = Objective.determineStatus(feedback, options)
        failures = []

        if status == ObjectiveStatus.STAGNANT:
            for metric in self.REFACTORING_CANDIDATE_METRICS:
                failures += [self.formatFinding(rc) for rc in self.getRefactoringCandidates(feedback, metric)]

        return failures

    def formatFinding(self, rc):
        return f"- {rc['subject']}\n  ({self.formatMetricName(rc['metric'])}, {rc['category']})"

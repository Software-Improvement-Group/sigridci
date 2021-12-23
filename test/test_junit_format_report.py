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

import os
import tempfile
import unittest
from sigridci.sigridci import JUnitFormatReport, TargetQuality


class JUnitReportTest(unittest.TestCase):
    maxDiff = None

    def testCreateXmlFileInJUnitFormat(self):
        tempDir = tempfile.mkdtemp()
        
        feedback = {
            "newCodeRatings": {
                "MAINTAINABILITY" : 2.0,
                "DUPLICATION" : 2.0,
                "UNIT_SIZE" : 4.0,
                "UNIT_COMPLEXITY" : 3.0
            },
            "refactoringCandidates": [
                { "subject" : "Aap.java", "metric" : "DUPLICATION", "category" : "introduced" },
                { "subject" : "Noot.java", "metric" : "UNIT_COMPLEXITY", "category" : "introduced" },
                { "subject" : "Mies.java", "metric" : "UNIT_COMPLEXITY", "category" : "unchanged" }
            ]
        }
        
        target = TargetQuality(f"{tempDir}/sigrid.yaml", 3.5)
        target.ratings["DUPLICATION"] = 2.0
    
        report = JUnitFormatReport()
        report.generate(feedback, None, target)
        
        with open("sigrid-ci-output/sigridci-junit-format-report.xml", "r") as f:
            reportContents = f.read()
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI" tests="5" errors="0" failures="1">
                <testcase name="Duplication"/>
                <testcase name="Unit Size"/>
                <testcase name="Unit Complexity">
                    <failure>Refactoring candidates:
                    
- Noot.java (introduced)
- Mies.java (unchanged)</failure>
                </testcase>
                <testcase name="Unit Interfacing"/>
                <testcase name="Module Coupling"/>
            </testsuite>
        """
        
        self.assertEqual(reportContents.strip().replace("    ", ""), expected.strip().replace("    ", ""))
        
    def testDoNotMarkAnyTestCasesFailedIfOverallRatingIsOK(self):
        tempDir = tempfile.mkdtemp()
        
        feedback = {
            "newCodeRatings": {
                "MAINTAINABILITY" : 4.0,
                "DUPLICATION" : 2.0
            }
        }
        
        report = JUnitFormatReport()
        report.generate(feedback, None, TargetQuality(f"{tempDir}/sigrid.yaml", 3.5))
        
        with open("sigrid-ci-output/sigridci-junit-format-report.xml", "r") as f:
            reportContents = f.read()
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI" tests="5" errors="0" failures="0">
                <testcase name="Duplication"/>
                <testcase name="Unit Size"/>
                <testcase name="Unit Complexity"/>
                <testcase name="Unit Interfacing"/>
                <testcase name="Module Coupling"/>
            </testsuite>
        """
        
        self.assertEqual(reportContents.strip().replace("    ", ""), expected.strip().replace("    ", ""))

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
    
        report = JUnitFormatReport()
        xml = report.generateXML(feedback, target)
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI">
                <testcase classname="Sigrid CI" name="Maintainability">
                    <failure>Refactoring candidates:
                    
- Aap.java
  (Duplication, introduced)
- Noot.java
  (Unit Complexity, introduced)
- Mies.java
  (Unit Complexity, unchanged)</failure>
                </testcase>
            </testsuite>
        """
        
        self.assertEqual(xml.strip().replace("    ", ""), expected.strip().replace("    ", ""))
        
    def testDoNotMarkAnyTestCasesFailedIfOverallRatingIsOK(self):
        tempDir = tempfile.mkdtemp()
        
        feedback = {
            "newCodeRatings": {
                "MAINTAINABILITY" : 4.0,
                "DUPLICATION" : 2.0
            }
        }
        
        report = JUnitFormatReport()
        xml = report.generateXML(feedback, TargetQuality(f"{tempDir}/sigrid.yaml", 3.5))
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI">
                <testcase classname="Sigrid CI" name="Maintainability"/>
            </testsuite>
        """
        
        self.assertEqual(xml.strip().replace("    ", ""), expected.strip().replace("    ", ""))
        
    def testOnlyReportRelevantSystemPropertiesIfMetricSpecificTargetsAreUsed(self):
        tempDir = tempfile.mkdtemp()
        
        target = TargetQuality(f"{tempDir}/sigrid.yaml", 3.5)
        target.ratings["UNIT_COMPLEXITY"] = 5.0
        
        feedback = {
            "newCodeRatings": {
                "MAINTAINABILITY" : 4.0,
                "UNIT_SIZE" : 4.0,
                "UNIT_COMPLEXITY" : 4.0
            },
            "refactoringCandidates": [
                { "subject" : "Aap.java", "metric" : "UNIT_SIZE", "category" : "introduced" },
                { "subject" : "Noot.java", "metric" : "UNIT_COMPLEXITY", "category" : "introduced" }
            ]
        }
        
        report = JUnitFormatReport()
        xml = report.generateXML(feedback, target)
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI">
                <testcase classname="Sigrid CI" name="Maintainability">
                    <failure>Refactoring candidates:
                    
- Noot.java
  (Unit Complexity, introduced)</failure>
                </testcase>
            </testsuite>
        """
        
        self.assertEqual(xml.strip().replace("    ", ""), expected.strip().replace("    ", ""))

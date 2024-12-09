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

from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.junit_format_report import JUnitFormatReport


class JUnitReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", targetRating=3.5)

    def testCreateXmlFileInJUnitFormat(self):
        feedback = {
            "baselineRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "changedCodeBeforeRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "newCodeRatings": {
                "MAINTAINABILITY" : 1.2,
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
        
        report = JUnitFormatReport()
        xml = report.generateXML(feedback, self.options)
            
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
        feedback = {
            "baselineRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "changedCodeBeforeRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "newCodeRatings": {
                "MAINTAINABILITY" : 4.0,
                "DUPLICATION" : 2.0
            }
        }
        
        report = JUnitFormatReport()
        xml = report.generateXML(feedback, self.options)
            
        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI">
                <testcase classname="Sigrid CI" name="Maintainability"/>
            </testsuite>
        """
        
        self.assertEqual(xml.strip().replace("    ", ""), expected.strip().replace("    ", ""))

    def testReportAllSystemPropertiesIfMaintainabilityFailsEvenIfMetricSpecificTargetsFail(self):
        feedback = {
            "baselineRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "changedCodeBeforeRatings": {
                "MAINTAINABILITY": 1.6,
            },
            "newCodeRatings": {
                "MAINTAINABILITY" : 1.3,
                "UNIT_SIZE" : 4.0,
                "UNIT_COMPLEXITY" : 4.0
            },
            "refactoringCandidates": [
                {"subject" : "Aap.java", "metric" : "UNIT_SIZE", "category" : "introduced"},
                {"subject" : "Noot.java", "metric" : "UNIT_COMPLEXITY", "category" : "introduced"}
            ]
        }

        report = JUnitFormatReport()
        xml = report.generateXML(feedback, self.options)

        expected = """
            <?xml version="1.0" ?>
            <testsuite name="Sigrid CI">
                <testcase classname="Sigrid CI" name="Maintainability">
                    <failure>Refactoring candidates:
                    
- Aap.java
  (Unit Size, introduced)
- Noot.java
  (Unit Complexity, introduced)</failure>
                </testcase>
            </testsuite>
        """

        self.assertEqual(xml.strip().replace("    ", ""), expected.strip().replace("    ", ""))

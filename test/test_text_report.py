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

import io
import os
import types
import unittest
from sigridci.sigridci import Report, TextReport, TargetQuality


class TextReportTest(unittest.TestCase):

    maxDiff = None

    def testFormatTextRefactoringCandidate(self):
        rc1 = {"subject" : "aap", "category" : "introduced", "metric" : "UNIT_SIZE"}
        rc2 = {"subject" : "noot\nmies", "category" : "worsened", "metric" : "DUPLICATION"}
        rc3 = {"subject" : "noot::mies", "category" : "worsened", "metric" : "UNIT_SIZE"}
        
        report = TextReport()
        
        self.assertEqual(report.formatRefactoringCandidate(rc1), "    - (introduced)   aap")
        self.assertEqual(report.formatRefactoringCandidate(rc2), "    - (worsened)     noot\n                     mies")
        self.assertEqual(report.formatRefactoringCandidate(rc3), "    - (worsened)     noot\n                     mies")

    def testPrintRegularReport(self):
        feedback = {
            "baseine": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": [{"subject":"a.py::aap()", "category":"introduced", "metric":"UNIT_SIZE"}]
        }
    
        target = TargetQuality("/tmp/nonexistent", 3.5)
    
        buffer = io.StringIO()
        report = TextReport(buffer)
        report.generate(feedback, types.SimpleNamespace(publish=False), target)
        
        expected = """
-----------------------------------------------------------------------------------------
Refactoring candidates
-----------------------------------------------------------------------------------------

Duplication
    None

Unit Size
    - (introduced)   a.py
                     aap()

Unit Complexity
    None

Unit Interfacing
    None

Module Coupling
    None

-----------------------------------------------------------------------------------------
Maintainability ratings
-----------------------------------------------------------------------------------------
System property            Baseline on N/A          New/changed code    Target           
\033[96mVolume                     (N/A)                    N/A                                  \033[0m
\033[96mDuplication                (4.0)                    5.0                                  \033[0m
\033[96mUnit Size                  (4.0)                    2.0                                  \033[0m
\033[96mUnit Complexity            (N/A)                    N/A                                  \033[0m
\033[96mUnit Interfacing           (N/A)                    N/A                                  \033[0m
\033[96mModule Coupling            (N/A)                    N/A                                  \033[0m
\033[96mComponent Balance          (N/A)                    N/A                                  \033[0m
\033[96mComponent Independence     (N/A)                    N/A                                  \033[0m
\033[96mComponent Entanglement     (N/A)                    N/A                                  \033[0m
-----------------------------------------------------------------------------------------
\033[91mMaintainability            (4.0)                    3.0                 3.5              \033[0m
        """
                
        self.assertEqual(buffer.getvalue().strip(), expected.strip())

    def testPrintOverallColumnWhenPublishing(self):
        feedback = {
            "baseine": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": [{"subject":"a.py::aap()", "category":"introduced", "metric":"UNIT_SIZE"}]
        }
    
        target = TargetQuality("/tmp/nonexistent", 3.5)
    
        buffer = io.StringIO()
        report = TextReport(buffer)
        report.generate(feedback, types.SimpleNamespace(publish=True), target)
        
        expected = """
-----------------------------------------------------------------------------------------
Refactoring candidates
-----------------------------------------------------------------------------------------

Duplication
    None

Unit Size
    - (introduced)   a.py
                     aap()

Unit Complexity
    None

Unit Interfacing
    None

Module Coupling
    None

-----------------------------------------------------------------------------------------
Maintainability ratings
-----------------------------------------------------------------------------------------
System property            Baseline on N/A          New/changed code    Target    Overall
\033[96mVolume                     (N/A)                    N/A                           N/A    \033[0m
\033[96mDuplication                (4.0)                    5.0                           4.0    \033[0m
\033[96mUnit Size                  (4.0)                    2.0                           4.0    \033[0m
\033[96mUnit Complexity            (N/A)                    N/A                           N/A    \033[0m
\033[96mUnit Interfacing           (N/A)                    N/A                           N/A    \033[0m
\033[96mModule Coupling            (N/A)                    N/A                           N/A    \033[0m
\033[96mComponent Balance          (N/A)                    N/A                           N/A    \033[0m
\033[96mComponent Independence     (N/A)                    N/A                           N/A    \033[0m
\033[96mComponent Entanglement     (N/A)                    N/A                           N/A    \033[0m
-----------------------------------------------------------------------------------------
\033[91mMaintainability            (4.0)                    3.0                 3.5       4.0    \033[0m
        """
        
        self.assertEqual(buffer.getvalue().strip(), expected.strip())
        
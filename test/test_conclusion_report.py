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
from sigridci.sigridci import ConclusionReport, Report, SigridApiClient, TargetQuality


class ConclusionReportTest(unittest.TestCase):
    maxDiff = None

    def testDisplayLandingPageFromClient(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": []
        }
    
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", publish=True, \
            sigridurl="https://example-sigrid.com", subsystem=None)
        target = TargetQuality("", 5.0)
        apiClient = SigridApiClient(args)
        buffer = io.StringIO()
        
        report = ConclusionReport(apiClient, buffer)
        report.generate("1234", feedback, args, target)
        
        expected = """
\033[1m\033[33m
** Sigrid CI run complete: Your code did not meet your Sigrid target for maintainable code **
\033[0m

-------------------------------------------------------------------------
View your analysis results in Sigrid:
    https://example-sigrid.com/aap/noot/-/sigrid-ci/1234?targetRating=5.0
-------------------------------------------------------------------------
        """
                
        self.assertEqual(buffer.getvalue().strip(), expected.strip())

    def testSigridLinkIsLowercase(self):
        args = types.SimpleNamespace(partner="sig", customer="Aap", system="NOOT", publish=True, \
            sigridurl="https://example-sigrid.com", subsystem=None)
        report = ConclusionReport(SigridApiClient(args), io.StringIO())
        
        self.assertEqual(report.getSigridUrl(args), "https://sigrid-says.com/aap/noot")
        
    def testSpecialTextIfNoCodeChanged(self):
        feedback = {
            "baseine": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": []
        }
    
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", publish=True, \
            sigridurl="https://example-sigrid.com", subsystem=None)
        target = TargetQuality("", 5.0)
        apiClient = SigridApiClient(args)
        buffer = io.StringIO()
        
        report = ConclusionReport(apiClient, buffer)
        report.generate("1234", feedback, args, target)
        
        expected = """
\033[1m\033[96m
** Sigrid CI run complete: No files relevant for maintainability were changed **
\033[0m

-------------------------------------------------------------------------
View your analysis results in Sigrid:
    https://example-sigrid.com/aap/noot/-/sigrid-ci/1234?targetRating=5.0
-------------------------------------------------------------------------
        """
                
        self.assertEqual(buffer.getvalue().strip(), expected.strip())

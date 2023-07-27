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

from io import StringIO

from sigridci.pipeline_summary_report import PipelineSummaryReport
from sigridci.publish_options import PublishOptions, RunMode
from unittest import TestCase


class ConclusionReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_AND_PUBLISH, "/tmp",
            targetRating=3.5, sigridURL="https://example-sigrid.com")

    def testDisplayLandingPageFromClient(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.2},
            "refactoringCandidates": []
        }
    
        buffer = StringIO()
        report = PipelineSummaryReport(buffer, ansiColors=False)
        report.generate("1234", feedback, self.options)
        
        expected = """
** SIGRID CI RUN COMPLETE: THE CODE YOU WROTE DID NOT MEET THE TARGET FOR MAINTAINABLE CODE **


-------------------------------------------------------------------------
View your analysis results in Sigrid:
    https://example-sigrid.com/aap/noot/-/sigrid-ci/1234?targetRating=3.5
-------------------------------------------------------------------------
        """
                
        self.assertEqual(buffer.getvalue().strip(), expected.strip())

    def testSigridLinkIsLowercase(self):
        self.options.customer = "Aap"
        self.options.system = "NOOT"

        buffer = StringIO()
        report = PipelineSummaryReport(buffer, ansiColors=False)

        self.assertEqual(report.getSigridUrl(self.options), "https://example-sigrid.com/aap/noot")
        
    def testSpecialTextIfNoCodeChanged(self):
        feedback = {
            "baseine": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"MAINTAINABILITY": None},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": []
        }

        buffer = StringIO()
        report = PipelineSummaryReport(buffer, ansiColors=False)
        report.generate("1234", feedback, self.options)

        expected = """
** SIGRID CI RUN COMPLETE: NO FILES CONSIDERED FOR MAINTAINABILITY WERE CHANGED **


-------------------------------------------------------------------------
View your analysis results in Sigrid:
    https://example-sigrid.com/aap/noot/-/sigrid-ci/1234?targetRating=3.5
-------------------------------------------------------------------------
        """

        self.assertEqual(buffer.getvalue().strip(), expected.strip())

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

import inspect
import tempfile
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.json_report import JsonReport


class JsonReportTest(TestCase):
    maxDiff = None

    def testDumpJsonFeedbackToFile(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4}
        }

        options = PublishOptions(
            customer="aap",
            system="noot",
            runMode=RunMode.FEEDBACK_ONLY,
            sourceDir="/tmp",
            outputDir=tempfile.mkdtemp()
        )

        report = JsonReport()
        report.generate("1234", feedback, options)

        with open(f"{options.outputDir}/sigridci.json", "r") as f:
            contents = f.read()

        expected = """
            {
                "baseline": "20220110",
                "baselineRatings": {
                    "DUPLICATION": 4.0,
                    "UNIT_SIZE": 4.0,
                    "MAINTAINABILITY": 4.0
                },
                "changedCodeBeforeRatings": {
                    "MAINTAINABILITY": 2.6
                },
                "newCodeRatings": {
                    "DUPLICATION": 5.0,
                    "UNIT_SIZE": 2.0,
                    "MAINTAINABILITY": 3.0
                },
                "overallRatings": {
                    "DUPLICATION": 4.5,
                    "UNIT_SIZE": 3.0,
                    "MAINTAINABILITY": 3.4
                }
            }
        """

        self.assertEqual(contents.strip(), inspect.cleandoc(expected).strip())

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
from unittest import TestCase

# The entry point script is not part of a Python module, so we
# are forced to use the infamous Python path modification for
# this test.
import sys
sys.path.append("sigridci")

from generate_reports import generateReports
from sigridci.publish_options import PublishOptions, RunMode


class GenerateReportsTest(TestCase):

    def testOutputDirectoryIsConfigurable(self):
        tempDir = tempfile.mkdtemp()
        outputDir = tempfile.mkdtemp()
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, tempDir, outputDir=outputDir, targetRating=4)

        with open(f"{tempDir}/test.json", "w", encoding="utf8") as f:
            f.write("""{
                "baseline": "20220110",
                "baselineRatings": {"MAINTAINABILITY": 4.0},
                "changedCodeBeforeRatings": {"MAINTAINABILITY": 2.6},
                "changedCodeAfterRatings": {"MAINTAINABILITY": 2.8},
                "newCodeRatings": {"MAINTAINABILITY": 3.0},
                "overallRatings": {"MAINTAINABILITY": 3.4},
                "refactoringCandidates": []
            }""")

        generateReports(f"{tempDir}/test.json", options)

        self.assertTrue(os.path.exists(outputDir))
        self.assertTrue(os.path.exists(f"{outputDir}/feedback.md"))

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

import json
from tempfile import NamedTemporaryFile, mkdtemp
from unittest import TestCase

from sigridci.sigridci.azure_pull_request_report import AzurePullRequestReport
from sigridci.sigridci.objective import ObjectiveStatus
from sigridci.sigridci.publish_options import PublishOptions, RunMode


class AzurePullRequestReportTest(TestCase):

    def testCommentIsDependentOnStatus(self):
        with NamedTemporaryFile() as f:
            f.write("This is Markdown feedback\n\n...with multiple lines".encode("utf8"))

            report = AzurePullRequestReport()

            self.assertEqual("closed", report.buildRequestBody(f.name, ObjectiveStatus.ACHIEVED)["status"])
            self.assertEqual("closed", report.buildRequestBody(f.name, ObjectiveStatus.IMPROVED)["status"])
            self.assertEqual("active", report.buildRequestBody(f.name, ObjectiveStatus.UNCHANGED)["status"])
            self.assertEqual("active", report.buildRequestBody(f.name, ObjectiveStatus.WORSENED)["status"])
            self.assertEqual("active", report.buildRequestBody(f.name, ObjectiveStatus.UNKNOWN)["status"])

    def testPostNewComment(self):
        tempDir = mkdtemp()
        with open(f"{tempDir}/feedback.md", "w") as f:
            f.write("# Sigrid CI feedback\n\ntest\n")

        mockAzureResponse = {
            "value": [
                {
                    "id": 1,
                    "comments": [
                        {
                            "id": 2,
                            "content": "This is a comment"
                        }
                    ]
                }
            ]
        }

        azure = MockAzure(mockAzureResponse)
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, tempDir, outputDir=tempDir)
        feedback = {"newCodeRatings": {}, "baselineRatings": {}}
        azure.generate("1234", feedback, options)

        self.assertEqual(["GET", "POST"], azure.calledEndPoints)

    def testUpdateExistingComment(self):
        tempDir = mkdtemp()
        with open(f"{tempDir}/feedback.md", "w") as f:
            f.write("# Sigrid CI feedback\n\ntest\n")

        mockAzureResponse = {
            "value": [
                {
                    "id": 1,
                    "comments": [
                        {
                            "id": 2,
                            "content": "# Sigrid CI says"
                        }
                    ]
                }
            ]
        }

        azure = MockAzure(mockAzureResponse)
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, tempDir, outputDir=tempDir)
        feedback = {"newCodeRatings": {}, "baselineRatings": {}}
        azure.generate("1234", feedback, options)

        self.assertEqual(["GET", "PATCH"], azure.calledEndPoints)


class MockAzure(AzurePullRequestReport):

    def __init__(self, response):
        super().__init__()
        self.response = response
        self.calledEndPoints = []

    def isSupported(self, options):
        return True

    def callAzure(self, method, body, threadId):
        self.calledEndPoints.append(method)
        return self

    def read(self):
        return json.dumps(self.response)

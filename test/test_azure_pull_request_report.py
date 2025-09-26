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
from tempfile import mkdtemp
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.azure_pull_request_report import AzurePullRequestReport
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport


class AzurePullRequestReportTest(TestCase):

    def testCommentIsDependentOnStatus(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        good = {"newCodeRatings" : {"MAINTAINABILITY" : 5.0}}
        bad = {"newCodeRatings" : {"MAINTAINABILITY" : 2.0}}
        report = AzurePullRequestReport(MaintainabilityMarkdownReport())

        self.assertEqual("closed", report.buildRequestBody("", good, options)["status"])
        self.assertEqual("closed", report.buildRequestBody("", bad, options)["status"])

    def testPostNewComment(self):
        tempDir = mkdtemp()

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

        mockAzureResponse = {
            "value": [
                {
                    "id": 1,
                    "comments": [
                        {
                            "id": 2,
                            "content": "# Sigrid Maintainability feedback"
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
        super().__init__(MaintainabilityMarkdownReport())
        self.response = response
        self.calledEndPoints = []

    def isSupported(self, options):
        return True

    def callAzure(self, method, body, threadId):
        self.calledEndPoints.append(method)
        return self

    def read(self):
        return json.dumps(self.response)

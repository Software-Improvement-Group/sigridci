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

import base64
import json
import os
import urllib.error
from unittest import TestCase
from unittest.mock import patch

from sigridci.sigridci.capability import MAINTAINABILITY
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from sigridci.sigridci.reports.gerrit_report import GerritCredentials, GerritReport
from sigridci.sigridci.upload_log import UploadLog


MOCK_GERRIT_ENV = {
    "GERRIT_BASE_URL": "https://gerrit.example.com",
    "GERRIT_REPO": "acme/widget",
    "GERRIT_BRANCH": "main",
    "GERRIT_CHANGE_ID": "I1234",
    "GERRIT_USER": "aap",
    "GERRIT_PASSWORD": "noot"
}


class GerritReportTest(TestCase):

    def setUp(self):
        UploadLog.clear()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, capabilities=[MAINTAINABILITY])

        self.feedback = {
            MAINTAINABILITY: {
                "baseline": "20220110",
                "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
                "changedCodeBeforeRatings": {"MAINTAINABILITY": 2.6},
                "changedCodeAfterRatings": {"MAINTAINABILITY": 2.8},
                "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
                "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
                "refactoringCandidates": []
            }
        }

    @patch.dict(os.environ, MOCK_GERRIT_ENV)
    def testPostComment(self):
        gerrit = MockGerrit(CombinedMarkdownFeedbackReport({}))
        gerrit.generate("1234", self.feedback, self.options)

        self.assertEqual(1, len(gerrit.comments))
        credentials, comment = gerrit.comments[0]
        self.assertEqual(GerritCredentials(**{
            "baseURL": "https://gerrit.example.com",
            "repo": "acme/widget",
            "branch": "main",
            "changeID": "I1234",
            "user": "aap",
            "password": "noot"
        }), credentials)
        self.assertIn("View this system in Sigrid", comment)

    @patch.dict(os.environ, MOCK_GERRIT_ENV)
    def testDoNotIncludeMarkdownImages(self):
        gerrit = MockGerrit(CombinedMarkdownFeedbackReport({}))
        gerrit.generate("1234", self.feedback, self.options)

        credentials, comment = gerrit.comments[0]
        self.assertNotIn("![", comment)
        self.assertNotIn("matomo.php", comment)

    @patch.dict(os.environ, {}, clear=True)
    def testDoNothingOutsideGerrit(self):
        gerrit = MockGerrit(CombinedMarkdownFeedbackReport({}))
        gerrit.generate("1234", self.feedback, self.options)

        self.assertEqual([], gerrit.comments)
        self.assertEqual([], UploadLog.history)

    @patch.dict(os.environ, MOCK_GERRIT_ENV)
    def testDoNothingInPublishOnlyMode(self):
        options = PublishOptions("aap", "noot", RunMode.PUBLISH_ONLY, capabilities=[MAINTAINABILITY])
        gerrit = MockGerrit(CombinedMarkdownFeedbackReport({}))
        gerrit.generate("1234", self.feedback, options)

        self.assertEqual([], gerrit.comments)

    @patch.dict(os.environ, MOCK_GERRIT_ENV | {"GERRIT_PASSWORD": ""})
    def testSkipWhenCredentialsAreIncomplete(self):
        gerrit = MockGerrit(CombinedMarkdownFeedbackReport({}))
        gerrit.generate("1234", self.feedback, self.options)

        self.assertEqual([], gerrit.comments)
        self.assertEqual(["Incomplete Gerrit credentials, skipping Gerrit integration."], UploadLog.history)

    @patch.dict(os.environ, MOCK_GERRIT_ENV)
    @patch("urllib.request.urlopen")
    def testSendRequestToGerritAPI(self, urlopen):
        gerrit = GerritReport(CombinedMarkdownFeedbackReport({}))
        gerrit.postGerritComment(gerrit.getCredentials(), "Hello")

        request = urlopen.call_args.args[0]
        expectedAuth = base64.b64encode(b"aap:noot").decode("ascii")
        expectedBody = {
            "comments": {
                "/PATCHSET_LEVEL": [{"message": "Hello", "unresolved": False}]
            }
        }

        self.assertEqual("https://gerrit.example.com/a/changes/acme%2Fwidget~main~I1234/revisions/current/review",
                         request.full_url)
        self.assertEqual("application/json", request.get_header("Content-type"))
        self.assertEqual(f"Basic {expectedAuth}", request.get_header("Authorization"))
        self.assertEqual(expectedBody, json.loads(request.data.decode("utf-8")))
        self.assertEqual(["Posted feedback to Gerrit"], UploadLog.history)

    @patch.dict(os.environ, MOCK_GERRIT_ENV)
    @patch("urllib.request.urlopen")
    def testDoNotExitOnFailingGerritRequest(self, urlopen):
        urlopen.side_effect = urllib.error.HTTPError("https://gerrit.example.com", 401, "Unauthorized", {}, None)

        gerrit = GerritReport(CombinedMarkdownFeedbackReport({}))
        gerrit.postGerritComment(gerrit.getCredentials(), "Hello")

        self.assertTrue(any(message.startswith("Failed to publish feedback to Gerrit") for message in UploadLog.history))


class MockGerrit(GerritReport):

    def __init__(self, markdownReport):
        super().__init__(markdownReport)
        self.comments = []

    def postGerritComment(self, credentials, comment):
        self.comments.append((credentials, comment))

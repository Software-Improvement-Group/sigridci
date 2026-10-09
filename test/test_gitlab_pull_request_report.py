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
import os
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.gitlab_pull_request_report import GitLabPullRequestReport
from sigridci.sigridci.upload_log import UploadLog
from sigridci.sigridci.capability import MAINTAINABILITY
from sigridci.sigridci.reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport


MOCK_GITLAB_ENV = {
    "CI_API_V4_URL" : "https://nonexistent-example.com",
    "CI_MERGE_REQUEST_PROJECT_ID" : "1234",
    "CI_MERGE_REQUEST_IID" : "5678"
}


class GitLabPullRequestReportTest(TestCase):

    def setUp(self):
        UploadLog.clear()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, capabilities=[MAINTAINABILITY])

        self.feedback = {
            MAINTAINABILITY : {
                "baseline": "20220110",
                "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
                "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
                "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
                "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
                "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
                "refactoringCandidates": []
            }
        }

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV)
    def testPostNewComment(self):
        gitlab = MockGitLab(CombinedMarkdownFeedbackReport({}))
        gitlab.generate("1234", self.feedback, self.options)

        self.assertEqual(["Published feedback to GitLab"], UploadLog.history)
        self.assertEqual(["POST https://nonexistent-example.com/projects/1234/merge_requests/5678/notes"], gitlab.called)

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV)
    def testUpdateExistingComment(self):
        gitlab = MockGitLab(CombinedMarkdownFeedbackReport({}))
        gitlab.generate("1234", self.feedback, self.options)
        gitlab.generate("1234", self.feedback, self.options)

        expectedLog = [
            "Published feedback to GitLab",
            "Updated existing GitLab feedback"
        ]

        expectedCalls = [
            "POST https://nonexistent-example.com/projects/1234/merge_requests/5678/notes",
            "PUT https://nonexistent-example.com/projects/1234/merge_requests/5678/notes/1"
        ]

        self.assertEqual(expectedLog, UploadLog.history)
        self.assertEqual(expectedCalls, gitlab.called)

    @mock.patch.dict(os.environ, MOCK_GITLAB_ENV | {"SIGRIDCI_GITLAB_COMMENT_TOKEN" : "1234"})
    def testDoNotExitOnFailingGitLabRequest(self):
        gitlab = GitLabPullRequestReport(CombinedMarkdownFeedbackReport({}))
        gitlab.generate("1234", self.feedback, self.options)

        self.assertTrue(message for message in UploadLog.history if any(message.startswith("Error contacting GitLab")))


class MockGitLab(GitLabPullRequestReport):
    def __init__(self, markdownReport):
        super().__init__(markdownReport)
        self.called = []
        self.comments = []

    def callAPI(self, method, url, body):
        self.called.append(f"{method} {url}")
        if method == "POST":
            self.comments.append(json.loads(body) | {"id" : len(self.comments) + 1})
        return self

    def isWithinGitLabMergeRequestPipeline(self, options):
        return True

    def findExistingCommentId(self):
        return next((comment["id"] for comment in self.comments if self.isExistingComment(comment)), None)

    def read(self):
        return "test"

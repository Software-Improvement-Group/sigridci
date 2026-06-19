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
from tempfile import mkdtemp
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.github_pull_request_report import GitHubPullRequestReport
from sigridci.sigridci.reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from sigridci.sigridci.reports.security_markdown_report import SecurityMarkdownReport
from sigridci.sigridci.upload_log import UploadLog


MOCK_GITHUB_ENV = {
    "GITHUB_EVENT_NAME" : "pull_request",
    "GITHUB_API_URL" : "https://nonexistent-example.com",
    "GITHUB_REPOSITORY" : "acme/widget",
    "GITHUB_REF" : "refs/pull/5678/merge"
}


class GitHubPullRequestReportTest(TestCase):

    def setUp(self):
        UploadLog.clear()
        self.tempDir = mkdtemp()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, outputDir=self.tempDir)

        self.feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": []
        }

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV)
    def testPostNewComment(self):
        github = MockGitHub(MaintainabilityMarkdownReport())
        github.generate("1234", self.feedback, self.options)

        self.assertEqual(["Published Maintainability feedback to GitHub"], UploadLog.history)
        self.assertEqual(["POST https://nonexistent-example.com/repos/acme/widget/issues/5678/comments"], github.called)

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV)
    def testUpdateExistingComment(self):
        github = MockGitHub(MaintainabilityMarkdownReport())
        github.generate("1234", self.feedback, self.options)
        github.generate("1234", self.feedback, self.options)

        expectedLog = [
            "Published Maintainability feedback to GitHub",
            "Updated existing GitHub Maintainability feedback"
        ]

        expectedCalls = [
            "POST https://nonexistent-example.com/repos/acme/widget/issues/5678/comments",
            "PATCH https://nonexistent-example.com/repos/acme/widget/issues/comments/1"
        ]

        self.assertEqual(expectedLog, UploadLog.history)
        self.assertEqual(expectedCalls, github.called)

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV)
    def testDoNotUpdateDifferentTypeOfFeedback(self):
        github = MockGitHub(MaintainabilityMarkdownReport())
        github.generate("1234", self.feedback, self.options)
        github.generate("1234", self.feedback, self.options)

        other = MockGitHub(SecurityMarkdownReport(self.options))
        other.generate("1234", {"runs" : []}, self.options)
        other.generate("1234", {"runs" : []}, self.options)

        expectedLog = [
            "Published Maintainability feedback to GitHub",
            "Updated existing GitHub Maintainability feedback",
            "Published Security feedback to GitHub",
            "Updated existing GitHub Security feedback"
        ]

        self.assertEqual(expectedLog, UploadLog.history)

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV | {"SIGRIDCI_GITHUB_COMMENT_TOKEN" : "1234"})
    def testDoNotExitOnFailingGitHubRequest(self):
        github = GitHubPullRequestReport(MaintainabilityMarkdownReport())
        github.generate("1234", self.feedback, self.options)

        self.assertTrue(message for message in UploadLog.history if any(message.startswith("Error contacting GitHub")))

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV | {"SIGRIDCI_GITHUB_COMMENT_TOKEN" : "1234", "GITHUB_REF" : "refs/heads/main"})
    def testNotInPipelineWhenRefIsNotAPullRequest(self):
        github = GitHubPullRequestReport(MaintainabilityMarkdownReport())

        self.assertFalse(github.isWithinGitHubPullRequestPipeline(self.options))
        self.assertIsNone(github.getPullRequestNumber())

    @mock.patch.dict(os.environ, MOCK_GITHUB_ENV)
    def testPullRequestNumberOnlyParsedFromActualPullRefs(self):
        github = GitHubPullRequestReport(MaintainabilityMarkdownReport())
        cases = {
            "refs/pull/5678/merge": "5678",   # real PR ref
            "refs/heads/123": None,           # digit-named branch, not a PR
            "refs/tags/v1": None,
            "refs/pull/abc/merge": None,      # non-numeric PR number
            "refs/pull": None,                # truncated
            "": None,                         # missing
        }
        for ref, expected in cases.items():
            with mock.patch.dict(os.environ, {"GITHUB_REF": ref}):
                self.assertEqual(expected, github.getPullRequestNumber(), ref)


class MockGitHub(GitHubPullRequestReport):

    def __init__(self, markdownReport):
        super().__init__(markdownReport)
        self.called = []
        self.comments = []

    def callAPI(self, method, url, body):
        self.called.append(f"{method} {url}")
        if method == "POST":
            self.comments.append(json.loads(body) | {"id" : len(self.comments) + 1})
        return self

    def isWithinGitHubPullRequestPipeline(self, options):
        return True

    def findExistingCommentId(self):
        return next((comment["id"] for comment in self.comments if self.isExistingComment(comment)), None)

    def read(self):
        return "test"

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

from tempfile import mkdtemp
from unittest import TestCase

from sigridci.sigridci.gitlab_pull_request_report import GitLabPullRequestReport
from sigridci.sigridci.markdown_report import MarkdownReport
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.upload_log import UploadLog


class GitLabPullRequestReportTest(TestCase):

    def setUp(self):
        UploadLog.clear()

        self.tempDir = mkdtemp()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, targetRating=3.5)

        self.feedback = {
            "baseline": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "changedCodeBeforeRatings" : {"MAINTAINABILITY" : 2.6},
            "changedCodeAfterRatings" : {"MAINTAINABILITY" : 2.8},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.4},
            "refactoringCandidates": []
        }

        with open(f"{self.tempDir}/feedback.md", "w") as f:
            # Use the *actual* Markdown report so we're sure we can handle
            # any layout changes.
            markdownReport = MarkdownReport()
            f.write(markdownReport.renderMarkdown("1234", self.feedback, self.options))

    def testPostNewComment(self):
        gitlab = MockGitLab(None)
        gitlab.generate("1234", self.feedback, self.options)

        self.assertEqual(["Published feedback to GitLab"], UploadLog.history)

    def testUpdateExistingComment(self):
        gitlab = MockGitLab("1")
        gitlab.generate("1234", self.feedback, self.options)

        self.assertEqual(["Updated existing GitLab feedback"], UploadLog.history)


class MockGitLab(GitLabPullRequestReport):

    def __init__(self, existingCommentId):
        super().__init__()
        self.existingCommentId = existingCommentId

    def buildPostCommentURL(self, existingCommentId):
        return str(existingCommentId)

    def callAPI(self, method, url, body):
        return self

    def isWithinGitLabMergeRequestPipeline(self):
        return True

    def findExistingCommentId(self):
        return self.existingCommentId

    def read(self):
        return "test"

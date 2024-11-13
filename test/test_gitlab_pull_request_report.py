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

from tempfile import NamedTemporaryFile, mkdtemp
from unittest import TestCase

from sigridci.sigridci.gitlab_pull_request_report import GitLabPullRequestReport
from sigridci.sigridci.markdown_report import MarkdownReport
from sigridci.sigridci.objective import ObjectiveStatus
from sigridci.sigridci.publish_options import PublishOptions, RunMode



class GitLabPullRequestReportTest(TestCase):

    def testPostNewComment(self):
        gitlab = MockGitLab()

    def testUpdateExistingComment(self):
        pass


class MockGitLab(GitLabPullRequestReport):

    def isWithinGitLabMergeRequestPipeline(self):
        return True

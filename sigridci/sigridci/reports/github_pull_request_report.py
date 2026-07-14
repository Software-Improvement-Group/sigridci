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
import ssl
import urllib.parse
import urllib.request

from .report import Report, MarkdownRenderer
from ..api_caller import ApiCaller
from ..publish_options import RunMode
from ..upload_log import UploadLog


class GitHubPullRequestReport(Report):

    def __init__(self, markdownRenderer: MarkdownRenderer):
        self.markdownRenderer = markdownRenderer

        certPath = os.getenv("SIGRID_GITHUB_CA_CERT_PATH")
        self.sslContext = ssl.create_default_context(cafile=certPath) if certPath else None

    def generate(self, analysisId, feedback, options):
        if self.isWithinGitHubPullRequestPipeline(options):
            try:
                existingCommentId = self.findExistingCommentId()
                body = self.buildRequestBody(self.markdownRenderer.renderMarkdown(analysisId, feedback, options))

                if existingCommentId is None:
                    self.callAPI("POST", self.buildCommentsURL(), body)
                    UploadLog.log(f"Published {self.markdownRenderer.getCapability().displayName} feedback to GitHub")
                else:
                    self.callAPI("PATCH", self.buildCommentURL(existingCommentId), body)
                    UploadLog.log(f"Updated existing GitHub {self.markdownRenderer.getCapability().displayName} feedback")
            except SystemExit as e:
                print(f"Failed to publish feedback to GitHub: {e}")

    def isWithinGitHubPullRequestPipeline(self, options):
        return os.environ.get("GITHUB_EVENT_NAME") == "pull_request" and \
            options.runMode == RunMode.FEEDBACK_ONLY and \
            "SIGRIDCI_GITHUB_COMMENT_TOKEN" in os.environ and \
            self.getPullRequestNumber() is not None

    def callAPI(self, method, url, body):
        request = urllib.request.Request(url, body, method=method)
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", f"Bearer {os.environ['SIGRIDCI_GITHUB_COMMENT_TOKEN']}")
        request.add_header("X-GitHub-Api-Version", "2022-11-28")

        api = ApiCaller("GitHub", pollInterval=5)
        return api.retryRequest(lambda: urllib.request.urlopen(request, context=self.sslContext))

    def getPullRequestNumber(self):
        # GITHUB_REF format for pull requests: refs/pull/{number}/merge
        ref = os.environ.get("GITHUB_REF", "")
        parts = ref.split("/")
        if len(parts) >= 3 and parts[0] == "refs" and parts[1] == "pull" and parts[2].isdigit():
            return parts[2]
        UploadLog.log(f"Could not extract pull request number from GITHUB_REF '{ref}'; skipping pull request comment")
        return None

    def buildCommentsURL(self):
        baseURL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        repo = os.environ["GITHUB_REPOSITORY"]
        return f"{baseURL}/repos/{repo}/issues/{self.getPullRequestNumber()}/comments"

    def buildCommentURL(self, commentId):
        baseURL = os.environ.get("GITHUB_API_URL", "https://api.github.com")
        repo = os.environ["GITHUB_REPOSITORY"]
        return f"{baseURL}/repos/{repo}/issues/comments/{commentId}"

    def buildRequestBody(self, markdown):
        return json.dumps({"body": markdown}).encode("utf-8")

    def findExistingCommentId(self):
        with self.callAPI("GET", self.buildCommentsURL(), None) as f:
            for comment in json.load(f):
                if self.isExistingComment(comment):
                    return comment["id"]

    def isExistingComment(self, comment):
        header = f"{self.markdownRenderer.getCapability().displayName} feedback"
        body = comment.get("body", "")
        return body.startswith(("# Sigrid", "# [Sigrid]")) and header.lower() in body.lower()

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
import urllib.request

from .report import Report, MarkdownRenderer
from ..api_caller import ApiCaller
from ..publish_options import RunMode
from ..upload_log import UploadLog


class GitLabPullRequestReport(Report):

    def __init__(self, markdownRenderer: MarkdownRenderer):
        self.markdownRenderer = markdownRenderer

        certPath = os.getenv("SIGRID_GITLAB_CA_CERT_PATH")
        self.sslContext = ssl.create_default_context(cafile=certPath) if certPath else None

    def generate(self, analysisId, feedback, options):
        if self.isWithinGitLabMergeRequestPipeline(options):
            try:
                existingCommentId = self.findExistingCommentId()
                body = self.buildRequestBody(self.markdownRenderer.renderMarkdown(analysisId, feedback, options))

                if existingCommentId is None:
                    self.callAPI("POST", self.buildPostCommentURL(None), body)
                    UploadLog.log(f"Published {self.markdownRenderer.getCapability().displayName} feedback to GitLab")
                else:
                    self.callAPI("PUT", self.buildPostCommentURL(existingCommentId), body)
                    UploadLog.log(f"Updated existing GitLab {self.markdownRenderer.getCapability().displayName} feedback")
            except SystemExit:
                print("Failed to publish feedback to Gitab")

    def isWithinGitLabMergeRequestPipeline(self, options):
        return "CI_MERGE_REQUEST_IID" in os.environ and \
            "SIGRIDCI_GITLAB_COMMENT_TOKEN" in os.environ and \
            options.runMode == RunMode.FEEDBACK_ONLY

    def callAPI(self, method, url, body):
        request = urllib.request.Request(url, body, method=method)
        request.add_header("Content-Type", "application/json")
        request.add_header("PRIVATE-TOKEN", os.environ["SIGRIDCI_GITLAB_COMMENT_TOKEN"])

        api = ApiCaller("GitLab", pollInterval=5)
        return api.retryRequest(lambda: urllib.request.urlopen(request, context=self.sslContext))

    def buildPostCommentURL(self, existingCommentId):
        baseURL = os.environ["CI_API_V4_URL"]
        projectId = os.environ["CI_MERGE_REQUEST_PROJECT_ID"]
        mergeRequestId = os.environ["CI_MERGE_REQUEST_IID"]

        url = f"{baseURL}/projects/{projectId}/merge_requests/{mergeRequestId}/notes"
        if existingCommentId is not None:
            url += f"/{existingCommentId}"
        return url


    def buildRequestBody(self, markdown):
        body = {"body" : markdown}
        return json.dumps(body).encode("utf-8")

    def findExistingCommentId(self):
        baseURL = os.environ["CI_API_V4_URL"]
        projectId = os.environ["CI_MERGE_REQUEST_PROJECT_ID"]
        mergeRequestId = os.environ["CI_MERGE_REQUEST_IID"]
        url = f"{baseURL}/projects/{projectId}/merge_requests/{mergeRequestId}/notes?page=1&per_page=100"

        with self.callAPI("GET", url, None) as f:
            for comment in json.load(f):
                if self.isExistingComment(comment):
                    return comment["id"]

    def isExistingComment(self, comment):
        header = f"{self.markdownRenderer.getCapability().displayName} feedback"
        return comment["body"].startswith(("# Sigrid", "# [Sigrid]")) and header.lower() in comment["body"].lower()

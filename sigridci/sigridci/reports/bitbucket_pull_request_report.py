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


class BitBucketPullRequestReport(Report):
    def __init__(self, markdownRenderer: MarkdownRenderer):
        self.markdownRenderer = markdownRenderer

        certPath = os.getenv("SIGRID_GITLAB_CA_CERT_PATH")
        self.sslContext = ssl.create_default_context(cafile=certPath) if certPath else None

    def generate(self, analysisId, feedback, options):
        if self.shouldPostComment(options):
            try:
                existingCommentId = self.findExistingCommentId()
                comment = self.markdownRenderer.renderMarkdown(analysisId, feedback, options)
                self.postComment(comment, existingCommentId)
                UploadLog.log(f"Posted {self.markdownRenderer.getCapability().displayName} BitBucket comment")
            except SystemExit:
                print("Failed to publish feedback to GitLab")

    def shouldPostComment(self, options):
        return "BITBUCKET_PR_ID" in os.environ \
            and "SIGRIDCI_BITBUCKET_COMMENT_TOKEN" in os.environ \
            and options.runMode == RunMode.FEEDBACK_ONLY

    def postComment(self, comment, existingCommentId=None):
        baseURL = os.environ.get("BITBUCKET_API_URL", "https://api.bitbucket.org/2.0")
        workspace = os.environ["BITBUCKET_WORKSPACE"]
        slug = os.environ["BITBUCKET_REPO_SLUG"]
        pullRequestId = os.environ["BITBUCKET_PR_ID"]

        method = "POST"
        url = f"{baseURL}/repositories/{workspace}/{slug}/pullrequests/{pullRequestId}/comments"
        if existingCommentId is not None:
            method = "PUT"
            url += f"/{existingCommentId}"

        body = {"content" : {"raw" : comment}}

        request = urllib.request.Request(url, json.dumps(body).encode("utf-8"), method=method)
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", f"Bearer {os.environ['SIGRIDCI_BITBUCKET_COMMENT_TOKEN']}")

        api = ApiCaller("BitBucket", pollInterval=5)
        return api.retryRequest(lambda: urllib.request.urlopen(request, context=self.sslContext))

    def updateComment(self, existingCommentId, comment):
        pass

    def findExistingCommentId(self):
        return None

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


class AzurePullRequestReport(Report):
    AZURE_API_VERSION = "6.0"

    def __init__(self, markdownRenderer: MarkdownRenderer):
        self.markdownRenderer = markdownRenderer

        certPath = os.getenv("SIGRID_AZURE_CA_CERT_PATH")
        self.sslContext = ssl.create_default_context(cafile=certPath) if certPath else None

    def generate(self, analysisId, feedback, options):
        if not self.isSupported(options):
            return

        UploadLog.log("Sending feedback to Azure DevOps API")

        markdown = self.markdownRenderer.renderMarkdown(analysisId, feedback, options)

        try:
            # We want to update the existing comment, to avoid spamming people with new
            # comments every time they make a commit. We have no way to persist this,
            # so we need to check the existing comments.
            existingId = self.findExistingSigridCommentThreadId()

            if existingId == None:
                self.callAzure("POST", self.buildRequestBody(markdown, feedback, options), None)
                UploadLog.log(f"Published new {self.markdownRenderer.getCapability()} feedback to Azure DevOps")
            else:
                self.callAzure("PATCH", self.buildRequestBody(markdown, feedback, options), existingId)
                UploadLog.log(f"Updated existing {self.markdownRenderer.getCapability()} feedback in Azure DevOps")
        except SystemExit:
            print("Failed to publish feedback to Azure DevOps")

    def isSupported(self, options):
        return "SYSTEM_ACCESSTOKEN" in os.environ and \
            "SYSTEM_PULLREQUEST_PULLREQUESTID" in os.environ and \
            options.runMode == RunMode.FEEDBACK_ONLY

    def findExistingSigridCommentThreadId(self):
        existingThreads = json.load(self.callAzure("GET", None, None))

        for thread in existingThreads["value"]:
            for comment in thread["comments"]:
                if self.isExistingComment(comment):
                    return thread["id"]

        return None

    def isExistingComment(self, comment):
        header = f"{self.markdownRenderer.getCapability()} feedback".lower()
        return comment["content"].startswith(("# Sigrid", "# [Sigrid]")) and header in comment["content"].lower()

    def callAzure(self, method, body, threadId):
        request = urllib.request.Request(self.buildURL(threadId), json.dumps(body).encode("utf-8"))
        request.method = method
        request.add_header("Authorization", f"Bearer {os.environ['SYSTEM_ACCESSTOKEN']}")
        request.add_header("Content-Type", "application/json")

        api = ApiCaller("Azure DevOps", pollInterval=5)
        return api.retryRequest(lambda: urllib.request.urlopen(request, context=self.sslContext))

    def buildURL(self, threadId):
        baseURL = os.environ["SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"]
        project = os.environ["SYSTEM_TEAMPROJECTID"]
        repo = os.environ["BUILD_REPOSITORY_NAME"]
        pr = os.environ["SYSTEM_PULLREQUEST_PULLREQUESTID"]

        if threadId:
            return f"{baseURL}{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads/{threadId}?api-version={self.AZURE_API_VERSION}"
        else:
            return f"{baseURL}{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads?api-version={self.AZURE_API_VERSION}"

    def buildRequestBody(self, markdown, feedback, options):
        return {
            "comments": [{
                "parentCommentId": 0,
                "content": markdown,
                "commentType": "text"
            }],
            "status": self.getCommentStatus(feedback, options)
        }

    def getCommentStatus(self, feedback, options):
        if self.markdownRenderer.isObjectiveSuccess(feedback, options):
            return "closed"
        else:
            return "active"

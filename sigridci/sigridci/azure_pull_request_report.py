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
import urllib.error
import urllib.request

from .objective import Objective, ObjectiveStatus
from .publish_options import RunMode
from .report import Report
from .upload_log import UploadLog


class AzurePullRequestReport(Report):
    AZURE_API_VERSION = "6.0"

    def generate(self, analysisId, feedback, options):
        feedbackFile = f"{options.outputDir}/feedback.md"

        if not self.isSupported(options) or not os.path.exists(feedbackFile):
            return

        try:
            UploadLog.log("Sending feedback to Azure DevOps API")

            # We want to update the existing comment, to avoid spamming people with new
            # comments every time they make a commit. We have no way to persist this,
            # so we need to check the existing comments.
            existingId = self.findExistingSigridCommentThreadId()
            status = Objective.determineStatus(feedback, options)

            if existingId == None:
                self.callAzure("POST", self.buildRequestBody(feedbackFile, status), None)
                UploadLog.log("Published new feedback to Azure DevOps")
            else:
                self.callAzure("PATCH", self.buildRequestBody(feedbackFile, status), existingId)
                UploadLog.log("Updated existing feedback in Azure DevOps")
        except urllib.error.HTTPError as e:
            UploadLog.log(f"Warning: Azure DevOps API error: {e.code} / {e.fp.read()}")

    def isSupported(self, options):
        return "SYSTEM_ACCESSTOKEN" in os.environ and \
            "SYSTEM_PULLREQUEST_PULLREQUESTID" in os.environ and \
            options.runMode == RunMode.FEEDBACK_ONLY

    def findExistingSigridCommentThreadId(self):
        existingThreads = json.load(self.callAzure("GET", None, None))

        for thread in existingThreads["value"]:
            for comment in thread["comments"]:
                if comment["content"].startswith("# Sigrid"):
                    return thread["id"]

        return None

    def callAzure(self, method, body, threadId):
        request = urllib.request.Request(self.buildURL(threadId), json.dumps(body).encode("utf-8"))
        request.method = method
        request.add_header("Authorization", f"Bearer {os.environ['SYSTEM_ACCESSTOKEN']}")
        request.add_header("Content-Type", "application/json")
        return urllib.request.urlopen(request)

    def buildURL(self, threadId):
        baseURL = os.environ["SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"]
        project = os.environ["SYSTEM_TEAMPROJECTID"]
        repo = os.environ["BUILD_REPOSITORY_NAME"]
        pr = os.environ["SYSTEM_PULLREQUEST_PULLREQUESTID"]
        version = self.AZURE_API_VERSION

        if threadId:
            return f"{baseURL}{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads/{threadId}?api-version={version}"
        else:
            return f"{baseURL}{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads?api-version={version}"

    def buildRequestBody(self, feedbackFile, status):
        with open(feedbackFile, mode="r", encoding="utf-8") as f:
            feedback = f.read()

        commentStatus = "closed" if status in [ObjectiveStatus.ACHIEVED, ObjectiveStatus.IMPROVED] else "active"

        return {
            "comments": [{
                "parentCommentId": 0,
                "content": feedback,
                "commentType": "text"
            }],
            "status": commentStatus
        }

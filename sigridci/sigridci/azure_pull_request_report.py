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

from .publish_options import RunMode
from .report import Report
from .upload_log import UploadLog


class AzurePullRequestReport(Report):
    AZURE_API_VERSION = "6.0"

    def generate(self, analysisId, feedback, options):
        feedbackFile = f"{options.outputDir}/feedback.md"

        if not self.isSupported(options) or not os.path.exists(feedbackFile):
            return

        UploadLog.log("Sending feedback to Azure DevOps API")

        request = urllib.request.Request(self.buildURL(), self.buildRequestBody(feedbackFile))
        request.add_header("Authorization", f"Bearer {os.environ['SYSTEM_ACCESSTOKEN']}")
        request.add_header("Content-Type", "application/json")
        try:
            urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            UploadLog.log(f"Warning: Azure DevOps API error: {e.code} / {e.fp.read()}")

    def isSupported(self, options):
        return "SYSTEM_ACCESSTOKEN" in os.environ and \
            "SYSTEM_PULLREQUEST_PULLREQUESTID" in os.environ and \
            options.runMode == RunMode.FEEDBACK_ONLY

    def buildURL(self):
        baseURL = os.environ["SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"]
        project = os.environ["SYSTEM_TEAMPROJECTID"]
        repo = os.environ["BUILD_REPOSITORY_NAME"]
        pr = os.environ["SYSTEM_PULLREQUEST_PULLREQUESTID"]
        version = self.AZURE_API_VERSION
        return f"{baseURL}{project}/_apis/git/repositories/{repo}/pullRequests/{pr}/threads?api-version={version}"

    def buildRequestBody(self, feedbackFile):
        with open(feedbackFile, mode="r", encoding="utf-8") as f:
            feedback = f.read()

        body = {
            "comments": [{
                "parentCommentId": 0,
                "content": feedback,
                "commentType": "text"
            }],
            "status": "active"
        }

        return json.dumps(body).encode("utf-8")

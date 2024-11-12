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


class GitLabPullRequestReport(Report):
    def generate(self, analysisId, feedback, options):
        if not self.isWithinGitLabMergeRequestPipeline() or options.runMode != RunMode.FEEDBACK_ONLY:
            return

        for feedbackFile in self.getFeedbackFiles(options):
            baseURL = os.environ["CI_API_V4_URL"]
            projectId = os.environ["CI_MERGE_REQUEST_PROJECT_ID"]
            mergeRequestId = os.environ["CI_MERGE_REQUEST_IID"]
            url = f"{baseURL}/projects/{projectId}/merge_requests/{mergeRequestId}/notes"

            try:
                request = urllib.request.Request(url, self.buildRequestBody(feedbackFile))
                request.add_header("Content-Type", "application/json")
                request.add_header("PRIVATE-TOKEN", os.environ["SIGRIDCI_GITLAB_COMMENT_TOKEN"])
                urllib.request.urlopen(request)
                UploadLog.log("Published feedback to GitLab")
            except urllib.error.HTTPError as e:
                UploadLog.log(f"Warning: GitLab API error: {e.code} / {e.fp.read()}")

    def isWithinGitLabMergeRequestPipeline(self):
        return "CI_MERGE_REQUEST_IID" in os.environ and "SIGRIDCI_GITLAB_COMMENT_TOKEN" in os.environ

    def getFeedbackFiles(self, options):
        fileNames = ["feedback.md", "osh-feedback.md", "security-feedback.md"]
        files = [f"{options.outputDir}/{fileName}" for fileName in fileNames]
        return [file for file in files if os.path.exists(file)]

    def buildRequestBody(self, feedbackFile):
        with open(feedbackFile, mode="r", encoding="utf-8") as f:
            feedback = f.read()

        body = {
            "body" : feedback
        }

        return json.dumps(body).encode("utf-8")

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

import base64
import json
import os
import ssl
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from io import StringIO

from .combined_text_report import CombinedTextReport
from .report import Report
from ..api_caller import ApiCaller
from ..publish_options import PublishOptions, RunMode
from ..reports.combined_markdown_feedback_report import CombinedMarkdownFeedbackReport
from ..upload_log import UploadLog


@dataclass(frozen=True)
class GerritCredentials:
    baseURL: str
    repo: str
    branch: str
    changeID: str
    user: str
    password: str


class GerritReport(Report):
    def __init__(self, masterReport: CombinedMarkdownFeedbackReport):
        self.masterReport = masterReport

        certPath = os.getenv("SIGRID_GERRIT_CA_CERT_PATH")
        self.sslContext = ssl.create_default_context(cafile=certPath) if certPath else None

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        if not "GERRIT_BASE_URL" in os.environ or options.runMode == RunMode.PUBLISH_ONLY:
            return

        credentials = self.getCredentials()

        if "" in asdict(credentials).values():
            UploadLog.log("Incomplete Gerrit credentials, skipping Gerrit integration.")
            return

        buffer = StringIO()
        plainTextReport = CombinedTextReport(self.masterReport, output=buffer)
        plainTextReport.generate(analysisId, feedback, options)
        self.postGerritComment(credentials, plainTextReport.ANSI_PATTERN.sub("", buffer.getvalue()))

    def getCredentials(self) -> GerritCredentials:
        return GerritCredentials(
            baseURL=os.getenv("GERRIT_BASE_URL") or "",
            repo=os.getenv("GERRIT_REPO") or "",
            branch=os.getenv("GERRIT_BRANCH") or "",
            changeID=os.getenv("GERRIT_CHANGE_ID") or "",
            user=os.getenv("GERRIT_USER") or "",
            password=os.getenv("GERRIT_PASSWORD") or ""
        )

    def postGerritComment(self, credentials: GerritCredentials, comment: str) -> None:
        repo = urllib.parse.quote(credentials.repo, safe="")
        branch = urllib.parse.quote(credentials.branch, safe="")

        url = f"{credentials.baseURL}/a/changes/{repo}~{branch}~{credentials.changeID}/revisions/current/review"
        body = {"message" : comment}
        basicAuth = base64.b64encode(f"{credentials.user}:{credentials.password}".encode("utf8")).decode("ascii")

        request = urllib.request.Request(url, json.dumps(body).encode("utf-8"))
        request.add_header("Content-Type", "application/json")
        request.add_header("Authorization", f"Basic {basicAuth}")

        try:
            api = ApiCaller("Gerrit", pollInterval=5)
            api.retryRequest(lambda: urllib.request.urlopen(request, context=self.sslContext))
            UploadLog.log("Posted feeback to Gerrit")
        except SystemExit as e:
            UploadLog.log(f"Failed to publish feedback to Gerrit: {e}")

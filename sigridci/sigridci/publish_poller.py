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

import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from .upload_log import UploadLog


class PublishPoller:
    def __init__(self, apiClient):
        self.apiClient = apiClient
        self.pollInterval = 300
        self.pollAttempts = 24

    def waitForSnapshot(self, start):
        UploadLog.log("Waiting for analysis results to be available in Sigrid")

        licenses = self.apiClient.fetchLicenses()

        if "ARCHITECTURE_QUALITY" in licenses:
            self.pollAnalysisResults(lambda: self.isArchitectureReady(start))

        if "SECURITY" in licenses:
            self.pollAnalysisResults(lambda: self.isSecurityReady(start))

        UploadLog.log("Analysis results are now available in Sigrid")

    def pollAnalysisResults(self, operation):
        for i in range(self.pollAttempts):
            if operation():
                return
            time.sleep(self.pollInterval)
        raise Exception("Timeout waiting for analysis results to be available in Sigrid")

    def isArchitectureReady(self, start):
        architectureGraph = self.apiClient.fetchArchitectureGraph()
        analysisDate = datetime.strptime(architectureGraph["metadata"]["analysisDate"], "%Y-%m-%d %H:%M:%S")
        # The architecture analysis date returned by the API is incorrectly
        # based on the Amsterdam time zone instead of UTC.
        analysisDate = analysisDate.replace(tzinfo=ZoneInfo("Europe/Amsterdam")).replace(tzinfo=timezone.utc)
        return analysisDate >= start

    def isSecurityReady(self, start):
        headers = self.apiClient.fetchSecurityHeaders()
        lastRun = headers.get("x-sig-tpf-last-run")
        if not lastRun:
            return False
        analysisDate = datetime.strptime(lastRun, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
        return analysisDate >= start

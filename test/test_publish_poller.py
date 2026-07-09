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

import os
from datetime import datetime, timezone
from unittest import TestCase, mock

from sigridci.sigridci.publish_poller import PublishPoller
from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci.upload_log import UploadLog


class PublishPollerTest(TestCase):

    def setUp(self):
        self.start = datetime.strptime("2026-07-06", "%Y-%m-%d").replace(tzinfo=timezone.utc)
        UploadLog.clear()

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "abcdefg"})
    def testWaitForResults(self):
        poller = PublishPoller(SigridApiStub(["MAINTAINABILITY", "ARCHITECTURE_QUALITY", "SECURITY"], 1, 3))
        poller.pollInterval = 1
        poller.waitForSnapshot(self.start)

        expected = [
            "Using token ending in '****defg'",
            "Waiting for analysis results to be available in Sigrid",
            "Analysis results are now available in Sigrid"
        ]

        self.assertEqual(UploadLog.history, expected)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "abcdefg"})
    def testOnlyPollRelevantLicenses(self):
        poller = PublishPoller(SigridApiStub(["MAINTAINABILITY", "ARCHITECTURE_QUALITY"], 1, 9999))
        poller.pollInterval = 1
        poller.waitForSnapshot(self.start)

        expected = [
            "Using token ending in '****defg'",
            "Waiting for analysis results to be available in Sigrid",
            "Analysis results are now available in Sigrid"
        ]

        self.assertEqual(UploadLog.history, expected)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "abcdefg"})
    def testTimeoutIfItTakesTooLong(self):
        poller = PublishPoller(SigridApiStub(["MAINTAINABILITY", "ARCHITECTURE_QUALITY"], 9999, 9999))
        poller.pollInterval = 1

        expected = [
            "Using token ending in '****defg'",
            "Waiting for analysis results to be available in Sigrid",
            "Analysis results are now available in Sigrid"
        ]

        with self.assertRaises(Exception):
            poller.waitForSnapshot(self.start)
            self.assertEqual(UploadLog.history, expected)


class SigridApiStub(SigridApiClient):
    def __init__(self, licenses, aqAttempts, securityAttempts):
        super().__init__(PublishOptions("aap", "noot", RunMode.PUBLISH_ONLY))
        self.licenses = licenses
        self.aqAttempts = aqAttempts
        self.securityAttempts = securityAttempts

    def fetchLicenses(self):
        return self.licenses

    def fetchArchitectureGraph(self):
        self.aqAttempts -= 1
        analysisDate = "2026-07-01 00:00:00" if self.aqAttempts > 0 else "2026-07-06 00:07:55"
        return {
            "partner": "sig",
            "customer": "aap",
            "system": "noot",
            "snapshot": {
                "id": "20260706",
                "date": "2026-07-06"
            },
            "metadata": {
                "analysisDate": analysisDate
            }
        }

    def fetchSecurityHeaders(self):
        self.securityAttempts -= 1
        analysisDate = "Mon, 01 Jul 2026 00:00:00 GMT" if self.securityAttempts > 0 else "Mon, 06 Jul 2026 21:56:55 GMT"
        return {
            "x-sig-tpf-last-run": analysisDate
        }

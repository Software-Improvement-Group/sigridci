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

import io
import os
import urllib.request
from email.message import Message
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci.upload_log import UploadLog


class SigridApiClientTest(TestCase):

    def tearDown(self):
        UploadLog.clear()

    def testIsValidToken(self):
        self.assertFalse(SigridApiClient.isValidToken(None))
        self.assertFalse(SigridApiClient.isValidToken(""))
        self.assertFalse(SigridApiClient.isValidToken("$"))
        self.assertTrue(SigridApiClient.isValidToken("zeiYh/WYQ==" * 10))

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testStripTrailingWhitespaxceFromToken(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp")
        apiClient = SigridApiClient(options)

        self.assertEqual("mytoken", apiClient.token)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testAddSubsystemParameter(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", subsystem="mies")
        apiClient = ApiStub(options)
        apiClient.obtainUploadLocation(True)

        self.assertEqual(apiClient.called, ["/inboundresults/sig/aap/noot/ci/uploads/v1/publishonly?subsystem=mies"])

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testAddConvertParameter(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", convert="beinformed")
        apiClient = ApiStub(options)
        apiClient.obtainUploadLocation(True)

        self.assertEqual(apiClient.called, ["/inboundresults/sig/aap/noot/ci/uploads/v1/publishonly?convert=beinformed"])

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testAddConvertParameter(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", convert="beinformed", subsystem="mies")
        apiClient = ApiStub(options)
        apiClient.obtainUploadLocation(True)

        self.assertEqual(apiClient.called, ["/inboundresults/sig/aap/noot/ci/uploads/v1/publishonly?subsystem=mies&convert=beinformed"])

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testLogToken(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", showUploadContents=True)
        ApiStub(options)

        self.assertEqual(["Using token ending in '****oken'"], UploadLog.history)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testErrorHandlerNoHeadersNorBody(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", showUploadContents=True)
        apiClient = SigridApiClient(options)
        error = urllib.request.HTTPError("https://example.com", 401, "No reason", Message(), None)
        with self.assertRaises(SystemExit):
            apiClient.handleError(error, "Sigrid")

        self.assertIn("You are not authenticated to Sigrid (HTTP status 401 for https://example.com), please check if your token is valid", UploadLog.history)
        self.assertIn("Response headers:\n\n", UploadLog.history)
        self.assertIn("Response body:\n", UploadLog.history)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testErrorHandlerWithHeadersAndBody(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", showUploadContents=True)
        apiClient = SigridApiClient(options)
        fp = io.BytesIO(b"{}")
        headers = Message()
        headers["aap"] = "noot"
        error = urllib.request.HTTPError("https://example.com", 403, "No reason", headers, fp)
        with self.assertRaises(SystemExit):
            apiClient.handleError(error, "Sigrid")

        self.assertIn("You are not authorized to access Sigrid for this system (HTTP status 403 for https://example.com)", UploadLog.history)
        self.assertIn("Response headers:\naap: noot\n\n", UploadLog.history)
        self.assertIn("Response body:\n{}", UploadLog.history)

    @mock.patch.dict(os.environ, {"SIGRID_CI_TOKEN" : "mytoken\n"})
    def testErrorHandlerWith404(self):
        options = PublishOptions("aap", "noot", runMode=RunMode.PUBLISH_ONLY, sourceDir="/tmp", showUploadContents=True)
        apiClient = SigridApiClient(options)
        error = urllib.request.HTTPError("https://example.com", 404, "No reason", Message(), None)
        apiClient.handleError(error, "Sigrid")

        expectedLog = [
            "Using token ending in '****oken'",
            "HTTP Error 404: No reason",
            "Response headers:\n\n",
            "Response body:\n"
        ]

        self.assertEqual(expectedLog, UploadLog.history)

class ApiStub(SigridApiClient):
    def __init__(self, options: PublishOptions):
        super().__init__(options)
        self.called = []

    def callSigridAPI(self, path, body=None, contentType=None):
        self.called.append(path)

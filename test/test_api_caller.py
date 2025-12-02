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
import urllib.request
from email.message import Message
from unittest import TestCase
from urllib.error import URLError, HTTPError

from sigridci.sigridci.api_caller import ApiCaller
from sigridci.sigridci.upload_log import UploadLog


class ApiCallerTest(TestCase):

    def tearDown(self):
        UploadLog.clear()

    def testErrorHandlerNoHeadersNorBody(self):
        api = ApiCaller("Test", 1)
        error = urllib.request.HTTPError("https://example.com", 401, "No reason", Message(), io.BytesIO(b""))

        with self.assertRaises(SystemExit):
            api.handleError(error)

        self.assertIn("You are not authenticated to Test (HTTP status 401 for https://example.com)", UploadLog.history)
        self.assertIn("No response headers", UploadLog.history)
        self.assertIn("No response body", UploadLog.history)

    def testErrorHandlerWithHeadersAndBody(self):
        api = ApiCaller("Test", 1)
        headers = Message()
        headers["aap"] = "noot"
        error = urllib.request.HTTPError("https://example.com", 403, "No reason", headers, io.BytesIO(b"{}"))

        with self.assertRaises(SystemExit):
            api.handleError(error)

        self.assertIn("You are not authorized to access Test (HTTP status 403 for https://example.com)", UploadLog.history)
        self.assertIn("Response headers:\n{'aap': 'noot'}", UploadLog.history)
        self.assertIn("Response body:\n{}", UploadLog.history)

    def testErrorHandlerWith404(self):
        api = ApiCaller("Test", 1)
        error = urllib.request.HTTPError("https://example.com", 404, "No reason", {}, None)
        api.handleError(error)

        expectedLog = [
            "HTTP Error 404: No reason",
            "No response headers",
            "No response body"
        ]

        self.assertEqual(expectedLog, UploadLog.history)

    def testErrorHandlerWithTimeout(self):
        api = ApiCaller("Test", 1)

        with self.assertRaises(SystemExit):
            api.retryRequest(lambda: self.raiseTimeoutError(), attempts=1)

        expected = [
            "Test did not respond within the timeout period",
            "Test is currently unavailable, failed after 1 attempts"
        ]

        self.assertEqual(expected, UploadLog.history)

    def testErrorHandlerWithUrlError(self):
        api = ApiCaller("Test", 1)

        with self.assertRaises(SystemExit):
            api.retryRequest(lambda: self.raiseUrlError(), attempts=1)

        expected = [
            "Error contacting Test: <urlopen error some reason> (URLError)",
            "Test is currently unavailable, failed after 1 attempts"
        ]

        self.assertEqual(expected, UploadLog.history)

    def testExitOnHttp502(self):
        api = ApiCaller("Test", 1)
        with self.assertRaises(SystemExit):
            api.retryRequest(lambda: self.raiseHttp502(), attempts=1)

    def raiseTimeoutError(self):
        raise TimeoutError()

    def raiseUrlError(self):
        raise URLError("some reason")

    def raiseHttp502(self):
        raise HTTPError("", 502, "", None, None)

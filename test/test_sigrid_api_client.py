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
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.sigrid_api_client import SigridApiClient


class SigridApiClientTest(TestCase):

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

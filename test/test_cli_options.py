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

from unittest import TestCase

from sigridci.sigridci.capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY
from sigridci.sigridci.cli_options import parseCapabilities


class CliOptionsTest(TestCase):

    def testParseCapabilities(self):
        self.assertEqual(parseCapabilities("maintainability"), [MAINTAINABILITY])
        self.assertEqual(parseCapabilities("osh"), [OPEN_SOURCE_HEALTH])
        self.assertEqual(parseCapabilities("maintainability,security"), [MAINTAINABILITY, SECURITY])

    def testErrorOnInvalidCapability(self):
        with self.assertRaises(SystemExit):
            parseCapabilities("invalid")

    def testDisableCapabilities(self):
        self.assertEqual(parseCapabilities("maintainability,security", None), [MAINTAINABILITY, SECURITY])
        self.assertEqual(parseCapabilities("maintainability,security", ""), [MAINTAINABILITY, SECURITY])
        self.assertEqual(parseCapabilities("maintainability,security", "security"), [MAINTAINABILITY])

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

import tempfile
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode


class PublishOptionsTest(TestCase):

    def testLocateScopeFile(self):
        tempDir = tempfile.mkdtemp()
        with open(f"{tempDir}/sigrid.yaml", "w") as f:
            f.write("component_depth: 2\n")

        options = self.toOptions("aap", "noot", tempDir)

        self.assertEqual("component_depth: 2", options.readScopeFile().strip())

    def testReturnNoneIfThereIsNoScopeFile(self):
        tempDir = tempfile.mkdtemp()
        options = self.toOptions("aap", "noot", tempDir)

        self.assertIsNone(options.readScopeFile())

    def testValidateSystemNameAccordingToRules(self):
        self.assertTrue(self.toOptions("noot", "aap").isValidSystemName())
        self.assertTrue(self.toOptions("noot", "aap-noot").isValidSystemName())
        self.assertTrue(self.toOptions("noot", "aap123").isValidSystemName())
        self.assertTrue(self.toOptions("noot", "AAP").isValidSystemName())
        self.assertTrue(self.toOptions("noot", "a" * 59).isValidSystemName())
        self.assertTrue(self.toOptions("noot", "aa").isValidSystemName())

        self.assertFalse(self.toOptions("noot", "aap_noot").isValidSystemName())
        self.assertFalse(self.toOptions("noot", "a").isValidSystemName())
        self.assertFalse(self.toOptions("noot", "$$$").isValidSystemName())
        self.assertFalse(self.toOptions("noot", "-aap").isValidSystemName())
        self.assertFalse(self.toOptions("noot", "a" * 65).isValidSystemName())
        self.assertFalse(self.toOptions("noot", "aap--aap").isValidSystemName())
        self.assertFalse(self.toOptions("noot", "20230222").isValidSystemName())

    def testValidateSubSystemNameAccordingToRules(self):
        # insert logic to test isValidSubSystemName according to the rules
        pass

    def toOptions(self, customer, system, tempDir="/tmp"):
        return PublishOptions(customer, system, RunMode.FEEDBACK_ONLY, tempDir)

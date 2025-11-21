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
        self.assertTrue(self.toOptions("aap", "noot").isValidSystemName())
        self.assertTrue(self.toOptions("aap", "aap-noot").isValidSystemName())
        self.assertTrue(self.toOptions("aap", "noot123").isValidSystemName())
        self.assertTrue(self.toOptions("aap", "NOOT").isValidSystemName())
        self.assertTrue(self.toOptions("aap", "n"*59).isValidSystemName())
        self.assertTrue(self.toOptions("aap", "nn").isValidSystemName())

        self.assertFalse(self.toOptions("aap", "aap_noot").isValidSystemName())
        self.assertFalse(self.toOptions("aap", "n").isValidSystemName())
        self.assertFalse(self.toOptions("aap", "$$$").isValidSystemName())
        self.assertFalse(self.toOptions("aap", "-noot").isValidSystemName())
        self.assertFalse(self.toOptions("aap", "n"*65).isValidSystemName())
        self.assertFalse(self.toOptions("aap", "noot--noot").isValidSystemName())
        self.assertFalse(self.toOptions("aap", "20230222").isValidSystemName())

    def testValidateSubSystemNameAccordingToRules(self):
        self.assertTrue(self.toOptions("noot", "aap", "sub.system-1/part").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "a").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "A1._-/b").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "subsystem").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "sub.system/part-name").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "subsystem123").isValidSubSystemName())
        self.assertTrue(self.toOptions("noot", "aap", "SUBSYSTEM").isValidSubSystemName())
        
        self.assertFalse(self.toOptions("noot", "aap", ".subsystem").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", "subsystem.").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", "subsystem123!").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", "sub..system").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", "sub system").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", ".").isValidSubSystemName())
        self.assertFalse(self.toOptions("noot", "aap", "sub//system").isValidSubSystemName())

    def toOptions(self, customer, system, tempDir="/tmp"):
        return PublishOptions(customer, system, RunMode.FEEDBACK_ONLY, tempDir)

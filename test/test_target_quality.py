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
import unittest
from sigridci.sigridci import TargetQuality


class TargetQualityTest(unittest.TestCase):

    def testNormalModeOnlyRequiresOverallRatingToMeetTarget(self):
        target = TargetQuality("/tmp/nonexistent", 3.5)

        self.assertFalse(target.meetsQualityTargets({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertTrue(target.meetsQualityTargets({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertTrue(target.meetsQualityTargets({"newCodeRatings" : {"DUPLICATION" : 2}}))
        
    def testTargetsForSpecificSystemProperties(self):
        target = TargetQuality("/tmp/nonexistent", 4)
        target.ratings["DUPLICATION"] = 4

        self.assertFalse(target.meetsQualityTargets({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertFalse(target.meetsQualityTargets({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertFalse(target.meetsQualityTargets({"newCodeRatings" : {"DUPLICATION" : 2}}))
        self.assertTrue(target.meetsQualityTargets({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 4}}))
        self.assertTrue(target.meetsQualityTargets({"newCodeRatings" : {"DUPLICATION" : 5}}))
        
    def testUseTargetRatingIfNoConfigFileExists(self):
        sourceDir = tempfile.mkdtemp()
        configFile = f"{sourceDir}/sigrid.yaml"
        target = TargetQuality(configFile, 3.5)
        
        self.assertEqual(target.ratings.get("MAINTAINABILITY", None), 3.5)
        self.assertEqual(target.ratings.get("DUPLICATION", None), None)
        
    def testLoadTargetsFromConfigFile(self):
        yaml = """
            sigridci:
              target:
                maintainability: 4.0
                DUPLICATION: 3
        """
    
        sourceDir = tempfile.mkdtemp()
        configFile = self.createTempFile(sourceDir, "sigrid.yaml", yaml)
        target = TargetQuality(configFile, 3.5)
        
        self.assertEqual(target.ratings.get("MAINTAINABILITY", None), 4.0)
        self.assertEqual(target.ratings.get("DUPLICATION", None), 3.0)
        self.assertEqual(target.ratings.get("UNIT_SIZE", None), None)

    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"

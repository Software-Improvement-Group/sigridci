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
import tempfile
import types
import unittest
import urllib
import zipfile
from sigridci.sigridci import SigridApiClient, Report, TextReport, UploadOptions, TargetQuality, LOG_HISTORY, SYSTEM_NAME_PATTERN


class SigridCiTest(unittest.TestCase):
    
    DEFAULT_ARGS = types.SimpleNamespace(partner="sig", customer="Aap", system="NOOT", sigridurl="", \
                                         publish=False, publishonly=False)

    def setUp(self):
        os.environ["SIGRID_CI_ACCOUNT"] = "dummy"
        os.environ["SIGRID_CI_TOKEN"] = "dummy"
        LOG_HISTORY.clear()

    def testForceLowerCaseForCustomerAndSystemName(self):
        args = types.SimpleNamespace(partner="sig", customer="Aap", system="NOOT", sigridurl="", publish=False, publishonly=False)
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.urlCustomerName, "aap")
        self.assertEqual(apiClient.urlSystemName, "noot")
        
    def testFeedbackTemplateOnlyContainsAsciiCharacters(self):
        with open("sigridci/sigridci-feedback-template.html", mode="r", encoding="ascii") as templateRef:
            template = templateRef.read()
            
    def testDoNotThrowExeptionFor404(self):
        apiClient = SigridApiClient(self.DEFAULT_ARGS)
        apiClient.processHttpError(urllib.error.HTTPError("http://www.sig.eu", 404, "", {}, None))
            
    def testDoThrowExceptionForClientError(self):
        apiClient = SigridApiClient(self.DEFAULT_ARGS)
        
        self.assertRaises(Exception, apiClient.processHttpError, \
            urllib.error.HTTPError("http://www.sig.eu", 400, "", {}, None), True)
            
    def testGetRefactoringCandidatesForNewFormat(self):
        feedback = {
            "refactoringCandidates": [{"subject":"a/b.java::Duif.vuur()","category":"introduced","metric":"UNIT_SIZE"}]
        }
        
        report = Report()
        unitSize = report.getRefactoringCandidates(feedback, "UNIT_SIZE")
        
        self.assertEqual(len(unitSize), 1)
        self.assertEqual(unitSize[0]["subject"], "a/b.java::Duif.vuur()")
            
    def testRegularUploadPathDoesNotPublishByDefault(self):
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", sigridurl="https://example.com", \
            publish=False, publishonly=False)
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.getRequestUploadPath(True), "/sig/aap/noot/ci/uploads/v1")
        
    def testPublishOptionChangesUploadPath(self):
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", sigridurl="https://example.com", \
            publish=True, publishonly=False)
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.getRequestUploadPath(True), "/sig/aap/noot/ci/uploads/v1/publish")
        
    def testFormatBaseline(self):
        report = Report()

        self.assertEqual(report.formatBaseline({"baseline" : "20211015"}), "2021-10-15")
        self.assertEqual(report.formatBaseline({"baseline" : None}), "N/A")
        self.assertEqual(report.formatBaseline({"baseline" : ""}), "N/A")
        self.assertEqual(report.formatBaseline({}), "N/A")
        
    def testNormalModeOnlyRequiresOverallRatingToMeetTarget(self):
        target = TargetQuality("/tmp/nonexistent", 3.5)

        self.assertFalse(target.meetsOverallQualityTarget({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertTrue(target.meetsOverallQualityTarget({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertTrue(target.meetsOverallQualityTarget({"newCodeRatings" : {"DUPLICATION" : 2}}))
        
    def testTargetsForSpecificSystemProperties(self):
        target = TargetQuality("/tmp/nonexistent", 4)
        target.ratings["DUPLICATION"] = 4

        self.assertFalse(target.meetsOverallQualityTarget({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertFalse(target.meetsOverallQualityTarget({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertFalse(target.meetsOverallQualityTarget({"newCodeRatings" : {"DUPLICATION" : 2}}))
        self.assertTrue(target.meetsOverallQualityTarget({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 4}}))
        self.assertTrue(target.meetsOverallQualityTarget({"newCodeRatings" : {"DUPLICATION" : 5}}))
        
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
    
    def validateSystemNameAccordingToRules(self):
        self.assertTrue(SYSTEM_NAME_PATTERN.match("aap"))
        self.assertTrue(SYSTEM_NAME_PATTERN.match("aap-noot"))
        self.assertTrue(SYSTEM_NAME_PATTERN.match("aap123"))
        
        self.assertFalse(SYSTEM_NAME_PATTERN.match("aap_noot"))
        self.assertFalse(SYSTEM_NAME_PATTERN.match("a"))
        self.assertFalse(SYSTEM_NAME_PATTERN.match("$$$"))

    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"
    
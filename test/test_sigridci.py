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
from sigridci.sigridci import SystemUploadPacker, SigridApiClient, Report, TextReport, UploadOptions, \
                              TargetQuality, LOG_HISTORY


class SigridCiTest(unittest.TestCase):
    
    DEFAULT_ARGS = types.SimpleNamespace(partner="sig", customer="Aap", system="NOOT", sigridurl="", \
                                         publish=False, publishonly=False)

    def setUp(self):
        os.environ["SIGRID_CI_ACCOUNT"] = "dummy"
        os.environ["SIGRID_CI_TOKEN"] = "dummy"

    def testCreateZipFromDirectory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        self.createTempFile(sourceDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.prepareUpload(sourceDir, outputFile)

        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()    

        self.assertEqual(entries, ["a.py", "b.py"])

    def testPreserveDirectoryStructureInUpload(self):
        sourceDir = tempfile.mkdtemp()
        subDirA = sourceDir + "/a"
        os.mkdir(subDirA)
        self.createTempFile(subDirA, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.prepareUpload(sourceDir, outputFile)
        
        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(entries, ["a/a.py", "b/b.py"])
        
    def testDefaultExcludePatterns(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDir = sourceDir + "/node_modules"
        os.mkdir(subDir)
        self.createTempFile(subDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.prepareUpload(sourceDir, outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(zipfile.ZipFile(outputFile).namelist(), ["a.py"])
        
    def testCustomExcludePatterns(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDir = sourceDir + "/b"
        os.mkdir(subDir)
        self.createTempFile(subDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(excludePatterns=["b/"]))
        uploadPacker.prepareUpload(sourceDir, outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(zipfile.ZipFile(outputFile).namelist(), ["a.py"])
        
    def testIncludeGitHistory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDir = sourceDir + "/.git"
        os.mkdir(subDir)
        self.createTempFile(subDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(includeHistory=True))
        uploadPacker.prepareUpload(sourceDir, outputFile)
        
        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()

        self.assertEqual(entries, [".git/b.py", "a.py"])
        
    def testExcludeGitHistory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDir = sourceDir + "/.git"
        os.mkdir(subDir)
        self.createTempFile(subDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(includeHistory=False))
        uploadPacker.prepareUpload(sourceDir, outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(zipfile.ZipFile(outputFile).namelist(), ["a.py"])
        
    def testErrorIfUploadExceedsMaximumSize(self):
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(2000000))
            
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.MAX_UPLOAD_SIZE_MB = 1
    
        self.assertRaises(Exception, uploadPacker.prepareUpload, sourceDir, tempfile.mkstemp()[1])
        
    def testLogMessageWhenUploadTooSmall(self):
        LOG_HISTORY.clear()
    
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(1))
            
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.prepareUpload(sourceDir, tempfile.mkstemp()[1])

        self.assertEqual(LOG_HISTORY, ["Upload size is 1 MB", \
            "Warning: Upload is very small, source directory might not contain all source code"])
            
    def testLogUploadContents(self):
        LOG_HISTORY.clear()
    
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(1))
        with open(sourceDir + "/b.py", "wb") as f:
            f.write(os.urandom(1))
            
        uploadPacker = SystemUploadPacker(UploadOptions(showContents=True))
        uploadPacker.prepareUpload(sourceDir, tempfile.mkstemp()[1])

        self.assertEqual(LOG_HISTORY, ["Adding file to upload: a.py", "Adding file to upload: b.py", \
            "Upload size is 1 MB", \
            "Warning: Upload is very small, source directory might not contain all source code"])
        
    def testUsePathPrefixInUpload(self):
        sourceDir = tempfile.mkdtemp()
        subDirA = sourceDir + "/a"
        os.mkdir(subDirA)
        self.createTempFile(subDirA, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(pathPrefix="frontend"))
        uploadPacker.prepareUpload(sourceDir, outputFile)
        
        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(entries, ["frontend/a/a.py", "frontend/b/b.py"])
        
    def testPathPrefixDoesNotLeadToDoubleSlash(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(pathPrefix="/backend/"))
        uploadPacker.prepareUpload(sourceDir, outputFile)
        
        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(entries, ["backend/a.py"])
        
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
        
    def testFormatTextRefactoringCandidate(self):
        rc1 = {"subject" : "aap", "category" : "introduced", "metric" : "UNIT_SIZE"}
        rc2 = {"subject" : "noot\nmies", "category" : "worsened", "metric" : "DUPLICATION"}
        rc3 = {"subject" : "noot::mies", "category" : "worsened", "metric" : "UNIT_SIZE"}
        
        report = TextReport()
        
        self.assertEqual(report.formatRefactoringCandidate(rc1), \
            "    - (introduced)   aap")
        
        self.assertEqual(report.formatRefactoringCandidate(rc2), \
            "    - (worsened)     noot\n                     mies")
            
        self.assertEqual(report.formatRefactoringCandidate(rc3), \
            "    - (worsened)     noot\n                     mies")
            
    def testRegularUploadPathDoesNotPublishByDefault(self):
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", sigridurl="https://example.com", \
            publish=False, publishonly=False)
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.getRequestUploadPath(), "/sig/aap/noot/ci/uploads/v1")
        
    def testPublishOptionChangesUploadPath(self):
        args = types.SimpleNamespace(partner="sig", customer="aap", system="noot", sigridurl="https://example.com", \
            publish=True, publishonly=False)
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.getRequestUploadPath(), "/sig/aap/noot/ci/uploads/v1/publish")
        
    def testFormatBaseline(self):
        report = Report()

        self.assertEqual(report.formatBaseline({"baseline" : "20211015"}), "2021-10-15")
        self.assertEqual(report.formatBaseline({"baseline" : None}), "N/A")
        self.assertEqual(report.formatBaseline({"baseline" : ""}), "N/A")
        self.assertEqual(report.formatBaseline({}), "N/A")
        
    def testNormalModeOnlyRequiresOverallRatingToMeetTarget(self):
        target = TargetQuality("/tmp/nonexistent", 3.5)

        self.assertFalse(target.isOverallPassed({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertTrue(target.isOverallPassed({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertTrue(target.isOverallPassed({"newCodeRatings" : {"DUPLICATION" : 2}}))
        
    def testTargetsForSpecificSystemProperties(self):
        target = TargetQuality("/tmp/nonexistent", 4)
        target.ratings["DUPLICATION"] = 4

        self.assertFalse(target.isOverallPassed({"newCodeRatings" : {"MAINTAINABILITY" : 3, "DUPLICATION" : 2}}))
        self.assertFalse(target.isOverallPassed({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 2}}))
        self.assertFalse(target.isOverallPassed({"newCodeRatings" : {"DUPLICATION" : 2}}))
        self.assertTrue(target.isOverallPassed({"newCodeRatings" : {"MAINTAINABILITY" : 4, "DUPLICATION" : 4}}))
        self.assertTrue(target.isOverallPassed({"newCodeRatings" : {"DUPLICATION" : 5}}))
        
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
        writer = open(dir + "/" + name, "w")
        writer.write(contents)
        writer.close()
        return dir + "/" + name
    
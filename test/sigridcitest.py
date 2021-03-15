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
import zipfile
from sigridci.sigridci import SystemUploadPacker, SigridApiClient

class SigridCiTest(unittest.TestCase):

    def testCreateZipFromDirectory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        self.createTempFile(sourceDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker()
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
        
        uploadPacker = SystemUploadPacker()
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
        
        uploadPacker = SystemUploadPacker()
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
        
        uploadPacker = SystemUploadPacker(["b/"])
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
        
        uploadPacker = SystemUploadPacker([], True)
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
        
        uploadPacker = SystemUploadPacker([], False)
        uploadPacker.prepareUpload(sourceDir, outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(zipfile.ZipFile(outputFile).namelist(), ["a.py"])
        
    def testErrorIfUploadExceedsMaximumSize(self):
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(2000000))

        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker()
        uploadPacker.MAX_UPLOAD_SIZE_MB = 1
    
        self.assertRaises(Exception, uploadPacker.prepareUpload, sourceDir, outputFile)
        
    def testForceLowerCaseForCustomerAndSystemName(self):
        args = types.SimpleNamespace(partner="sig", customer="Aap", system="NOOT", sigridurl="")
        apiClient = SigridApiClient(args)
        
        self.assertEqual(apiClient.urlCustomerName, "aap")
        self.assertEqual(apiClient.urlSystemName, "noot")
        
    def testFeedbackTemplateOnlyContainsAsciiCharacters(self):
        with open("sigridci/sigridci-feedback-template.html", mode="r", encoding="ascii") as templateRef:
            template = templateRef.read()

    def createTempFile(self, dir, name, contents):
        writer = open(dir + "/" + name, "w")
        writer.write(contents)
        writer.close()
        return dir + "/" + name
    
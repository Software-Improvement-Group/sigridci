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
import subprocess
import unittest
import zipfile
from sigridci.sigridci import SystemUploadPacker, UploadOptions, LOG_HISTORY

class SystemUploadPackerTest(unittest.TestCase):

    def setUp(self):
        LOG_HISTORY.clear()

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
        
    def testExcludeDollarTfDirectories(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "z.py", "z")
        subDir = sourceDir + "/$tf"
        os.mkdir(subDir)
        self.createTempFile(subDir, "a.py", "a")
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions())
        uploadPacker.prepareUpload(sourceDir, outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(zipfile.ZipFile(outputFile).namelist(), ["z.py"])
        
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
        tempDir = tempfile.mkdtemp()
        subprocess.call(["git", "clone", "https://github.com/BetterCodeHubTraining/cspacman.git", tempDir])
        
        outputFile = tempfile.mkstemp()[1]
        
        uploadPacker = SystemUploadPacker(UploadOptions(excludePatterns="", includeHistory=True))
        uploadPacker.prepareUpload(tempDir, outputFile)
        
        entries = zipfile.ZipFile(outputFile).namelist()
        entries.sort()

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertIn("git.log", entries)
        
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
           
    def testLogUploadContents(self):
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(1))
        with open(sourceDir + "/b.py", "wb") as f:
            f.write(os.urandom(1))
            
        uploadPacker = SystemUploadPacker(UploadOptions(showContents=True))
        uploadPacker.prepareUpload(sourceDir, tempfile.mkstemp()[1])
        
        expected = [
            "Adding file to upload: a.py", 
            "Adding file to upload: b.py", 
            "Upload size is 1 MB", 
            "Warning: Upload is very small, source directory might not contain all source code"
        ]

        self.assertEqual(LOG_HISTORY, expected)
        
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

    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"
    
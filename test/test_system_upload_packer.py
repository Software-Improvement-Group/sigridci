# Copyright Software Improvement Group
# Copyright Alliander N.V.
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
from unittest import TestCase
from zipfile import ZipFile

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.system_upload_packer import SystemUploadPacker
from sigridci.sigridci.upload_log import UploadLog


class SystemUploadPackerTest(TestCase):

    def setUp(self):
        UploadLog.clear()

    def testCreateZipFromDirectory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        self.createTempFile(sourceDir, "b.py", "b")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        entries = ZipFile(outputFile).namelist()
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

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)
        
        entries = ZipFile(outputFile).namelist()
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

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(ZipFile(outputFile).namelist(), ["a.py"])
        
    def testExcludeDollarTfDirectories(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "z.py", "z")
        subDir = sourceDir + "/$tf"
        os.mkdir(subDir)
        self.createTempFile(subDir, "a.py", "a")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(ZipFile(outputFile).namelist(), ["z.py"])
        
    def testCustomExcludePatterns(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")

        subDirC = sourceDir + "/c"
        os.mkdir(subDirC)
        self.createTempFile(subDirC, "c.py", "c")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, excludePatterns=["b/b.py"])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["a.py", "c/c.py"])

    def testEmptyStringExcludePattern(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")
        subDirC = sourceDir + "/c"
        os.mkdir(subDirC)
        self.createTempFile(subDirC, "c.py", "c")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, excludePatterns=[""])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["a.py", "b/b.py", "c/c.py"])

    def testEmptyStringIncludePattern(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")
        subDirC = sourceDir + "/c"
        os.mkdir(subDirC)
        self.createTempFile(subDirC, "c.py", "c")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, includePatterns=[""])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["a.py", "b/b.py", "c/c.py"])

    def testCustomIncludePatterns(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")

        subDirC = sourceDir + "/c"
        os.mkdir(subDirC)
        self.createTempFile(subDirC, "c.py", "c")

        subDirD = sourceDir + "/d"
        os.mkdir(subDirD)
        self.createTempFile(subDirD, "d.py", "d")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, includePatterns=["/c/", "/d/"])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["c/c.py", "d/d.py"])

    def testCustomIncludeAndExcludePatterns(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        subDirB = sourceDir + "/b"
        os.mkdir(subDirB)
        self.createTempFile(subDirB, "b.py", "b")

        subDirC = subDirB + "/c"
        os.mkdir(subDirC)
        self.createTempFile(subDirC, "c.py", "c")

        subDirD = subDirB + "/d"
        os.mkdir(subDirD)
        self.createTempFile(subDirD, "d.py", "d")
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir,
                                 includePatterns=["/b/"], excludePatterns=["/d/"])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["b/b.py", "b/c/c.py"])

    def testIncludePatternShouldStillIncludeGitHistory(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "a")
        self.createTempFile(sourceDir, "b.py", "b")
        self.createTempFile(sourceDir, "git.log", "something")

        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, includePatterns=["a.py"])
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(sorted(ZipFile(outputFile).namelist()), ["a.py", "git.log"])

    def testIncludeGitHistory(self):
        tempDir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "https://github.com/BetterCodeHubTraining/cspacman.git", tempDir])
        
        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, tempDir, includeHistory=True)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)
        
        entries = ZipFile(outputFile).namelist()
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

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, includeHistory=False)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(ZipFile(outputFile).namelist(), ["a.py"])
        
    def testErrorIfUploadExceedsMaximumSize(self):
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(2000000))

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.MAX_UPLOAD_SIZE_MB = 1
    
        self.assertRaises(Exception, uploadPacker.prepareUpload, sourceDir, tempfile.mkstemp()[1])
           
    def testLogUploadContents(self):
        sourceDir = tempfile.mkdtemp()
        with open(sourceDir + "/a.py", "wb") as f:
            f.write(os.urandom(1))
        with open(sourceDir + "/b.py", "wb") as f:
            f.write(os.urandom(1))

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir, showUploadContents=True)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(tempfile.mkstemp()[1])
        
        expected = [
            "Adding file to upload: a.py", 
            "Adding file to upload: b.py", 
            "Upload size is 1 MB", 
            "Warning: Upload is very small, source directory might not contain all source code"
        ]

        self.assertEqual(UploadLog.history, expected)

    def testExcludeFileExtensions(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "")
        self.createTempFile(sourceDir, "b.zip", "")
        self.createTempFile(sourceDir, "c.tar", "")

        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(ZipFile(outputFile).namelist(), ["a.py"])


    def testInvalidSymlink(self):
        sourceDir = tempfile.mkdtemp()
        self.createTempFile(sourceDir, "a.py", "")
        os.symlink(sourceDir + "/a.py", sourceDir + "/link-to-a.py")
        os.symlink(sourceDir + "/b.py", sourceDir + "/link-to-nonexisting-b.py")

        outputFile = tempfile.mkstemp()[1]

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir)
        uploadPacker = SystemUploadPacker(options)
        uploadPacker.prepareUpload(outputFile)

        self.assertEqual(os.path.exists(outputFile), True)
        self.assertEqual(ZipFile(outputFile).namelist(), ["a.py", "link-to-a.py"])

    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"

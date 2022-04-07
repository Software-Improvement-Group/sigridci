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
import unittest
import urllib
from sigridci.sigridci import SigridApiClient, SigridCiRunner, UploadOptions, TargetQuality, LOG_HISTORY

class SigridCiRunnerTest(unittest.TestCase):

    def setUp(self):
        os.environ["SIGRID_CI_ACCOUNT"] = "dummy"
        os.environ["SIGRID_CI_TOKEN"] = "dummy"
        LOG_HISTORY.clear()

    def testRegularRun(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(publish=False)
        
        runner = SigridCiRunner()
        runner.run(apiClient, options, target, [])

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Submitting upload"
        ]
        
        expectedCalls = [
            "analysis-results/sigridci/aap/noot/v1/ci", 
            "inboundresults/sig/aap/noot/ci/uploads/v1", 
            "UPLOAD",
            "analysis-results/sigridci/aap/noot/v1/ci/results/123"
        ]

        self.assertEqual(LOG_HISTORY, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)
        
    def testPublishRun(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir, publishOnly=False)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(publish=True)
        
        runner = SigridCiRunner()
        runner.run(apiClient, options, target, [])

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Publishing upload"
        ]
        
        expectedCalls = [
            "analysis-results/sigridci/aap/noot/v1/ci", 
            "inboundresults/sig/aap/noot/ci/uploads/v1/publish", 
            "UPLOAD",
            "analysis-results/sigridci/aap/noot/v1/ci/results/123"
        ]

        self.assertEqual(LOG_HISTORY, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)
        
    def testPublishOnlyRun(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir, publishOnly=True)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(publish=True)
        
        runner = SigridCiRunner()
        runner.run(apiClient, options, target, [])

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Publishing upload",
            "Your project's source code has been published to Sigrid"
        ]
        
        expectedCalls = [
            "analysis-results/sigridci/aap/noot/v1/ci", 
            "inboundresults/sig/aap/noot/ci/uploads/v1/publish", 
            "UPLOAD"
        ]

        self.assertEqual(LOG_HISTORY, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)
        
    def testOnBoardingRun(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(systemExists=False)
        
        runner = SigridCiRunner()
        runner.run(apiClient, options, target, [])

        expectedLog = [
            "System is not yet on-boarded to Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "System 'noot' is on-boarded to Sigrid, and will appear in sigrid-says.com shortly"
        ]
        
        expectedCalls = [
            "analysis-results/sigridci/aap/noot/v1/ci", 
            "inboundresults/sig/aap/noot/ci/uploads/v1/onboarding", 
            "UPLOAD"
        ]

        self.assertEqual(LOG_HISTORY, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)
        
    def testExitWithMessageIfUploadEmpty(self):
        tempDir = tempfile.mkdtemp()    
        options = UploadOptions(sourceDir=tempDir)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(systemExists=False)
        
        runner = SigridCiRunner()
        with self.assertRaises(SystemExit):
            runner.run(apiClient, options, target, [])
            
    def testRetryIfUploadFailsTheFirstTime(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(systemExists=True, uploadAttempts=3)
        
        runner = SigridCiRunner()
        runner.run(apiClient, options, target, [])

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Retrying upload",
            "Retrying upload"
        ]

        self.assertEqual(LOG_HISTORY, expectedLog)
    
    def testExitIfUploadKeepsFailing(self):
        tempDir = tempfile.mkdtemp()    
        self.createTempFile(tempDir, "a.py", "print(123)")
        
        options = UploadOptions(sourceDir=tempDir)
        target = TargetQuality("/tmp/nonexistent", 3.5)
        apiClient = MockApiClient(systemExists=True, uploadAttempts=99)
        runner = SigridCiRunner()
        
        expectedLog = [
            "Found system in Sigrid",
            "Creating upload", 
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload", 
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Retrying upload",
            "Retrying upload",
            "Retrying upload"
            "Sigrid is currently unavailable"
        ]
        
        with self.assertRaises(SystemExit):
            runner.run(apiClient, options, target, [])
        self.assertEqual(LOG_HISTORY, expectedLog)
        
    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"
        
        
class MockApiClient(SigridApiClient):
    def __init__(self, publish=False, systemExists=True, uploadAttempts=0):
        self.called = []
        self.urlPartnerName = "sig"
        self.urlCustomerName = "aap"
        self.urlSystemName = "noot"
        self.publish = publish
        self.systemExists = systemExists
        self.uploadAttempts = uploadAttempts
        self.attempt = 0
        self.POLL_INTERVAL = 1

    def callSigridAPI(self, api, path):
        self.called.append(f"{api}{path}")
    
        if not self.systemExists and path == "/sigridci/aap/noot/v1/ci":
            # Mock a HTTP 404.
            raise urllib.error.HTTPError(path, 404, "", {}, None)
        
        return {
            "ciRunId" : "123",
            "uploadUrl" : "dummy"
        }
        
    def attemptUpload(self, url, upload):
        self.attempt += 1
        if self.attempt >= self.uploadAttempts:            
            self.called.append("UPLOAD")
            return True
        else:
            raise urllib.error.HTTPError("/upload", 500, "", {}, None)
     
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
import urllib.error
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci.sigridci_runner import SigridCiRunner
from sigridci.sigridci.upload_log import UploadLog


class SigridCiRunnerTest(TestCase):

    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, self.tempDir, targetRating=3.5)

        UploadLog.clear()

        os.environ["SIGRID_CI_ACCOUNT"] = "dummy"
        os.environ["SIGRID_CI_TOKEN"] = "dummy"
        os.environ["externalid"] = ""
        os.environ["divisionname"] = ""
        os.environ["suppliernames"] = ""
        os.environ["teamnames"] = ""

    def testForceLowerCaseForCustomerAndSystemName(self):
        self.options.customer = "Aap"
        self.options.system = "NOOT"

        apiClient = SigridApiClient(self.options)

        self.assertEqual(apiClient.urlCustomerName, "aap")
        self.assertEqual(apiClient.urlSystemName, "noot")

    def testRegularRun(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Upload successful",
            "Waiting for analysis results"
        ]

        expectedCalls = [
            "/analysis-results/sigridci/aap/noot/v1/ci",
            "/inboundresults/sig/aap/noot/ci/uploads/v1",
            "UPLOAD",
            "/analysis-results/sigridci/aap/noot/v1/ci/results/123",
            "/analysis-results/api/v1/system-metadata/aap/noot"
        ]

        self.assertEqual(UploadLog.history, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)

    def testPublishRun(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        self.options.runMode = RunMode.FEEDBACK_AND_PUBLISH

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Publishing upload",
            "Upload successful",
            "Waiting for analysis results"
        ]

        expectedCalls = [
            "/analysis-results/sigridci/aap/noot/v1/ci",
            "/inboundresults/sig/aap/noot/ci/uploads/v1/publish",
            "UPLOAD",
            "/analysis-results/sigridci/aap/noot/v1/ci/results/123",
            "/analysis-results/api/v1/system-metadata/aap/noot"
        ]

        self.assertEqual(UploadLog.history, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)

    def testPublishOnlyRun(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        self.options.runMode = RunMode.PUBLISH_ONLY

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Publishing upload",
            "Upload successful",
            "Your project's source code has been published to Sigrid"
        ]

        expectedCalls = [
            "/analysis-results/sigridci/aap/noot/v1/ci",
            "/inboundresults/sig/aap/noot/ci/uploads/v1/publishonly",
            "UPLOAD",
            "/analysis-results/api/v1/system-metadata/aap/noot"
        ]

        self.assertEqual(UploadLog.history, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)

    def testOnBoardingRun(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        apiClient = MockApiClient(self.options, systemExists=False)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "System is not yet on-boarded to Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Upload successful",
            "System 'noot' has been on-boarded and will appear in Sigrid shortly"
        ]

        expectedCalls = [
            "/analysis-results/sigridci/aap/noot/v1/ci",
            "/inboundresults/sig/aap/noot/ci/uploads/v1/onboarding",
            "UPLOAD"
        ]

        self.assertEqual(UploadLog.history, expectedLog)
        self.assertEqual(apiClient.called, expectedCalls)

    def testAddSubsystemOptionToUrl(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        self.options.subsystem = "mysubsystem"
        self.options.runMode = RunMode.FEEDBACK_AND_PUBLISH

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedCalls = [
            "/analysis-results/sigridci/aap/noot/v1/ci",
            "/inboundresults/sig/aap/noot/ci/uploads/v1/publish?subsystem=mysubsystem",
            "UPLOAD",
            "/analysis-results/sigridci/aap/noot/v1/ci/results/123",
            "/analysis-results/api/v1/system-metadata/aap/noot"
        ]

        self.assertEqual(apiClient.called, expectedCalls)

    def testExitWithMessageIfUploadEmpty(self):
        apiClient = MockApiClient(self.options, systemExists=False)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []

        with self.assertRaises(SystemExit):
            runner.run()

    def testRetryIfUploadFailsTheFirstTime(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        apiClient = MockApiClient(self.options, systemExists=True, uploadAttempts=3)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Retrying",
            "Retrying",
            "Upload successful",
            "Waiting for analysis results"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testExitIfUploadKeepsFailing(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        apiClient = MockApiClient(self.options, systemExists=True, uploadAttempts=99)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Retrying",
            "Retrying",
            "Retrying",
            "Retrying",
            "Retrying",
            "Sigrid is currently unavailable, failed after 5 attempts"
        ]

        with self.assertRaises(SystemExit):
            runner.run()
        self.assertEqual(UploadLog.history, expectedLog)

    def testReadScopeFileWhenInRepository(self):
        self.createTempFile(self.tempDir, "sigrid.yaml", "component_depth: 1")

        self.assertEquals(self.options.readScopeFile(), "component_depth: 1")

    def testScopeFileIsNoneWhenNotInRepository(self):
        self.assertIsNone(self.options.readScopeFile())

    def testValidateScopeFile(self):
        self.createTempFile(self.tempDir, "sigrid.yaml", "languages:\n- java")

        apiClient = MockApiClient(self.options)
        apiClient.responses["/inboundresults/sig/aap/noot/ci/validate/v1"] = {"valid": True};

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Validating scope configuration file",
            "Validation passed",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Upload successful",
            "Waiting for analysis results"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testFailIfScopeFileIsNotValid(self):
        self.createTempFile(self.tempDir, "sigrid.yaml", "languages:\n- aap")

        apiClient = MockApiClient(self.options)
        apiClient.responses["/inboundresults/sig/aap/noot/ci/validate/v1"] = {"valid" : False, "notes" : ["test"]}

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []

        with self.assertRaises(SystemExit):
            runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Validating scope configuration file",
            "--------------------------------------------------------------------------------",
            "Invalid scope configuration file:",
            "    - test",
            "--------------------------------------------------------------------------------"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testDumpAvailableMetadataToOutput(self):
        self.createTempFile(self.tempDir, "sigrid.py", "print(123)")

        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/api/v1/system-metadata/aap/noot"] = {"aap" : 2, "noot" : None};

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB",
            "Warning: Upload is very small, source directory might not contain all source code",
            "Preparing upload",
            "Sigrid CI analysis ID: 123",
            "Submitting upload",
            "Upload successful",
            "Waiting for analysis results"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testValidateMetadataFileIfPresent(self):
        self.createTempFile(self.tempDir, "sigrid-metadata.yaml", "metadata:\n  division: aap")

        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/sigridci/aap/validate"] = {"valid" : True, "notes": []}

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Validating Sigrid metadata file",
            "Validation passed"
        ]

        self.assertEqual(UploadLog.history[0:3], expectedLog)

    def testFailIfMetadataFileIsNotValid(self):
        self.createTempFile(self.tempDir, "sigrid-metadata.yaml", "metadata:\n  typo: aap")

        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/sigridci/aap/validate"] = {"valid" : False, "notes": ["test"]}

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []

        with self.assertRaises(SystemExit):
            runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Validating Sigrid metadata file",
            "--------------------------------------------------------------------------------",
            "Invalid Sigrid metadata file:",
            "    - test",
            "--------------------------------------------------------------------------------"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testDoNotValidateMetadataFileIfNotPresent(self):
        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []

        with self.assertRaises(SystemExit):
            runner.run()

        expectedLog = [
            "Found system in Sigrid",
            "Creating upload",
            "Upload size is 1 MB"
        ]

        self.assertEqual(UploadLog.history, expectedLog)

    def testDoNotGenerateFileWithoutEnvironmentVariables(self):
        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.prepareMetadata()

        self.assertEqual(os.path.exists(f"{self.tempDir}/sigrid-metadata.yaml"), False)

    def testDoGenerateFileIfEnvironmentVariablesAreUsed(self):
        os.environ["externalid"] = "1234"

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.prepareMetadata()

        self.assertEqual(os.path.exists(f"{self.tempDir}/sigrid-metadata.yaml"), True)
        with open(f"{self.tempDir}/sigrid-metadata.yaml") as f:
            self.assertEqual(f.read(), "metadata:\n  externalID: \"1234\"\n")

    def testIgnoreEmptyEnvironmentVariables(self):
        os.environ["externalid"] = "1234"
        os.environ["divisionname"] = ""

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.prepareMetadata()

        self.assertEqual(os.path.exists(f"{self.tempDir}/sigrid-metadata.yaml"), True)
        with open(f"{self.tempDir}/sigrid-metadata.yaml") as f:
            self.assertEqual(f.read(), "metadata:\n  externalID: \"1234\"\n")

    def testTeamNamesAndSupplierNamesAreList(self):
        os.environ["suppliernames"] = "aap"
        os.environ["teamnames"] = "noot"

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.prepareMetadata()

        self.assertEqual(os.path.exists(f"{self.tempDir}/sigrid-metadata.yaml"), True)
        with open(f"{self.tempDir}/sigrid-metadata.yaml") as f:
            self.assertEqual(f.read(), "metadata:\n  teamNames: [\"noot\"]\n  supplierNames: [\"aap\"]\n")

    def testErrorIfEnvironmentVariablesAreUsedButFileAlreadyExists(self):
        self.createTempFile(self.tempDir, "sigrid-metadata.yaml", "metadata:\n  externalID: 1")
        os.environ["externalid"] = "1234"

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        with self.assertRaises(Exception):
            runner.prepareMetadata()

        self.assertEqual(os.path.exists(f"{self.tempDir}/sigrid-metadata.yaml"), True)
        with open(f"{self.tempDir}/sigrid-metadata.yaml") as f:
            self.assertEqual(f.read(), "metadata:\n  externalID: 1")

    def testPreferNewCodeTargetIfAvailable(self):
        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/api/v1/objectives/aap/noot/config"] = {
            "NEW_CODE_QUALITY" : 4.0,
            "MAINTAINABILITY" : 3.5
        }

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        target = runner.loadSigridTarget()

        self.assertEqual(target, 4.0)

    def testUseMaintainabilityTargetIfNoNewCodeTarget(self):
        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/api/v1/objectives/aap/noot/config"] = {"MAINTAINABILITY" : 2.0}

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        target = runner.loadSigridTarget()

        self.assertEqual(target, 2.0)

    def testFallbackToDefaultTargetIfNoSigridObjectives(self):
        apiClient = MockApiClient(self.options)
        apiClient.responses["/analysis-results/api/v1/objectives/aap/noot/config"] = {}

        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        target = runner.loadSigridTarget()

        self.assertEqual(target, 3.5)

    def testUploadShouldBeDeletedAfterSubmission(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        runner.run()

        for root, dirs, files in os.walk("."):
            for file in files:
                self.assertFalse(file.endswith(".zip"))

    def testExitWhenSystemIsNotActive(self):
        self.createTempFile(self.tempDir, "a.py", "print(123)")

        self.options.system = "i-am-not-active"

        apiClient = MockApiClient(self.options)
        runner = SigridCiRunner(self.options, apiClient)
        runner.reports = []
        with self.assertRaises(SystemExit) as raised:
            runner.run()

        self.assertTrue(1 in raised.exception.args)
        self.assertEqual(UploadLog.history, ["System aap-i-am-not-active has been deactivated (HTTP status 410)"])

    def createTempFile(self, dir, name, contents):
        with open(f"{dir}/{name}", "w") as fileRef:
            fileRef.write(contents)
        return f"{dir}/{name}"

        
class MockApiClient(SigridApiClient):

    def __init__(self, options, *, systemExists=True, uploadAttempts=0):
        super().__init__(options)

        self.called = []
        self.systemExists = systemExists
        self.uploadAttempts = uploadAttempts
        self.attempt = 0
        self.responses = {}
        self.POLL_INTERVAL = 1

    def callSigridAPI(self, path, body=None, contentType=None):
        self.called.append(path)
    
        if not self.systemExists and path.endswith("/sigridci/aap/noot/v1/ci"):
            # Mock a HTTP 404.
            raise urllib.error.HTTPError(path, 404, "", {}, None)

        if path.endswith("/sigridci/aap/i-am-not-active/v1/ci"):
            # Mock a HTTP 410.
            raise urllib.error.HTTPError(path, 410, "System aap-i-am-not-active has been deactivated", {}, None)

        defaultResponse = {"ciRunId" : "123", "uploadUrl" : "dummy"}
        return self.responses.get(path, defaultResponse)
        
    def attemptUpload(self, url, upload):
        self.attempt += 1
        if self.attempt >= self.uploadAttempts:            
            self.called.append("UPLOAD")
            return True
        else:
            raise urllib.error.HTTPError("/upload", 500, "", {}, None)
     

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
import sys

from .capability import OPEN_SOURCE_HEALTH, SECURITY, Capability
from .feedback_provider import FeedbackProvider
from .platform import Platform
from .publish_options import PublishOptions, RunMode
from .sigrid_api_client import SigridApiClient
from .upload_log import UploadLog


class SigridCiRunner:
    METADATA_FIELDS = [
        "displayName",
        "divisionName",
        "teamNames",
        "supplierNames",
        "lifecyclePhase",
        "inProductionSince",
        "businessCriticality",
        "targetIndustry",
        "deploymentType",
        "applicationType",
        "externalID",
        "isDevelopmentOnly",
        "remark"
    ]

    DOCS_URL = "https://docs.sigrid-says.com"
    MISSING_SCOPE_URL = f"{DOCS_URL}/reference/analysis-scope-configuration.html#removing-the-scope-configuration-file"

    def __init__(self, options: PublishOptions, apiClient: SigridApiClient):
        self.options = options
        self.apiClient = apiClient

    def run(self):
        self.prepareRun()
        self.performLicenseCheck()

        systemExists = self.apiClient.checkSystemExists()
        UploadLog.log("Found system in Sigrid" if systemExists else "System is not yet on-boarded to Sigrid")

        metadata = self.apiClient.fetchMetadata() if systemExists else {}
        if systemExists and not metadata.get("active", True):
            UploadLog.log("Publish blocked: System has been deactivated by your Sigrid administrator in the Sigrid system settings page")
            sys.exit(1)

        self.prepareMetadata()
        self.validateConfigurationFiles(metadata)
        analysisId = self.apiClient.submitUpload(systemExists)

        if not systemExists:
            UploadLog.log(f"System '{self.options.system}' has been on-boarded and will appear in Sigrid shortly")
            return 0
        elif self.options.runMode == RunMode.PUBLISH_ONLY:
            UploadLog.log("Your project's source code has been published to Sigrid")
            self.displayMetadata(metadata)
            return 0
        else:
            return self.displayFeedback(analysisId, metadata)

    def prepareRun(self):
        # We don't use the options.feedbackURL directly, since that's intended
        # for interactive usage, but we can use it to check if feedback is
        # disabled.
        if self.options.feedbackURL:
            self.apiClient.logPlatformInformation(Platform.getPlatformId())

    def performLicenseCheck(self):
        licenseData = self.apiClient.fetchLicenses()
        licenses = licenseData.get("licenses", licenseData.get("licences", []))
        missing = [capability.name for capability in self.options.capabilities if capability.name not in licenses]
        if len(missing) > 0:
            UploadLog.log(f"You do not have the Sigrid license for {', '.join(missing)}.")
            sys.exit(1)


    def displayFeedback(self, analysisId, metadata):
        objectives = self.apiClient.fetchObjectives()
        exitCode = 0

        self.displayMetadata(metadata)

        for capability in self.options.capabilities:
            feedback = self.apiClient.fetchAnalysisResults(analysisId, capability)
            feedbackProvider = FeedbackProvider(capability, self.options, objectives)
            feedbackProvider.analysisId = analysisId
            feedbackProvider.feedback = feedback
            feedbackProvider.previousFeedback = self.loadFeedbackBaseline(capability)
            success = feedbackProvider.generateReports()
            if not success:
                exitCode += capability.exitCode

        return exitCode

    def loadFeedbackBaseline(self, capability):
        if capability == OPEN_SOURCE_HEALTH:
            return self.apiClient.fetchOpenSourceHealth()
        elif capability == SECURITY:
            return self.apiClient.fetchSecurityFindings()
        else:
            return None

    def validateConfigurationFiles(self, metadata):
        scope = self.options.readScopeFile()

        if scope is not None:
            if self.options.subsystem not in (None, "", "root", "scopefile"):
                UploadLog.log("Warning: You cannot provide a scope configuration file for a subsystem, it will be ignored.")

            self.validateConfiguration(lambda: self.apiClient.validateScopeFile(scope), "scope configuration file")
            if OPEN_SOURCE_HEALTH in self.options.capabilities and not "dependencychecker:" in scope:
                self.showValidationError("scope configuration file", ["Missing required field 'dependencychecker'."])
            if SECURITY in self.options.capabilities and not "thirdpartyfindings:" in scope:
                self.showValidationError("scope configuration file", ["Missing required field 'thirdpartyfindings'."])

        if scope is None and metadata.get("scopeFileInRepository") and not self.options.subsystem and not self.options.ignoreMissingScopeFile:
            message = {"valid" : False, "notes" : ["Missing sigrid.yaml file", f"See {self.MISSING_SCOPE_URL}"]}
            self.validateConfiguration(lambda: message, "scope configuration file")

        metadataFile = self.options.readMetadataFile()
        if metadataFile is not None:
            self.validateConfiguration(lambda: self.apiClient.validateMetadata(metadataFile), "Sigrid metadata file")

    def validateConfiguration(self, validationCall, configurationName):
        UploadLog.log(f"Validating {configurationName}")
        validationResult = validationCall()
        if validationResult["valid"]:
            UploadLog.log("Validation passed")
        else:
            self.showValidationError(configurationName, validationResult["notes"])

    def showValidationError(self, configurationName, notes):
        UploadLog.log("-" * 80)
        UploadLog.log(f"Invalid {configurationName}:")
        for note in notes:
            UploadLog.log(f"    - {note}")
        UploadLog.log("-" * 80)
        sys.exit(1)

    def displayMetadata(self, metadata):
        if self.options.readMetadataFile() == None:
            print("")
            print("Sigrid metadata for this system:")
            for key, value in metadata.items():
                if value:
                    print(f"    {key}:".ljust(30) + str(value))

    def prepareMetadata(self):
        getMetadataValue = lambda field: os.environ.get(field.lower(), "")
        metadata = {field: getMetadataValue(field) for field in self.METADATA_FIELDS if getMetadataValue(field)}

        if len(metadata) > 0:
            if self.options.readMetadataFile() != None:
                raise Exception("Cannot add metadata using environment variables if metadata YAML file is already used")

            with open(f"{self.options.sourceDir}/sigrid-metadata.yaml", "w") as writer:
                writer.write("metadata:\n")
                for name, value in metadata.items():
                    formattedValue = f"[\"{value}\"]" if name in ["teamNames", "supplierNames"] else f"\"{value}\""
                    writer.write(f"  {name}: {formattedValue}\n")

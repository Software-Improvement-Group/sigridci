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

from .publish_options import PublishOptions, RunMode
from .sigrid_api_client import SigridApiClient
from .upload_log import UploadLog
from .reports.ascii_art_report import AsciiArtReport
from .reports.azure_pull_request_report import AzurePullRequestReport
from .reports.gitlab_pull_request_report import GitLabPullRequestReport
from .reports.json_report import JsonReport
from .reports.junit_format_report import JUnitFormatReport
from .reports.maintainability_markdown_report import MaintainabilityMarkdownReport
from .reports.pipeline_summary_report import PipelineSummaryReport
from .reports.static_html_report import StaticHtmlReport


class SigridCiRunner:
    DEFAULT_OBJECTIVE = 3.5

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

    def __init__(self, options: PublishOptions, apiClient: SigridApiClient):
        self.options = options
        self.apiClient = apiClient

        self.reports = [
            AsciiArtReport(),
            MaintainabilityMarkdownReport(),
            StaticHtmlReport(),
            JUnitFormatReport(),
            JsonReport(),
            AzurePullRequestReport(MaintainabilityMarkdownReport()),
            GitLabPullRequestReport(MaintainabilityMarkdownReport()),
            PipelineSummaryReport()
        ]

    def run(self):
        systemExists = self.apiClient.checkSystemExists()
        UploadLog.log("Found system in Sigrid" if systemExists else "System is not yet on-boarded to Sigrid")

        if systemExists and not self.apiClient.fetchMetadata().get("active", True):
            UploadLog.log("Publish blocked: System has been deactivated by your Sigrid administrator, in the Sigrid system settings page")
            sys.exit(1)

        self.prepareMetadata()
        self.validateConfigurationFiles()
        analysisId = self.apiClient.submitUpload(systemExists)

        if not systemExists:
            UploadLog.log(f"System '{self.options.system}' has been on-boarded and will appear in Sigrid shortly")
        elif self.options.runMode == RunMode.PUBLISH_ONLY:
            UploadLog.log("Your project's source code has been published to Sigrid")
            self.displayMetadata()
        else:
            self.displayFeedback(analysisId)

    def displayFeedback(self, analysisId):
        if self.options.targetRating == "sigrid":
            self.options.targetRating = self.loadSigridTarget()

        feedback = self.apiClient.fetchAnalysisResults(analysisId)
        self.displayMetadata()

        if not os.path.exists(self.options.outputDir):
            os.mkdir(self.options.outputDir)

        for report in self.reports:
            report.generate(analysisId, feedback, self.options)

    def validateConfigurationFiles(self):
        scope = self.options.readScopeFile()
        if scope:
            self.validateConfiguration(lambda: self.apiClient.validateScopeFile(scope), "scope configuration file")

        metadataFile = self.options.readMetadataFile()
        if metadataFile:
            self.validateConfiguration(lambda: self.apiClient.validateMetadata(metadataFile), "Sigrid metadata file")

    def validateConfiguration(self, validationCall, configurationName):
        UploadLog.log(f"Validating {configurationName}")
        validationResult = validationCall()

        if validationResult["valid"]:
            UploadLog.log("Validation passed")
        else:
            UploadLog.log("-" * 80)
            UploadLog.log(f"Invalid {configurationName}:")
            for note in validationResult["notes"]:
                UploadLog.log(f"    - {note}")
            UploadLog.log("-" * 80)
            sys.exit(1)

    def displayMetadata(self):
        if self.options.readMetadataFile() == None:
            print("")
            print("Sigrid metadata for this system:")
            for key, value in self.apiClient.fetchMetadata().items():
                if value:
                    print(f"    {key}:".ljust(20) + str(value))

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

    def loadSigridTarget(self):
        objectives = self.apiClient.fetchObjectives()
        targetRating = objectives.get("MAINTAINABILITY", self.DEFAULT_OBJECTIVE)
        UploadLog.log("Using Sigrid for target rating (%.1f stars)" % targetRating)
        return targetRating

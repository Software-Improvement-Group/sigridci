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

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from tempfile import TemporaryDirectory

from .publish_options import PublishOptions, RunMode
from .system_upload_packer import SystemUploadPacker
from .upload_log import UploadLog


class SigridApiClient:
    API_VERSION = "v1"
    POLL_INTERVAL = 30
    POLL_ATTEMPTS = 60

    def __init__(self, options: PublishOptions):
        self.options = options
        self.baseURL = options.sigridURL
        self.urlPartnerName = urllib.parse.quote_plus(options.partner.lower())
        self.urlCustomerName = urllib.parse.quote_plus(options.customer.lower())
        self.urlSystemName = urllib.parse.quote_plus(options.system.lower())
        self.token = os.environ["SIGRID_CI_TOKEN"].strip()

        UploadLog.log(f"Using token ending in '****{self.token[-4:]}'")

    def callSigridAPI(self, path, body=None, contentType=None):
        delimiter = "" if path.startswith("/") else "/"
        url = f"{self.baseURL}/rest{delimiter}{path}"
        request = urllib.request.Request(url, body)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", f"Bearer {self.token}".encode("utf8"))
        if contentType is not None:
            request.add_header("Content-Type", contentType)

        response = urllib.request.urlopen(request)
        if response.status == 204:
            return {}

        responseBody = response.read().decode("utf8")
        if len(responseBody) == 0:
            UploadLog.log("Received empty response")
            return {}
        else:
            return json.loads(responseBody)

    def retry(self, operation, *, attempts=5, allow404=False, allowEmpty=True, server="Sigrid"):
        for attempt in range(attempts):
            try:
                response = operation()
                if allowEmpty or response != {}:
                    return response
            except urllib.error.HTTPError as e:
                return self.handleError(e, allow404, server)

            # These statements are intentionally outside the except-block,
            # since we want to retry for empty response on some end points.
            UploadLog.log("Retrying")
            time.sleep(self.POLL_INTERVAL)

        UploadLog.log(f"{server} is currently unavailable, failed after {attempts} attempts")
        sys.exit(1)

    @staticmethod
    def handleError(e: urllib.error.HTTPError, allow404, server: str):
        if e.code == 404 and allow404:
            return False
        if e.code == 401:
            UploadLog.log(f"You are not authenticated to {server} (HTTP status {e.code} for {e.url}), please check if your token is valid")
        elif e.code == 403:
            UploadLog.log(f"You are not authorized to access {server} for this system (HTTP status {e.code} for {e.url})")
        elif e.code == 410:
            if e.reason:
                UploadLog.log(f"{e.reason} (HTTP status {e.code} for {e.url})")
            else:
                UploadLog.log(f"The system no longer exists (HTTP status {e.code} for {e.url})")
        else:
            UploadLog.log(str(e))
        SigridApiClient.printResponse(e)

    @staticmethod
    def printResponse(e: urllib.error.HTTPError):
        UploadLog.log(f"Response headers:\n{str(e.headers)}")
        if e.fp is not None:
            UploadLog.log(f"Response body:\n{e.fp.read().decode()}")
        else:
            UploadLog.log("No response body")
        sys.exit(1)

    def submitUpload(self, systemExists):
        with TemporaryDirectory() as tempDir:
            UploadLog.log("Creating upload")
            uploadPacker = SystemUploadPacker(self.options)
            upload = os.path.join(tempDir, "upload.zip")
            uploadPacker.prepareUpload(upload)

            UploadLog.log("Preparing upload")
            uploadLocation = self.obtainUploadLocation(systemExists)
            uploadUrl = uploadLocation["uploadUrl"]
            analysisId = uploadLocation["ciRunId"]
            UploadLog.log(f"Sigrid CI analysis ID: {analysisId}")
            UploadLog.log("Submitting upload" if self.options.runMode == RunMode.FEEDBACK_ONLY else "Publishing upload")
            self.uploadBinaryFile(uploadUrl, upload)

            return analysisId

    def obtainUploadLocation(self, systemExists):
        path = f"/inboundresults/{self.urlPartnerName}/{self.urlCustomerName}/{self.urlSystemName}/ci/uploads/{self.API_VERSION}"

        if not systemExists:
            path += "/onboarding"
        elif self.options.runMode == RunMode.PUBLISH_ONLY:
            path += "/publishonly"
        elif self.options.runMode == RunMode.FEEDBACK_AND_PUBLISH:
            path += "/publish"

        if self.options.subsystem and self.options.convert:
            path += "?subsystem=" + urllib.parse.quote_plus(self.options.subsystem) + "&convert=" + urllib.parse.quote_plus(self.options.convert)
        elif self.options.subsystem:
            path += "?subsystem=" + urllib.parse.quote_plus(self.options.subsystem)
        elif self.options.convert:
            path += "?convert=" + urllib.parse.quote_plus(self.options.convert)

        return self.retry(lambda: self.callSigridAPI(path))

    def validateScopeFile(self, scopeFile):
        path = f"/inboundresults/{self.urlPartnerName}/{self.urlCustomerName}/{self.urlSystemName}/ci/validate/{self.API_VERSION}"
        return self.retry(lambda: self.callSigridAPI(path, scopeFile.encode("utf8"), "application/yaml"))

    def validateMetadata(self, metadataFile):
        path = f"/analysis-results/sigridci/{self.urlCustomerName}/validate"
        return self.retry(lambda: self.callSigridAPI(path, metadataFile.encode("utf8"), "application/yaml"))

    def uploadBinaryFile(self, url, upload):
        self.retry(lambda: self.attemptUpload(url, upload), server="object store")
        UploadLog.log(f"Upload successful")

    def attemptUpload(self, url, upload):
        with open(upload, "rb") as uploadRef:
            uploadRequest = urllib.request.Request(url, data=uploadRef)
            uploadRequest.method = "PUT"
            uploadRequest.add_header("Content-Type", "application/zip")
            uploadRequest.add_header("Content-Length", "%d" % os.path.getsize(upload))
            uploadRequest.add_header("x-amz-server-side-encryption", "AES256")
            urllib.request.urlopen(uploadRequest)

    def checkSystemExists(self):
        path = f"/analysis-results/sigridci/{self.urlCustomerName}/{self.urlSystemName}/{self.API_VERSION}/ci"
        return self.retry(lambda: self.callSigridAPI(path), allow404=True) != False

    def fetchAnalysisResults(self, analysisId):
        UploadLog.log("Waiting for analysis results")
        path = f"/analysis-results/sigridci/{self.urlCustomerName}/{self.urlSystemName}/{self.API_VERSION}/ci/results/{analysisId}"
        return self.retry(lambda: self.callSigridAPI(path), attempts=self.POLL_ATTEMPTS, allowEmpty=False)

    def fetchMetadata(self):
        path = f"/analysis-results/api/{self.API_VERSION}/system-metadata/{self.urlCustomerName}/{self.urlSystemName}"
        return self.retry(lambda: self.callSigridAPI(path))

    def fetchObjectives(self):
        path = f"/analysis-results/api/{self.API_VERSION}/objectives/{self.urlCustomerName}/{self.urlSystemName}/config"
        return self.retry(lambda: self.callSigridAPI(path))

    @staticmethod
    def isValidToken(token):
        return token is not None and len(token) >= 64

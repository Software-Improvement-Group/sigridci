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
import ssl
import urllib.parse
import urllib.request
from tempfile import TemporaryDirectory

from .api_caller import ApiCaller
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
        self.sslContext = ssl.create_default_context(cafile=os.getenv("SIGRID_CA_CERT")) if os.environ.get("SIGRID_CA_CERT") else None

        UploadLog.log(f"Using token ending in '****{self.token[-4:]}'")

        if os.environ.get("SIGRID_CI_PROXY_URL"):
            proxyHandler = urllib.request.ProxyHandler({
                "http": os.environ["SIGRID_CI_PROXY_URL"],
                "https": os.environ["SIGRID_CI_PROXY_URL"],
            })
            proxyOpener = urllib.request.build_opener(proxyHandler)
            urllib.request.install_opener(proxyOpener)

    def callSigridAPI(self, path, body=None, contentType=None):
        delimiter = "" if path.startswith("/") else "/"
        url = f"{self.baseURL}/rest{delimiter}{path}"
        request = urllib.request.Request(url, body)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", f"Bearer {self.token}".encode("utf8"))
        if contentType is not None:
            request.add_header("Content-Type", contentType)

        response = urllib.request.urlopen(request, context=self.sslContext)
        if response.status == 204:
            return {}

        responseBody = response.read().decode("utf8")
        if len(responseBody) == 0:
            UploadLog.log("Received empty response")
            return {}
        else:
            return json.loads(responseBody)

    def retry(self, operation, *, attempts=5, allow404=False, allowEmpty=True):
        api = ApiCaller("Sigrid", self.POLL_INTERVAL)
        return api.retryRequest(operation, attempts=attempts, allow404=allow404, allowEmpty=allowEmpty)

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
        api = ApiCaller("S3", self.POLL_INTERVAL)
        api.retryRequest(lambda: self.attemptUpload(url, upload))
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

    def fetchLicenses(self):
        path = f"/analysis-results/api/{self.API_VERSION}/licenses/{self.urlCustomerName}"
        return self.retry(lambda: self.callSigridAPI(path))

    def logPlatformInformation(self, platformId):
        try:
            url = f"{self.options.sigridURL}/usage/matomo.php?idsite=6&rec=1&ca=1&e_c=sigridci.platform&e_a={platformId}"
            request = urllib.request.Request(url)
            urllib.request.urlopen(request)
        except:
            UploadLog.log("Failed to log platform information")

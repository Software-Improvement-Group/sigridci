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

import http.client
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from .upload_log import UploadLog


class ApiCaller:
    def __init__(self, service, pollInterval):
        self.service = service
        self.pollInterval = pollInterval

    def retryRequest(self, operation, *, attempts=5, allow404=False, allowEmpty=True):
        for attempt in range(attempts):
            try:
                response = operation()
                if allowEmpty or response != {}:
                    return response
            except urllib.error.HTTPError as e:
                if e.code == 404 and allow404:
                    return False
                self.handleError(e)
            except TimeoutError:
                UploadLog.log(f"{self.service} did not respond within the timeout period")
            except (urllib.error.URLError, http.client.HTTPException) as e:
                UploadLog.log(f"Error contacting {self.service}: {str(e)} ({type(e).__name__})")

            # These statements are intentionally outside the except-block,
            # since we want to retry for empty response on some end points.
            if attempt != attempts - 1:
                UploadLog.log("Retrying")
                time.sleep(self.pollInterval)

        UploadLog.log(f"{self.service} is currently unavailable, failed after {attempts} attempts")
        sys.exit(1)

    def handleError(self, e: urllib.error.HTTPError):
        if e.code == 401:
            UploadLog.log(f"You are not authenticated to {self.service} (HTTP status {e.code} for {e.url})")
            self.printResponse(e)
            sys.exit(1)
        elif e.code == 403:
            UploadLog.log(f"You are not authorized to access {self.service} (HTTP status {e.code} for {e.url})")
            self.printResponse(e)
            sys.exit(1)
        elif e.code == 410:
            if e.reason:
                UploadLog.log(f"{e.reason} (HTTP status {e.code} for {e.url})")
            else:
                UploadLog.log(f"The system no longer exists (HTTP status {e.code} for {e.url})")
            sys.exit(1)
        else:
            UploadLog.log(str(e))
            self.printResponse(e)

    def printResponse(self, e: urllib.error.HTTPError):
        headers = dict(e.headers)
        if headers:
            UploadLog.log(f"Response headers:\n{headers}")
        else:
            UploadLog.log("No response headers")

        body = e.fp.read().decode("utf8") if e.fp else ""
        if body:
            UploadLog.log(f"Response body:\n{body}")
        else:
            UploadLog.log("No response body")

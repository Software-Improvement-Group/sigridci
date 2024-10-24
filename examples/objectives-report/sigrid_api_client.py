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
import urllib.request
from datetime import datetime


class SigridApiClient:
    def __init__(self, sigridURL, customer, token):
        self.sigridURL = sigridURL
        self.customer = customer
        self.token = token

    def callEndPoint(self, path, body=None):
        request = urllib.request.Request(f"{self.sigridURL}/rest/analysis-results/api/v1{path}", body)
        request.add_header("Accept", "application/json")
        request.add_header("Authorization", f"Bearer {self.token}".encode("utf8"))
        response = urllib.request.urlopen(request)
        
        if response.status >= 400:
            raise Exception(f"Sigrid API returns HTTP status {response.status}")
        
        responseBody = response.read().decode("utf8")
        return json.loads(responseBody)

    def fetchSystemNames(self):
        response = self.callEndPoint(f"/maintainability/{self.customer}")
        return sorted(entry["system"] for entry in response["systems"])

    def fetchMaintainability(self):
        response = self.callEndPoint(f"/maintainability/{self.customer}")
        return sorted(response["systems"], key=lambda e: -e["volumeInPersonMonths"])
        
    def fetchMetadata(self):
        response = self.callEndPoint(f"/system-metadata/{self.customer}")
        return {system["systemName"]: system for system in response}
        
    def fetchSystemMetadata(self, system):
        return self.callEndPoint(f"/system-metadata/{self.customer}/{system}")
        
    def fetchPortfolioObjectives(self):
        response = self.callEndPoint(f"/objectives/{self.customer}")
        # Use a deterministic sort order, since the API returns objectives
        # in a different/random order every time.
        response["objectives"].sort(key=lambda o: o["id"])
        return response["objectives"]

    def fetchObjectivesEvaluation(self, start, end):
        if isinstance(start, datetime):
            start = start.strftime("%Y-%m-%d")
        if isinstance(end, datetime):
            end = end.strftime("%Y-%m-%d")
        response = self.callEndPoint(f"/objectives-evaluation/{self.customer}?startDate={start}&endDate={end}")
        return response["systems"]

    def fetchArchitectureGraph(self, system):
        return self.callEndPoint(f"/architecture-quality/{self.customer}/{system}/raw")

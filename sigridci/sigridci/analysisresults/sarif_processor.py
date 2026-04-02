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

from dataclasses import dataclass
from enum import Enum

from ..objective import Objective


class FindingStatus(Enum):
    INTRODUCED = "Introduced"
    FIXED = "Fixed"
    REMAINING = "Remaining"
    ACCEPTED = "Accepted"


@dataclass
class Finding:
    fingerprint: str
    risk: str
    description: str
    file: str
    line: int
    partOfObjective: bool
    status: FindingStatus


class SarifProcessor:
    EXCLUDED_TOOLS = ["SIG Open Source Health"]
    UNKNOWN_LOCATION = "(unknown location)"

    def __init__(self, options, objective):
        self.options = options
        self.objective = objective

    def extractFindings(self, feedback):
        if feedback is None or not feedback.get("runs"):
            return []

        for run in feedback["runs"]:
            if self.isSuccessfulRun(run) and not self.isExcludedTool(run):
                for result in run.get("results", []):
                    fingerprint = result["fingerprints"]["sigFingerprint/v1"]
                    risk = (result.get("properties", {}).get("severity") or "UNKNOWN").upper()
                    location = self.getLocation(result)
                    file = self.rewriteSubSystem(location.get("artifactLocation", {}).get("uri", self.UNKNOWN_LOCATION))
                    line = location.get("region", {}).get("startLine", 0)
                    partOfObjective = Objective.isFindingIncluded(risk, self.objective)
                    status = self.getFindingStatus(result)

                    if file is not None and risk in Objective.SEVERITY_OBJECTIVE:
                        yield Finding(fingerprint, risk, result["message"]["text"], file, line, partOfObjective, status)

    def isExcludedTool(self, run):
        return run["tool"]["driver"]["name"] in self.EXCLUDED_TOOLS

    def isSuccessfulRun(self, run):
        if not "invocations" in run or len(run["invocations"]) == 0:
            return True
        return run["invocations"][0].get("executionSuccessful", True)

    def getLocation(self, result):
        if not "locations" in result or len(result["locations"]) == 0:
            return {}
        return result["locations"][0].get("physicalLocation", {})

    def getFindingStatus(self, result):
        if result["properties"].get("status") == "ACCEPTED":
            return FindingStatus.ACCEPTED

        state = result.get("baselineState", "unknown")
        if state == "absent":
            return FindingStatus.FIXED
        elif state == "new":
            return FindingStatus.INTRODUCED
        else:
            return FindingStatus.REMAINING

    def rewriteSubSystem(self, file):
        if not self.options.subsystem or not file:
            return file

        prefix = f"{self.options.subsystem}/"

        if file.startswith(f"{self.options.subsystem}/"):
            return file.removeprefix(prefix)
        else:
            return None

    def filterStatus(self, findings, status, *, partOfObjective):
        result = [finding for finding in findings if finding.status == status]
        if partOfObjective:
            result = [finding for finding in result if finding.partOfObjective]
        return result

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
from typing import List, Optional

from ..objective import Objective


@dataclass
class LibraryVulnerability:
    id: str
    link: Optional[str]


@dataclass
class Risk:
    severity: str
    meetsObjective: bool


@dataclass
class Library:
    name: str
    transitive: bool
    version: str
    latestVersion: str
    files: List[str]
    vulnerabilities: List[LibraryVulnerability]
    licenses: List[str]
    vulnerabilityRisk: Risk
    licenseRisk: Risk
    fixable: bool

    def meetsObjectives(self):
        return self.vulnerabilityRisk.meetsObjective and self.licenseRisk.meetsObjective


class CycloneDXProcessor:
    def __init__(self, options, vulnerabilityObjective, licenseObjective=None):
        self.options = options
        self.vulnerabilityObjective = vulnerabilityObjective
        self.licenseObjective = licenseObjective

    def extractLibraries(self, feedback):
        if feedback is None:
            return

        for component in feedback.get("components", []):
            name = f"{component['group']}:{component['name']}" if component.get("group") else component["name"]
            files = list(self.getOccurrenceLocations(component))
            properties = {prop["name"]: prop["value"] for prop in component["properties"]}
            transitive = properties.get("sigrid:transitive") == "TRANSITIVE"
            version = component.get("version", "?")
            latestVersion = properties.get("sigrid:latest:version", "").replace("?", "")
            licenses = [license["license"]["name"] for license in component.get("licenses", [])]
            vulnerabilities = list(self.getComponentVulnerabilities(component, feedback))
            fixable = latestVersion and version != latestVersion

            vulnerabilityRisk = self.parseRisk(properties.get("sigrid:risk:vulnerability", "UNKNOWN"), self.vulnerabilityObjective)
            licenseRisk = self.parseRisk(properties.get("sigrid:risk:legal", "UNKNOWN"), self.licenseObjective)

            if self.isInteresting(vulnerabilityRisk, licenseRisk) and self.isRelevantSubSystem(files):
                yield Library(name, transitive, version, latestVersion, files, vulnerabilities, licenses,
                    vulnerabilityRisk, licenseRisk, fixable)

    def getOccurrenceLocations(self, component):
        if component.get("evidence") and component["evidence"].get("occurrences"):
            for occurrence in component["evidence"]["occurrences"]:
                yield occurrence["location"]

    def getComponentVulnerabilities(self, component, feedback):
        for vuln in feedback.get("vulnerabilities", []):
            affected = [affects["ref"] for affects in vuln["affects"]]
            if component.get("bom-ref") in affected:
                link = vuln["source"]["url"] if vuln.get("source") else None
                yield LibraryVulnerability(vuln["id"], link)

    def parseRisk(self, severity, objective):
        meetsObjective = objective is None or Objective.meetsFindingObjective([severity], objective)
        return Risk(severity, meetsObjective)

    def isInteresting(self, vulnerabilityRisk, licenseRisk):
        return vulnerabilityRisk.severity not in ("UNKNOWN", "NONE") or \
            not licenseRisk.meetsObjective

    def isRelevantSubSystem(self, files):
        if not self.options.subsystem or len(files) == 0:
            return True
        return any(file for file in files if file.startswith(f"{self.options.subsystem}/"))

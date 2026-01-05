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
from typing import List

from ..objective import Objective


@dataclass
class Library:
    risk: str
    name: str
    transitive: bool
    version: str
    latestVersion: str
    files: List[str]
    fixable: bool
    partOfObjective: bool


class CycloneDXProcessor:

    def extractLibraries(self, feedback, objective):
        if feedback is None:
            return

        for component in feedback.get("components", []):
            name = f"{component['group']}:{component['name']}" if component.get("group") else component["name"]
            files = list(self.getOccurrenceLocations(component))
            properties = {prop["name"]: prop["value"] for prop in component["properties"]}
            risk = properties["sigrid:risk:vulnerability"]
            transitive = properties.get("sigrid:transitive") == "TRANSITIVE"
            version = component["version"]
            latestVersion = properties.get("sigrid:latest:version", "").replace("?", "")

            if risk not in ("NONE", "UNKNOWN"):
                fixable = latestVersion and version != latestVersion
                partOfObjective = Objective.isFindingIncluded(risk, objective)
                yield Library(risk, name, transitive, version, latestVersion, files, fixable, partOfObjective)

    def getOccurrenceLocations(self, component):
        if component.get("evidence") and component["evidence"].get("occurrences"):
            for occurrence in component["evidence"]["occurrences"]:
                yield occurrence["location"]

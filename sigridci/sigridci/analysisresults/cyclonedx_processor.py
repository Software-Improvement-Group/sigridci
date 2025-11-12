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
    version: str
    latestVersion: str
    files: List[str]


class CycloneDXProcessor:

    def extractRelevantLibraries(self, feedback, objective):
        if feedback is None:
            return

        for component in feedback.get("components", []):
            name = f"{component['group']}:{component['name']}" if component.get("group") else component["name"]
            files = [occurrence["location"] for occurrence in component.get("evidence", []).get("occurrences", [])]
            properties = {prop["name"]: prop["value"] for prop in component["properties"]}
            risk = properties["sigrid:risk:vulnerability"]
            latestVersion = properties["sigrid:latest:version"].replace("?", "")

            if Objective.isFindingIncluded(risk, objective):
                yield Library(risk, name, component["version"], latestVersion, files)

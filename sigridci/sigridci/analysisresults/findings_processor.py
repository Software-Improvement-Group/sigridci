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

from ..objective import Objective


@dataclass
class Finding:
    fingerprint: str
    risk: str
    description: str
    file: str
    line: int
    partOfObjective: bool


class FindingsProcessor:
    def __init__(self, options, objective):
        self.options = options
        self.objective = objective

    def extractFindings(self, feedback):
        if feedback is None:
            return []

        findings = []
        if "runs" in feedback:
            sarifProcessor = SarifProcessor()
            findings += list(sarifProcessor.extractFindings(feedback, self.objective))
        else:
            sigridFindingsProcessor = SigridFindingsProcessor()
            findings += list(sigridFindingsProcessor.extractFindings(feedback, self.objective))

        return [finding for finding in findings if self.isRelevantSubSystem(finding)]

    def isRelevantSubSystem(self, finding):
        subsystem = self.options.subsystem
        return not subsystem or not finding.file or finding.file.startswith(f"{subsystem}/")


class SarifProcessor:
    def extractFindings(self, feedback, objective):
        rules = list(self.getRules(feedback))

        for run in feedback["runs"]:
            for result in run.get("results", []):
                fingerprint = result["fingerprints"]["sigFingerprint/v1"]
                risk = self.getFindingSeverity(result, rules)
                file = result["locations"][0]["physicalLocation"]["artifactLocation"]["uri"]
                line = result["locations"][0]["physicalLocation"]["region"]["startLine"]
                partOfObjective = Objective.isFindingIncluded(risk, objective)
                yield Finding(fingerprint, risk, result["message"]["text"], file, line, partOfObjective)

    def getRules(self, feedback):
        for run in feedback["runs"]:
            for rule in run.get("rules", []):
                properties = rule.get("properties", {})
                if properties.get("severity"):
                    yield rule

    def getFindingSeverity(self, result, rules):
        severity = result.get("properties", {}).get("severity")
        if not severity:
            for rule in rules:
                if rule["id"] == result["ruleId"]:
                    severity = rule["properties"]["severity"].replace("ERROR", "HIGH").replace("WARNING", "MEDIUM")
        return severity.upper() if severity else "UNKNOWN"


class SigridFindingsProcessor:
    def extractFindings(self, feedback, objective):
        for finding in feedback:
            partOfObjective = Objective.isFindingIncluded(finding["severity"], objective)
            yield Finding(finding["id"], finding["severity"], finding["type"],
                          finding["filePath"], finding["startLine"], partOfObjective)

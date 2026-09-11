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
from abc import ABC, abstractmethod

from .architecture_markdown_report import ArchitectureMarkdownReport
from .maintainability_markdown_report import MaintainabilityMarkdownReport
from .osh_markdown_report import OpenSourceHealthMarkdownReport
from .security_markdown_report import SecurityMarkdownReport
from ..objective import Objective


class InlineResultsReport(ABC):
    def generate(self, analysisId, feedback, options):
        payload = self.buildPayload(feedback, options)
        print("Inline results: " + payload["capability"])
        print(json.dumps(payload))

    @abstractmethod
    def buildPayload(self, feedback, options):
        pass


class MaintainabilityInlineResultsReport(InlineResultsReport, MaintainabilityMarkdownReport):
    # Ratings that are still tracked in older Sigrid systems but are no longer part of
    # the current quality model. See Objective.SYSTEM_PROPERTIES for the current metrics.
    CURRENT_METRICS = Objective.SYSTEM_PROPERTIES + ["MAINTAINABILITY"]

    # Maps the raw feedback's ratings dicts to the column names used in the "ratings" table below.
    RATINGS_KEYS_NAMES = {
        "baselineRatings": "systemBaseline",
        "overallRatings": "systemNew",
        "changedCodeBeforeRatings": "changedCodeBefore",
        "newCodeRatings": "newAndChangedCodeAfter"
    }

    # changedCodeAfterRatings isn't shown in the ratings table, but still needs to be
    # stripped from the payload along with the other raw ratings dicts.
    RAW_RATINGS_KEYS = list(RATINGS_KEYS_NAMES) + ["changedCodeAfterRatings"]

    def buildPayload(self, feedback, options):
        payload = dict(feedback)
        payload["capability"] = self.getCapability().shortName
        payload["objectiveMet"] = self.isObjectiveSuccess(feedback, options)
        payload.pop("refactoringCandidatesPerType", None)
        payload["ratings"] = self.buildRatings(feedback)

        for ratingsKey in self.RAW_RATINGS_KEYS:
            payload.pop(ratingsKey, None)

        payload["refactoringCandidates"] = [self.cleanRefactoringCandidate(rc) for rc in payload.get("refactoringCandidates", [])]
        return payload

    def buildRatings(self, feedback):
        return [
            {
                "metric": metric,
                **{name: feedback.get(rawKey, {}).get(metric) for rawKey, name in self.RATINGS_KEYS_NAMES.items()}
            }
            for metric in self.CURRENT_METRICS
        ]

    def cleanRefactoringCandidate(self, rc):
        rc = dict(rc)
        rc.pop("occurrences", None)
        return rc


class OpenSourceHealthInlineResultsReport(InlineResultsReport, OpenSourceHealthMarkdownReport):
    def buildPayload(self, feedback, options):
        libraries = list(self.processor.extractLibraries(feedback))
        return {
            "capability": self.getCapability().shortName,
            "objectiveMet": self.isObjectiveSuccess(feedback, options),
            "baseline": self.getBaseline(feedback),
            "libraries": [self.buildLibrary(library) for library in libraries]
        }

    def buildLibrary(self, library):
        return {
            "name": library.name,
            "version": library.version,
            "latestVersion": library.latestVersion,
            "transitive": library.transitive,
            "fixable": library.fixable,
            "licenses": library.licenses,
            "vulnerabilities": [{"id": vuln.id, "link": vuln.link} for vuln in library.vulnerabilities],
            "vulnerabilityRisk": {"severity": library.vulnerabilityRisk.severity,
                                   "meetsObjective": library.vulnerabilityRisk.meetsObjective},
            "licenseRisk": {"severity": library.licenseRisk.severity,
                             "meetsObjective": library.licenseRisk.meetsObjective},
            "files": library.files
        }


class SecurityInlineResultsReport(InlineResultsReport, SecurityMarkdownReport):
    def buildPayload(self, feedback, options):
        findings = self.extractFindings(feedback)
        return {
            "capability": self.getCapability().shortName,
            "objectiveMet": self.isObjectiveSuccess(feedback, options),
            "baseline": feedback.get("baseline"),
            "findings": [self.buildFinding(finding) for finding in findings]
        }

    def buildFinding(self, finding):
        return {
            "fingerprint": finding.fingerprint,
            "risk": finding.risk,
            "description": finding.description,
            "file": finding.file,
            "line": finding.line,
            "partOfObjective": finding.partOfObjective,
            "status": finding.status.value
        }


class ArchitectureInlineResultsReport(InlineResultsReport, ArchitectureMarkdownReport):
    def buildPayload(self, feedback, options):
        return {
            "capability": self.getCapability().shortName,
            "objectiveMet": self.isObjectiveSuccess(feedback, options),
            "baseline": feedback.get("baseline"),
            "findings": feedback.get("dependencyFeedback", [])
        }

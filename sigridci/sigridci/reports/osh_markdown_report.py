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

from typing import Any, Iterator

from .markdown_fragment import MarkdownFragment, FeedbackFinding, Location, Summary
from ..analysisresults.cyclonedx_processor import CycloneDXProcessor, Library, Risk
from ..capability import OPEN_SOURCE_HEALTH, Capability
from ..objective import Objective
from ..publish_options import PublishOptions


class OpenSourceHealthMarkdownReport(MarkdownFragment):
    RELEVANT_RISK = ("CRITICAL", "HIGH", "MEDIUM")

    def __init__(self, options: PublishOptions, objectives: dict[str, Any]):
        self.options = options
        self.vulnerabilityObjective = objectives.get("OSH_MAX_SEVERITY") or Objective.DEFAULT_FINDING_OBJECTIVE
        self.licenseObjective = objectives.get("OSH_MAX_LICENSE_RISK")
        self.previousFeedback = None
        self.processor = CycloneDXProcessor(options, self.vulnerabilityObjective, self.licenseObjective)

    def getSummary(self, feedback: dict, options: PublishOptions) -> list[Summary]:
        totalLibraryCount = len(feedback.get("components", []))

        if totalLibraryCount == 0:
            return [Summary("💭", "Sigrid did not find any open source libraries.")]

        relevantLibraries = list(self.processor.extractLibraries(feedback))
        summary = [self.getVulnerabilitySummary(relevantLibraries)]
        if self.licenseObjective:
            summary.append(self.getLicenseSummary(relevantLibraries))
        return summary

    def getVulnerabilitySummary(self, libraries: list[Library]) -> Summary:
        objectiveDisplayName = f"{self.formatSeverity(self.vulnerabilityObjective)} open source vulnerabilities"
        fixable = [lib for lib in libraries if not lib.vulnerabilityRisk.meetsObjective and lib.fixable]
        unfixable = [lib for lib in libraries if not lib.vulnerabilityRisk.meetsObjective and not lib.fixable]

        if len(fixable) > 0:
            return Summary("❌️", f"You have {objectiveDisplayName}.")
        elif len(unfixable) > 0:
            return Summary("😑 ", f"There are vulnerable open source libraries you need to investigate.")
        else:
            return Summary("✅ ", f"You do not have {objectiveDisplayName}.")

    def getLicenseSummary(self, libraries: list[Library]) -> Summary:
        culprits = [lib for lib in libraries if not lib.licenseRisk.meetsObjective]
        if len(culprits) == 0:
            return Summary("✅ ", f"You have no license issues in open source libraries.")
        else:
            return Summary("❌", f"You have open source libraries with license issues.")

    def formatSeverity(self, objective):
        # We phrase objectives for findings as the "worst" severity
        # that is still allowed. So an objective of HIGH means high-severity
        # findings are allowed, but critical-severity findings are not allowed.
        # In the feedback, we want to phrase this in terms of goal, i.e. the
        # "least-worst" severity that is *not* allowed.
        if objective == "INFORMATION":
            return "no low-severity"
        if objective == "CRITICAL" or objective not in Objective.SEVERITY_OBJECTIVE:
            return "any"
        if objective == "NONE":
            return "no"
        index = Objective.SEVERITY_OBJECTIVE.index(objective)
        return f"no {Objective.SEVERITY_OBJECTIVE[index - 1].lower()}-severity"

    def findUpdatedLibraries(self, previous, current):
        getKey = lambda library: f"{library.name}@{library.version}"
        currentKeys = set(getKey(lib) for lib in current)
        return [lib for lib in previous if not getKey(lib) in currentKeys]

    def getBaseline(self, feedback):
        if self.previousFeedback is None:
            return feedback["metadata"]["timestamp"][0:10]
        return self.previousFeedback["metadata"]["timestamp"][0:10]

    def getCapability(self) -> Capability:
        return OPEN_SOURCE_HEALTH

    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        libraries = list(self.processor.extractLibraries(feedback))
        fixable = [lib for lib in libraries if not lib.meetsObjectives() and lib.fixable]
        return len(fixable) == 0

    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        for lib in self.processor.extractLibraries(feedback):
            yield from self.toFindings(lib, checkObjective=True)

    def getNonUrgentFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        for lib in self.processor.extractLibraries(feedback):
            if lib.vulnerabilityRisk.meetsObjective and lib.licenseRisk.meetsObjective:
                yield from self.toFindings(lib, checkObjective=False)

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        libraries = list(self.processor.extractLibraries(feedback))
        previousLibraries = list(self.processor.extractLibraries(self.previousFeedback))
        for lib in self.findUpdatedLibraries(previousLibraries, libraries):
            yield from self.toFindings(lib, checkObjective=False)

    def toFindings(self, lib: Library, *, checkObjective: bool) -> Iterator[FeedbackFinding]:
        locations = [Location(file) for file in lib.files]

        if self.isRelevantRisk(lib.vulnerabilityRisk, checkObjective=checkObjective):
            title = f"{self.formatLibName(lib)} contains known vulnerabilities."
            formatVulnLink = lambda vuln: f"[{vuln.id}]({vuln.link})" if vuln.link else vuln.id
            details = ["Vulnerabilities:"] + [formatVulnLink(vuln) for vuln in lib.vulnerabilities]
            yield FeedbackFinding(lib.vulnerabilityRisk.severity, OPEN_SOURCE_HEALTH, title, details, locations)

        if self.isRelevantRisk(lib.licenseRisk, checkObjective=checkObjective):
            title = f"{self.formatLibName(lib)} has license risks."
            details = ["Licenses:"] + lib.licenses
            yield FeedbackFinding(lib.licenseRisk.severity, OPEN_SOURCE_HEALTH, title, details, locations)

    def isRelevantRisk(self, risk: Risk, *, checkObjective: bool) -> bool:
        return not risk.meetsObjective or (not checkObjective and risk.severity in self.RELEVANT_RISK)

    def formatLibName(self, lib: Library) -> str:
        name = lib.name
        if ":" in name:
            name = name[name.index(":") + 1:]
        name = f"`{name}` {lib.version}"
        if lib.transitive:
            name += " (transitive)"
        return name

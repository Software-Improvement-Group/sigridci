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

import os
from typing import Iterator

from .markdown_fragment import MarkdownFragment, FeedbackFinding, Location, Summary
from ..capability import ARCHITECTURE, Capability
from ..publish_options import PublishOptions


class ArchitectureMarkdownReport(MarkdownFragment):
    FINDING_NAMES = {
        "UNDESIRABLE" : "Undesirable dependency",
        "CYCLIC" : "Cyclic dependency"
    }

    FINDING_SEVERITY = {
        "UNDESIRABLE" : "HIGH",
        "CYCLIC" : "MEDIUM"
    }

    def formatDependencyLocation(self, hierarchy):
        topLevelComponent = hierarchy[0]
        file = next((se for se in hierarchy if se["type"] == "FILE"), None)

        location = topLevelComponent["shortName"]
        if file:
            location += f" ▶ {file['shortName']}"
        return location

    def getDependencyLocations(self, dependency: dict) -> list[Location]:
        file = next((se for se in dependency["sourceHierarchy"] if se["type"] == "FILE"), None)
        if not file:
            return []
        lines = dependency.get("lines", [])
        line = lines[0][0] if len(lines) > 0 else 0
        return [Location(file["name"], line)]

    def formatLines(self, dependency):
        lines = dependency.get("lines")
        if not lines:
            return ""
        elif len(lines) == 1:
            return f" (line {lines[0][0]})"
        else:
            return f" (lines {', '.join(line[0] for line in lines)})"

    def getSummary(self, feedback: dict, options: PublishOptions) -> list[Summary]:
        if len(self.getNegativeFeedback(feedback)) == 0:
            return [Summary("✅ ", "Your changes did not introduce any architecture issues.")]
        else:
            return [Summary("⚠️ ", "Your changes introduced architecture issues.")]

    def getCapability(self) -> Capability:
        return ARCHITECTURE

    def getMarkdownFile(self, options: PublishOptions) -> str:
        return os.path.abspath(f"{options.outputDir}/architecture-feedback.md")

    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        # We always consider architecture feedback a warning
        # rather than an error. We don't want to hard-fail
        # the pipeline like we do for e.g. security findings.
        return True

    def getDependencyFeedback(self, feedback, activity):
        dependencyFeedback = feedback.get("dependencyFeedback", [])
        return [
            dep
            for dep in dependencyFeedback
            if dep["qualification"] in self.FINDING_NAMES and dep["activity"] in activity
        ]

    def getPositiveFeedback(self, feedback):
        return self.getDependencyFeedback(feedback, ("REMOVED", "DECREASED"))

    def getNegativeFeedback(self, feedback):
        return self.getDependencyFeedback(feedback, ("INTRODUCED", "INCREASED"))

    def getRemainingFeedback(self, feedback):
        return sum(feedback["remaining"].values())

    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        return (self.toFinding(dep) for dep in self.getNegativeFeedback(feedback))

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        return (self.toFinding(dep) for dep in self.getPositiveFeedback(feedback))

    def toFinding(self, dependency: dict) -> FeedbackFinding:
        severity = self.FINDING_SEVERITY.get(dependency["qualification"]) or "UNKNOWN"
        title = self.FINDING_NAMES.get(dependency["qualification"]) or dependency["qualification"].title()
        suffix = dependency["activity"].title()
        locations = self.getDependencyLocations(dependency)

        details = [
            f"Source: {self.formatDependencyLocation(dependency['sourceHierarchy'])}{self.formatLines(dependency)}",
            f"Target: {self.formatDependencyLocation(dependency['targetHierarchy'])}"
        ]

        return FeedbackFinding(severity, ARCHITECTURE, f"{title} ({suffix})", details, locations)

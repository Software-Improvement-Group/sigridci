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
from dataclasses import dataclass
from typing import List

from .report import Report, MarkdownRenderer
from .security_markdown_report import SecurityMarkdownReport
from ..objective import Objective


@dataclass
class Library:
    risk: str
    name: str
    version: str
    latestVersion: str
    files: List[str]


class OpenSourceHealthMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = SecurityMarkdownReport.MAX_FINDINGS
    SYMBOLS = SecurityMarkdownReport.SEVERITY_SYMBOLS
    SORT_RISK = list(SecurityMarkdownReport.SEVERITY_SYMBOLS.keys())

    def __init__(self, objective = "CRITICAL"):
        super().__init__()
        self.objective = objective
        self.previousFeedback = None

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        libraries = list(self.extractRelevantLibraries(feedback))
        previousLibraries = list(self.extractRelevantLibraries(self.previousFeedback))

        fixable = [lib for lib in libraries if self.isFixable(lib)]
        unfixable = [lib for lib in libraries if not self.isFixable(lib)]
        updated = self.findUpdatedLibraries(previousLibraries, libraries)

        details = f"Sigrid compared your code against the baseline of {self.getBaseline(feedback)}.\n\n"
        if len(updated) > 0:
            details += "## 👍 What went well?\n\n"
            details += f"> You updated **{len(updated)}** vulnerable open source libraries.\n\n"
            details += self.generateFindingsTable(updated, options)
        if len(fixable) > 0:
            details += "## 👎 What could be better?\n\n"
            details += f"> You have **{len(fixable)}** vulnerable open source libraries with a fix available.  \n"
            details += "> Consider upgrading to a version that no longer contains the vulnerability.\n\n"
            details += self.generateFindingsTable(fixable, options)
        if len(unfixable) > 0:
            details += "## 😑 You have findings that you need to investigate in more depth\n\n"
            details += f"> You have **{len(unfixable)}** vulnerable open source libraries without a fix available.  \n"
            details += "> You need to investigate the security risk, and discuss how to manage it accordingly.\n\n"
            details += self.generateFindingsTable(unfixable, options)

        sigridLink = f"{self.getSigridUrl(options)}/-/open-source-health"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        objectiveDisplayName = f"{self.objective.lower()}-severity open source vulnerabilities"
        if self.isObjectiveSuccess(feedback, options):
            return f"✅  You achieved your objective of having no {objectiveDisplayName}."
        else:
            return f"⚠️  You failed to meet your objective of having no {objectiveDisplayName}."

    def generateFindingsTable(self, libraries, options):
        md = "| Vulnerability risk | Library | Latest version | Location(s) |\n"
        md += "|----|----|----|----|\n"

        for library in sorted(libraries, key=lambda lib: self.SORT_RISK.index(lib.risk))[0:self.MAX_FINDINGS]:
            symbol = self.SYMBOLS[library.risk]
            locations = "<br />".join(self.decorateLink(options, file, file) for file in library.files)
            md += f"| {symbol} | {library.name} {library.version} | {library.latestVersion} | {locations} |\n"

        if len(libraries) > self.MAX_FINDINGS:
            md += f"| | ... {len(libraries) - self.MAX_FINDINGS} more vulnerable open source libraries | |\n"

        return f"{md}\n"

    def extractRelevantLibraries(self, feedback):
        if feedback is None:
            return

        for component in feedback.get("components", []):
            name = f"{component['group']}:{component['name']}" if component.get("group") else component["name"]
            files = [occurrence["location"] for occurrence in component["evidence"]["occurrences"]]
            properties = {prop["name"]: prop["value"] for prop in component["properties"]}
            risk = properties["sigrid:risk:vulnerability"]
            latestVersion = properties["sigrid:latest:version"].replace("?", "")

            if Objective.isFindingIncluded(risk, self.objective):
                yield Library(risk, name, component["version"], latestVersion, files)

    def isFixable(self, library):
        return library.latestVersion and library.version != library.latestVersion

    def findUpdatedLibraries(self, previous, current):
        getKey = lambda library: f"{library.name}@{library.version}"
        currentKeys = set(getKey(lib) for lib in current)
        return [lib for lib in previous if not getKey(lib) in currentKeys]

    def getBaseline(self, feedback):
        if self.previousFeedback is None:
            return feedback["metadata"]["timestamp"][0:10]
        return self.previousFeedback["metadata"]["timestamp"][0:10]

    def getCapability(self):
        return "Open Source Health"

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/osh-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        fixable = [lib for lib in self.extractRelevantLibraries(feedback) if self.isFixable(lib)]
        return len(fixable) == 0

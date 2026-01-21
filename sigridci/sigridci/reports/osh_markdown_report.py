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

from .report import Report, MarkdownRenderer
from .security_markdown_report import SecurityMarkdownReport
from ..analysisresults.cyclonedx_processor import CycloneDXProcessor
from ..capability import OPEN_SOURCE_HEALTH
from ..objective import Objective


class OpenSourceHealthMarkdownReport(Report, MarkdownRenderer):
    MAX_FINDINGS = SecurityMarkdownReport.MAX_FINDINGS
    DOCS_LINK = "https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks"

    def __init__(self, vulnObjective="HIGH", licenseObjective=None):
        super().__init__()
        self.vulnObjective = vulnObjective
        self.licenseObjective = licenseObjective
        self.previousFeedback = None
        self.processor = CycloneDXProcessor(self.vulnObjective, self.licenseObjective)

    def generate(self, analysisId, feedback, options):
        with open(self.getMarkdownFile(options), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def renderMarkdown(self, analysisId, feedback, options):
        libraries = list(self.processor.extractLibraries(feedback))
        previousLibraries = list(self.processor.extractLibraries(self.previousFeedback))

        fixable = [lib for lib in libraries if lib.fixable]
        unfixable = [lib for lib in libraries if not lib.fixable]
        updated = self.findUpdatedLibraries(previousLibraries, libraries)

        details = f"Sigrid compared your code against the baseline of {self.getBaseline(feedback)}.\n\n"
        if len(updated) > 0:
            details += "## 👍 What went well?\n\n"
            details += f"> You updated **{len(updated)}** open source libraries that previously had issues.\n\n"
            details += self.generateFindingsTable(updated, options)
        if len(fixable) > 0:
            details += "## 👎 What could be better?\n\n"
            details += f"> You have **{len(fixable)}** open source libraries with issues.\n\n"
            details += self.generateFindingsTable(fixable, options)
            details += "If you believe these findings are false positives, "
            details += f"you can [exclude them in the Sigrid configuration]({self.DOCS_LINK}).\n\n"
        if len(unfixable) > 0:
            details += "## 😑 You have findings that you need to investigate in more depth\n\n"
            details += f"> You have **{len(unfixable)}** vulnerable open source libraries without a fix available.  \n"
            details += "> You need to investigate the security risk, and discuss how to manage it accordingly.\n\n"
            details += self.generateFindingsTable(unfixable, options)

        sigridLink = f"{self.getSigridUrl(options)}/-/open-source-health"
        return self.renderMarkdownTemplate(feedback, options, details, sigridLink)

    def getSummary(self, feedback, options):
        libraries = list(self.processor.extractLibraries(feedback))
        summary = [self.getVulnerabilitySummary(libraries)]
        if self.licenseObjective:
            summary.append(self.getLicenseSummary(libraries))
        return summary

    def getVulnerabilitySummary(self, libraries):
        objectiveDisplayName = f"{Objective.getSeverityObjectiveLabel(self.vulnObjective)} open source vulnerabilities"
        fixable = [lib for lib in libraries if not lib.vulnerabilityRisk.meetsObjective and lib.fixable]
        unfixable = [lib for lib in libraries if not lib.vulnerabilityRisk.meetsObjective and not lib.fixable]

        if len(fixable) > 0:
            return f"❌️  You failed to meet your objective of having {objectiveDisplayName}."
        elif len(unfixable) > 0:
            return f"😑  There are vulnerable open source libraries you need to investigate."
        else:
            return f"✅  You achieved your objective of having {objectiveDisplayName}."

    def getLicenseSummary(self, libraries):
        culprits = [lib for lib in libraries if not lib.licenseRisk.meetsObjective]
        if len(culprits) == 0:
            return f"✅  You achieved your objective of having no open source libraries with license issues."
        else:
            return f"❌  You failed to meet your objective of having no open source libraries with license issues."

    def generateFindingsTable(self, libraries, options):
        md = "| Vulnerabilities | License | Library | Latest version | Location(s) |\n"
        md += "|----|----|----|----|----|\n"

        for library in sorted(libraries, key=lambda lib: Objective.sortBySeverity(lib.vulnerabilityRisk.severity))[0:self.MAX_FINDINGS]:
            vulnCheck = "⚠️" if library.vulnerabilityRisk.meetsObjective else "❌"
            licenseCheck = "✅" if library.licenseRisk.meetsObjective else "❌"
            suffix = self.formatInfoLine(library)
            locations = "<br />".join(self.decorateLink(options, file, file) for file in library.files)
            md += f"| {vulnCheck} | {licenseCheck} | {library.name} {library.version}{suffix} | {library.latestVersion} | {locations} |\n"

        if len(libraries) > self.MAX_FINDINGS:
            md += f"| | ... {len(libraries) - self.MAX_FINDINGS} more vulnerable open source libraries | |\n"

        return f"{md}\n"

    def formatInfoLine(self, library):
        info = "(Transitive) " if library.transitive else ""
        if len(library.vulnerabilities) > 0:
            formatVulnLink = lambda vuln: f"[{vuln.id}]({vuln.link})" if vuln.link else vuln.id
            info += ", ".join(formatVulnLink(vuln) for vuln in library.vulnerabilities)
        return f"<br />*{info}*" if info else ""

    def findUpdatedLibraries(self, previous, current):
        getKey = lambda library: f"{library.name}@{library.version}"
        currentKeys = set(getKey(lib) for lib in current)
        return [lib for lib in previous if not getKey(lib) in currentKeys]

    def getBaseline(self, feedback):
        if self.previousFeedback is None:
            return feedback["metadata"]["timestamp"][0:10]
        return self.previousFeedback["metadata"]["timestamp"][0:10]

    def getCapability(self):
        return OPEN_SOURCE_HEALTH

    def getMarkdownFile(self, options):
        return os.path.abspath(f"{options.outputDir}/osh-feedback.md")

    def isObjectiveSuccess(self, feedback, options):
        libraries = list(self.processor.extractLibraries(feedback))
        fixable = [lib for lib in libraries if not lib.meetsObjectives() and lib.fixable]
        return len(fixable) == 0

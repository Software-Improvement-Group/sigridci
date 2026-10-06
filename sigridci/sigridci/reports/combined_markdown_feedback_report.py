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
from typing import Any, Iterator

from .architecture_markdown_report import ArchitectureMarkdownReport
from .maintainability_markdown_report import MaintainabilityMarkdownReport
from .markdown_fragment import FeedbackFinding, MarkdownFragment, Location
from .osh_markdown_report import OpenSourceHealthMarkdownReport
from .report import Report
from .security_markdown_report import SecurityMarkdownReport
from ..capability import MAINTAINABILITY, Capability, ARCHITECTURE, OPEN_SOURCE_HEALTH, SECURITY
from ..platform import Platform, OSH_EXCLUDE_DOCS, SECURITY_EXCLUDE_RULE_DOCS, SECURITY_EXCLUDE_FILE_DOCS, \
    AQ_EXCLUDE_DOCS
from ..publish_options import PublishOptions
from ..telemetry import Telemetry


class CombinedMarkdownFeedbackReport(Report):
    MAINTAINABILITY_SYMBOLS = {
        "VERY_HIGH" : "🔴",
        "HIGH" : "🟠",
        "MODERATE" : "🟡",
        "MEDIUM" : "🟡",
        "LOW" : "🟢",
        "UNKNOWN" : "⚪️"
    }

    SEVERITY_SYMBOLS = {
        "CRITICAL" : "🟣",
        "HIGH" : "🔴",
        "MEDIUM" : "🟠",
        "LOW" : "🟡",
        "NONE" : "🟢",
        "INFORMATION" : "🔵",
        "UNKNOWN" : "⚪️"
    }

    def __init__(self, objectives: dict[str, Any]):
        self.objectives = objectives
        self.previousFeedback: dict[Capability, dict] = {}

        self.tableLineSeparator = "<br />" if Platform.isHtmlMarkdownSupported() else " • "
        self.decorateLinks = True

    def prepareFragments(self, options: PublishOptions) -> Iterator[MarkdownFragment]:
        if MAINTAINABILITY in options.capabilities:
            yield MaintainabilityMarkdownReport(self.objectives)
        if ARCHITECTURE in options.capabilities:
            yield ArchitectureMarkdownReport()
        if OPEN_SOURCE_HEALTH in options.capabilities:
            vulnerabilityObjective = self.objectives.get("OSH_MAX_SEVERITY")
            licenseObjective = self.objectives.get("OSH_MAX_LICENSE_RISK")
            yield OpenSourceHealthMarkdownReport(options, vulnerabilityObjective, licenseObjective)
        if SECURITY in options.capabilities:
            securityObjective = self.objectives.get("SECURITY_MAX_SEVERITY")
            yield SecurityMarkdownReport(options, securityObjective or "CRITICAL")

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        with open(os.path.abspath(f"{options.outputDir}/feedback.md"), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            yield from fragment.getFindings(capabilityFeedback, options)

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            yield from fragment.getPositiveFindings(capabilityFeedback, options)

    def sortFindings(self, finding: FeedbackFinding) -> int:
        if finding.capability == MAINTAINABILITY:
            severities = list(self.MAINTAINABILITY_SYMBOLS.keys())
            return severities.index(finding.severity) + 100 if finding.severity in severities else 999
        else:
            severities = list(self.SEVERITY_SYMBOLS.keys())
            return severities.index(finding.severity) if finding.severity in severities else 999

    def renderMarkdown(self, analysisId: str, feedback: dict, options: PublishOptions) -> str:
        negative = sorted(self.getFindings(feedback, options), key=self.sortFindings)
        positive = sorted(self.getPositiveFindings(feedback, options), key=self.sortFindings)

        md = f"# [Sigrid]({options.sigridURL}) objectives check: {self.renderConclusion(feedback, options)}\n\n"
        md += self.renderObjectiveSummary(feedback, options)
        if len(negative) > 0:
            md += "#### Failed checks\n\n"
            md += self.renderFindingsTable(negative, options)
        if len(positive) > 0:
            md += "#### What went well\n\n"
            md += self.renderDetailsStart("Things that went well")
            md += self.renderFindingsTable(positive, options)
            md += self.renderDetailsEnd()
        md += self.renderFooter(options)
        return md

    def renderConclusion(self, feedback: dict, options: PublishOptions) -> str:
        success = self.getExitCode(feedback, options) == 0
        return "✅ Passed" if success else "❌ Failed"

    def renderObjectiveSummary(self, feedback: dict, options: PublishOptions) -> str:
        md = ""
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            for summaryLine in fragment.getSummary(capabilityFeedback, options):
                symbol = "✅" if fragment.isObjectiveSuccess(capabilityFeedback, options) else "❌"
                md += f"- {symbol} **{fragment.getCapability().displayName}** {summaryLine}\n"
        return md + "\n"

    def renderFindingsTable(self, findings: list[FeedbackFinding], options: PublishOptions) -> str:
        md = "| Risk | Finding | Details | Location | Actions |\n"
        md += "|-----|---------|---------|----------|---------|\n"
        for finding in findings:
            symbol = self.renderSeverity(finding)
            title = f"**{finding.capability.displayName}**{self.tableLineSeparator}{finding.title}"
            location = self.tableLineSeparator.join(self.renderLocation(loc, options) for loc in finding.locations)
            actions = self.renderActionLink(finding.capability)
            md += f"| {symbol} | {title} | {finding.details} | {location} | {actions} |\n"
        return md + "\n\n"

    def renderDetailsStart(self, title) -> str:
        if Platform.isHtmlMarkdownSupported():
            return f"<details><summary>**{title}**</summary>\n\n"
        else:
            return f"**{title}**"

    def renderDetailsEnd(self) -> str:
        if Platform.isHtmlMarkdownSupported():
            return "\n</details>\n\n"
        else:
            return "\n"

    def renderLocation(self, location: Location, options: PublishOptions) -> str:
        filePath = location.file
        if options.subsystem and filePath.startswith(f"{options.subsystem}/"):
            filePath = filePath[len(options.subsystem) + 1:]

        label = filePath.split("/")[-1].split("\\")[-1]
        link = Platform.createPullRequestFileURL(filePath, location.line)
        if not link or not self.decorateLinks:
            return label
        return f"[{self.escapeMarkdownLabel(label)}]({link})"

    def escapeMarkdownLabel(self, label: str) -> str:
        return label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")

    def renderFooter(self, options: PublishOptions) -> str:
        md = "----\n\n"
        md += f"[**View this system in Sigrid**]({self.getSigridUrl(options)})\n\n"
        if options.feedbackURL:
            telemetry = Telemetry(options)
            url = telemetry.getURL("sigridci.feedbackview", "sigridci.feedbackview")
            md += f"![© Software Improvement Group]({url})"
        return md

    def renderSeverity(self, finding: FeedbackFinding) -> str:
        if finding.capability == MAINTAINABILITY:
            return self.MAINTAINABILITY_SYMBOLS.get(finding.severity) or "⚪️"
        else:
            return self.SEVERITY_SYMBOLS.get(finding.severity) or "⚪️"

    def renderActionLink(self, capability: Capability) -> str:
        if capability == ARCHITECTURE:
            return f"[Exclude]({AQ_EXCLUDE_DOCS})"
        elif capability == OPEN_SOURCE_HEALTH:
            return f"[Exclude]({OSH_EXCLUDE_DOCS})"
        elif capability == SECURITY:
            excludeFile = f"[Exclude file]({SECURITY_EXCLUDE_FILE_DOCS})"
            excludeRule = f"[Exclude rule]({SECURITY_EXCLUDE_RULE_DOCS})"
            return f"{excludeFile}{self.tableLineSeparator}{excludeRule}"
        else:
            return ""

    def getExitCode(self, feedback: dict[Capability, dict], options: PublishOptions) -> int:
        exitCode = 0
        for fragment in self.prepareFragments(options):
            capability = fragment.getCapability()
            if not fragment.isObjectiveSuccess(feedback[capability], options):
                exitCode += capability.exitCode
        return exitCode

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

import html
import os
import re
from typing import Any, Iterator

from .architecture_markdown_report import ArchitectureMarkdownReport
from .maintainability_markdown_report import MaintainabilityMarkdownReport
from .markdown_fragment import FeedbackFinding, MarkdownFragment, Location
from .osh_markdown_report import OpenSourceHealthMarkdownReport
from .report import Report
from .security_markdown_report import SecurityMarkdownReport
from ..capability import MAINTAINABILITY, Capability, ARCHITECTURE, OPEN_SOURCE_HEALTH, SECURITY
from ..objective import ObjectiveStatus
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

    FILE_PATH_PATTERN = re.compile(r'[/\\]')

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
            previous = self.previousFeedback.get(OPEN_SOURCE_HEALTH)
            yield OpenSourceHealthMarkdownReport(options, self.objectives, previous)
        if SECURITY in options.capabilities:
            previous = self.previousFeedback.get(SECURITY)
            yield SecurityMarkdownReport(options, self.objectives, previous)

    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        with open(os.path.abspath(f"{options.outputDir}/feedback.md"), "w", encoding="utf-8") as f:
            f.write(self.renderMarkdown(analysisId, feedback, options))

    def getFindings(self, feedback: dict, options: PublishOptions) -> list[FeedbackFinding]:
        findings: list[FeedbackFinding] = []
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            findings.extend(fragment.getFindings(capabilityFeedback, options))
        return sorted(findings, key=self.sortFindings)

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> list[FeedbackFinding]:
        findings: list[FeedbackFinding] = []
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            findings.extend(fragment.getPositiveFindings(capabilityFeedback, options))
        return sorted(findings, key=self.sortFindings)

    def getNonUrgentFindings(self, feedback: dict, options: PublishOptions) -> list[FeedbackFinding]:
        findings: list[FeedbackFinding] = []
        for fragment in self.prepareFragments(options):
            capabilityFeedback = feedback[fragment.getCapability()]
            findings.extend(fragment.getNonUrgentFindings(capabilityFeedback, options))
        return sorted(findings, key=self.sortFindings)

    def sortFindings(self, finding: FeedbackFinding) -> int:
        if finding.capability == MAINTAINABILITY:
            severities = list(self.MAINTAINABILITY_SYMBOLS.keys())
            return severities.index(finding.severity) + 100 if finding.severity in severities else 999
        else:
            severities = list(self.SEVERITY_SYMBOLS.keys())
            return severities.index(finding.severity) if finding.severity in severities else 999

    def renderMarkdown(self, analysisId: str, feedback: dict, options: PublishOptions) -> str:
        negative = self.getFindings(feedback, options)
        nonurgent = self.getNonUrgentFindings(feedback, options)
        positive = self.getPositiveFindings(feedback, options)

        md = f"# [Sigrid]({options.sigridURL}) objectives check: {self.renderConclusion(feedback, options)}\n\n"
        md += self.renderObjectiveSummary(feedback, options)
        if len(negative) > 0:
            md += "#### Failed checks\n\n"
            md += "Risk: 🟣 critical | 🔴 high | 🟠 medium | 🟡 low |\n\n"
            md += self.renderFindingsTable(negative, options)
        if len(nonurgent) > 0:
            md += self.renderDetailsStart("Non-urgent findings")
            md += "These findings do not fail your objectives, but you might still want to look at them.\n\n"
            md += self.renderFindingsTable(nonurgent, options)
            md += self.renderDetailsEnd()
        if len(positive) > 0:
            md += self.renderDetailsStart(f"Things that went well: You fixed/improved {len(positive)} findings")
            md += self.renderFindingsTable(positive, options)
            md += self.renderDetailsEnd()
        if MAINTAINABILITY in options.capabilities:
            maintainabilityReport = MaintainabilityMarkdownReport(self.objectives)
            if not ObjectiveStatus.UNKNOWN in maintainabilityReport.getObjectiveStatuses(feedback[MAINTAINABILITY]):
                md += self.renderDetailsStart("Detailed maintainability ratings")
                md += maintainabilityReport.renderRatingsTable(feedback[MAINTAINABILITY])
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
            for summary in fragment.getSummary(capabilityFeedback, options):
                capabilityName = fragment.getCapability().displayName
                capabilitySuffix = " (Beta)" if fragment.getCapability().beta else ""
                md += f"- {summary.symbol}  **{capabilityName}{capabilitySuffix}:** {summary.text}\n"
        return f"{md}\n"

    def renderFindingsTable(self, findings: list[FeedbackFinding], options: PublishOptions) -> str:
        md = "| Risk | Finding | Details | Location | Actions |\n"
        md += "|------|---------|---------|----------|---------|\n"
        for finding in findings[0:options.getMaxShownFindings()]:
            symbol = self.renderSeverity(finding)
            title = f"**{finding.capability.displayName}**{self.tableLineSeparator}{self.escapeMarkdownCell(finding.title)}"
            details = self.tableLineSeparator.join(self.escapeMarkdownCell(d) for d in finding.details)
            location = self.tableLineSeparator.join(self.renderLocation(loc, options) for loc in finding.locations[0:3])
            actions = self.renderActionLink(finding.capability)
            md += f"| {symbol} | {title} | {details} | {location} | {actions} |\n"
        if len(findings) > options.getMaxShownFindings():
            remaining = len(findings) - options.getMaxShownFindings()
            md += f"| ⚪️ | ... and {remaining} more findings | | | |\n"
        return f"{md}\n"

    def renderDetailsStart(self, title: str) -> str:
        if Platform.isHtmlMarkdownSupported():
            return f"<details><summary><strong>{title}</strong></summary>\n\n"
        else:
            return f"**{title}**\n\n"

    def renderDetailsEnd(self) -> str:
        if Platform.isHtmlMarkdownSupported():
            return "\n</details>\n\n"
        else:
            return "\n"

    def renderLocation(self, location: Location, options: PublishOptions) -> str:
        filePath = location.file
        if options.subsystem and filePath.startswith(f"{options.subsystem}/"):
            filePath = filePath[len(options.subsystem) + 1:]

        label = self.formatLocationLabel(location)
        link = Platform.createPullRequestFileURL(filePath, location.line)
        if not link or not self.decorateLinks:
            return label
        return f"[{self.escapeMarkdownLabel(label)}]({link})"

    def formatLocationLabel(self, location: Location) -> str:
        label = self.FILE_PATH_PATTERN.split(location.file)[-1]
        if location.line > 1:
            label += f" (line {location.line})"
        return label

    def escapeMarkdownCell(self, label: str) -> str:
        return html.escape(label.replace("|", " ").replace("\n", ""))

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

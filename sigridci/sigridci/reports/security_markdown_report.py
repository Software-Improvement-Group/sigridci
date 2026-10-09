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

from .markdown_fragment import MarkdownFragment, FeedbackFinding, Location, Summary
from ..analysisresults.sarif_processor import SarifProcessor, FindingStatus, Finding
from ..capability import SECURITY, Capability
from ..objective import Objective
from ..publish_options import PublishOptions


class SecurityMarkdownReport(MarkdownFragment):
    # We phrase objectives as the "worst" severity that is still allowed.
    # So an objective of HIGH means critical findings are not allowed,
    # but high findings are allowed.
    OBJECTIVE_SEVERITY_SUMMARIES = {
        "CRITICAL" : "any",
        "HIGH" : "no critical",
        "MEDIUM" : "no critical or high",
        "LOW" : "no critical, high or medium",
        "INFORMATION" : "no critical, high, medium, or low",
        "NONE" : "no"
    }

    def __init__(self, options: PublishOptions, objectives: dict[str, Any], previousFeedback: Any = None):
        self.objective = objectives.get("SECURITY_MAX_SEVERITY") or Objective.DEFAULT_FINDING_OBJECTIVE
        self.processor = SarifProcessor(options, self.objective)
        self.previousFeedback = previousFeedback

    def getSummary(self, feedback: dict, options: PublishOptions) -> list[Summary]:
        severitySummary = self.OBJECTIVE_SEVERITY_SUMMARIES.get(self.objective) or "N/A"
        if self.isObjectiveSuccess(feedback, options):
            return [Summary("✅ ", f"You achieved your objective of having {severitySummary} security findings.")]
        else:
            return [Summary("❌️", f"You did not meet your objective of having {severitySummary} security findings.")]

    def getCapability(self) -> Capability:
        return SECURITY

    def getMarkdownFile(self, options: PublishOptions) -> str:
        return os.path.abspath(f"{options.outputDir}/security-feedback.md")

    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        allFindings = self.extractFindings(feedback)
        relevantFindings = self.processor.filterStatus(allFindings, FindingStatus.INTRODUCED, partOfObjective=True)
        return len(relevantFindings) == 0

    def extractFindings(self, feedback: dict) -> list[Finding]:
        findings = list(self.processor.extractFindings(feedback))

        if self.previousFeedback is not None:
            # For on-premise Sigrid we need to check for new findings ourselves,
            # since we don't have an end point to perform that logic.
            previousFindings = list(self.processor.extractFindings(self.previousFeedback))
            previousFingerprints = [finding.fingerprint for finding in previousFindings]

            for finding in findings:
                if finding.status == FindingStatus.REMAINING and finding.fingerprint not in previousFingerprints:
                    finding.status = FindingStatus.INTRODUCED

        return findings

    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        findings = self.extractFindings(feedback)
        for finding in self.processor.filterStatus(findings, FindingStatus.INTRODUCED, partOfObjective=True):
            yield self.convertFinding(finding)

    def getNonUrgentFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        findings = self.extractFindings(feedback)
        for finding in self.processor.filterStatus(findings, FindingStatus.INTRODUCED, partOfObjective=False):
            if not finding.partOfObjective:
                yield self.convertFinding(finding)

    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        findings = self.extractFindings(feedback)
        for finding in self.processor.filterStatus(findings, FindingStatus.FIXED, partOfObjective=False):
            yield self.convertFinding(finding)

    def convertFinding(self, finding: Finding) -> FeedbackFinding:
        location = Location(finding.file, finding.line)
        return FeedbackFinding(finding.risk, SECURITY, finding.title, [finding.description], [location])

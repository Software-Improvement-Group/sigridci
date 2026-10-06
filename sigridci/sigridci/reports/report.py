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

import urllib.parse
from abc import ABC, abstractmethod
from datetime import datetime

from ..capability import Capability
from ..platform import Platform
from ..publish_options import PublishOptions
from ..telemetry import Telemetry


class Report(ABC):
    RISK_CATEGORIES = ["VERY_HIGH", "HIGH", "MODERATE", "MEDIUM", "LOW"]
    GOOD_CATEGORIES = ["fixed", "improved"]
    BAD_CATEGORIES = ["introduced", "worsened"]
    UNCHANGED_CATEGORIES = ["unchanged"]

    @abstractmethod
    def generate(self, analysisId: str, feedback: dict, options: PublishOptions) -> None:
        pass

    def formatMetricName(self, metric: str) -> str:
        return metric.replace("_PROP", "").title().replace("_", " ")

    def formatRating(self, ratings: dict[str, float], metric: str, naText: str = "N/A") -> str:
        if ratings.get(metric, None) == None:
            return naText
        return "%.1f" % ratings[metric]

    def formatBaseline(self, feedback: dict) -> str:
        if not feedback.get("baseline", None):
            return "N/A"
        snapshotDate = datetime.strptime(feedback["baseline"], "%Y%m%d")
        return snapshotDate.strftime("%Y-%m-%d")

    def getRefactoringCandidates(self, feedback: dict, metric: str) -> list[dict]:
        refactoringCandidates = feedback.get("refactoringCandidates", [])
        return [rc for rc in refactoringCandidates if rc["metric"] == metric or metric == "MAINTAINABILITY"]

    def filterRefactoringCandidates(self, feedback: dict, categories: list[str]) -> list[dict]:
        matches = [rc for rc in feedback.get("refactoringCandidates", []) if rc["category"] in categories]
        matches.sort(key=lambda rc: self.RISK_CATEGORIES.index(rc.get("riskCategory", "")))
        return matches

    def getSigridUrl(self, options: PublishOptions) -> str:
        customer = urllib.parse.quote_plus(options.customer.lower())
        system = urllib.parse.quote_plus(options.system.lower())
        return f"{options.sigridURL}/{customer}/{system}"


class MarkdownRenderer(Report, ABC):
    def __init__(self):
        self.decorateLinks = True
        self.tableLineSeparator = "<br />" if Platform.isHtmlMarkdownSupported() else " • "

    @abstractmethod
    def renderMarkdown(self, analysisId: str, feedback: dict, options: PublishOptions) -> str:
        pass

    def renderMarkdownTemplate(self, feedback: dict, options: PublishOptions, details: str, sigridLink: str) -> str:
        md = f"# {self.formatTitle(sigridLink)}\n\n"
        for summaryLine in self.getSummary(feedback, options):
            md += f"**{summaryLine}**\n\n"
        if len(details) > 0:
            if Platform.isHtmlMarkdownSupported():
                md += "<details><summary>Show details</summary>\n\n"
            md += details
            if Platform.isHtmlMarkdownSupported():
                md += "</details>\n\n"
        md += self.renderFooter(options, sigridLink)
        return md

    def formatTitle(self, sigridLink: str) -> str:
        capability = self.getCapability()
        suffix = " *(Beta)*" if capability.beta else ""
        return f"[Sigrid]({sigridLink}) {capability.displayName} feedback{suffix}"

    def renderFooter(self, options: PublishOptions, sigridLink: str) -> str:
        md = "----\n\n"
        md += f"[**View this system in Sigrid**]({sigridLink})\n\n"
        if options.feedbackURL:
            telemetry = Telemetry(options)
            url = telemetry.getURL("sigridci.feedbackview", f"sigridci.feedbackview.{self.getCapability().shortName}")
            md += f"![© Software Improvement Group]({url})"
        return md

    @abstractmethod
    def getSummary(self, feedback: dict, options: PublishOptions) -> list[str]:
        pass

    @abstractmethod
    def getCapability(self) -> Capability:
        pass

    @abstractmethod
    def getMarkdownFile(self, options: PublishOptions) -> str:
        pass

    @abstractmethod
    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        pass

    def decorateLink(self, options: PublishOptions, label: str, file: str, line: int = 0) -> str:
        if options.subsystem and file.startswith(f"{options.subsystem}/"):
            file = file[len(options.subsystem) + 1:]
        link = Platform.createPullRequestFileURL(file, line)
        if not link or not self.decorateLinks:
            return label
        return f"[{self.escapeMarkdownLabel(label)}]({link})"

    def escapeMarkdownLabel(self, label: str) -> str:
        return label.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")

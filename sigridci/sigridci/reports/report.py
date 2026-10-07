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

from ..publish_options import PublishOptions


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

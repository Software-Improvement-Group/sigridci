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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterator

from ..capability import Capability
from ..publish_options import PublishOptions


@dataclass(frozen=True)
class Summary:
    symbol: str
    text: str


@dataclass(frozen=True)
class Location:
    file: str
    line: int = 0


@dataclass(frozen=True)
class FeedbackFinding:
    severity: str
    capability: Capability
    title: str
    details: list[str]
    locations: list[Location]


class MarkdownFragment(ABC):
    @abstractmethod
    def getCapability(self) -> Capability:
        pass

    @abstractmethod
    def isObjectiveSuccess(self, feedback: dict, options: PublishOptions) -> bool:
        pass

    @abstractmethod
    def getSummary(self, feedback: dict, options: PublishOptions) -> list[Summary]:
        pass

    @abstractmethod
    def getFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        pass

    @abstractmethod
    def getNonUrgentFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        pass

    @abstractmethod
    def getPositiveFindings(self, feedback: dict, options: PublishOptions) -> Iterator[FeedbackFinding]:
        pass

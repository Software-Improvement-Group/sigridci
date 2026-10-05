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
from typing import Any, Union

from .report import Report, MarkdownRenderer
from ..capability import MAINTAINABILITY, Capability
from ..objective import Objective, ObjectiveStatus
from ..platform import Platform
from ..publish_options import PublishOptions


class MarkdownFeedbackReport:
    def __init__(self, objectives: dict[str, Any], decorateLinks: bool):
        self.objectives = objectives
        self.decorateLinks = decorateLinks

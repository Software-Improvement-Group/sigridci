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
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union


class RunMode(Enum):
    FEEDBACK_ONLY = 1
    FEEDBACK_AND_PUBLISH = 2
    PUBLISH_ONLY = 3


@dataclass
class PublishOptions:
    customer: str
    system: str
    runMode: RunMode
    sourceDir: str = "."
    subsystem: str = ""
    excludePatterns: List[str] = field(default_factory=lambda: [])
    includePatterns: List[str] = field(default_factory=lambda: [])
    includeHistory: bool = False
    showUploadContents: bool = False
    convert: str = None
    targetRating: Union[float, str] = "sigrid"
    outputDir: str = "sigrid-ci-output"
    sigridURL: str = "https://sigrid-says.com"
    feedbackURL: str = "https://docs.sigrid-says.com/landing/feedback.html"
    partner: str = "sig"

    SYSTEM_NAME_PATTERN = re.compile("^[a-z0-9]+(-[a-z0-9]+)*$", re.IGNORECASE)
    SYSTEM_NAME_LENGTH = range(2, 65)

    def getSystemId(self):
        return f"{self.partner}-{self.customer}-{self.system}"

    def isValidSystemName(self):
        return self.SYSTEM_NAME_PATTERN.match(self.system) and \
            len(self.system) >= self.SYSTEM_NAME_LENGTH.start and \
            not self.system.isdigit() and \
            (len(self.system) + len(self.customer) + 1) in self.SYSTEM_NAME_LENGTH

    def readScopeFile(self):
        return self.locateFile(["sigrid.yaml", "sigrid.yml"])

    def readMetadataFile(self):
        return self.locateFile(["sigrid-metadata.yaml", "sigrid-metadata.yml"])

    def locateFile(self, possibleFileNames):
        for file in possibleFileNames:
            if os.path.exists(f"{self.sourceDir}/{file}"):
                with open(f"{self.sourceDir}/{file}", "r") as f:
                    return f.read()
        return None

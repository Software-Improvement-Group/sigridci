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

from dataclasses import dataclass


@dataclass
class Capability:
    name: str
    displayName: str
    shortName: str
    exitCode: int
    beta: bool


MAINTAINABILITY = Capability("MAINTAINABILITY", "Maintainability", "maintainability", 2, False)
OPEN_SOURCE_HEALTH = Capability("OPEN_SOURCE_HEALTH", "Open Source Health", "osh", 4, False)
SECURITY = Capability("SECURITY", "Security", "security", 8, True)

CAPABILITY_SHORT_NAMES = {cap.shortName: cap for cap in [MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY]}

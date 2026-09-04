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

import sys
from argparse import SUPPRESS

from .capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY


CAPABILITIES = {cap.shortName: cap for cap in [MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY]}
DEFAULT_CAPABILITIES = "maintainability,osh,security"


def parseCapabilities(names):
    try:
        return [CAPABILITIES[name.lower().strip()] for name in names.split(",")]
    except KeyError as e:
        print(f"Invalid value for --capability: {str(e)}")
        sys.exit(1)


def addSigridConnectionArguments(parser):
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--customer", type=str, required=True, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, required=True, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help="Sigrid base URL.")


def addPublishArguments(parser):
    addSigridConnectionArguments(parser)
    parser.add_argument("--ignore-missing-scope-file", action="store_true", help="File sigrid.yaml is handled separately.")
    parser.add_argument("--subsystem", type=str, default="", help="Publishes your code as a subsystem within a Sigrid system.")
    parser.add_argument("--convert", type=str, default="", help="Code conversion for specific technologies")
    parser.add_argument("--source", type=str, required=True, help="Path of your project's source code.")
    parser.add_argument("--capability", type=str, default=DEFAULT_CAPABILITIES, help=f"Comma-separated Sigrid capabilities ({','.join(CAPABILITIES.keys())}).")
    parser.add_argument("--exclude", type=str, default="", help="Comma-separated list of files/directories to exclude.")
    parser.add_argument("--include", type=str, default="", help="Comma-separated list of files/directories to include.")

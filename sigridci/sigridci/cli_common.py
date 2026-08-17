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
import sys
from argparse import SUPPRESS

from .capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY
from .platform import Platform
from .publish_options import PublishOptions, RunMode
from .sigrid_api_client import SigridApiClient
from .sigridci_runner import SigridCiRunner
from .upload_log import UploadLog


CAPABILITIES = {cap.shortName: cap for cap in [MAINTAINABILITY, OPEN_SOURCE_HEALTH, SECURITY]}
DEFAULT_CAPABILITIES = "maintainability,osh"


def parseCapabilities(names):
    try:
        return [CAPABILITIES[name.lower().strip()] for name in names.split(",")]
    except KeyError as e:
        print(f"Invalid value for --capability: {str(e)}")
        sys.exit(1)


def addCommonArguments(parser):
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--ignore-missing-scope-file", action="store_true", help="File sigrid.yaml is handled separately.")
    parser.add_argument("--customer", type=str, required=True, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, required=True, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--subsystem", type=str, default="", help="Publishes your code as a subsystem within a Sigrid system.")
    parser.add_argument("--convert", type=str, default="", help="Code conversion for specific technologies")
    parser.add_argument("--source", type=str, required=True, help="Path of your project's source code.")
    parser.add_argument("--capability", type=str, default=DEFAULT_CAPABILITIES, help=f"Comma-separated Sigrid capabilities ({','.join(CAPABILITIES.keys())}).")
    parser.add_argument("--exclude", type=str, default="", help="Comma-separated list of files/directories to exclude.")
    parser.add_argument("--include", type=str, default="", help="Comma-separated list of files/directories to include.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help="Sigrid base URL.")


def validateOptions(options):
    if not options.isValidSystemName():
        maxNameLength = PublishOptions.SYSTEM_NAME_LENGTH.stop - (len(options.customer) + 1)
        print(f"Invalid system name, system name should match '{PublishOptions.SYSTEM_NAME_PATTERN.pattern}' "
              f", not completely numeric, and be {PublishOptions.SYSTEM_NAME_LENGTH.start} to {maxNameLength} characters long (inclusive).")
        sys.exit(1)

    if not options.isValidSubSystemName():
        print(f"Invalid subsystem name, subsystem name should match '{PublishOptions.SUBSYSTEM_NAME_PATTERN.pattern}'"
              ", must be at least two characters long and not contain consecutive dots or slashes.")
        sys.exit(1)


def runSigridCi(options):
    if not os.path.exists(options.sourceDir):
        print(f"Source code directory not found: {options.sourceDir}")
        sys.exit(1)

    validateOptions(options)
    Platform.checkEnvironment()

    UploadLog.log("Starting Sigrid CI")
    runner = SigridCiRunner(options, SigridApiClient(options))
    exitCode = runner.run()
    if options.runMode == RunMode.FEEDBACK_ONLY:
        sys.exit(exitCode)

#!/usr/bin/env python3

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
from argparse import ArgumentParser, SUPPRESS

from sigridci.capability import MAINTAINABILITY, OPEN_SOURCE_HEALTH
from sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigrid_api_client import SigridApiClient
from sigridci.platform import Platform
from sigridci.sigridci_runner import SigridCiRunner
from sigridci.upload_log import UploadLog


CAPABILITIES = {cap.shortName: cap for cap in [MAINTAINABILITY, OPEN_SOURCE_HEALTH]}


def parsePublishOptions(args):
    return PublishOptions(
        partner=args.partner.lower(),
        customer=args.customer.lower(),
        system=args.system.lower(),
        subsystem=args.subsystem,
        convert=args.convert,
        runMode=parseRunMode(args),
        capabilities=parseCapabilities(args.capability),
        sourceDir=args.source,
        excludePatterns=args.exclude.split(","),
        includePatterns=args.include.split(","),
        includeHistory=True,
        showUploadContents=args.showupload,
        outputDir=args.out,
        sigridURL=args.sigridurl,
        ignoreMissingScopeFile=args.ignore_missing_scope_file
    )


def parseRunMode(args):
    if args.publishonly:
        return RunMode.PUBLISH_ONLY
    elif args.publish:
        return RunMode.FEEDBACK_AND_PUBLISH
    else:
        return RunMode.FEEDBACK_ONLY


def parseTarget(target):
    if target == "sigrid":
        return "sigrid"
    return float(target)


def parseCapabilities(names):
    try:
        return [CAPABILITIES[name.lower().strip()] for name in names.split(",")]
    except KeyError as e:
        print(f"Invalid value for --capability: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    parser = ArgumentParser(description="Starts a Sigrid CI analysis and provides feedback on the outcomes.")
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--ignore-missing-scope-file", action="store_true", help="File sigrid.yaml is handled separately.")
    parser.add_argument("--customer", type=str, required=True, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, required=True, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--subsystem", type=str, default="", help="Publishes your code as a subsystem within a Sigrid system.")
    parser.add_argument("--convert", type=str, default="", help="Code conversion for specific technologies")
    parser.add_argument("--source", type=str, required=True, help="Path of your project's source code.")
    parser.add_argument("--capability", type=str, default="maintainability", help=f"Comma-separated Sigrid capabilities ({','.join(CAPABILITIES.keys())}).")
    parser.add_argument("--publish", action="store_true", help="Publishes analysis results to Sigrid.")
    parser.add_argument("--publishonly", action="store_true", help="Only publishes to Sigrid without waiting for results.")
    parser.add_argument("--exclude", type=str, default="", help="Comma-separated list of files/directories to exclude.")
    parser.add_argument("--include", type=str, default="", help="Comma-separated list of files/directories to include.")
    parser.add_argument("--showupload", action="store_true", help="Logs the contents of the upload published to Sigrid.")
    parser.add_argument("--out", type=str, default="sigrid-ci-output", help="Output directory for Sigrid CI feedback.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help="Sigrid base URL.")
    # These options are now obsolete, but we leave them here to avoid breaking people's configuration.
    parser.add_argument("--include-history", action="store_true", help=SUPPRESS)
    parser.add_argument("--targetquality", type=str, help=SUPPRESS)
    # Dummy argument used when passing false to boolean arguments.
    # BooleanOptionalAction would solve this, but requires Python 3.9+.
    parser.add_argument("--dummy", action="store_true", help=SUPPRESS)
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"Source code directory not found: {args.source}")
        sys.exit(1)

    Platform.checkEnvironment()
    options = parsePublishOptions(args)
    apiClient = SigridApiClient(options)

    if not options.isValidSystemName():
        maxNameLength = PublishOptions.SYSTEM_NAME_LENGTH.stop - (len(args.customer) + 1)
        print(f"Invalid system name, system name should match '{PublishOptions.SYSTEM_NAME_PATTERN.pattern}' "
              f", not completely numeric, and be {PublishOptions.SYSTEM_NAME_LENGTH.start} to {maxNameLength} characters long (inclusive).")
        sys.exit(1)
    
    if not options.isValidSubSystemName():
        print(f"Invalid subsystem name, subsystem name should match '{PublishOptions.SUBSYSTEM_NAME_PATTERN.pattern}'"
              ", must be at least two characters long and not contain consecutive dots or slashes.")
        sys.exit(1)

    UploadLog.log("Starting Sigrid CI")
    runner = SigridCiRunner(options, apiClient)
    exitCode = runner.run()
    if options.runMode == RunMode.FEEDBACK_ONLY:
        sys.exit(exitCode)

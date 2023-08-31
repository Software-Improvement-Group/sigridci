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

from sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci_runner import SigridCiRunner
from sigridci.upload_log import UploadLog


def parsePublishOptions(args):
    return PublishOptions(
        partner=args.partner.lower(),
        customer=args.customer.lower(),
        system=args.system.lower(),
        subsystem=args.subsystem,
        runMode=parseRunMode(args),
        sourceDir=args.source,
        excludePatterns=args.exclude.split(","),
        includePatterns=[f'/{path}/' for path in args.include.split(",")],
        includeHistory=args.include_history,
        showUploadContents=args.showupload,
        targetRating=parseTarget(args.targetquality),
        sigridURL=args.sigridurl
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


if __name__ == "__main__":
    parser = ArgumentParser(description="Starts a Sigrid CI analysis and provides feedback on the outcomes.")
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--customer", type=str, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--subsystem", type=str, default="", help="Publishes your code as a subsystem within a Sigrid system.")
    parser.add_argument("--source", type=str, help="Path of your project’s source code.")
    parser.add_argument("--targetquality", type=str, default="sigrid", help=SUPPRESS)
    parser.add_argument("--publish", action="store_true", help="Publishes analysis results to Sigrid.")
    parser.add_argument("--publishonly", action="store_true", help="Only publishes to Sigrid without waiting for results.")
    parser.add_argument("--exclude", type=str, default="", help="Comma-separated list of files/directories to exclude.")
    parser.add_argument("--include", type=str, default="", help="Comma-separated list of files/directories to include.")
    parser.add_argument("--showupload", action="store_true", help="Logs the contents of the upload published to Sigrid.")
    parser.add_argument("--include-history", action="store_true", help="Publish repository history to Sigrid.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help=SUPPRESS)
    # Dummy argument used when passing false to boolean arguments.
    # BooleanOptionalAction would solve this, but requires Python 3.9+.
    parser.add_argument("--dummy", action="store_true", help=SUPPRESS)
    args = parser.parse_args()

    if None in [args.customer, args.system, args.source]:
        parser.print_help()
        sys.exit(1)

    if sys.version_info.major == 2 or sys.version_info.minor < 7:
        print("Sigrid CI requires Python 3.7 or higher")
        sys.exit(1)

    if not SigridApiClient.isValidToken(os.environ.get("SIGRID_CI_TOKEN", None)):
        print("Missing or incomplete environment variable SIGRID_CI_TOKEN")
        sys.exit(1)

    if not os.path.exists(args.source):
        print(f"Source code directory not found: {args.source}")
        sys.exit(1)

    if args.exclude and args.include:
        print(f"You can use either exclude or include. Not both")
        sys.exit(1)

    options = parsePublishOptions(args)
    apiClient = SigridApiClient(options)

    if not options.isValidSystemName():
        maxNameLength = PublishOptions.SYSTEM_NAME_LENGTH.stop - (len(args.customer) + 1)
        print(f"Invalid system name, system name should match '{PublishOptions.SYSTEM_NAME_PATTERN.pattern}' "
              f"and be {PublishOptions.SYSTEM_NAME_LENGTH.start} to {maxNameLength} characters long (inclusive).")
        sys.exit(1)

    UploadLog.log("Starting Sigrid CI")
    runner = SigridCiRunner(options, apiClient)
    runner.run()

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

import argparse
import os
import sys

from sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigrid_api_client import SigridApiClient
from sigridci.sigridci_runner import SigridCiRunner
from sigridci.upload_log import UploadLog


def parsePublishOptions(args):
    return PublishOptions(
        partner=args.partner,
        customer=args.customer,
        system=args.system,
        subsystem=args.subsystem,
        runMode=parseRunMode(args),
        sourceDir=args.source,
        excludePatterns=args.exclude.split(","),
        includeHistory=args.include_history,
        showUploadContents=args.showupload,
        targetRating=args.targetquality
    )


def parseRunMode(args):
    if args.publishonly:
        return RunMode.PUBLISH_ONLY
    elif args.publish:
        return RunMode.FEEDBACK_AND_PUBLISH
    else:
        return RunMode.FEEDBACK_ONLY


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--partner", type=str, default="sig")
    parser.add_argument("--customer", type=str)
    parser.add_argument("--system", type=str)
    parser.add_argument("--source", type=str)
    parser.add_argument("--targetquality", type=str, default="sigrid")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--publishonly", action="store_true")
    parser.add_argument("--exclude", type=str, default="")
    parser.add_argument("--subsystem", type=str, default="")
    parser.add_argument("--showupload", action="store_true")
    parser.add_argument("--include-history", action="store_true")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com")
    # Dummy argument used when passing false to boolean arguments.
    # BooleanOptionalAction would solve this, but requires Python 3.9+.
    parser.add_argument("--dummy", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if None in [args.customer, args.system, args.source]:
        parser.print_help()
        sys.exit(1)

    if sys.version_info.major == 2 or sys.version_info.minor < 7:
        print("Sigrid CI requires Python 3.7 or higher")
        sys.exit(1)

    if not SigridCiRunner.isValidToken(os.environ.get("SIGRID_CI_TOKEN", None)):
        print("Missing or incomplete environment variable SIGRID_CI_TOKEN")
        sys.exit(1)

    if not os.path.exists(args.source):
        print(f"Source code directory not found: {args.source}")
        sys.exit(1)
        
    if not SigridCiRunner.isValidSystemName(args.customer, args.system):
        maxNameLength = SigridCiRunner.SYSTEM_NAME_LENGTH.stop - (len(args.customer) + 1)
        print(f"Invalid system name, system name should match '{SigridCiRunner.SYSTEM_NAME_PATTERN.pattern}' "
              f"and be {SigridCiRunner.SYSTEM_NAME_LENGTH.start} to {maxNameLength} characters long (inclusive).")
        sys.exit(1)

    UploadLog.log("Starting Sigrid CI")

    options = parsePublishOptions(args)
    apiClient = SigridApiClient(options)

    runner = SigridCiRunner(options, apiClient)
    runner.run()

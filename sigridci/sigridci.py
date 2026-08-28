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

from argparse import ArgumentParser, SUPPRESS

from sigridci.cli_options import addPublishArguments, parseCapabilities
from sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci_runner import runAnalysis


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
        detailLevel=args.detaillevel,
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


if __name__ == "__main__":
    parser = ArgumentParser(description="Starts a Sigrid CI analysis and provides feedback on the outcomes.")
    addPublishArguments(parser)
    parser.add_argument("--publish", action="store_true", help="Publishes analysis results to Sigrid.")
    parser.add_argument("--publishonly", action="store_true", help="Only publishes to Sigrid without waiting for results.")
    parser.add_argument("--showupload", action="store_true", help="Logs the contents of the upload published to Sigrid.")
    parser.add_argument("--detaillevel", type=str, default="default", help="Detail level for how much feedback to provide.")
    parser.add_argument("--out", type=str, default="sigrid-ci-output", help="Output directory for Sigrid CI feedback.")
    # These options are now obsolete, but we leave them here to avoid breaking people's configuration.
    parser.add_argument("--include-history", action="store_true", help=SUPPRESS)
    parser.add_argument("--targetquality", type=str, help=SUPPRESS)
    # Dummy argument used when passing false to boolean arguments.
    # BooleanOptionalAction would solve this, but requires Python 3.9+.
    parser.add_argument("--dummy", action="store_true", help=SUPPRESS)
    args = parser.parse_args()

    runAnalysis(parsePublishOptions(args))

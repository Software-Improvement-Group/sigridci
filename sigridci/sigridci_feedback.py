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

import json
import os
import sys
from argparse import ArgumentParser, Namespace
from typing import Any

from sigridci.capability import Capability, CAPABILITY_SHORT_NAMES, SECURITY
from sigridci.cli_options import addSigridConnectionArguments
from sigridci.feedback_provider import FeedbackProvider
from sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigrid_api_client import SigridApiClient


def parseFeedbackOptions(args: Namespace, capability: Capability) -> PublishOptions:
    options = PublishOptions(
        partner=args.partner,
        customer=args.customer,
        system=args.system,
        runMode=RunMode.FEEDBACK_ONLY,
        capabilities=[capability],
        detailLevel=args.detaillevel,
        outputDir=args.out,
        sigridURL=args.sigridurl
    )

    # Don't include the feedback links when running in local/on-premise mode.
    if args.analysisresults:
        options.feedbackURL = ""

    return options


def determineObjectives(options: PublishOptions) -> dict:
    if not os.environ.get("SIGRID_CI_TOKEN"):
        return {}
    apiClient = SigridApiClient(options)
    return apiClient.fetchObjectives()


def loadPreviousAnalysisResults(capability: Capability, options: PublishOptions, origin: str) -> Any:
    if not os.environ.get("SIGRID_CI_TOKEN"):
        return None
    elif capability == SECURITY and origin == "sigrid":
        apiClient = SigridApiClient(options)
        return apiClient.fetchSecurityFindings()
    else:
        with open(origin, mode="r", encoding="utf-8") as f:
            return json.load(f)


if __name__ == "__main__":
    parser = ArgumentParser(description="Provides Sigrid CI feedback for the specified analysis.")
    addSigridConnectionArguments(parser)
    parser.add_argument("--detaillevel", type=str, default="default", help="Detail level for how much feedback to provide.")
    parser.add_argument("--out", type=str, default="sigrid-ci-output", help="Output directory for Sigrid CI feedback.")
    parser.add_argument("--capability", type=str, required=True, choices=list(CAPABILITY_SHORT_NAMES.keys()))
    parser.add_argument("--analysisresults", type=str, required=True, help="Analysis results JSON file.")
    parser.add_argument("--previousresults", type=str, help="Previous results for comparison, either a file or 'sigrid'.")
    args = parser.parse_args()

    capability = CAPABILITY_SHORT_NAMES[args.capability.lower()]
    options = parseFeedbackOptions(args, capability)
    objectives = determineObjectives(options)

    feedbackProvider = FeedbackProvider("local", options, objectives)
    with open(args.analysisresults, mode="r", encoding="utf-8") as f:
        feedbackProvider.registerFeedback(capability, json.load(f))
    if args.previousresults:
        previousFeedback = loadPreviousAnalysisResults(capability, options, args.previousresults)
        feedbackProvider.registerPreviousFeedback(capability, previousFeedback)

    sys.exit(feedbackProvider.generateReports())

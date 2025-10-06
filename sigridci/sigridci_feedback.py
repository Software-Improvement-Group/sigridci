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

from sigridci.feedback_provider import FeedbackProvider
from sigridci.publish_options import PublishOptions, RunMode, Capability
from sigridci.sigrid_api_client import SigridApiClient


OBJECTIVE_SUCCESS_EXIT_CODE = 0
OBJECTIVE_FAILED_EXIT_CODE = 115

CAPABILITIES = {
    "maintainability" : Capability.MAINTAINABILITY,
    "osh" : Capability.OPEN_SOURCE_HEALTH,
    "security" : Capability.SECURITY
}


def parseFeedbackOptions(args):
    options = PublishOptions(
        partner=args.partner,
        customer=args.customer,
        system=args.system,
        runMode=RunMode.FEEDBACK_ONLY,
        capabilities=[CAPABILITIES[args.capability.lower()]],
        outputDir=args.out,
        sigridURL=args.sigridurl
    )

    # Don't include the feedback links when running in local/on-premise mode.
    if args.analysisresults:
        options.feedbackURL = ""

    return options


def determineObjectives(options):
    if not os.environ.get("SIGRID_CI_TOKEN"):
        return {}
    apiClient = SigridApiClient(options)
    return apiClient.fetchObjectives()


if __name__ == "__main__":
    parser = ArgumentParser(description="Provides Sigrid CI feedback for the specified analysis.")
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--customer", type=str, required=True, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, required=True, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--out", type=str, default="sigrid-ci-output", help="Output directory for Sigrid CI feedback.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help="Sigrid base URL.")
    parser.add_argument("--capability", type=str, required=True, choices=list(CAPABILITIES.keys()))
    parser.add_argument("--analysisresults", type=str, required=True, help="Analysis results JSON file.")
    parser.add_argument("--previousresults", type=str, help="Baseline analysis results JSON file used for comparison.")
    args = parser.parse_args()

    options = parseFeedbackOptions(args)
    objectives = determineObjectives(options)

    feedbackProvider = FeedbackProvider(CAPABILITIES[args.capability], options, objectives)
    feedbackProvider.loadLocalAnalysisResults(args.analysisresults)
    if args.previousresults:
        feedbackProvider.loadPreviousAnalysisResults(args.previousresults)
    success = feedbackProvider.generateReports()

    sys.exit(OBJECTIVE_SUCCESS_EXIT_CODE if success else OBJECTIVE_FAILED_EXIT_CODE)

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

from .publish_options import PublishOptions, RunMode
from .sigrid_api_client import SigridApiClient


def checkEnvironment():
    if sys.version_info.major == 2 or sys.version_info.minor < 7:
        print("Sigrid CI requires Python 3.7 or higher")
        sys.exit(1)

    if not SigridApiClient.isValidToken(os.environ.get("SIGRID_CI_TOKEN", None)):
        print("Missing or incomplete environment variable SIGRID_CI_TOKEN")
        sys.exit(1)


def parseFeedbackCommandLineArguments(capability):
    checkEnvironment()

    parser = ArgumentParser(description=f"Produces Sigrid {capability} feedback for the specified analysis.")
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--customer", type=str, help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", type=str, help="Name of your system in Sigrid, letters/digits/hyphens only.")
    parser.add_argument("--out", type=str, default="sigrid-ci-output", help="Output directory for Sigrid CI feedback.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help=SUPPRESS)
    parser.add_argument("--analysisid", type=str, help="Sigrid CI analysis ID.")
    args = parser.parse_args()

    if None in [args.customer, args.system, args.analysisid]:
        parser.print_help()
        sys.exit(1)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    return args


def getFeedbackPublishOptions(args):
    return PublishOptions(
        partner=args.partner,
        customer=args.customer,
        system=args.system,
        runMode=RunMode.FEEDBACK_ONLY,
        outputDir=args.out,
        sigridURL=args.sigridurl
    )

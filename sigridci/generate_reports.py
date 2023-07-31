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
from argparse import ArgumentParser, SUPPRESS

from sigridci.ascii_art_report import AsciiArtReport
from sigridci.junit_format_report import JUnitFormatReport
from sigridci.markdown_report import MarkdownReport
from sigridci.pipeline_summary_report import PipelineSummaryReport
from sigridci.publish_options import PublishOptions, RunMode
from sigridci.static_html_report import StaticHtmlReport


def generateReports(feedbackFile, options, outputDir):
    with open(feedbackFile, "r") as f:
        feedback = json.load(f)

    if not os.path.exists(args.out):
        os.mkdir(args.out)

    reports = [
        AsciiArtReport(),
        MarkdownReport(outputDir),
        StaticHtmlReport(outputDir),
        JUnitFormatReport(outputDir),
        PipelineSummaryReport()
    ]

    for report in reports:
        report.generate("", feedback, options)


if __name__ == "__main__":
    parser = ArgumentParser(description="Generates Sigrid CI feedback reports based on existing analysis results.")
    parser.add_argument("--partner", type=str, default="sig", help=SUPPRESS)
    parser.add_argument("--customer", type=str)
    parser.add_argument("--system", type=str)
    parser.add_argument("--sat-ci-json", type=str, help="Location of the SAT CI JSON file.")
    parser.add_argument("--targetquality", type=float, default=3.5, help="Target rating for code quality.")
    parser.add_argument("--out", type=str, help="Output directory where to generate the reports.")
    parser.add_argument("--sigridurl", type=str, default="https://sigrid-says.com", help="Sigrid base URL.")
    args = parser.parse_args()

    if None in [args.customer, args.system, args.sat_ci_json, args.targetquality, args.out]:
        parser.print_help()
        sys.exit(1)

    options = PublishOptions(
        partner=args.partner,
        customer=args.customer,
        system=args.system,
        sourceDir="/tmp",
        runMode=RunMode.FEEDBACK_ONLY,
        targetRating=args.targetquality,
        sigridURL=args.sigridurl
    )

    generateReports(args.sat_ci_json, options, args.out)

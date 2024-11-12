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

from sigridci.sigrid_api_client import SigridApiClient
from sigridci.command_line_helper import getFeedbackPublishOptions, parseFeedbackCommandLineArguments
from sigridci.report.security_markdown_report import SecurityMarkdownReport
from sigridci.report.security_code_climate_report import SecurityCodeClimateReport
from sigridci.upload_log import UploadLog


if __name__ == "__main__":
    args = parseFeedbackCommandLineArguments("Security")
    options = getFeedbackPublishOptions(args)
    apiClient = SigridApiClient(options)

    UploadLog.log(f"Retrieving Sigrid CI Security feedback for analysis ID {args.analysisid}")
    # TODO load analysis results once end point is available.
    with open(args.analysisid, mode="r", encoding="utf-8") as f:
        feedback = json.load(f)

    for report in [SecurityMarkdownReport(), SecurityCodeClimateReport()]:
        report.generate(args.analysisid, feedback, options)

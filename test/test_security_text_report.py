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

import inspect
import json
import os
from io import StringIO
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.security_text_report import SecurityTextReport


class SecurityTextReportTest(TestCase):

    def testPrintFindings(self):
        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/aap", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/security.sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        buffer = StringIO()
        report = SecurityTextReport("HIGH", output=buffer)
        report.generate("1234", feedback, options)

        expected = """
            Security findings
            
                🟣 Weak Hash algorithm used
                    In Security.java (line 33)
        """

        self.assertEqual(inspect.cleandoc(expected), buffer.getvalue().strip())

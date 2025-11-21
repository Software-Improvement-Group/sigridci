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
from unittest import TestCase

from sigridci.sigridci.analysisresults.findings_processor import FindingsProcessor


class FindingsProcessorTest(TestCase):

    def testExtractAllFindingsSarif(self):
        with open(os.path.dirname(__file__) + "/testdata/security.sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = FindingsProcessor()
        findings = list(processor.extractAllFindings(feedback))

        self.assertEqual(len(findings), 2)
        self.assertEqual(findings[0].risk, "CRITICAL")
        self.assertEqual(findings[0].description, "Weak Hash algorithm used")
        self.assertEqual(findings[1].risk, "MEDIUM")
        self.assertEqual(findings[1].description, "Some other finding")

    def testExtractRelevantFindings(self):
        with open(os.path.dirname(__file__) + "/testdata/security.sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = FindingsProcessor()
        findings = list(processor.extractRelevantFindings(feedback, "HIGH"))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].risk, "CRITICAL")
        self.assertEqual(findings[0].description, "Weak Hash algorithm used")

    def testExtractAllFindingsNative(self):
        with open(os.path.dirname(__file__) + "/testdata/security.sig.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = FindingsProcessor()
        findings = list(processor.extractAllFindings(feedback))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].fingerprint, "0006d9dd-5288-424a-bf8b-077c98ef00ee")
        self.assertEqual(findings[0].risk, "MEDIUM")
        self.assertEqual(findings[0].description, "String comparisons using '===', '!==', '!=' and '==' is vulnerable to timing attacks")
        self.assertEqual(findings[0].file, "widgets/com.mendix.widget.native.WebView/com/mendix/widget/native/webview/WebView.android.js")
        self.assertEqual(findings[0].line, 853)

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

from unittest import TestCase

from sigridci.sigridci.markdown_report import MarkdownReport
from sigridci.sigridci.publish_options import PublishOptions, RunMode


class MarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", targetRating=3.5)

    def testMarkdown(self):
        feedback = {
            "baseine": "20220110",
            "baselineRatings": {"DUPLICATION": 4.0, "UNIT_SIZE": 4.0, "MAINTAINABILITY": 4.0},
            "newCodeRatings": {"DUPLICATION": 5.0, "UNIT_SIZE": 2.0, "MAINTAINABILITY": 3.0},
            "overallRatings": {"DUPLICATION": 4.5, "UNIT_SIZE": 3.0, "MAINTAINABILITY": 3.5},
            "refactoringCandidates": [{"subject": "a.py::aap()", "category": "introduced", "metric": "UNIT_SIZE"}]
        }

        report = MarkdownReport()
        markdown = report.renderMarkdown("1234", feedback, self.options)

        expected = """
# Sigrid maintainability feedback

**\u274C Your code failed to meet your Sigrid objective of 3.5 stars**

## Sigrid ratings

| System property | Baseline on N/A | New/changed code |
|-----------------|---------------------------------------------|------------------|
| Volume | (N/A) | N/A |
| Duplication | (4.0) | 5.0 |
| Unit Size | (4.0) | 2.0 |
| Unit Complexity | (N/A) | N/A |
| Unit Interfacing | (N/A) | N/A |
| Module Coupling | (N/A) | N/A |
| Component Independence | (N/A) | N/A |
| Component Entanglement | (N/A) | N/A |
| **Maintainability** | **(4.0)** | **3.0** |

## Refactoring candidates


**Unit Size**

- *(introduced)* aap()

----

- [**View this system in Sigrid**](https://sigrid-says.com/aap/noot)
- [**View this feedback in Sigrid**](https://sigrid-says.com/aap/noot/-/sigrid-ci/1234?targetRating=3.5)
        """

        self.assertEqual(markdown.strip(), expected.strip())

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

import unittest
from sigridci.sigridci import CodeClimateReport


class CodeClimateReportTest(unittest.TestCase):

    maxDiff = None

    def testGenerateReport(self):
        feedback = {
            "refactoringCandidates": [
                {"subject": "aap", "category": "introduced", "metric": "UNIT_SIZE"},
                {
                    "subject": "noot (lines 8-14)\nmies (lines 10-16)\nwim (lines 10-16)",
                    "category": "worsened",
                    "metric": "DUPLICATION"
                },
                {"subject": "noot::mies", "category": "worsened", "metric": "UNIT_SIZE"}
            ]
        }

        report = CodeClimateReport()
        r = report.generateReport(feedback)

        self.assertEqual(len(r), 3)
        self.assertEqual(r[0], {
            "type": "issue",
            "check_name": "Unit Size",
            "description": "Unit Size finding",
            "content": {
                "body": "aap"
            },
            "categories": ["Complexity"],
            "location": {
                "path": "aap"
            },
            "other_locations": None
        })
        self.assertEqual(r[1], {
            "type": "issue",
            "check_name": "Duplication",
            "description": "Duplication finding",
            "content": {
                "body": "noot (lines 8-14)\nmies (lines 10-16)\nwim (lines 10-16)"
            },
            "categories": ["Complexity"],
            "location": {
                "path": "noot",
                "lines": {
                    "begin": 8,
                    "end": 14
                }
            },
            "other_locations": [
                {"path": "mies", "lines": {"begin": 10, "end": 16}},
                {"path": "wim", "lines": {"begin": 10, "end": 16}}
            ]
        })
        self.assertEqual(r[2], {**r[2], **{
            "location": {"path": "noot"},
            "other_locations": None
        }})

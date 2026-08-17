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

import contextlib
import io
import json
from unittest import TestCase

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.inline_results_report import MaintainabilityInlineResultsReport, \
    OpenSourceHealthInlineResultsReport, SecurityInlineResultsReport


class InlineResultsReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, "/tmp", feedbackURL="")

    def testMaintainabilityPayloadKeepsRawFeedbackAndAddsCapabilityInfo(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"MAINTAINABILITY": 4.0},
            "newCodeRatings": {"MAINTAINABILITY": 3.0},
            "refactoringCandidates": []
        }

        report = MaintainabilityInlineResultsReport()
        payload = report.buildPayload(feedback, self.options)

        self.assertEqual("maintainability", payload["capability"])
        self.assertFalse(payload["objectiveMet"])
        self.assertEqual("20220110", payload["baseline"])
        maintainabilityRow = next(r for r in payload["ratings"] if r["metric"] == "MAINTAINABILITY")
        self.assertEqual(4.0, maintainabilityRow["systemBaseline"])
        self.assertEqual(3.0, maintainabilityRow["newAndChangedCodeAfter"])

    def testMaintainabilityPayloadBuildsRatingsTableAndDropsRawRatingsDicts(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {"VOLUME": 3.6, "COMPONENT_BALANCE_PROP": None, "MAINTAINABILITY": 4.0},
            "overallRatings": {"MAINTAINABILITY": 4.1},
            "newCodeRatings": {"MAINTAINABILITY": 3.0},
            "changedCodeBeforeRatings": {"MAINTAINABILITY": 3.8},
            "changedCodeAfterRatings": {"MAINTAINABILITY": 3.9},
            "refactoringCandidates": [],
            "refactoringCandidatesPerType": {"DUPLICATION": []}
        }

        report = MaintainabilityInlineResultsReport()
        payload = report.buildPayload(feedback, self.options)

        self.assertNotIn("baselineRatings", payload)
        self.assertNotIn("overallRatings", payload)
        self.assertNotIn("newCodeRatings", payload)
        self.assertNotIn("changedCodeBeforeRatings", payload)
        self.assertNotIn("changedCodeAfterRatings", payload)
        self.assertNotIn("refactoringCandidatesPerType", payload)

        metrics = [row["metric"] for row in payload["ratings"]]
        self.assertNotIn("VOLUME", metrics)
        self.assertNotIn("COMPONENT_BALANCE_PROP", metrics)

        maintainabilityRow = next(r for r in payload["ratings"] if r["metric"] == "MAINTAINABILITY")
        self.assertEqual(4.0, maintainabilityRow["systemBaseline"])
        self.assertEqual(4.1, maintainabilityRow["systemNew"])
        self.assertEqual(3.0, maintainabilityRow["newAndChangedCodeAfter"])
        self.assertEqual(3.8, maintainabilityRow["changedCodeBefore"])

    def testMaintainabilityPayloadDropsOccurrencesFromRefactoringCandidates(self):
        feedback = {
            "baseline": "20220110",
            "baselineRatings": {},
            "newCodeRatings": {},
            "refactoringCandidates": [
                {"subject": "Foo.java (lines 1-10)", "category": "unchanged", "metric": "DUPLICATION",
                 "riskCategory": "HIGH", "occurrences": [{"filePath": "Foo.java", "startLine": 1, "endLine": 10}]},
                {"subject": "Foo.java::doStuff()", "category": "unchanged", "metric": "UNIT_SIZE",
                 "riskCategory": "HIGH", "occurrences": [{"filePath": "Foo.java", "startLine": 1, "endLine": 10}]}
            ]
        }

        report = MaintainabilityInlineResultsReport()
        payload = report.buildPayload(feedback, self.options)

        duplication, unitSize = payload["refactoringCandidates"]
        self.assertNotIn("occurrences", duplication)
        self.assertNotIn("occurrences", unitSize)

    def testOpenSourceHealthPayloadSummarizesOnlyLibrariesWithRisk(self):
        feedback = {
            "metadata": {"timestamp": "2025-09-29T00:00:00Z"},
            "components": [
                {
                    "name": "safe-lib",
                    "version": "1.0",
                    "properties": [{"name": "sigrid:risk:vulnerability", "value": "NONE"},
                                    {"name": "sigrid:risk:legal", "value": "NONE"}],
                    "licenses": []
                },
                {
                    "name": "risky-lib",
                    "version": "1.0",
                    "bom-ref": "risky-lib@1.0",
                    "properties": [{"name": "sigrid:risk:vulnerability", "value": "CRITICAL"},
                                    {"name": "sigrid:risk:legal", "value": "NONE"},
                                    {"name": "sigrid:latest:version", "value": "2.0"}],
                    "licenses": [{"license": {"name": "MIT"}}],
                    "evidence": {"occurrences": [{"location": "requirements.txt"}]}
                }
            ],
            "vulnerabilities": [
                {"id": "CVE-2025-1234", "affects": [{"ref": "risky-lib@1.0"}], "source": {"url": "https://example.com"}}
            ]
        }

        report = OpenSourceHealthInlineResultsReport(self.options)
        payload = report.buildPayload(feedback, self.options)

        self.assertEqual("osh", payload["capability"])
        self.assertFalse(payload["objectiveMet"])
        self.assertEqual("2025-09-29", payload["baseline"])

        self.assertEqual(1, len(payload["libraries"]))
        library = payload["libraries"][0]
        self.assertEqual("risky-lib", library["name"])
        self.assertEqual("2.0", library["latestVersion"])
        self.assertTrue(library["fixable"])
        self.assertEqual(["MIT"], library["licenses"])
        self.assertEqual([{"id": "CVE-2025-1234", "link": "https://example.com"}], library["vulnerabilities"])
        self.assertEqual("CRITICAL", library["vulnerabilityRisk"]["severity"])
        self.assertFalse(library["vulnerabilityRisk"]["meetsObjective"])

    def testSecurityPayloadUsesCleanFindingFields(self):
        feedback = {
            "baseline": "20220110",
            "runs": [
                {
                    "tool": {"driver": {"name": "Semgrep"}},
                    "results": [
                        {
                            "ruleId": "some-rule",
                            "message": {"text": "SQL injection risk"},
                            "locations": [{"physicalLocation": {"artifactLocation": {"uri": "Foo.java"},
                                                                  "region": {"startLine": 42}}}],
                            "properties": {"severity": "CRITICAL"},
                            "fingerprints": {"sigFingerprint/v1": "abc123"},
                            "baselineState": "new"
                        }
                    ]
                }
            ]
        }

        report = SecurityInlineResultsReport(self.options)
        payload = report.buildPayload(feedback, self.options)

        self.assertEqual("security", payload["capability"])
        self.assertFalse(payload["objectiveMet"])
        self.assertEqual("20220110", payload["baseline"])

        finding = payload["findings"][0]
        self.assertEqual("abc123", finding["fingerprint"])
        self.assertEqual("CRITICAL", finding["risk"])
        self.assertEqual("SQL injection risk", finding["description"])
        self.assertEqual("Foo.java", finding["file"])
        self.assertEqual(42, finding["line"])
        self.assertTrue(finding["partOfObjective"])
        self.assertEqual("Introduced", finding["status"])

    def testGeneratePrintsCapabilityNameThenCompactSingleLineJson(self):
        feedback = {"baseline": "20220110", "baselineRatings": {}, "newCodeRatings": {}, "refactoringCandidates": []}
        report = MaintainabilityInlineResultsReport()

        with contextlib.redirect_stdout(io.StringIO()) as output:
            report.generate("1234", feedback, self.options)

        lines = output.getvalue().splitlines()
        self.assertEqual(2, len(lines))
        self.assertEqual("maintainability", lines[0])
        parsed = json.loads(lines[1])
        self.assertEqual("maintainability", parsed["capability"])

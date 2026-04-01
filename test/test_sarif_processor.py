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

from sigridci.sigridci.analysisresults.sarif_processor import SarifProcessor, FindingStatus
from sigridci.sigridci.publish_options import PublishOptions, RunMode


class FindingsProcessorTest(TestCase):

    def testExtractAllFindingsSarif(self):
        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        findings = list(processor.extractFindings(feedback))

        self.assertEqual(len(findings), 4)
        self.assertEqual(findings[0].risk, "CRITICAL")
        self.assertEqual(findings[0].description, "Puma4")
        self.assertEqual(findings[0].file, "neutron/neutron/db/sqlalchemytypes.py")
        self.assertEqual(findings[1].risk, "HIGH")
        self.assertEqual(findings[1].description, "Puma2")
        self.assertEqual(findings[1].file, "neutron/neutron/ipam/drivers/neutrondb_ipam/driver.py")

    def testIgnoreInformationSeverityFindings(self):
        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        severities = sorted(set(finding.risk for finding in processor.extractFindings(feedback)))

        self.assertEqual(severities, ["CRITICAL", "HIGH"])

    def testDetectFindingStatus(self):
        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        findings = list(processor.extractFindings(feedback))

        self.assertEqual(findings[0].status, FindingStatus.INTRODUCED)
        self.assertEqual(findings[1].status, FindingStatus.INTRODUCED)
        self.assertEqual(findings[2].status, FindingStatus.ACCEPTED)
        self.assertEqual(findings[3].status, FindingStatus.FIXED)

    def testLoadFindingsFromOnPremiseSarif(self):
        with open(os.path.dirname(__file__) + "/testdata/security-onpremise.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        findings = list(processor.extractFindings(feedback))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].risk, "HIGH")
        self.assertEqual(findings[0].description, "InterruptedException and ThreadDeath should not be ignored")
        self.assertEqual(findings[0].file, "Aap.java")

    def testFilterOshFindingsFromSecurityFeedbackInOnPremise(self):
        with open(os.path.dirname(__file__) + "/testdata/security-onpremise-osh.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        findings = list(processor.extractFindings(feedback))

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].risk, "HIGH")
        self.assertEqual(findings[0].description, "DocumentBuilderFactory being instantiated for XXE vulnerabilities")
        self.assertEqual(findings[0].file, "SecurityExample.java")

    def testHandleAbsentInvocationsList(self):
        with open(os.path.dirname(__file__) + "/testdata/security-sigrid-api-sarif.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        for run in feedback["runs"]:
            run["invocations"] = []

        options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY)
        processor = SarifProcessor(options, "HIGH")
        findings = list(processor.extractFindings(feedback))

        self.assertEqual(len(findings), 4)

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
from unittest import TestCase, mock

from sigridci.sigridci.publish_options import PublishOptions, RunMode
from sigridci.sigridci.reports.osh_markdown_report import OpenSourceHealthMarkdownReport


class OpenSourceHealthMarkdownReportTest(TestCase):
    maxDiff = None

    def setUp(self):
        self.options = PublishOptions("aap", "noot", RunMode.FEEDBACK_ONLY, sourceDir="/tmp", feedbackURL="")

        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            self.feedback = json.load(f)

        with open(os.path.dirname(__file__) + "/testdata/osh-junit-previous.json", encoding="utf-8", mode="r") as f:
            self.previousFeedback = json.load(f)

    def testIncludeFindingsBasedOnObjectives(self):
        report = OpenSourceHealthMarkdownReport(self.options, {})
        summary = report.getSummary(self.feedback, self.options)
        negative = list(report.getFindings(self.feedback, self.options))
        nonurgent = list(report.getNonUrgentFindings(self.feedback, self.options))

        self.assertEqual(summary[0].text, "You have no critical-severity open source vulnerabilities.")

        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0].title, "`log4j-core` 2.14.1 contains known vulnerabilities.")

        self.assertEqual(len(nonurgent), 3)
        self.assertEqual(nonurgent[0].title, "`commons-io` 2.9.0 contains known vulnerabilities.")
        self.assertEqual(nonurgent[1].title, "`classgraph` 4.8.106 (transitive) contains known vulnerabilities.")
        self.assertEqual(nonurgent[2].title, "`junit`  contains known vulnerabilities.")

    def testShowUpdatedLibraries(self):
        report = OpenSourceHealthMarkdownReport(self.options, {"OSH_MAX_SEVERITY" : "MEDIUM"})
        report.previousFeedback = self.previousFeedback
        positive = list(report.getPositiveFindings(self.feedback, self.options))

        self.assertEqual(len(positive), 1)
        self.assertEqual(positive[0].title, "`commons-other` 1.99 contains known vulnerabilities.")

    def testShowLegalRiskIfObjectiveIsSet(self):
        objectives = {
            "OSH_MAX_SEVERITY" : "CRITICAL",
            "OSH_MAX_LICENSE_RISK" : "LOW"
        }

        report = OpenSourceHealthMarkdownReport(self.options, objectives)
        summary = report.getSummary(self.feedback, self.options)
        negative = list(report.getFindings(self.feedback, self.options))

        self.assertEqual(summary[0].text, "You do not have any open source vulnerabilities.")
        self.assertEqual(summary[1].text, "You have open source libraries with license issues.")
        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0].title, "`mockito-junit-jupiter` 3.10.0 has license risks.")

    def testSpecialStatusIfThereAreNoLibraries(self):
        emptyFeedback = {
            "metadata": {
                "timestamp": "2026-02-03"
            },
            "components": []
        }

        objectives = {
            "OSH_MAX_SEVERITY" : "CRITICAL",
            "OSH_MAX_LICENSE_RISK" : "LOW"
        }

        report = OpenSourceHealthMarkdownReport(self.options, objectives)
        summary = report.getSummary(emptyFeedback, self.options)

        self.assertEqual(summary[0].text, "Sigrid did not find any open source libraries.")

    def testGreenCheckmarkIfThereAreLibrariesButNoFindings(self):
        emptyFeedback = {
            "metadata": {
                "timestamp": "2026-02-03"
            },
            "components": [
                {
                    "name": "platform-browser-dynamic",
                    "purl": "pkg:npm/%40angular/platform-browser-dynamic@21.0.9",
                    "type": "library",
                    "group": "@angular",
                    "bom-ref": "pkg:npm/%40angular/platform-browser-dynamic@21.0.9?package-id=d540fd8750e7344a",
                    "version": "21.0.9",
                    "evidence": {},
                    "licenses": [],
                    "properties": [
                        {
                            "name": "sigrid:risk:vulnerability",
                            "value": "NONE"
                        },
                        {
                            "name": "sigrid:risk:legal",
                            "value": "NONE"
                        }
                    ]
                }
            ]
        }

        objectives = {
            "OSH_MAX_SEVERITY" : "CRITICAL",
            "OSH_MAX_LICENSE_RISK" : "LOW"
        }

        report = OpenSourceHealthMarkdownReport(self.options, objectives)
        summary = report.getSummary(emptyFeedback, self.options)

        self.assertEqual(summary[0].text, "You do not have any open source vulnerabilities.")

    def testOnlyReportIssuesRelevantToSubSystem(self):
        self.options.subsystem = "aap"

        with open(os.path.dirname(__file__) + "/testdata/osh-subsystem.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        report = OpenSourceHealthMarkdownReport(self.options, {})
        negative = list(report.getFindings(feedback, self.options))

        self.assertEqual(len(negative), 1)
        self.assertEqual(negative[0].title, "`example-aap` 1.0 contains known vulnerabilities.")

    def testSeverityObjectiveLabel(self):
        report = OpenSourceHealthMarkdownReport(self.options, {})
        report.decorateLinks = False

        self.assertEqual("any", report.formatSeverity("CRITICAL"))
        self.assertEqual("no critical-severity", report.formatSeverity("HIGH"))
        self.assertEqual("no high-severity", report.formatSeverity("MEDIUM"))
        self.assertEqual("no medium-severity", report.formatSeverity("LOW"))
        self.assertEqual("no low-severity", report.formatSeverity("INFORMATION"))
        self.assertEqual("no", report.formatSeverity("NONE"))

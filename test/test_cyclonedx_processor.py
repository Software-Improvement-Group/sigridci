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

from sigridci.sigridci.analysisresults.cyclonedx_processor import CycloneDXProcessor


class CycloneDXProcessorTest(TestCase):

    def testExtractAllLibraries(self):
        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = CycloneDXProcessor()
        libraries = list(processor.extractLibraries(feedback, "NONE"))

        self.assertEqual(len(libraries), 4)
        self.assertEqual(libraries[0].risk, "CRITICAL")
        self.assertEqual(libraries[0].name, "org.apache.logging.log4j:log4j-core")
        self.assertEqual(libraries[1].risk, "HIGH")
        self.assertEqual(libraries[1].name, "commons-io:commons-io")

    def testExtractLibrariesMatchingObjective(self):
        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = CycloneDXProcessor()
        libraries = list(processor.extractLibraries(feedback, "HIGH"))

        self.assertEqual(len(libraries), 4)
        self.assertEqual(libraries[0].name, "org.apache.logging.log4j:log4j-core")
        self.assertEqual(libraries[0].partOfObjective, True)
        self.assertEqual(libraries[1].name, "commons-io:commons-io")
        self.assertEqual(libraries[1].partOfObjective, False)
        self.assertEqual(libraries[2].name, "io.github.classgraph:classgraph")
        self.assertEqual(libraries[2].partOfObjective, False)
        self.assertEqual(libraries[3].name, "junit:junit")
        self.assertEqual(libraries[3].partOfObjective, False)

    def testExtractVulnerabilities(self):
        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = CycloneDXProcessor()
        libraries = list(processor.extractLibraries(feedback, "NONE"))

        self.assertEqual(libraries[0].name, "org.apache.logging.log4j:log4j-core")
        self.assertEqual(len(libraries[0].vulnerabilities), 4)
        self.assertEqual(libraries[0].vulnerabilities[0].id, "CVE-2021-45046")
        self.assertEqual(libraries[0].vulnerabilities[0].link, "")
        self.assertEqual(libraries[0].vulnerabilities[1].id, "CVE-2021-45105")
        self.assertEqual(libraries[0].vulnerabilities[1].link, "")
        self.assertEqual(libraries[0].vulnerabilities[2].id, "CVE-2021-44228")
        self.assertEqual(libraries[0].vulnerabilities[2].link, "https://nvd.nist.gov/vuln/detail/CVE-2021-44228")
        self.assertEqual(libraries[0].vulnerabilities[3].id, "CVE-2021-44832")
        self.assertEqual(libraries[0].vulnerabilities[3].link, "")

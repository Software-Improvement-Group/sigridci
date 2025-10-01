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
        libraries = list(processor.extractRelevantLibraries(feedback, "NONE"))

        self.assertEqual(len(libraries), 34)
        self.assertEqual(libraries[0].risk, "NONE")
        self.assertEqual(libraries[0].name, "org.gradle:test-retry-gradle-plugin")
        self.assertEqual(libraries[0].version, "1.2.1")
        self.assertEqual(libraries[0].latestVersion, "")
        self.assertEqual(libraries[0].files, ["buildSrc/build.gradle.kts"])

    def testExtractLibrariesMatchingObjective(self):
        with open(os.path.dirname(__file__) + "/testdata/osh-junit.json", encoding="utf-8", mode="r") as f:
            feedback = json.load(f)

        processor = CycloneDXProcessor()
        libraries = list(processor.extractRelevantLibraries(feedback, "CRITICAL"))

        self.assertEqual(len(libraries), 1)
        self.assertEqual(libraries[0].risk, "CRITICAL")
        self.assertEqual(libraries[0].name, "org.apache.logging.log4j:log4j-core")

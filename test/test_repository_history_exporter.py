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

import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from unittest import TestCase

from sigridci.sigridci.repository_history_exporter import RepositoryHistoryExporter
from sigridci.sigridci.upload_log import UploadLog


class RepositoryHistoryExporterTest(TestCase):
    maxDiff = None

    def setUp(self):
        UploadLog.clear()

    def testExportGitHistory(self):
        tempDir = tempfile.mkdtemp()
        output = subprocess.run(["git", "clone", "https://github.com/BetterCodeHubTraining/cspacman.git", tempDir])
        output.check_returncode()

        historyExporter = RepositoryHistoryExporter()
        # By default, we only export the last year of history. We use a longer
        # period here to make sure the test doesn't break because the test
        # repository didn't receive any commits.
        historyExporter.CUTOFF_DATE = datetime.now() + timedelta(days=-9999)
        historyExporter.exportHistory(tempDir)

        with open(f"{tempDir}/git.log", "r", encoding="utf-8") as f:
            historyEntries = f.read().strip().split("\n")

        id = "f59c21c9de5bee332d51cea5caef4b2500ea100e"
        name = "199b4fba40cbc81fd5c7493cba5a7a23c5a8872626d9cb8bec46d7a052bb747e"
        email = "768edd5d023df7cf4dec32fbe7cc00ec5aed4435aecc3721bdb767e1b862f461"
        committerName = "f911e414cf6bdfc595532ab166b5ba0f63d73c021452fcdacbda363dda6ad8fb"
        committerEmail = "3c205d8fc749f72977b9331e3179773c315bb1f4860c366de2abe9ec9337730b"
        date = "2023-08-15 13:57:07 +0200"
        message = "Create sigrid-publish.yml"

        self.assertEqual(historyEntries[0], f"'@@@;{id};{name};{email};{committerName};{committerEmail};{date};{message}'")

    def testTolerantParsingOfCommitMessage(self):
        log = "@@@;1234;John Smith;j.smith@sig.eu;GitHub;noreply@github.com;2023-11-29 10:48:32 +0100;a;b;c"
        historyExporter = RepositoryHistoryExporter()
        result = historyExporter.anonymizeHistoryEntry(log)

        authorName = "ef61a579c907bbed674c0dbcbcf7f7af8f851538eef7b8e58c5bee0b8cfdac4a"
        authorEmail = "318f8c6a1732a7a6c60e2200ec56edf41780425d81e5eb30aed6fdc025edccab"
        committerName = "f911e414cf6bdfc595532ab166b5ba0f63d73c021452fcdacbda363dda6ad8fb"
        committerEmail = "3c205d8fc749f72977b9331e3179773c315bb1f4860c366de2abe9ec9337730b"

        self.assertEqual(result, f"@@@;1234;{authorName};{authorEmail};{committerName};{committerEmail};2023-11-29 10:48:32 +0100;a\n")

    def testWarningWhenHistoryContainsSingleEntry(self):
        tempDir = tempfile.mkdtemp()
        output = subprocess.run(["git", "clone", "--depth", "1", "https://github.com/BetterCodeHubTraining/cspacman.git", tempDir])
        output.check_returncode()

        historyExporter = RepositoryHistoryExporter()
        historyExporter.exportHistory(tempDir)

        expected = [
            "Including repository history in upload",
            "Warning: Git history seems to be missing, maybe you're using a shallow clone?"
        ]

        self.assertEqual(UploadLog.history, expected)

    def testSupportMultipleRepositoriesInSamePipeline(self):
        tempDir = tempfile.mkdtemp()

        sub1 = subprocess.run(["git", "clone", "https://github.com/BetterCodeHubTraining/cspacman.git", f"{tempDir}/cspacman"])
        sub1.check_returncode()

        sub2 = subprocess.run(["git", "clone", "https://github.com/LeaVerou/awesomplete.git", f"{tempDir}/awesomplete"])
        sub2.check_returncode()

        historyExporter = RepositoryHistoryExporter()
        historyExporter.CUTOFF_DATE = datetime.now() + timedelta(days=-9999)
        historyExporter.exportHistory(tempDir)

        self.assertFalse(os.path.exists(f"{tempDir}/git.log"))
        self.assertTrue(os.path.exists(f"{tempDir}/cspacman/git.log"))
        self.assertTrue(os.path.exists(f"{tempDir}/awesomplete/git.log"))

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
import os.path
import subprocess
import tempfile
from unittest import TestCase
from sigridci.repository_history_exporter import RepositoryHistoryExporter


class RepositoryHistoryExporterTest(TestCase):

    def testExportGitHistory(self):
        tempDir = tempfile.mkdtemp()
        output = subprocess.run(["git", "clone", "https://github.com/BetterCodeHubTraining/cspacman.git", tempDir])
        output.check_returncode()

        historyExporter = RepositoryHistoryExporter()
        historyExporter.exportHistory(tempDir)

        with open(f"{tempDir}/git.log", "r", encoding="utf-8") as f:
            historyEntries = f.read().strip().split("\n")

        self.assertEquals(historyEntries[0],
          "'@@@;3e161af9218e6f20a095a96ee246763e9c01f1e3;Thomas Kraus (tukraus);thomas@sig.nl;2016-05-24 09:25:40 +0200;remove javascript'")

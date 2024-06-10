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

import hashlib
import os
import subprocess
from datetime import datetime, timedelta

from .upload_log import UploadLog


class RepositoryHistoryExporter:
    GIT_LOG_FORMAT = "@@@;%H;%an;%ae;%ad;%s"
    CUTOFF_DATE = datetime.now() + timedelta(days=-365)
    LIGHTWEIGHT_HISTORY_EXPORT_FILE = "git.log"
    COMMIT_PREFIXES = ("@@@", "'@@@")

    def exportHistory(self, sourceDir):
        if os.path.exists(f"{sourceDir}/.git"):
            self.exportGitHistory(sourceDir)
        else:
            UploadLog.log("No repository history found")

    def exportGitHistory(self, sourceDir):
        gitCommand = ["git", "-C", sourceDir, "--no-pager", "log", "--date=iso", f"--format='{self.GIT_LOG_FORMAT}'",
                      "--numstat", "--no-merges", f"--after={self.CUTOFF_DATE.strftime('%Y-%m-%d')}"]

        try:
            output = subprocess.run(gitCommand, stdout=subprocess.PIPE)
            if output.returncode == 0:
                UploadLog.log("Including repository history in upload")
                history = output.stdout.decode("utf8", "ignore")
                self.createHistoryExportFile(history, f"{sourceDir}/{self.LIGHTWEIGHT_HISTORY_EXPORT_FILE}")
            else:
                UploadLog.log("Exporting repository history failed")
        except Exception as e:
            UploadLog.log("Error while trying to include repository history: " + str(e))

    def createHistoryExportFile(self, history, outputFile):
        entries = 0

        with open(outputFile, "w", encoding="utf8") as f:
            for line in history.strip().split("\n"):
                f.write(self.anonymizeHistoryEntry(line))
                if line.startswith(self.COMMIT_PREFIXES):
                    entries += 1

        if entries <= 1:
            UploadLog.log("Warning: Git history seems to be missing, maybe you're using a shallow clone?")

    def anonymizeHistoryEntry(self, gitLog):
        anonymized = ""

        for line in gitLog.strip().split("\n"):
            if line.startswith(self.COMMIT_PREFIXES):
                marker, id, name, email, date, message, *rest = line.split(";")
                name = hashlib.sha256(name.encode("utf8")).hexdigest()
                email = hashlib.sha256(email.encode("utf8")).hexdigest()
                anonymized += ";".join([marker, id, name, email, date, message]) + "\n"
            else:
                anonymized += line + "\n"

        return anonymized

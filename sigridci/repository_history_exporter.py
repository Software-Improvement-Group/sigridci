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

from sigridci.upload_log import UploadLog


class RepositoryHistoryExporter:

    def exportHistory(self, sourceDir):
        if os.path.exists(f"{sourceDir}/.git"):
            self.exportGitHistory(sourceDir)
        else:
            UploadLog.log("No repository history found")

    def exportGitHistory(self, sourceDir):
        gitCommand = ["git", "-C", sourceDir, "--no-pager", "log", "--date=iso",
                      "--format='@@@;%H;%an;%ae;%ad;%s'", "--numstat", "--no-merges"]

        try:
            output = subprocess.run(gitCommand, stdout=subprocess.PIPE)
            if output.returncode == 0:
                UploadLog.log("Including repository history in upload")
                with open(f"{sourceDir}/git.log", "w") as f:
                    f.write(output.stdout.decode("utf8"))
            else:
                UploadLog.log("Exporting repository history failed")
        except Exception as e:
            UploadLog.log("Error while trying to include repository history: " + str(e))

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
import sys


class Platform:
    @staticmethod
    def isGitHub():
        return "GITHUB_REPOSITORY" in os.environ

    @staticmethod
    def isGitLab():
        return "GITLAB_CI" in os.environ

    @staticmethod
    def isAzureDevOps():
        return "BUILD_REPOSITORY_NAME" in os.environ

    @staticmethod
    def isBitBucket():
        return "BITBUCKET_REPO_SLUG" in os.environ

    @staticmethod
    def isHtmlMarkdownSupported():
        if os.environ.get("SIGRID_CI_MARKDOWN_HTML") in ("false", "0"):
            return False
        return Platform.isGitHub() or Platform.isGitLab() or Platform.isAzureDevOps()

    @staticmethod
    def checkEnvironment():
        if sys.version_info.major == 2 or sys.version_info.minor < 7:
            print("Sigrid CI requires Python 3.7 or higher")
            sys.exit(1)

        token = os.environ.get("SIGRID_CI_TOKEN", None)
        if not Platform.isValidToken(token):
            print("Missing or incomplete environment variable SIGRID_CI_TOKEN")
            sys.exit(1)

    @staticmethod
    def isValidToken(token):
        return token is not None and len(token) >= 64

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
    def isJenkins():
        return "BUILD_NUMBER" in os.environ

    @staticmethod
    def getPlatformId():
        if Platform.isGitHub():
            return "github"
        elif Platform.isGitLab():
            return "gitlab"
        elif Platform.isAzureDevOps():
            return "azure-devops"
        elif Platform.isBitBucket():
            return "bitbucket"
        elif Platform.isJenkins():
            return "Jenkins"
        else:
            return "unknown"

    @staticmethod
    def isHtmlMarkdownSupported():
        if os.environ.get("SIGRID_CI_MARKDOWN_HTML") in ("false", "0"):
            return False
        return Platform.isGitHub() or Platform.isGitLab() or Platform.isAzureDevOps()

    @staticmethod
    def createPullRequestFileURL(file, line=0):
        # GitLab
        if Platform.hasEnv("CI_SERVER_URL", "CI_PROJECT_PATH", "CI_COMMIT_REF_NAME"):
            server = os.environ["CI_SERVER_URL"]
            project = os.environ["CI_PROJECT_PATH"]
            branch = os.environ["CI_COMMIT_REF_NAME"]
            return f"{server}/{project}/-/blob/{branch}/{file}#L{line}"

        # GitHub
        if Platform.hasEnv("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_HEAD_REF"):
            server = os.environ["GITHUB_SERVER_URL"]
            repo = os.environ["GITHUB_REPOSITORY"]
            branch = os.environ["GITHUB_HEAD_REF"]
            return f"{server}/{repo}/blob/{branch}/{file}#L{line}"

        # Azure DevOps
        if Platform.hasEnv("SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI", "SYSTEM_PULLREQUEST_SOURCEBRANCH"):
            repo = os.environ["SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI"]
            branch = os.environ["SYSTEM_PULLREQUEST_SOURCEBRANCH"].split("/")[-1]
            return f"{repo}?path={file}&version=GB{branch}&line={line}"

        return None

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
    def hasEnv(*names):
        return all(os.environ.get(name) for name in names)

    @staticmethod
    def isValidToken(token):
        return token is not None and len(token) >= 64

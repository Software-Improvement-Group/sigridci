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
import urllib.parse


DOCS_URL = f"https://docs.sigrid-says.com"
SCOPE_DOCS = f"{DOCS_URL}/reference/analysis-scope-configuration.html"
OSH_EXCLUDE_DOCS = f"{SCOPE_DOCS}#exclude-open-source-health-risks"
SECURITY_EXCLUDE_RULE_DOCS = f"{SCOPE_DOCS}#excluding-security-rules"
SECURITY_EXCLUDE_FILE_DOCS = f"{SCOPE_DOCS}#excluding-files-and-directories-from-security-scanning"
SECURITY_BETA_DOCS = f"{DOCS_URL}/sigridci-integration/using-sigridci.html#security-feedback-beta"


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
            # Jenkins uses very generic environment variable names, so we only
            # conclude it's Jenkins after trying everything else.
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
        # SCM-supplied values such as the branch name are untrusted (a fork PR
        # controls them), so we URL-encode them to keep them confined to the URL
        # and prevent breaking out of the surrounding Markdown link. We keep "/"
        # in path segments since branches and file paths may legitimately
        # contain it, but encode it in query parameters.
        encodePath = lambda value: urllib.parse.quote(value, safe="/")
        encodeParam = lambda value: urllib.parse.quote(value, safe="")

        # GitLab
        if Platform.hasEnv("CI_SERVER_URL", "CI_PROJECT_PATH", "CI_COMMIT_REF_NAME"):
            server = os.environ["CI_SERVER_URL"]
            project = encodePath(os.environ["CI_PROJECT_PATH"])
            branch = encodePath(os.environ["CI_COMMIT_REF_NAME"])
            return f"{server}/{project}/-/blob/{branch}/{encodePath(file)}#L{line}"

        # GitHub
        if Platform.hasEnv("GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_HEAD_REF"):
            server = os.environ["GITHUB_SERVER_URL"]
            repo = encodePath(os.environ["GITHUB_REPOSITORY"])
            branch = encodePath(os.environ["GITHUB_HEAD_REF"])
            return f"{server}/{repo}/blob/{branch}/{encodePath(file)}#L{line}"

        # Azure DevOps
        if Platform.hasEnv("SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI", "SYSTEM_PULLREQUEST_SOURCEBRANCH"):
            repo = os.environ["SYSTEM_PULLREQUEST_SOURCEREPOSITORYURI"]
            branch = encodeParam(os.environ["SYSTEM_PULLREQUEST_SOURCEBRANCH"].split("/")[-1])
            return f"{repo}?path={encodeParam(file)}&version=GB{branch}&line={line}"

        return None

    @staticmethod
    def checkEnvironment():
        if sys.version_info.major == 2 or sys.version_info.minor < 9:
            print("Sigrid CI requires Python 3.9 or higher")
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

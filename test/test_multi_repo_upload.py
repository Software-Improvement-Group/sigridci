# Copyright 2024 Software Improvement Group
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

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Load the script as a module without executing __main__
_SCRIPT = Path(__file__).resolve().parent.parent / "multi-repository-upload" / "sigrid-git-upload.py"
_spec = importlib.util.spec_from_file_location("sigrid_git_upload", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_repo_name_from_url = _mod._repo_name_from_url
_find_duplicate_names = _mod._find_duplicate_names
_resolve_sigridci_script = _mod._resolve_sigridci_script


class RepoNameFromUrlTest(unittest.TestCase):

    def test_https_url_with_git_suffix(self):
        self.assertEqual("myrepo", _repo_name_from_url("https://github.com/org/myrepo.git"))

    def test_https_url_without_git_suffix(self):
        self.assertEqual("myrepo", _repo_name_from_url("https://github.com/org/myrepo"))

    def test_ssh_url_with_git_suffix(self):
        self.assertEqual("myrepo", _repo_name_from_url("git@github.com:org/myrepo.git"))

    def test_ssh_url_without_git_suffix(self):
        self.assertEqual("myrepo", _repo_name_from_url("git@github.com:org/myrepo"))

    def test_trailing_slash_is_ignored(self):
        self.assertEqual("myrepo", _repo_name_from_url("https://github.com/org/myrepo/"))

    def test_url_ending_in_git_without_dot(self):
        # A repo actually named "mygit" should not be stripped
        self.assertEqual("mygit", _repo_name_from_url("https://github.com/org/mygit"))


class FindDuplicateNamesTest(unittest.TestCase):

    def test_no_duplicates(self):
        urls = [
            "https://github.com/org/repo1.git",
            "https://github.com/org/repo2.git",
        ]
        self.assertEqual([], _find_duplicate_names(urls))

    def test_single_duplicate(self):
        urls = [
            "https://github.com/org/repo.git",
            "https://gitlab.com/other/repo.git",
        ]
        self.assertEqual(["repo"], _find_duplicate_names(urls))

    def test_multiple_duplicates(self):
        urls = [
            "https://github.com/org/alpha.git",
            "https://github.com/org/beta.git",
            "https://gitlab.com/x/alpha.git",
            "https://gitlab.com/x/beta.git",
        ]
        duplicates = _find_duplicate_names(urls)
        self.assertIn("alpha", duplicates)
        self.assertIn("beta", duplicates)

    def test_empty_list(self):
        self.assertEqual([], _find_duplicate_names([]))


class ResolveSigridciScriptTest(unittest.TestCase):

    def test_default_path_found(self):
        # The default sigridci.py exists inside this repository
        script = _resolve_sigridci_script(None)
        self.assertTrue(script.exists(), f"Expected sigridci.py to exist at {script}")
        self.assertEqual("sigridci.py", script.name)

    def test_explicit_path_pointing_to_directory_with_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake_script = Path(tmp) / "sigridci.py"
            fake_script.touch()
            result = _resolve_sigridci_script(tmp)
            self.assertEqual(fake_script.resolve(), result)

    def test_explicit_path_missing_directory(self):
        with self.assertRaises(SystemExit):
            _resolve_sigridci_script("/nonexistent/path/that/does/not/exist")

    def test_explicit_path_directory_without_script(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(SystemExit):
                _resolve_sigridci_script(tmp)


if __name__ == "__main__":
    unittest.main()

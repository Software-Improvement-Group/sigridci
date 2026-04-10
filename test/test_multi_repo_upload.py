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
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Load the script as a module without executing __main__
_SCRIPT = Path(__file__).resolve().parent.parent / "multi-repository-upload" / "sigrid-git-upload.py"
_spec = importlib.util.spec_from_file_location("sigrid_git_upload", _SCRIPT)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

_repo_name_from_url = _mod._repo_name_from_url
_find_duplicate_names = _mod._find_duplicate_names
_resolve_sigridci_script = _mod._resolve_sigridci_script
_prepare_source_dir = _mod._prepare_source_dir
_run_sigridci = _mod._run_sigridci


def _make_local_git_repo(parent_dir: str, name: str) -> str:
    """Create a minimal local git repository and return its path."""
    repo_path = os.path.join(parent_dir, name)
    os.makedirs(repo_path)
    subprocess.run(["git", "init", repo_path], capture_output=True, check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.email", "test@example.com"],
                   capture_output=True, check=True)
    subprocess.run(["git", "-C", repo_path, "config", "user.name", "Test"],
                   capture_output=True, check=True)
    readme = os.path.join(repo_path, "README.md")
    Path(readme).write_text(f"# {name}\n")
    subprocess.run(["git", "-C", repo_path, "add", "."], capture_output=True, check=True)
    subprocess.run(["git", "-C", repo_path, "commit", "-m", "init"],
                   capture_output=True, check=True)
    return repo_path


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


class PrepareSourceDirTest(unittest.TestCase):
    """Test _prepare_source_dir by cloning real local git repositories."""

    def test_clones_single_repo_into_named_subdirectory(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin = _make_local_git_repo(tmp, "origin-repo")
            source_dir = os.path.join(tmp, "source")
            _prepare_source_dir(source_dir, [origin], None, None)
            self.assertTrue(os.path.isdir(os.path.join(source_dir, "origin-repo")))
            self.assertTrue(os.path.isfile(os.path.join(source_dir, "origin-repo", "README.md")))

    def test_clones_multiple_repos_into_separate_subdirectories(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin_a = _make_local_git_repo(tmp, "repo-a")
            origin_b = _make_local_git_repo(tmp, "repo-b")
            source_dir = os.path.join(tmp, "source")
            _prepare_source_dir(source_dir, [origin_a, origin_b], None, None)
            self.assertTrue(os.path.isdir(os.path.join(source_dir, "repo-a")))
            self.assertTrue(os.path.isdir(os.path.join(source_dir, "repo-b")))

    def test_copies_sigrid_yaml_to_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin = _make_local_git_repo(tmp, "repo")
            sigrid_yaml = Path(tmp) / "sigrid.yaml"
            sigrid_yaml.write_text("component_depth: 1\n")
            source_dir = os.path.join(tmp, "source")
            _prepare_source_dir(source_dir, [origin], sigrid_yaml, None)
            self.assertTrue(os.path.isfile(os.path.join(source_dir, "sigrid.yaml")))

    def test_copies_sigrid_metadata_yaml_to_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin = _make_local_git_repo(tmp, "repo")
            metadata_yaml = Path(tmp) / "sigrid-metadata.yaml"
            metadata_yaml.write_text("display_name: Test\n")
            source_dir = os.path.join(tmp, "source")
            _prepare_source_dir(source_dir, [origin], None, metadata_yaml)
            self.assertTrue(os.path.isfile(os.path.join(source_dir, "sigrid-metadata.yaml")))


class EndToEndTest(unittest.TestCase):
    """Test the full main() flow with local git repos and a mocked sigridci call."""

    def test_full_flow_calls_sigridci_with_correct_arguments(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin = _make_local_git_repo(tmp, "my-service")
            assertions_made = {}

            def fake_run_sigridci(sigridci_script, customer, system, source_dir, sigrid_url, token):
                assertions_made["customer"] = customer
                assertions_made["system"] = system
                assertions_made["sigrid_url"] = sigrid_url
                assertions_made["token"] = token
                assertions_made["has_repo_dir"] = os.path.isdir(os.path.join(source_dir, "my-service"))

            env = {"SIGRID_CI_TOKEN": "test-token"}
            argv = ["sigrid-git-upload.py", "--customer", "acme", "--system", "platform", origin]
            with patch.dict(os.environ, env), \
                 patch.object(sys, "argv", argv), \
                 patch.object(_mod, "_run_sigridci", side_effect=fake_run_sigridci):
                _mod.main()

            self.assertEqual("acme", assertions_made["customer"])
            self.assertEqual("platform", assertions_made["system"])
            self.assertEqual("https://sigrid-says.com", assertions_made["sigrid_url"])
            self.assertEqual("test-token", assertions_made["token"])
            self.assertTrue(assertions_made["has_repo_dir"])

    def test_full_flow_exits_without_token(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin = _make_local_git_repo(tmp, "my-service")
            env_without_token = {k: v for k, v in os.environ.items() if k != "SIGRID_CI_TOKEN"}
            argv = ["sigrid-git-upload.py", "--customer", "acme", "--system", "platform", origin]
            with patch.dict(os.environ, env_without_token, clear=True), \
                 patch.object(sys, "argv", argv):
                with self.assertRaises(SystemExit):
                    _mod.main()

    def test_full_flow_exits_on_duplicate_repo_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            origin_a = _make_local_git_repo(tmp, "origins-a")
            origin_b = _make_local_git_repo(tmp, "origins-b")
            # Rename origins-b so it produces the same last-segment name as origins-a
            # by cloning both under the same bare name via file URLs
            url_a = f"file://{origin_a}"
            url_b = f"file://{origin_a}"  # intentional: same URL → same name
            argv = ["sigrid-git-upload.py", "--customer", "acme", "--system", "platform",
                    url_a, url_b]
            with patch.dict(os.environ, {"SIGRID_CI_TOKEN": "tok"}), \
                 patch.object(sys, "argv", argv):
                with self.assertRaises(SystemExit):
                    _mod.main()


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
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
"""sigrid-git-upload.py - Upload multiple git repositories to Sigrid as a single system."""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Optional

DEFAULT_SIGRIDCI_SCRIPT = Path(__file__).resolve().parent.parent / "sigridci" / "sigridci.py"


def _repo_name_from_url(git_url: str) -> str:
    """Derive a filesystem-safe folder name from a git clone URL."""
    name = git_url.rstrip("/").removesuffix(".git")
    return name.split("/")[-1]


def _clone_repo_to_directory(git_url: str, target_dir: str) -> None:
    """Clone a git repository into the target directory with full history."""
    print(f"  Cloning {git_url} …")
    result = subprocess.run(
        ["git", "clone", "--config", "core.longpaths=true", git_url, target_dir],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"  ERROR cloning {git_url}:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Clone one or more git repositories, bundle them together with a "
            "sigrid.yaml scope file, and publish the result to Sigrid using "
            "the sigridci script."
        ),
    )
    parser.add_argument("--customer", required=True,
                        help="Name of your organization's Sigrid account.")
    parser.add_argument("--system", required=True,
                        help="Name of the system in Sigrid (letters, digits, hyphens).")
    parser.add_argument("--sigrid-yaml", metavar="PATH",
                        help="Path to the sigrid.yaml scope configuration file.")
    parser.add_argument("--sigrid-metadata-yaml", metavar="PATH",
                        help="Path to the sigrid-metadata.yaml file.")
    parser.add_argument("--sigridci-path", metavar="PATH",
                        help="Path to the sigridci directory. Defaults to the sigridci/ directory in this repository.")
    parser.add_argument("--sigrid-url", default="https://sigrid-says.com", metavar="URL",
                        help="Sigrid base URL (default: https://sigrid-says.com).")
    parser.add_argument("git_urls", nargs="+", metavar="GIT_URL",
                        help="One or more git repository URLs to include.")
    return parser


def _resolve_optional_file(path_str: str, label: str) -> Path:
    path = Path(path_str).resolve()
    if not path.exists():
        print(f"ERROR: {label} not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path


def _find_duplicate_names(git_urls: List[str]) -> List[str]:
    seen: set = set()
    duplicates: List[str] = []
    for name in (_repo_name_from_url(u) for u in git_urls):
        if name in seen:
            duplicates.append(name)
        seen.add(name)
    return duplicates


def _prepare_source_dir(
    source_dir: str,
    git_urls: List[str],
    sigrid_yaml: Optional[Path],
    sigrid_metadata_yaml: Optional[Path],
) -> None:
    os.makedirs(source_dir)
    if sigrid_yaml:
        shutil.copy2(sigrid_yaml, os.path.join(source_dir, "sigrid.yaml"))
        print("  + sigrid.yaml")
    if sigrid_metadata_yaml:
        shutil.copy2(sigrid_metadata_yaml, os.path.join(source_dir, "sigrid-metadata.yaml"))
        print("  + sigrid-metadata.yaml")
    for git_url in git_urls:
        repo_name = _repo_name_from_url(git_url)
        _clone_repo_to_directory(git_url, os.path.join(source_dir, repo_name))
        print(f"  + {repo_name}/")


def _resolve_sigridci_script(sigridci_path: Optional[str]) -> Path:
    if sigridci_path:
        sigridci_dir = Path(sigridci_path).resolve()
        if not sigridci_dir.exists():
            print(f"ERROR: sigridci path not found: {sigridci_dir}", file=sys.stderr)
            sys.exit(1)
        script = sigridci_dir / "sigridci.py"
        if not script.exists():
            print(f"ERROR: sigridci.py not found at: {script}", file=sys.stderr)
            sys.exit(1)
    else:
        script = DEFAULT_SIGRIDCI_SCRIPT
        if not script.exists():
            print(f"ERROR: sigridci.py not found at the default location: {script}", file=sys.stderr)
            sys.exit(1)
    print(f"[2/3] Using sigridci: {script}")
    print()
    return script


def _run_sigridci(
    sigridci_script: Path,
    customer: str,
    system: str,
    source_dir: str,
    sigrid_url: str,
) -> None:
    print("[3/3] Publishing to Sigrid …")
    cmd = [
        sys.executable,
        str(sigridci_script),
        "--customer", customer,
        "--system", system,
        "--source", source_dir,
        "--publishonly",
        "--sigridurl", sigrid_url,
    ]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("\nERROR: sigridci failed", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = _build_arg_parser().parse_args()

    sigrid_yaml = _resolve_optional_file(args.sigrid_yaml, "sigrid.yaml") if args.sigrid_yaml else None
    sigrid_metadata_yaml = _resolve_optional_file(args.sigrid_metadata_yaml, "sigrid-metadata.yaml") if args.sigrid_metadata_yaml else None

    token = os.environ.get("SIGRID_CI_TOKEN", "").strip()
    if not token:
        print("ERROR: set the SIGRID_CI_TOKEN environment variable.", file=sys.stderr)
        sys.exit(1)

    duplicates = _find_duplicate_names(args.git_urls)
    if duplicates:
        print(f"ERROR: duplicate repository name(s): {', '.join(duplicates)}", file=sys.stderr)
        print("Rename the conflicting repos or use different URLs.", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as tmp_dir:
        print(f"\n[1/3] Cloning {len(args.git_urls)} repository(ies) …")
        source_dir = os.path.join(tmp_dir, "source")
        _prepare_source_dir(source_dir, args.git_urls, sigrid_yaml, sigrid_metadata_yaml)
        print()

        sigridci_script = _resolve_sigridci_script(args.sigridci_path)
        _run_sigridci(sigridci_script, args.customer, args.system, source_dir, args.sigrid_url, token)

    print(
        f"\nDone. '{args.system}' has been published to Sigrid.\n"
        f"After the analysis is done, results will be available at: {args.sigrid_url}/{args.customer}/{args.system}\n"
        "You will receive an email notification when the analysis is complete."
    )


if __name__ == "__main__":
    main()

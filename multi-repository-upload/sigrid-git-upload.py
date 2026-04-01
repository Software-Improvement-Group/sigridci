#!/usr/bin/env python3
"""
sigrid_git_upload.py - Upload multiple git repositories to Sigrid as a single system.

Clones multiple git repositories into subdirectories, creates a directory structure
with sigrid.yaml at the root, then uses sigridci to create zip and upload to Sigrid.

Usage:
    python sigrid-git-upload.py \\
        --customer <customer> \\
        --system   <system>   \\
        [--token <Sigrid CI token>] \\
        [--sigrid-yaml path/to/sigrid.yaml] \\
        [--sigrid-metadata-yaml path/to/sigrid-metadata.yaml] \\
        [--sigridci-path path/to/sigridci] - you can retrieve the latest version from https://github.com/Software-Improvement-Group/sigridci.git \\
        https://git.example.com/org/repo1.git \\
        https://git.example.com/org/repo2.git
    

Optional environment variables:
    SIGRID_CI_TOKEN     Bearer token for Sigrid API authentication. Only required if --token is not provided.
    SIGRID_CI_PROXY_URL Path of an HTTP/HTTPS proxy  (e.g. http://proxy:8080)
    SIGRID_CA_CERT      Path to a custom CA certificate bundle for TLS verification.
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SIGRIDCI_REPO_URL = "https://github.com/Software-Improvement-Group/sigridci.git"


def _repo_name_from_url(git_url: str) -> str:
    """Derive a filesystem-safe folder name from a git clone URL."""
    name = git_url.rstrip("/")
    if name.endswith(".git"):
        name = name[:-4]
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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
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
                        help="Path to local sigridci directory (if not provided, will clone from GitHub).")
    parser.add_argument("--sigrid-url", default="https://sigrid-says.com", metavar="URL",
                        help="Sigrid base URL (default: https://sigrid-says.com).")
    parser.add_argument("--token", metavar="TOKEN",
                        help="Sigrid CI token (overrides the SIGRID_CI_TOKEN environment variable).")
    parser.add_argument("git_urls", nargs="+", metavar="GIT_URL",
                        help="One or more git repository URLs to include.")
    return parser


def _resolve_optional_file(path_str: str, label: str) -> Path:
    path = Path(path_str).resolve()
    if not path.exists():
        print(f"ERROR: {label} not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path


def _find_duplicate_names(git_urls: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for name in (_repo_name_from_url(u) for u in git_urls):
        if name in seen:
            duplicates.append(name)
        seen.add(name)
    return duplicates


def _prepare_source_dir(
    source_dir: str,
    git_urls: list[str],
    sigrid_yaml: Path | None,
    sigrid_metadata_yaml: Path | None,
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


def _resolve_sigridci_script(tmp_dir: str, sigridci_path: str | None) -> Path:
    if sigridci_path:
        print("[2/3] Using local sigridci …")
        sigridci_dir = Path(sigridci_path).resolve()
        if not sigridci_dir.exists():
            print(f"ERROR: sigridci path not found: {sigridci_dir}", file=sys.stderr)
            sys.exit(1)
        script = sigridci_dir / "sigridci" / "sigridci.py"
        if not script.exists():
            print(f"ERROR: sigridci.py not found at: {script}", file=sys.stderr)
            sys.exit(1)
        print(f"  Using: {sigridci_dir}")
    else:
        print("[2/3] Cloning sigridci …")
        sigridci_dir_path = os.path.join(tmp_dir, "sigridci")
        result = subprocess.run(
            ["git", "clone", "--depth=1", SIGRIDCI_REPO_URL, sigridci_dir_path],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"ERROR: Failed to clone sigridci:\n{result.stderr}", file=sys.stderr)
            sys.exit(1)
        script = Path(sigridci_dir_path) / "sigridci" / "sigridci.py"
    print()
    return script


def _run_sigridci(
    sigridci_script: Path,
    customer: str,
    system: str,
    source_dir: str,
    sigrid_url: str,
    token: str,
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
    env = os.environ.copy()
    env["SIGRID_CI_TOKEN"] = token
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print("\nERROR: sigridci failed", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    args = _build_arg_parser().parse_args()

    sigrid_yaml = _resolve_optional_file(args.sigrid_yaml, "sigrid.yaml") if args.sigrid_yaml else None
    sigrid_metadata_yaml = _resolve_optional_file(args.sigrid_metadata_yaml, "sigrid-metadata.yaml") if args.sigrid_metadata_yaml else None

    token = (args.token or os.environ.get("SIGRID_CI_TOKEN", "")).strip()
    if not token:
        print("ERROR: provide --token or set the SIGRID_CI_TOKEN environment variable.", file=sys.stderr)
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

        sigridci_script = _resolve_sigridci_script(tmp_dir, args.sigridci_path)
        _run_sigridci(sigridci_script, args.customer, args.system, source_dir, args.sigrid_url, token)

    print(
        f"\nDone. '{args.system}' has been published to Sigrid.\n"
        f"After the analysis is done, results will be available at: {args.sigrid_url}/{args.customer}/{args.system}\n"
        "You will receive an email notification when the analysis is complete."
    )


if __name__ == "__main__":
    main()

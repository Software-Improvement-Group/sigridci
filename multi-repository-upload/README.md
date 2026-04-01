# sigrid-git-upload

Upload one or more git repositories to Sigrid as a single combined system. This script is only designed for manual upload runs and not to be used in a pipeline upload. It doesn't include any pull-request feedback.

The script clones each repository into a temporary directory, bundles them together (optionally with a `sigrid.yaml` scope file and metadata), and publishes the result to Sigrid using `sigridci`.

## Requirements

- Python 3.10+
- `git` available on `PATH`
- A valid Sigrid CI token

No additional Python packages are needed — only standard library modules are used.

## Usage

```
python sigrid-git-upload.py \
    --customer <customer> \
    --system   <system>   \
    [--token <token>] \
    [--sigrid-yaml path/to/sigrid.yaml] \
    [--sigrid-metadata-yaml path/to/sigrid-metadata.yaml] \
    [--sigridci-path path/to/sigridci] \
    https://git.example.com/org/repo1.git \
    https://git.example.com/org/repo2.git
```

## Arguments

| Argument | Required | Description |
|---|---|---|
| `GIT_URL ...` | Yes | One or more git repository URLs to include. |
| `--customer` | Yes | Name of your organization's Sigrid account. |
| `--system` | Yes | Name of the system in Sigrid (letters, digits, hyphens). |
| `--token` | No | Sigrid CI token. Overrides the `SIGRID_CI_TOKEN` environment variable. |
| `--sigrid-yaml` | No | Path to a `sigrid.yaml` scope configuration file to include at the root. |
| `--sigrid-metadata-yaml` | No | Path to a `sigrid-metadata.yaml` file to include at the root. |
| `--sigridci-path` | No | Path to a local `sigridci` checkout. If omitted, the latest version is cloned from GitHub automatically. |
| `--sigrid-url` | No | Sigrid base URL. Defaults to `https://sigrid-says.com`. |

## Environment variables

| Variable | Description |
|---|---|
| `SIGRID_CI_TOKEN` | Bearer token for Sigrid API authentication. Required unless `--token` is passed. |
| `SIGRID_CI_PROXY_URL` | HTTP/HTTPS proxy URL (e.g. `http://proxy:8080`). |
| `SIGRID_CA_CERT` | Path to a custom CA certificate bundle for TLS verification. |

## Example

```bash
export SIGRID_CI_TOKEN=your-token-here

python sigrid-git-upload.py \
    --customer acme \
    --system my-platform \
    --sigrid-yaml ./sigrid.yaml \
    https://github.com/acme/backend.git \
    https://github.com/acme/frontend.git \
    https://github.com/acme/shared-lib.git
```

This produces a single Sigrid system called `my-platform` containing all three repositories as subdirectories.

## How it works

1. **Clone** — each repository is cloned into its own subdirectory inside a temporary directory. `core.longpaths=true` is set to handle repositories with deeply nested paths on Windows.
2. **Resolve sigridci** — if `--sigridci-path` is not provided, the latest `sigridci` is cloned from GitHub.
3. **Publish** — `sigridci.py --publishonly` is invoked with the combined source directory, uploading it to Sigrid.

## Notes

- Two repositories with the same name (last path segment of the URL) cannot be combined — the script will exit with an error listing the duplicates.
- On Windows, file paths exceeding 260 characters require an administrator to enable long path support: `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1`.

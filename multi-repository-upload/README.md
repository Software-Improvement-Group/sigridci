# Upload multiple Git repositories to Sigrid

Upload one or more git repositories or local source folders to Sigrid as a single combined system. This script is only designed for manual upload runs and not to be used in a pipeline upload. It doesn't include any pull-request feedback.

The script accepts remote git URLs (which it clones) and/or local folder paths, bundles them together (optionally with a `sigrid.yaml` scope file and metadata), and publishes the result to Sigrid using `sigridci`.

## Requirements

- Python 3.9+
- `git` available on `PATH`
- A valid [Sigrid CI token](https://docs.sigrid-says.com/organization-integration/authentication-tokens.html)

No additional Python packages are needed — only standard library modules are used.

## Usage

```
./sigrid-git-upload.py \
    --customer <customer> \
    --system   <system>   \
    [--sigrid-yaml path/to/sigrid.yaml] \
    [--sigrid-metadata-yaml path/to/sigrid-metadata.yaml] \
    [--sigridci-path path/to/sigridci] \
    https://git.example.com/org/repo1.git \
    /path/to/local/repo2
```

On Windows, use `python sigrid-git-upload.py` instead of `./sigrid-git-upload.py`.

## Arguments

| Argument | Required | Description |
|---|---|---|
| `SOURCE ...` | Yes | One or more sources to include: remote git URLs (HTTPS/SSH) or local folder paths. |
| `--customer` | Yes | Name of your organization's Sigrid account. |
| `--system` | Yes | Name of the system in Sigrid (letters, digits, hyphens). |
| `--sigrid-yaml` | No | Path to a `sigrid.yaml` scope configuration file to include at the root. |
| `--sigrid-metadata-yaml` | No | Path to a `sigrid-metadata.yaml` file to include at the root. |
| `--sigridci-path` | No | Path to a local `sigridci` directory. Defaults to the `sigridci/` directory in this repository. |
| `--sigrid-url` | No | Sigrid base URL. Defaults to `https://sigrid-says.com`. |

## Environment variables

| Variable | Description |
|---|---|
| `SIGRID_CI_TOKEN` | Bearer token for Sigrid API authentication. **Required.** |
| `SIGRID_CI_PROXY_URL` | HTTP/HTTPS proxy URL (e.g. `http://proxy:8080`). |
| `SIGRID_CA_CERT` | Path to a custom CA certificate bundle for TLS verification. |

## Example

```bash
export SIGRID_CI_TOKEN=your-token-here

./sigrid-git-upload.py \
    --customer acme \
    --system my-platform \
    --sigrid-yaml ./sigrid.yaml \
    https://github.com/acme/backend.git \
    https://github.com/acme/frontend.git \
    /path/to/local/shared-lib
```

This produces a single Sigrid system called `my-platform` containing all three repositories as subdirectories.

## How it works

1. **Process sources** — each source is handled based on its type:
   - **Remote URL** — the repository is cloned into a temporary subdirectory. `core.longpaths=true` is set to handle deeply nested paths on Windows.
   - **Local git repository** — `git archive HEAD` is used to export only tracked files, automatically excluding untracked files such as `node_modules`, build outputs, and any other files ignored by git.
   - **Local non-git folder** — the folder is copied as-is.
2. **Resolve sigridci** — uses the `sigridci/` directory bundled in this repository. Override with `--sigridci-path` if needed.
3. **Publish** — `sigridci.py --publishonly` is invoked with the combined source directory, uploading it to Sigrid.

## Notes

- Two sources with the same name (folder name or last path segment of a URL) cannot be combined — the script will exit with an error listing the duplicates.
- On Windows, file paths exceeding 260 characters require an administrator to enable long path support: `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem\LongPathsEnabled = 1`.

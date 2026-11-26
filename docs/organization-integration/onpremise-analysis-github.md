# Sigrid on-premise: Analysis with GitHub Actions

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page shows how to run Sigrid-Multi-Analyzer in GitHub Actions, and how to receive Sigrid's feedback in pull requests. It builds on the general [analysis configuration](onpremise-analysis.md), which describes the environment variables and certificates.

## Source code in Sigrid

Sigrid shows source code files from GitHub in the Code Explorer. This needs an OAuth registration in the Helm chart, see [connection to source code repositories](onpremise-kubernetes.md#g-optional-connection-to-source-code-repositories). Set `SIGRID_SOURCES_REGISTRATION_ID` to the ID of that registration, unless it is the only one in the Helm chart. Without the registration, Sigrid shows an *Open in external VCS* button instead.

## Pull request feedback

Set the following variables in your pipeline:

| Variable                      | Description |
|-------------------------------|-------------|
| `CICD_COMMENT_TOKEN` | GitHub personal access token (classic) or fine-grained token with `pull-requests: write` permission |

To create the token:

- In GitHub, go to *Settings → Developer settings → Personal access tokens* (for your user or a service account).
- Create a fine-grained token with *Pull requests: Read and write* permission for the target repositories, or a classic token with the `repo` scope.
- In your repository or organization *Settings → Secrets and variables → Actions*, add a secret named `CICD_COMMENT_TOKEN` with the token as value, and pass it to the analysis job as an environment variable.

Sigrid will automatically detect pull request pipelines via the `GITHUB_EVENT_NAME` variable set by GitHub Actions and post or update a comment on the pull request. The `GITHUB_API_URL` variable set by GitHub Actions is used as the API endpoint, so this works for both github.com and GitHub Enterprise Server without extra configuration.

Note that `GITHUB_EVENT_NAME` is only defined as `pull_request` when the workflow is triggered by a pull request event, so the workflow running the analysis needs:

```yaml
on: [pull_request]
```

## Example pipeline

{% raw %}
```yaml
name: Sigrid
on: [pull_request]
jobs:
  sigrid-publish:
    runs-on: ubuntu-latest
    container:
      image: 571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:${{ vars.SIGRID_VERSION }}
    env:
      CUSTOMER: company_name
      SYSTEM: ${{ github.event.repository.name }}
      SIGRID_URL: https://sigrid.my-company.com
      SIGRID_SOURCES_REGISTRATION_ID: github-onprem
      SIGRID_CI_TOKEN: ${{ secrets.SIGRID_CI_TOKEN }}
      CICD_COMMENT_TOKEN: ${{ secrets.CICD_COMMENT_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      - run: run-analyzers --publish

```
{% endraw %}

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

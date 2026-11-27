# Sigrid on-premise: Analysis with GitLab CI/CD

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page shows how to run Sigrid-Multi-Analyzer in GitLab CI/CD, and how to receive Sigrid's feedback in merge requests. It builds on the general [analysis configuration](onpremise-analysis.md), which describes the environment variables and certificates.

## Source code in Sigrid

Sigrid shows source code files from GitLab in the Code Explorer. This needs an OAuth registration in the Helm chart, see [connection to source code repositories](onpremise-kubernetes.md#g-optional-connection-to-source-code-repositories). Set `SIGRID_SOURCES_REGISTRATION_ID` to the ID of that registration, unless it is the only one in the Helm chart. Without the registration, Sigrid shows an *Open in external VCS* button instead.

## Merge request feedback

Set the following variables in your pipeline:

| Variable                      | Description |
|-------------------------------|-------------|
| `CICD_COMMENT_TOKEN` | GitLab personal access token with `api` scope |

To create the token:

- In GitLab, go to your user (or a service account's) *Preferences → Access Tokens*, or use a [project or group access token](https://docs.gitlab.com/ee/user/project/settings/project_access_tokens.html).
- Create a token with the `api` scope. The token owner needs sufficient rights to post merge request comments in the target projects.
- In your project or group *Settings → CI/CD → Variables*, add a variable named `CICD_COMMENT_TOKEN` with the token as value. Use type "Variable" (not "File"), and do *not* mark it as protected, otherwise it is not available in merge request pipelines from unprotected branches.

Sigrid will automatically detect merge request pipelines via the `CI_MERGE_REQUEST_IID` variable set by GitLab CI and post or update a comment on the merge request.

Note that `CI_MERGE_REQUEST_IID` is only available in merge request pipelines, so the analysis job needs a rule that makes it run in them:

{% raw %}
```yaml
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
```
{% endraw %}

## Example pipeline

{% raw %}
```yaml
sigrid-publish:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  image:
    name: "571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:$SIGRID_VERSION"
  variables:
    CUSTOMER: "company_name"
    SYSTEM: "$CI_PROJECT_NAME"
    SIGRID_URL: "https://sigrid.my-company.com"
    SIGRID_SOURCES_REGISTRATION_ID: "gitlab-onprem"
    # SIGRID_CI_TOKEN and CICD_COMMENT_TOKEN are masked CI/CD variables of the project or group
  script:
    - "run-analyzers --publish"

```
{% endraw %}

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

# Sigrid on-premise: Analysis with Azure DevOps

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page shows how to run Sigrid-Multi-Analyzer in Azure Pipelines, for both Azure DevOps (cloud) and Azure DevOps Server, and how to receive Sigrid's feedback in pull requests. It builds on the general [analysis configuration](onpremise-analysis.md), which describes the environment variables and certificates.

## Source code in Sigrid

Sigrid shows source code files from Azure DevOps (cloud) in the Code Explorer. This needs an OAuth registration in the Helm chart, see [connection to source code repositories](onpremise-kubernetes.md#g-optional-connection-to-source-code-repositories). Set `SIGRID_SOURCES_REGISTRATION_ID` to the ID of that registration, unless it is the only one in the Helm chart. Without the registration, Sigrid shows an *Open in external VCS* button instead.

For Azure DevOps Server, Sigrid shows an *Open in external VCS* button, which opens the file in Azure DevOps Server instead, see [source code links](onpremise-kubernetes.md#source-code-links-for-azure-devops-server-and-gerrit). No OAuth registration is needed.

## Pull request feedback

Azure DevOps uses the built-in `SYSTEM_ACCESSTOKEN` — no separate token variable is needed. Pass it to the analysis step as an environment variable:

```yaml
env:
  SYSTEM_ACCESSTOKEN: $(System.AccessToken)
```

Two Azure DevOps settings are easy to miss. Without them, no pipeline runs for pull requests, or Sigrid cannot create comments:

- **Build validation:** Azure DevOps does not run pipelines for pull requests by default. Enable this per branch with a build policy that uses *Build validation*. See the [Azure DevOps documentation](https://learn.microsoft.com/en-us/azure/devops/repos/git/branch-policies?view=azure-devops&tabs=browser#build-validation).
- **Build Service permission:** The `<repo name> Build Service` user needs the *Contribute to pull requests* permission on the repository. See the [Azure DevOps documentation](https://learn.microsoft.com/en-us/azure/devops/repos/git/set-git-repository-permissions?view=azure-devops).

## Example pipeline for Azure DevOps (cloud)

{% raw %}
```yaml
trigger: none
pr:
  branches:
    include:
      - main
pool:
  vmImage: ubuntu-latest
variables:
  CUSTOMER: company_name
  SYSTEM: $(Build.Repository.Name)
  SIGRID_URL: https://sigrid.my-company.com
  SIGRID_SOURCES_REGISTRATION_ID: azure-devops-onprem
jobs:
  - job: sigrid_publish
    container: 571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:$(SIGRID_VERSION)
    steps:
      - checkout: self
      - script: run-analyzers --publish
        env:
          SIGRID_CI_TOKEN: $(SIGRID_CI_TOKEN)
          # Azure DevOps posts the comment with the built-in access token, instead of CICD_COMMENT_TOKEN
          SYSTEM_ACCESSTOKEN: $(System.AccessToken)

```
{% endraw %}

## Example pipeline for Azure DevOps Server

For Azure DevOps Server, use a self-hosted agent pool and omit the OAuth variable, since Azure DevOps Server has no OAuth registration in the Helm chart. Use `CICD_CA_CERT` if the server uses an internal CA:

{% raw %}
```yaml
trigger: none
pr:
  branches:
    include:
      - main
pool:
  name: my-self-hosted-pool  # an agent with Docker
variables:
  CUSTOMER: company_name
  SYSTEM: $(Build.Repository.Name)
  SIGRID_URL: https://sigrid.my-company.com
jobs:
  - job: sigrid_publish
    container: 571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:$(SIGRID_VERSION)
    steps:
      - checkout: self
      - script: run-analyzers --publish
        env:
          SIGRID_CI_TOKEN: $(SIGRID_CI_TOKEN)
          # Azure DevOps posts the comment with the built-in access token, instead of CICD_COMMENT_TOKEN
          SYSTEM_ACCESSTOKEN: $(System.AccessToken)

```
{% endraw %}

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

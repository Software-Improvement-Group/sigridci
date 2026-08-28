# Uploading your source code to Sigrid

This documentation covers cloud-based Sigrid. On-premise Sigrid requires integration with your development platform, 
which is explained in the section about [on-premise analysis configuration](../organization-integration/onpremise-analysis.md).
{: .attention }

## Recommended approach: Integrate Sigrid CI in your pipeline

Integrating Sigrid CI into your pipeline allows you to automatically publish your source code to Sigrid after every 
change. It also allows you to receive feedback from Sigrid within your development environment.

This documentation contains platform-specific instructions for integrating Sigrid CI into your pipeline:

- [GitHub](../sigridci-integration/github-actions.md)
- [GitLab](../sigridci-integration/gitlab.md)
- [Azure DevOps](../sigridci-integration/azure-devops.md)
- [BitBucket](../sigridci-integration/azure-devops.md)
- [Jenkins](../sigridci-integration/jenkins.md)
- [TeamCity](../sigridci-integration/teamcity.md)

## Manually uploading source code using Sigrid CI

In some situations, you may want to publish your source code to Sigrid *without* integrating Sigrid in your pipelines.
In those cases, you can manually run Sigrid CI from the command line:

- Make sure you have a Sigrid [API token](../organization-integration/authentication-tokens.md).
- Create an environment variable called `SIGRID_CI_TOKEN` containing your API token.
- Navigate to the directory containing your source code.
- Clone the Sigrid CI repository: `git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci`
- Run the script to publish your source code: `./sigridci/sigridci/sigridci.py --customer <example_customer_name> --system <example_system_name> --source . --publish`

## Uploading source code using SFTP

SFTP uploads are outdated. Prefer using [Sigrid CI](#recommended-approach-integrate-sigrid-ci-in-your-pipeline) to
publish your source code to Sigrid.
{: .warning }

See the [SFTP upload instructions](sftp-upload-instructions.md) if you are unable to use Sigrid CI and are therefore
forced to rely on SFTP uploads.

## Manually uploading source code using the SIG Upload Portal

Manual uploads are outdated. Prefer using [Sigrid CI manually](#manually-uploading-source-code-using-sigrid-ci) to
publish your source code to Sigrid.
{: .warning }

See the instructions for [using the SIG Upload Portal](manual-upload-instructions.md) for more information on how
to use the SIG Upload Portal in situations where you are unable to use Sigrid CI.

## Uploading multiple Git repositories as a single Sigrid system

If you need to combine several Git repositories into one Sigrid system for a one-off upload, 
you can use [multi repository upload script](../../multi-repository-upload/README.md) provided by SIG
on GitHub. The project documentation contains more instructions and examples on how to use this script.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or 
issues you may have after reading this document or when using Sigrid or Sigrid CI.

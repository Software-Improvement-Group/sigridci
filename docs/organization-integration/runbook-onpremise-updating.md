# Runbook: Updating Sigrid On-Premise

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This runbook explains how to keep your on-premise Sigrid deployment up-to-date. It is an excellent starting point for ongoing maintenance and ensures you follow a safe, repeatable update process.

> **Important:** Before updating, always review the [Helm Chart Release Notes](onpremise-helm-releases.md) to check for:
> - New features you may want to enable
> - Required changes in your Helm configuration
> - Breaking changes that require special attention

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation
- You have a running Sigrid Deployment
- You have access to Software Improvement Group AWS ECR registry

## Update Frequency

- **Sigrid Docker containers:** Monthly at minimum, ideally with each release
- **Sigrid Helm chart:** Only when new features or significant changes are released, preferably following each published chart version

## Update Instructions

1. Review the [Helm Chart Release Notes](onpremise-helm-releases.md) for relevant changes.
2. Update Helm Chart
3. Update Container images
4. Update the `imageTag` in the Helm chart configuration
5. Apply the updates using Helm

### Update Containers

Pull the latest Sigrid Docker images from SIG's AWS ECR registry or from your own container registry, depending on your setup.  
See [accessing SIG's AWS ECR](onpremise-aws-ecr.md) for detailed instructions if needed.

### Update image tag (Sigrid version)

Update the `imageTag` in the `global` section of the Helm chart values file (`custom-values.yaml`):

{% raw %}
```yaml
global:
  imageTag: "<REPLACE-WITH-LATEST-VERSION>"
```
{% endraw %}

### Apply the updates using Helm

To apply the updates using Helm, you can use the following command. Note how to do this might vary depending on how you deployed Sigrid.

{% raw %}
```bash
   helm upgrade --install sigrid-onprem ./sigrid-stack -n sigrid --values ./sigrid-stack/custom-values.yaml
```
{% endraw %}

## Test Instructions

1. Verify that all pods are running
2. Check the logs of key services for any errors
3. Access the Sigrid frontend and perform basic operations to ensure functionality.
4. Run a test analysis on a sample project to verify the entire pipeline is working correctly.
If any issues are encountered during testing, consider rolling back to the previous version and contacting support.

## Additional System Maintenance

In addition to updating Sigrid components, it's important to maintain other systems that Sigrid depends on:

- PostgreSQL: Ensure that your PostgreSQL database is regularly updated and maintained. Keep the PostgreSQL version within the latest two supported major versions.
- Other (e.g., GitLab): Regularly update and maintain your supporting systems.

The update frequency for these systems should be determined based on your organization's needs and policies. However, it's crucial to keep these systems up-to-date to ensure optimal performance, security, and compatibility with Sigrid.

Note: Specific update instructions for PostgreSQL and other systems are not provided here, as they can vary depending on your setup and chosen systems. Please refer to the official documentation of these systems for proper update procedures.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

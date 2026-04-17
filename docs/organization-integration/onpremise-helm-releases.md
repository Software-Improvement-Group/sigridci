# Sigrid On-Premise: Helm Chart Releases

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page provides an overview of Sigrid On-Premise Helm chart releases and their impact on deployments.

Helm chart releases are not published for every Sigrid release. This page only lists Helm chart versions that **introduce new capabilities or require action from platform teams**.  

A new chart version is typically released when changes in Sigrid affect the deployment configuration, such as:  
- New or changed configuration options  
- Infrastructure or dependency changes  
- Fixes in deployment behavior  
- Breaking changes affecting installation or upgrades  

For a complete overview of functional changes, features, and bug fixes in Sigrid itself, refer to the [general release notes](../reference/release-notes.md).  

This page focuses specifically on deployment-relevant changes, including required actions for upgrades.

## Helm Chart Release Notes

The Helm chart is published under the name `sigrid-stack`.

### Release 1.0.20260421 - BREAKING CHANGE

From now on, we no longer use semantic versioning (e.g. `0.4.14`) for Helm chart releases. Helm charts and container images now follow a unified date-based versioning scheme. All future releases use the format `1.0.YYYYMMDD`, aligned with the Sigrid container release versioning.

**Added:** Sigrid-Multi-Analyzer no longer connects directly to S3-compatible object storage. This simplifies the pipeline job but requires updates to the Helm configuration.

**Breaking:** This change requires Sigrid and Sigrid-Multi-Analyzer version `1.0.20260421` or later and requires the actions below.

**Actions**
- Update the Sigrid Helm chart and configuration before deploying Sigrid and Sigrid-Multi-Analyzer.
  1. Update Sigrid Helm chart.
  2. Update Helm configuration.
     - For the expected configuration, see [Kubernetes deployment](../organization-integration/onpremise-kubernetes.md#f1-configure-the-object-store).
     - Update the object store secret to only include `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
       - These keys are no longer required: `AWS_FORCE_PATH_STYLE`, `AWS_REGION`.
     - Remove deprecated configuration from Helm values: `inbound-api.config.importJob`.
     - Update `global.imageTag` or `image.tag` for individual services.
  3. Clean up pipeline job configuration.
     - Update `$SIGRID_VERSION`.
     - Remove all legacy object store settings from the Sigrid pipeline job, including:
       - `BUCKET`
       - `AWS_FORCE_PATH_STYLE`
       - `AWS_REGION`
       - `AWS_ACCESS_KEY_ID`
       - `AWS_SECRET_ACCESS_KEY`
       - `AWS_CA_BUNDLE`

### Release 0.4.14

**Added:** Database initialization can now also be performed automatically.  
If you are interested in using this feature, please refer to the [feature page](../organization-integration/onpremise-automated-database-initialization.md).  

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260309 or later; newer versions can be used, but the feature won't work on earlier releases.  

**Actions:** Update the Sigrid Helm chart and configuration to enable this new feature.

### Release 0.4.13 - BREAKING CHANGE

**Change:** Newly onboarded systems now automatically grant access to the uploader. Previously, access had to be granted manually. After updating the Helm chart and container images, this step is handled automatically.  

**Breaking:** This Helm chart version is required to deploy Sigrid and Sigrid-Multi-Analyzer 1.0.20260225 or later. Helm chart and container versions must always be released together.  

**Actions:** Update the Sigrid Helm chart and configuration before deploying Sigrid and Sigrid-Multi-Analyzer.  
For required configuration changes, see [these instructions](../organization-integration/onpremise-kubernetes.md#e2-create-a-secret-to-authorize-sigrid-system-configuration).

### Release 0.4.12

**Enhanced:** LDAP group synchronization now allows the group membership attribute to be configured.  
If you are interested in using this feature, please refer to the [feature page](../organization-integration/onpremise-ldap-group-sync.md).  

**Note:** This enhancement requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260224 or later; newer versions can be used, but the feature won't work on earlier releases.  

**Actions:** Update the Sigrid Helm chart and configuration to enable this feature.

### Release 0.4.11

**Added:** Sigrid now allows you to automatically synchronize group memberships using LDAP.  
If you are interested in using this feature, please refer to the [feature page](../organization-integration/onpremise-ldap-group-sync.md).  

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260223 or later; newer versions can be used, but the feature won't work on earlier releases.  

**Actions:** Update the Sigrid Helm chart and configuration to enable this new feature.

### Release 0.4.10

**New:** Open Source Health (OSH) is now available for Sigrid On-Premise!
This feature has been available on Sigrid SaaS and is now also supported on-premise. For an overview of its capabilities, see the [system features page](../capabilities/system-open-source-health.md).  
End users are recommended to also read the [on-premise OSH analysis guide](../organization-integration/onpremise-osh-analysis.md).

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20251222 or later; newer versions can be used, but the feature won't work on earlier releases.  

**Actions:** Update the Sigrid Helm chart and configuration to enable this feature.  
For required configuration changes, see [the OSH knowledge base updater instructions](../organization-integration/onpremise-osh-knowledgebase-updater.md).

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
# Sigrid On-Premise: Release Notes

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page lists Sigrid release notes that are noteworthy for on-premise deployments, either because they are specific to on-premise or because they require additional steps beyond the standard update.

A new Helm chart is released with every Sigrid release. Most updates only require updating the Sigrid and Sigrid-Multi-Analyzer container images. This page highlights changes that require additional attention, such as:
- New or changed Helm configuration options
- Infrastructure or dependency changes
- Breaking changes affecting installation or upgrades
- Fixes or features specific to on-premise deployments

For a complete overview of all Sigrid changes, refer to the [general release notes](../reference/release-notes.md).

The Helm chart is published under the name `sigrid-stack`.

### Release 1.0.20260713

**New:** The documentation and academy links shown in the Sigrid user interface are now configurable per deployment. This allows air-gapped environments to point the links to an internally mirrored documentation site, or to hide them entirely.

**New:** Sigrid administrators can now set a custom support email address for their organization via the Sigrid user interface (menu → "metadata"). When no address is set, Sigrid shows the default SIG support address (`support@softwareimprovementgroup.com`). This is a setting within Sigrid itself, not a Helm value. See the [organization metadata documentation](metadata.md#organization-level-metadata) for details.

<details markdown="1">
<summary>Details</summary>

The documentation and academy URLs are configured in the `sigrid-api` chart (chart version 0.3.2 and later):

{% raw %}
```yaml
sigrid-api:
  config:
    sigridConfigurableMetaURLs:
      documentationUrl: "https://docs.sigrid-says.com"
      academyUrl: "https://academy.sigrid-says.com"
```
{% endraw %}

The values above are the defaults. Behavior to be aware of:
- Setting a URL to the special value `none` hides the corresponding link in the Sigrid user interface.
- Both URLs must be set for the configuration to take effect. If either one is left empty, the entire configuration block is omitted and both links are hidden. Use `none` instead of an empty value to hide a single link.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required unless you want to override the default URLs.
</details>

### Release 1.0.20260701 - BREAKING CHANGE

**Change:** The bundled Bitnami `postgresql` subchart has been removed from `sigrid-stack`. **Only impactful if your deployment had `postgresql.enabled: true`** — the standard PostgreSQL setup ([your own database](onpremise-kubernetes.md#c-postgresql), initialized manually with `psql` or automatically via [`global.onPremise.postgresInit`](onpremise-automated-database-initialization.md)) is unchanged.

<details markdown="1">
<summary>Details</summary>

**Breaking:** On `helm upgrade`, the bundled Postgres pod and Service are torn down, _if_ you had this enabled; the data volume is left behind but no longer attached to anything.

**Actions:** Before upgrading, provide your own PostgreSQL, migrate the data, and update the application database URLs.
</details>

### Release 1.0.20260622

**Fixed:** The Sigrid Multi-Analyzer now fails early when a system has been deactivated in the Sigrid system settings page, instead of proceeding with the analysis and failing with a confusing error.

**Fixed:** Custom CA certificates were not being passed through to the feedback step, causing TLS failures when posting PR/MR comments on platforms configured with a custom certificate.  The `SIGRID_CA_CERT` value (or the new `CICD_CA_CERT` if set) is now forwarded correctly. A dedicated `CICD_CA_CERT` variable is now available if your CI/CD platform uses a different certificate than Sigrid itself.

<details markdown="1">
<summary>Details</summary>

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required.
</details>

### Release 1.0.20260616

**Fixed:** The Sigrid Multi-Analyzer now validates your Sigrid credentials and configuration *before* starting an analysis. The pipeline job now fails fast with a clear message when the `SIGRID_CI_TOKEN` is missing or incomplete, when the configured system name is invalid, or when the token does not have access to the system (HTTP 401/403). When the system does not exist in Sigrid yet, the job clearly reports that it will be on-boarded on the first analysis, instead of failing with a confusing error.

<details markdown="1">
<summary>Details</summary>

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required.
</details>

### Release 1.0.20260613

**Fixed:** The support page in the Sigrid UI now shows the Sigrid version number for on-premise deployments. Previously only a commit SHA was shown.

<details markdown="1">
<summary>Details</summary>

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required.
</details>

### Release 1.0.20260529

**Fixed:** Sigrid Multi-Analyzer now respects analyzer enabled/disabled flags in `sigrid.yaml`. DependencyChecker properly receives scope settings for blocklist enforcement.

<details markdown="1">
<summary>Details</summary>

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required.
</details>

### Release 1.0.20260518

**Fixed:** Fixed console errors caused by missing Matomo analytics stub in on-premises deployments without a Matomo instance.

<details markdown="1">
<summary>Details</summary>

**Note:** This fix is transparent to existing deployments. A new Helm value `nginx.config.fragment.location.matomo` is available for on-prem deployments that want to configure their own Matomo instance.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. No configuration changes required unless want to make use of Matomo.
</details>

### Release 1.0.20260512

**Updated:** The LDAP group sync integration now removes Sigrid users that are no longer present in LDAP by default. See the [on-premise documentation](../organization-integration/onpremise-ldap-group-sync.md) for more information.

<details markdown="1">
<summary>Details</summary>

**Note:** This behavior is controlled by the new `--remove-users` flag, which is now enabled by default alongside `--override-groups`. It can be disabled by overriding the `args` list in the Helm configuration values.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. Review the default `args` if you want to opt out of automatic user removal.
</details>

### Release 1.0.20260421 - BREAKING CHANGE

From now on, we're aligning the version number of Helm chart releases with container image tags. So both now follow a unified, date-based versioning scheme. All future releases use the format `1.0.YYYYMMDD`, aligned with the Sigrid container release versioning.

**Change:** Sigrid-Multi-Analyzer no longer connects directly to S3-compatible object storage. This simplifies the pipeline job but requires updates to the Helm configuration.

<details markdown="1">
<summary>Details</summary>

**Fixed:** Configuration values from `global.onPremise` only needed for `Job` pods are no longer passed to the API pods. During upgrading, this may show a diff as the unnecessary configuration values will be removed from `ConfigMap`s used by the API pods. Specifically, `ecrRepository`, `oshKbUpdater`, `ldapGroupSync` and `postgresInit` will disappear from those `ConfigMap`s, if those keys were already configured under `global.onPremise`.

**Breaking:** This change requires Sigrid and Sigrid-Multi-Analyzer version `1.0.20260421` or later and requires the actions below.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image before deploying.
1. Update Sigrid Helm chart to version 1.0.20260421, or greater.
2. Update Helm configuration.
   - For the expected configuration, see [Kubernetes deployment](../organization-integration/onpremise-kubernetes.md#f1-configure-the-object-store).
   - Remove deprecated configuration from Helm values: `inbound-api.config.importJob.objectStoreSecret`.
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
</details>

### Release 0.4.14

**Added:** Database initialization for on-premise Sigrid can now also be performed automatically.
If you are interested in using this feature, please refer to the [feature page](../organization-integration/onpremise-automated-database-initialization.md).

<details markdown="1">
<summary>Details</summary>

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260309 or later; newer versions can be used, but the feature won't work on earlier releases.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. Update the Helm configuration to enable this new feature.
</details>

### Release 0.4.13 - BREAKING CHANGE

**Change:** Newly onboarded systems now automatically grant access to the uploader. Previously, access had to be granted manually. After updating the Helm chart and container images, this step is handled automatically.

<details markdown="1">
<summary>Details</summary>

**Breaking:** This Helm chart version is required to deploy Sigrid and Sigrid-Multi-Analyzer 1.0.20260225 or later. Helm chart and container versions must always be released together.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image.
For required configuration changes, see [these instructions](../organization-integration/onpremise-kubernetes.md#e2-create-a-secret-to-authorize-sigrid-system-configuration).
</details>

### Release 0.4.12

**Updated:** LDAP group synchronization now allows the group membership attribute to be configured.
If you are interested in using this feature, please refer to the [feature page](../organization-integration/onpremise-ldap-group-sync.md).

<details markdown="1">
<summary>Details</summary>

**Note:** This enhancement requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260224 or later; newer versions can be used, but the feature won't work on earlier releases.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. Update the Helm configuration to enable this feature.
</details>

### Release 0.4.11

**Added:** On-premise Sigrid now supports automatic LDAP group synchronization. See the [on-premise documentation](../organization-integration/onpremise-ldap-group-sync.md) for more information.

<details markdown="1">
<summary>Details</summary>

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20260223 or later; newer versions can be used, but the feature won't work on earlier releases.

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. Update the Helm configuration to enable this new feature.
</details>

### Release 0.4.10

**Added:** Open Source Health is now available in on-premise Sigrid. See the [on-premise instructions](../organization-integration/onpremise-osh-knowledgebase-updater.md) for how to set this up.

<details markdown="1">
<summary>Details</summary>

**Note:** This feature requires Sigrid and Sigrid-Multi-Analyzer version 1.0.20251222 or later; newer versions can be used, but the feature won't work on earlier releases.
For an overview of OSH capabilities, see the [system features page](../capabilities/system-open-source-health.md).
End users are recommended to also read the [on-premise OSH analysis guide](../organization-integration/onpremise-osh-analysis.md).

**Actions:** Update the Sigrid Helm chart, Sigrid deployment images, and Sigrid-Multi-Analyzer image. Update the Helm configuration to enable this feature.
For required configuration changes, see [the OSH knowledge base updater instructions](../organization-integration/onpremise-osh-knowledgebase-updater.md).
</details>

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

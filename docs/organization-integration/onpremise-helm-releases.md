# Sigrid On-Premise: Helm Chart Releases

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page provides an overview of Sigrid On-Premise Helm chart releases and their impact on deployments.

Helm chart releases are not published for every Sigrid release. A new chart version is only released when changes in Sigrid require updates to the deployment configuration, such as:
- New or changed configuration options
- Infrastructure or dependency changes
- Fixes in deployment behavior
- Breaking changes affecting installation or upgrades

For a complete overview of functional changes, features, and bug fixes in Sigrid itself, refer to the [general release notes](../reference/release-notes.md).

This page focuses specifically on deployment-relevant changes, including required actions for upgrades.

---

## Helm Chart Release Notes

The Helm chart is published under the name `sigrid-stack`.

### Release 0.4.14 (2026-03-09)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

### Release 0.4.13 (2026-02-25)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

### Release 0.4.12 (2026-02-23)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

### Release 0.4.11 (2026-02-20)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

### Release 0.4.10 (2025-12-22)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

---

### 0.4.9 (2025-11-27)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

---

### 0.4.8 (2025-11-26)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

---

### 0.4.7 (2025-11-24)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

---

### 0.4.6 (2025-10-27)

**Added:** Configurable resource limits for analysis workers via Helm values  
**Changed:** PostgreSQL readiness probe updated for Helm deployment  
**Fixed:** Missing volume mount in worker pods  
**Breaking:** `values.yaml` key for ingress changed  
**Actions:** Update `values.yaml` before upgrading

---

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

## Infrastructure & Resource Requirements

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This document defines compute and storage resource requirements for:
- CI/CD workloads (e.g. static analysis jobs)
- Application workloads running on Kubernetes

### 1. Analysis (Sigrid-Multi-Analyzer)

Sigrid-Multi-Analyzer is the most resource-intensive component and must be sized accordingly.

**Requirements:**
- **Memory:**
  - Minimum: 5 GB RAM
  - Recommended: 16 GB RAM (depending on repository size)
- **CPU:** 2-4 vCPU
- **Storage:**: 5 GB (depending on repository size)
- **Environment:** Containerized job (e.g. GitLab CI/CD runner)

Analysis workloads may exhibit memory and disk usage spikes. Avoid strict limits close to the minimum requirements to prevent job failures.

During analysis, intermediate results are written to local disk before being uploaded to S3-compatible object storage.

---

### 2. Kubernetes (Node)

While Kubernetes itself has minimal requirements, worker nodes must be sized to support the workloads.

**Recommended baseline:**
- **CPU:** 4 vCPU
- **Memory:** 16 GB RAM
- **Storage:** 50 GB

This allows:
- Running multiple application pods
- Supporting high-memory and disk-intensive workloads such importing jobs
- Storing container images and temporary files on the node

For clusters running only Sigrid application components (API/frontend), lower disk sizes may be sufficient. Actual sizing depends on whether CI/CD workloads or other applications share the same nodes.

Node sizing must account for the largest schedulable workload (e.g. CI jobs requiring up to 16 GB RAM), not just average application usage.

Analysis jobs run in CI/CD, not in the cluster, unless CI/CD runners are deployed in the same cluster.

---

### 3. Application (Sigrid)

Resource requirements are defined per container/pod in the Helm configuration.  
You can start with the defaults, but these can always be overridden.

Example

```yaml
auth-api:
  image:
    repository: "softwareimprovementgroup/auth-api"
  replicas: 2
  podDisruptionBudget:
    minAvailable: 50%
  resources:
    limits:
      memory: 2Gi
    requests:
      cpu: 500m
      memory: 2Gi

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
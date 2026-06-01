## Infrastructure & Resource Requirements for Sigrid Components

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This document defines compute and storage resource requirements for Sigrid components, including:
- CI/CD workloads (e.g. static analysis jobs running in your existing CI/CD system)
- Application workloads running on Kubernetes

The numbers below reflect typical production workloads and are intended as a starting point. Actual sizing depends on team size, number of systems, CI/CD frequency, and codebase characteristics.

### 1. Analysis (Sigrid-Multi-Analyzer)

Sigrid-Multi-Analyzer is the most resource-intensive component and runs as jobs in your **existing CI/CD tool** (e.g. GitLab, GitHub Actions, Azure DevOps).

**Requirements:**
- **Memory:**
  - Minimum: 5 GB RAM
  - Recommended: 16 GB RAM (depending on repository size)
- **CPU:** 2-4 vCPU
- **Storage:** 5 GB (depending on repository size)
- **Environment:** Containerized job in your CI/CD system

Analysis workloads may exhibit memory and disk usage spikes. Avoid setting limits too close to the minimum requirements to prevent job failures.

During analysis, intermediate results are written to local disk before being uploaded to S3-compatible object storage.

#### Runner Placement

Sigrid-Multi-Analyzer runs as a job inside your CI/CD system (GitLab CI, GitHub Actions, Azure DevOps). The runners or agents that execute those jobs can be hosted anywhere, which affects your Kubernetes sizing:

- **Runners hosted outside the Sigrid cluster** (dedicated VMs, self-hosted agents): Analyzer memory spikes are fully isolated from Sigrid workloads. No additional Kubernetes capacity needed.
- **Runners hosted inside the Sigrid cluster**: The Kubernetes node pool must be sized to absorb analyzer memory overhead on top of the Sigrid services. Monitor memory pressure during peak CI/CD activity and size node pools conservatively.

#### Memory by Codebase Size

Memory requirements vary by language. JavaScript/TypeScript and Scala are notably more memory-intensive than average, while Go and Python tend to be more efficient.

| Lines of code | Recommended memory |
|---|---|
| < 100K | 5 GB |
| 100K - 300K | 8-10 GB |
| 300K - 600K | 17 GB |
| 600K - 1M | 26-30 GB |
| > 1M | 57+ GB |

As a rough formula:

```
Memory (GB) = 2 + (LoC / 100K × 3)
```

**Example:** 250K LoC → 2 + (2.5 × 3) = 9.5 GB

These are estimates. Real-world needs may vary based on code complexity and dependency depth. If using dynamic memory allocation, maintain an override mechanism for systems that consistently deviate from these guidelines.

### 2. Kubernetes (Node)

While Kubernetes itself has minimal requirements, worker nodes must be sized to support the workloads.

**Recommended baseline:**
- **CPU:** 4 vCPU
- **Memory:** 16 GB RAM
- **Storage:** 50 GB

This allows:
- Running multiple application pods
- Supporting high-memory and disk-intensive workloads such as importing jobs
- Storing container images and temporary files on the node

For clusters running only Sigrid application components (API/frontend), lower disk sizes may be sufficient. Actual sizing depends on whether CI/CD workloads or other applications share the same nodes.

Node sizing must account for the largest schedulable workload (e.g. CI jobs requiring up to 16 GB RAM), not just average application usage.

Analysis jobs run in CI/CD, not in the cluster, unless CI/CD runners are deployed in the same cluster.

#### Node Pool Sizing

For a typical enterprise deployment, start with 2 nodes of 8 vCPU / 32Gi RAM to cover services and typical import load. Add a third node if usage spikes during peak CI/CD activity.

**Import jobs** use 500m CPU and 5Gi memory each. Ten concurrent jobs require approximately 5 additional cores and 50Gi memory.

### 3. Application (Sigrid)

Resource requirements are defined per pod in the Helm configuration.
You can start with the defaults, but these can always be overridden.

- Memory request = memory limit for pods to prevent memory contention
- Changing CPU limits is not recommended, as they can have negative effects

The table below shows typical allocations for a two-replica setup:

| Service | Per replica (CPU / Memory) | × 2 replicas |
|---|---|---|
| nginx | 50m / 128Mi | 100m / 256Mi |
| auth-api | 500m / 2Gi | 1000m / 4Gi |
| sigrid-api | 500m / 3Gi | 1000m / 6Gi |
| inbound-api | 500m / 1Gi | 1000m / 2Gi |
| quality-model-service | 250m / 1Gi | 500m / 2Gi |
| ai-explanation-service | 100m / 1Gi | 200m / 2Gi |
| redis-ha (3 pods) | ~100m / 512Mi | 300m / 1.5Gi |
| **Services total** | | **~4 cores / ~18Gi** |

Example Helm configuration:

{% raw %}
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
```
{% endraw %}

### 4. PostgreSQL

- **Compute:** 4-8 vCores, 32Gi RAM for typical enterprise workloads
- **Connections:** `max_connections: 500` covers baseline traffic plus import spikes
- **Storage:** Start with 256Gi SSD with auto-increase enabled

### 5. Scaling Order

As usage grows, infrastructure components tend to reach capacity in the following order:

1. **Import job node pool**: first to feel pressure as more systems are onboarded and CI/CD pipelines run concurrently
2. **sigrid-api**: read traffic grows with user count and dashboard usage; HPA on CPU handles this well
3. **PostgreSQL**: connection count and throughput become bottlenecks before compute does

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

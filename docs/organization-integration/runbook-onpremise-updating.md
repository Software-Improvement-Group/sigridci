# Runbook: Sigrid On-Premise Updating

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This documentation provides guidance on how to keep on-premise Sigrid up-to-date, serving as a helpful starting point.

<sig-toc></sig-toc>

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation
- You have a running Sigrid Deployment
- You have access to Software Improvement Group DockerHub

## Update Frequency

We update container images daily for immediate improvements. The Helm chart is updated less frequently, only when new features or significant changes are released. This ensures you get rapid updates while maintaining chart stability.

- Sigrid Docker containers: Monthly at minimum, ideally with each release.
- Sigrid Helm chart: Quarterly, or whenever a new version is available.

## Update Instructions

1. Pull the latest Docker containers:
```bash
   INTERNAL_REGISTRY_BASE=<REPLACE-WITH-REGISTRY>
   VERSION=<REPLACE-WITH-LATEST-VERSION> # e.g. `1.0.20250206`

   for IMAGE in ai-explanation-service auth-api-db-migration auth-api quality-model-service \
            sigrid-api-db-migration sigrid-api sigrid-frontend sigrid-multi-analyzer \
            sigrid-multi-importer survey-service; do
     docker pull softwareimprovementgroup/${IMAGE}:${VERSION}
     docker tag softwareimprovementgroup/${IMAGE}:${VERSION} ${INTERNAL_REGISTRY_BASE}/softwareimprovementgroup/${IMAGE}:${VERSION}
     docker push ${INTERNAL_REGISTRY_BASE}/${IMAGE}:${VERSION}
   done
```

2. Pull the latest Helm chart:

```bash
   helm pull oci://registry-1.docker.io/softwareimprovementgroup/sigrid-stack --version <latest tag>
```

3. Update the `ImageTag` in the global section of the Helm chart's values file (usually `custom-values.yaml`):

```bash
   global:
     ImageTag: "<REPLACE-WITH-LATEST-VERSION>"
```

4. Apply the updates using Helm:

```bash
   helm upgrade --install sigrid-onprem ./sigrid-stack -n sigrid --values ./sigrid-stack/custom-values.yaml
```

## Test Instructions

1. After updating, verify that all pods are running:
2. Check the logs of key services for any errors
3. Access the Sigrid frontend and perform basic operations to ensure functionality.
4. Run a test analysis on a sample project to verify the entire pipeline is working correctly.
If any issues are encountered during testing, consider rolling back to the previous version and contacting support.

## Additional System Maintenance

In addition to updating Sigrid components, it's important to maintain other systems that Sigrid depends on:

- PostgreSQL: Ensure that your PostgreSQL database is regularly updated and maintained. Keep the PostgreSQL version within the latest two supported major versions.
- Other (e.g., GitLab): Regularly update and maintain your supporting systems.

The update frequency for these systems should be determined based on your organization's needs and policies. However, it's crucial to keep these systems up-to-date to ensure optimal performance, security, and compatibility with Sigrid.

Note: Specific update instructions for PostgreSQL and and other systems are not provided here, as they can vary depending on your setup and chosen systems. Please refer to the official documentation of these systems for proper update procedures.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

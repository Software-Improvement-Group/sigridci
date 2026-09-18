# Sigrid MCP server for Sigrid On-Premise

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

The [Sigrid MCP server](../integrations/integration-sigrid-mcp.md) lets AI coding assistants use Sigrid's analysis while developers work. On Sigrid On-Premise it runs inside your own cluster as an optional service. Unlike the other optional components, such as the LDAP group sync and the Open Source Health knowledge base updater, which are jobs, the MCP server is a long-running service with its own `mcp` subchart in `sigrid-stack`.

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- Sigrid On-Premise is installed and working, using the `sigrid-stack` Helm chart version 1.0.20260917 or later.
- Your Sigrid license includes the Sigrid MCP server.

The MCP server runs from the `sigrid-multi-analyzer` image, so no additional container image is needed.

## Enabling the MCP server

The MCP server is disabled by default. The minimal configuration to enable it is shown below. The MCP server validates Sigrid tokens with `auth-api` and retrieves data from `sigrid-api`, both via their cluster-internal service names. These are prefixed with your Helm release name, `sigrid-onprem` in this example. The server is exposed on the same host as Sigrid, under the `/mcp` path.

{% raw %}
```yaml
mcp:
  enabled: true
  env:
    # A list in your values file replaces the chart's default list, so the defaults are repeated here.
    - name: JAVA_TOOL_OPTIONS
      value: -Djava.security.egd=file:/dev/urandom -XX:MaxRAMPercentage=80.0 -Djava.io.tmpdir=/data
    - name: TMPDIR
      value: /data
    - name: TPF_PARALLEL_ANALYSIS
      value: "1"
    - name: MATOMO_BASE_URL
      value: "disabled"
    - name: JWKS_URI
      value: http://sigrid-onprem-auth-api/oauth2/jwks
    - name: SIGRID_API_BASE_URL
      value: http://sigrid-onprem-sigrid-api/api/v1
  ingress:
    className: "nginx"  # Use the same ingress controller as the other Sigrid services
    hosts:
      - host: "my-sigrid.example.com"
        paths:
          - path: /mcp
    tls:
      - secretName: my-sigrid-tls
        hosts:
          - "my-sigrid.example.com"
```
{% endraw %}

The subchart requests 7 CPU and 28Gi memory per replica by default. Lower `mcp.resources` if your node pool cannot accommodate this, keeping in mind that the MCP server runs Sigrid analyses on code sent by the assistant, so it needs memory comparable to an analysis job.

By default the subchart also creates a NetworkPolicy that limits egress to `auth-api` and `sigrid-api`, and a HorizontalPodAutoscaler that needs the Kubernetes metrics API. Set `mcp.networkPolicy.enabled: false` or `mcp.autoscaling.enabled: false` if your cluster does not support these.

## Connecting an AI coding assistant

After the `mcp` pod is running, developers connect their AI coding assistant to `https://my-sigrid.example.com/mcp` using an [authentication token](authentication-tokens.md) from your on-premise Sigrid. The [Sigrid MCP Integrations](../integrations/integration-sigrid-mcp.md#sigrid-on-premise) page lists the configuration per IDE.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

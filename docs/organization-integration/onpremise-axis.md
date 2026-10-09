# Sigrid Axis for Sigrid On-Premise

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation, in particular [Kubernetes Deployment](onpremise-kubernetes.md).
- Sigrid On-Premise is installed and working, using the `sigrid-stack` Helm chart version 1.0.20261012 or later.
- Your Sigrid license includes Sigrid Axis.

## Enabling Sigrid Axis

Sigrid Axis is the frontend for agentic tooling: AI coding assistants use it to consult and improve your systems using Sigrid's analysis. See [the general Sigrid Axis documentation](../axis/README.md) for what Axis offers and how developers connect their tools. This page covers deploying the Axis components in your own cluster. It is disabled by default and enabled as its own subchart in `sigrid-stack`. The minimal configuration is shown below.

{% raw %}
```yaml
sigrid-axis-frontend:
  enabled: true
  image:
    repository: softwareimprovementgroup/sigrid-axis/frontend
    tag: 1.0.20261012 # e.g. use Renovate to update this tag regularly
  ingress:
    enabled: true
    className: "nginx"  # Use the same ingress controller as the other Sigrid services
    annotations: { }  # Specify any ingress controller-specific annotations you need
    hosts:
      - host: "axis.example.com"
        tls:
          enabled: true
    extraPaths:
      - path: /rest  # Transparently reach Sigrid's backend APIs even though the host is different
        serviceName: my-sigrid-sigrid-stack-nginx  # <release-name>-sigrid-stack-nginx
```
{% endraw %}

The image is pulled from our Elastic Container Registry. See [using SIG's Elastic Container Registry](onpremise-aws-ecr.md) for the registry configuration.
{: .attention }

Axis requires its own host name, as in the example above. It cannot be served under a path of your existing Sigrid host, because Axis serves its frontend from `/` of its host.
{: .attention }

## Logging in to Sigrid Axis

Axis uses the same identity provider and OpenID Connect client as Sigrid, as configured in [Kubernetes Deployment](onpremise-kubernetes.md). Because Axis runs on its own host, it needs its own login callback. Register the Axis host as an additional registration in the `auth-api` configuration:

{% raw %}
```yaml
auth-api:
  config:
    oauth2:
      registration:
        sigridmfa:
          additionalRegistrations:
            sigrid-axis: "axis.example.com"
```
{% endraw %}

The label (`sigrid-axis` in the example) can be anything you like. Each host gets its own registration named `sigridmfa-` followed by the host name with dots replaced by dashes. This makes sure users return to Axis after logging in, instead of to Sigrid.

You also need to allow the Axis callback URL as an additional redirect URI of the OpenID Connect client in your identity provider. The callback URL follows the pattern `https://<host>/rest/auth/login/oauth2/code/sigridmfa-<host with dots replaced by dashes>`. For the example above, this is `https://axis.example.com/rest/auth/login/oauth2/code/sigridmfa-axis-example-com`.
{: .attention }

## The Axis metrics aggregator

Sigrid Axis shows weekly trends based on aggregated metrics. These metrics are aggregated by a **cronjob** in the `sigrid-stack` chart, which replaces the job that runs on [Sigrid SaaS](https://sigrid-says.com) in Airflow.

The cronjob is **enabled automatically when the Axis frontend is enabled**, and cannot run without it. No configuration is required: it connects to your PostgreSQL database as the same `import_user` used by the import jobs, reusing the secret from [the import job's PostgreSQL configuration](onpremise-kubernetes.md).

Each run aggregates the most recent weeks for all systems, and the current week is re-measured on every run. Results are stored in the `axis_metrics` schema of your `sigriddb` database.

### Optional configuration

The defaults are suitable for most deployments. The following settings can be overridden in the `global.onPremise.axisMetricsAggregator` section:

{% raw %}
```yaml
global:
  onPremise:
    axisMetricsAggregator:
      image:
        tag: 1.0.20261012 # e.g. use Renovate to update this tag regularly
      cronJobschedule: "0 2-5 * * *" # hourly between 02:00 and 05:00 UTC by default
      activeDeadlineSeconds: 3600 # maximum duration of a single run in seconds
      resources:
        requests:
          cpu: 1000m
          memory: 4Gi
        limits:
          memory: 4Gi
```
{% endraw %}

- `cronJobschedule` — the cron format schedule of the job. The default `"0 2-5 * * *"` triggers hourly during the night, which spreads the aggregation over a quiet period. A run that is skipped because the previous one is still active is picked up by the next trigger.
- `activeDeadlineSeconds` — how long a single run may take before Kubernetes cancels it. The default allows one hour.
- `resources` — the container's CPU request and memory. The default of 4Gi memory suffices for most deployments; lower it only if your node pool cannot accommodate it.

### Disabling the aggregator

Should you run into issues, for example with the container or the cronjob settings, you can disable the aggregator without disabling Axis itself:

{% raw %}
```yaml
global:
  onPremise:
    axisMetricsAggregator:
      enabled: false
```
{% endraw %}

The aggregator then stops running, and Axis will not receive updated weekly metrics until it is enabled again. Disabling it does not remove previously aggregated data.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
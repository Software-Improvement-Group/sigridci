# AI Explanation Service for Sigrid On-Premise

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

[Sigrid AI Explanations](../reference/ai-explanations.md) provide explanations of analysis findings directly in the Sigrid UI. In an on-premise deployment, these explanations are served by a dedicated, optional microservice, the **AI Explanation Service**, which runs inside your own cluster as part of the `sigrid-stack` Helm chart.

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- Sigrid On-Premise is installed and working.
- The `softwareimprovementgroup/ai-explanation-service` image is available in your image registry. It is part of the standard set of images listed in [Kubernetes deployment](onpremise-kubernetes.md#a-docker-image-registry), so no additional image is needed if you already pull the full set.

No additional license is needed: the AI Explanation Service serves static, pre-computed explanations that are included in standard Sigrid.

Unlike the other optional components, such as the Open Source Health knowledge base updater and the LDAP group sync, which are jobs, the AI Explanation Service is a long-running service with its own `ai-explanation-service` subchart in `sigrid-stack`.

## How it works

The AI Explanation Service does **not** contact any LLM, and does not require any outbound network access. It serves pre-computed explanations, which ship with the service. This means the service works out of the box in restricted and air-gapped environments.

## Enabling the AI Explanation Service

The service is disabled by default. The minimal configuration to enable it is shown below:

{% raw %}
```yaml
sigrid-stack:
  ai-explanation-service:
    enabled: true
    image:
      repository: softwareimprovementgroup/ai-explanation-service
      tag: 1.0.20260309
    config:
      secret:
        create: true
        data:
          username: "some-username"
          password: "S3cr3t"
```
{% endraw %}

Notes:

1. The image follows the same pattern as in the [OSH knowledge base updater](onpremise-osh-knowledgebase-updater.md): specify the `softwareimprovementgroup/ai-explanation-service` repository and pin a specific `image.tag` — the example shows a real tag from March 2026 — for instance using Renovate to update the tag regularly. The registry used is the same as for the other Sigrid images, as described in [Kubernetes deployment](onpremise-kubernetes.md#a-docker-image-registry).
2. The username and password in the secret are only used for authentication between `sigrid-api` and the AI Explanation Service. Their values are chosen by you; they only need to match on both sides, because the same secret is mounted by both services (see below).

As with all secrets in Sigrid's Helm chart, there are two ways to provide this secret: let the Helm chart create it (`secret.create: true` with inline `data`), or create it yourself and reference it (`secret.create: false` and `secret.secretName: "some-name"`). Referencing an existing secret is useful if you manage credentials with a secret management solution such as the External Secrets Operator:

{% raw %}
```yaml
sigrid-stack:
  ai-explanation-service:
    enabled: true
    config:
      secret:
        create: false
        secretName: sigrid-onprem-ai-explanation-service-config
```
{% endraw %}

The referenced secret needs to use the following keys:

{% raw %}
```yaml
username: "some-username"
password: "S3cr3t"
```
{% endraw %}

The username and password are only used for authentication between `sigrid-api` and the AI Explanation Service, and their values are chosen by you: they only need to match on both sides, because the same secret is mounted by both services.

If you do not specify a `secretName`, the Helm chart uses the default shared secret name, which is composed of the [Helm release name](https://helm.sh/docs/intro/using_helm/#helm-install) (the name passed to `helm install`, e.g. `sigrid-onprem`) followed by `ai-explanation-service-config`. If you prefer a different name for your own secret, that is fine, but you must then also point `sigrid-api` at it, so that both services mount the same secret:

{% raw %}
```yaml
sigrid-stack:
  ai-explanation-service:
    config:
      secret:
        create: false
        secretName: "my-own-name"
  sigrid-api:
    config:
      aiexplanationService:
        secretName: "my-own-name"
```
{% endraw %}

## Verification

After deploying, verify that the service is running and reachable (in the examples below, `sigrid` is the example namespace in which Sigrid is installed; substitute your own):

```
kubectl get pods -n sigrid -l app.kubernetes.io/name=ai-explanation-service
kubectl logs -n sigrid -l app.kubernetes.io/name=ai-explanation-service --tail=50
```

Inside the cluster, the service is reachable on `http://<release-name>-ai-explanation-service:8080`, e.g.:

```
kubectl exec -it deploy/sigrid-onprem-sigrid-api -n sigrid -- curl http://sigrid-onprem-ai-explanation-service:8080/health
```

In the Sigrid UI, AI Explanations appear alongside analysis findings once the service is enabled.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

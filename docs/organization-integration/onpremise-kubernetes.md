# Sigrid on-premise: Helm Chart configuration

This documentation is specific to the on-premise version of Sigrid. This does *not* apply to the software-as-a-service version of Sigrid, which can be accessed via [sigrid-says.com](https://sigrid-says.com) and is used by the vast majority of Sigrid users
{: .attention }

This documentation describes how to configure on-premise Sigrid, so you can deploy it into a user-provided Kubernetes cluster 
using a [Helm](https://helm.sh) chart provided by SIG. 

To use this Helm chart, it needs to be configured by providing your own `values.yaml`, as is typical 
for Helm. The current page describes how to deploy Sigrid on-premise in terms of the available 
configuration options in `values.yaml`. It is based on the `example-values.yaml` file available 
in the Helm chart, which provides examples of typical configuration values.

We strongly recommend to use the `example-values.yaml` file next to this documentation page, as 
the `example-values.yaml` file provides additional, important details.

Sigrid's Helm chart is distributed via a private Docker Hub registry, together with the Docker 
images that make up Sigrid, as described below. 

<sig-toc></sig-toc>

## Prerequisites

Sigrid requires:
- (A) A Docker image registry from which to pull the containers that constitute Sigrid.
- (B) A DNS (sub-)domain to run Sigrid on.
- (C) Access to two PostgreSQL databases (which would typically be hosted on the same PostgreSQL 
  cluster).
- (D) Access to an OpenID Connect identity provider.
- (E) Provide an RSA keypair for signing of unattended workflow tokens.
- (F) Access to an S3-compatible object store (e.g., Amazon's own S3 or [MinIO](https://min.io)).

Optional dependencies:
- (G) OAuth connection to one or more source code repositories (can be GitLab, GitHub, Azure 
  DevOps, or a combination).

## (A) Docker image registry

Sigrid consists of a number of Docker images, which the Software Improvement Group (SIG) 
distributes 
via [Docker Hub](https://hub.docker.com/u/softwareimprovementgroup). Upon becoming a SIG 
on-premise customer, users get credentials to access the private part of this registry.

It is possible to directly pull from this registry by specifying it globally:

```yaml
global:
  imageRegistry: "docker.io/softwareimprovementgroup"
  # Needed because hub.docker.com/u/softwareimprovementgroup is private:
  imagePullSecrets:
    - ...
```

The Helm chart gives precedence to the values for registry and repository set specifically for each
component and falls back to the global `imageRegistry` if needed. Keep in mind that some 
sub-charts behave in a different way, or do not honor `imageRegistry` at all. 

For air-gapped Sigrid on-premise deployments, images are typically pulled regularly to an 
internal image registry first; the (air-gapped) Kubernetes cluster then pulls from this registry.
In this case, it is best to point the global `imageRegistry` setting to the internal image registry.
It is, however, always possible to set the registry per component of Sigrid by using one or more 
of the following settings:
```yaml
sigrid-api:
  image:
    registry: "my-registry"
    repository: "alternative-image-name"
    tag: "some-tag"
```

Sigrid on-premise needs access to the following images published on [SIG's private Docker Hub]
(https://hub.docker.com/u/softwareimprovementgroup):
- `softwareimprovementgroup/sigrid-frontend`
- `softwareimprovementgroup/auth-api`
- `softwareimprovementgroup/auth-api-db-migration`
- `softwareimprovementgroup/sigrid-api`
- `softwareimprovementgroup/sigrid-api-db-migration`
- `softwareimprovementgroup/quality-model-service`
- `softwareimprovementgroup/survey-service`
- `softwareimprovementgroup/sigrid-multi-analysis-import`
- `softwareimprovementgroup/ai-explanation-service`

For the avoidance of doubt: the AI Explanation Service (last image in the list) does NOT contact 
any LLM by default. It just serves pre-computed explanations.

## (B) DNS (sub-)domain to run Sigrid on

Sigrid needs a (sub-)domain to run on, e.g. `sigrid.example.com`. This (sub-)domain needs to be 
configured using global configuration options:

```yaml
global:
  hosts:
    - host: "sigrid.example.com"
      tls:
        enabled: true
        secretName: "SOME-NAME"
```

In this fragment, `SOME-NAME` is the name of a Kubernetes secret containing the TLS certificate
of the provided (sub-)domain. The Helm chart creates one `Ingress` resource which routes traffic 
to a nginx deployment which routes traffic to the correct APIs. The configuration for this Ingress 
can be found at `nginx.ingress` where any needed annotations can be added, or the 
`IngressClass` can be set.

While technically, TLS can be disabled in the Helm chart, in practice it is required for any 
host except `localhost`. The reason is that Sigrid uses OAuth2 / OpenID Connect; the respective 
standards state that TLS is mandatory for all hosts except `localhost`. OAuth2/OpenID Connect 
compliant products typically follow this requirement. As a concrete example, several IdPs refuse 
to register callback URLs that do not start with `https` unless the host is `localhost` or `127.
0.0.1`.

## (C) PostgreSQL

Analysis results are stored in a PostgreSQL database server (or cluster in PostgreSQL terms), and
consequently, PostgreSQL is a non-optional dependency of Sigrid. Typically, deployments use a
PostgreSQL instance outside the Kubernetes cluster and consequently not managed by Helm. 

For Postgres, we support the latest 2 major versions. You can track the Postgres version 
history in [this overview](https://www.postgresql.org/support/versioning/).

This page assumes that a properly initialized PostgreSQL server is available and reachable from 
the Kubernetes cluster. In the Helm chart configuration, a number of mandatory settings need to be 
provided:
- The endpoint at which the PostgreSQL server is reachable. By default, Sigrid connects at 
  the standard port for PostgreSQL (5432).
- Passwords for various PostgreSQL users: `webapp_user`, `db_mgmt_user`, and `import_user`.

In PostgreSQL, users and roles are global at the PostgreSQL cluster (a.k.a. instance/server) 
level. The initialization script creates the following users and roles:
- `webapp_user`
- `db_mgmt_user`
- `import_user`
- `auth_db_webapp_user`
- `auth_db_mgmt_user`
- `import_user`
- `abstract_customer_role`

In addition, when first importing a system, Sigrid creates a role called `PARTNER_CUSTOMER_role`,
where `PARTNER` and `CUSTOMER` are placeholders for the configured partner and customer role. In 
case any of these users or roles already exists in the cluster, the initialization script or 
the first import fails.

Database users are created together with an initial database schema by initialization scripts 
provided by the Helm chart. The relevant files are `sigriddb-init` and `authdb-init`, and 
optionally `metricsuser-init`. They are present in the `sigrid-stack/files` directory of the 
Helm chart.

### Kubernetes secrets

Various parts of Sigrid need credentials to be able to connect to other parts. For instance,
several of the microservices need to be able to connect to a PostgreSQL instance. Sigrid's Helm
chart uses Kubernetes secrets for this, in the following way: the Helm chart can either create 
this secret, or use a reference to an existing secret created outside the chart.

A concrete example is provided in the next section.

### Configuring database access

One of the components that needs access to PostgreSQL is AuthAPI, which expects that it can get
database access credentials via a Kubernetes secret. One way to configure this is as follows:

```yaml
auth-api:
  config:
    datasource:
      data:
        url: "jdbc:postgresql://some.host/sigridauthdb"
        username: "webapp-user"
        password: "S3cr3t"
```

The above configuration results in the Helm chart rendering a Kubernetes secret containing the
JDBC connection string, username and password. Obviously, a `values.yaml` should not contain a 
cleartext password, typically setting the password interactively using the Helm CLI is preferred 
`helm install <name> <chart> --set auth-api.config.datasource.data.password="S3cr3t"`).

The other option is to create a Kubernetes secret elsewhere and reference it. Suppose the name of
this secret is `postgresql-sigridauthdb`, then the configuration is:

```yaml
auth-api:
  config:
    datasource:
      create: false
      secretName: postgresql-sigridauthdb
```

The secret created elsewhere needs to use the same keys as the secret that the Helm chart would 
create (in the above example: keys `url`, `username` and `password`). The `example-values.yaml` 
and Helm chart `values.yaml` contain the details for each secret.

## (D) Identity provider

The on-premise version of Sigrid only supports single-sign-on (SSO); it does not maintain users 
by itself. Hence, a connection to an identity provider (IdP) is mandatory and needs to be 
configured in the Helm chart.

The only supported protocol is OpenID Connect and consequently, it is best if an IdP compatible 
with OpenID Connect is available (e.g., [Okta](https://www.okta.com) or [Auth0](https://auth0.com)). 
While [Microsoft Entra](https://www.microsoft.com/en-us/security/business/microsoft-entra)
also supports OpenID Connect, it is currently not possible to connect to Microsoft Entra directly. 
Instead, a bridge needs to be used, such as [Keycloak](https://www.keycloak.org) or
[Dex](https://dexidp.io). The latter is provided by Sigrid's Helm chart as an option.

Note that for on-premise deployments, using SAML is only possible via a bridge such as [Dex]
(https://dexidp.io). Consequently, [SIG's documentation](usermanagement.md#2-using-single-sign-on-sso-with-an-identity-provider-idp) for connecting hosted Sigrid to an IdP 
does not apply.

Configuring an identity provider (IdP) is a two-step process:
1. Register an OpenID Connect client in the IdP.
2. Configure the client in Sigrid's Helm chart.

### Step 1: Register an OpenID Connect (OIDC) client in the IdP

We refer to the documentation of the IdP on how to register an OIDC client/app. This is often 
called "Add an OIDC application" or "Create an OIDC integration" in the documentation.

You typically need to provide a redirect URI (also called "login callback URL"). For on-premise 
Sigrid, this is _always_ `https://YOUR-DOMAIN.COM/rest/auth/login/oauth2/code/sigridmfa`, where 
`YOUR_DOMAIN.COM` is a placeholder for the (sub)domain on which the on-premise deployment of 
Sigrid will be hosted and configured as described in Section B in this document.

Registering an OpenID Connect client/app results in a client ID and client secret, which are 
generated by the IdP. We'll need those in the next step.

Note that many IdPs allow configuration of the information provided to clients in the OIDC identity token. Sigrid expects that this token reveals the email address, first name and last name of the user.

#### Step 2: Configure the client in Sigrid's Helm chart

For `auth-api`, the OIDC client needs to be configured. This is covered by 
the `oauth2` tree in `values.yaml`:

```yaml
global:
  hosts:
    - host: "my-sigrid.example.com"                            <-- Note 1
      tls:
        enabled: true
      
auth-api:
  config:
    oauth2:
      resourceServer:
        data:
          issuer-uri: "https://my-idp.example.com"             <-- Note 2
          jwk-set-uri: "https://my-idp.example.com/jwks.json"
      registration:
        sigridmfa:
          create: true                                         <-- Note 3
          data:
            client-id: "PASTE_HERE"                            <-- Note 4
            client-secret: "PASTE_HERE"
            scope: "openid,email,profile,groups"
      provider:
        sigridmfa:
          issuer-uri: "https://my-idp.example.com"
```

Notes:
1. The first `host` from `global.hosts` is used for the redirect URI: if the redirect URI isn't 
   overridden elsewhere in `values.yaml`, the redirect UIR is taken from this host. In the 
   example here, it would be https://my-sigrid.example.com/rest/auth/login/oauth2/code/sigridmfa.
2. These are obviously just examples. The issuer URI of many IdPs are not just a hostname, but 
   also include a path, e.g. `https://my-idp.example.com/oauth`. The `jwk-set-uri` doesn't 
   always end in `jwks.json`, but can be anything else e.g. `keys`.  
3. `create: true` indicates that the Helm chart will create a secret holding the client ID and 
   client secret. The alternative is to create a secret yourself, in which case you'd reference 
   the name of that secret here using `secretName`.
4. The client ID and secret provided by your IdP need to be pasted here.

## (E) Provide an RSA keypair for signing of unattended workflow tokens.

Sigrid provides a [public API](../integrations/sigrid-api-documentation.md) that allows access 
to Sigrid from scripts. This API is protected by personal access tokens that logged-in users can 
create in Sigrid's user interface. These tokens are called "unattended workflow tokens" (UWTs) 
in Sigrid.

UWTs are JSON web tokens and hence need to be signed. This means a keypair needs to be 
configured that Sigrid uses to sign UWTs. The steps are as follows:
1. Create a 2048-bit RSA keypair, for instance using OpenSSL. The key needs to be in PEM format 
   (this format is easy to recognize: it is an ASCII file starting with `-----BEGIN PRIVATE 
   KEY-----`). When using OpenSSL, the command is `openssl genrsa -out uwt_signing_key.pem 2048`.
2. Create a Kubernetes secret to hold this key. This secret needs to be an opaque secret with 
   two properties: `issuer-uri` (typically: `https://your-sigrid-domain`) and `private-key` (which 
   holds the keypair in PEM format created in step 1). 

As with all secrets in Sigrid's Helm chart, there are two ways to create this secret: create the 
secret yourself and reference it in your `values.yaml`, or let the Helm chart create it.

If you create the secret yourself, say with name `uwt-secret`, the configuration in your `values.
yaml` is:

```yaml
auth-api:
  config:
    unattendedWorkflowTokens:
      create: false
      secretName: "uwt-secret"
```

If you choose to let the Helm chart create the secret, the configuration in your `values.yaml` is:

```yaml
auth-api:
  config:
    unattendedWorkflowTokens:
      create: true
      data:
        issuer-uri: "https://my-sigrid.example.com/rest/auth"
        private-key: |
          -----BEGIN PRIVATE KEY-----
          MIIEvg ...
          (many lines omitted from the keypair created in step 1)  
          -----END PRIVATE KEY-----
```

## (F) Access to an S3-compatible object store

Access to an S3-compatible object store is mandatory for Sigrid, but only for the pipeline jobs 
that analyze systems and upload results to Sigrid. Hence, no S3 configuration is needed in the 
Helm chart.

## (G) Optional: connection to source code repositories

In on-premise deployments, source code analyzed by Sigrid is never copied over (uploaded) to 
Sigrid. Consequently, to view source code fragments in Sigrid's UI, Sigrid needs to be able to 
access the API of the code repository in which the code lives. This is best illustrated with an 
example. 

Sigrid can connect to GitLab, GitHub and Azure DevOps, each via OAuth2. This requires to first 
configure the code repository as an OAuth2 provider:
- For GitLab, see ["Configure GitLab as an OAuth 2.0 authentication identity provider"](https://docs.gitlab.com/ee/integration/oauth_provider.html).
- For GitHub, see ["Creating an OAuth app"](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app).
- For Azure DevOps, the modern way is via Microsoft Entra, see ["Quickstart: Register an application with the Microsoft identity platform"](https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app?tabs=certificate).

The newly created client registration can then be configured in the Helm chart like so:

```yaml
sigrid-api:
  config:
    repositories:
      enabled: true
      secret: true
      data:
        provider:
          gitlab-onprem-provider:
            issuer-uri: https://gitlab.your-domain.com              <-- Note 1
            base-url: https://gitlab.your-domain.com                <-- Note 2
            type: gitlab                                            <-- Note 3
        registration:
          gitlab-onprem-registration:
            client-id: SOME_ID                                      <-- Note 4
            client-secret: SOME_SECRET
            client-authentication-method: client_secret_post
            authorization-grant-type: authorization_code
            scope:
              - read_repository
            redirect-uri: https://sigrid.yourdomain.com/rest/analysis-results/repositories/login/oauth/code/gitlab-onprem
            provider: gitlab-onprem-provider                        <-- Note 5
```

Notes:
1. In this example, source code is stored in an on-premise Gitlab instance, which is the 
   provider in OAuth2 terms.
2. The base URL is used to access the API of the code repository. It is often, but not always, 
   equal to the issuer URI.
3. Must be `gitlab`, `github`, or `azure-devops`.
4. The client ID and secret are determined by the code repository, typically when creating the 
   registration. See for instance [the relevant GitLab documentation](https://docs.gitlab.com/ee/integration/oauth_provider.html).
5. Sigrid is registered as an OAuth2 client at the provider configured above with name 
   `gitlab-onprem`. 

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

# Sigrid on-premise: Helm Chart configuration

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
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

- `softwareimprovementgroup/ai-explanation-service`
- `softwareimprovementgroup/auth-api-db-migration`
- `softwareimprovementgroup/auth-api`
- `softwareimprovementgroup/quality-model-service`
- `softwareimprovementgroup/sigrid-api-db-migration`
- `softwareimprovementgroup/sigrid-api`
- `softwareimprovementgroup/sigrid-frontend`
- `softwareimprovementgroup/sigrid-multi-analyzer`
- `softwareimprovementgroup/sigrid-multi-importer`
- `softwareimprovementgroup/survey-service`

In addition, if your deployment is completely air-gapped, please ensure these public images are also published to your internal container registry.
- `nginxinc/nginx-unprivileged`
- `redis:7.2.4-alpine`
- `haproxy:2.9.4-alpine`

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

For PostgreSQL, we support the latest 2 major versions. You can track the Postgres version 
history in [this overview](https://www.postgresql.org/support/versioning/). While Sigrid is 
known to work on managed PostgreSQL (to be specific: on Amazon Web Services RDS), SIG only tests 
the Helm chart and this documentation against self-managed PostgreSQL.

It is the responsibility of the on-premise customer to initialize and manage PostgreSQL. The 
Helm chart (and this page) assumes that a properly initialized PostgreSQL server is available 
and reachable from the Kubernetes cluster. In the Helm chart configuration, a number of mandatory 
settings need to be provided:
- The endpoint at which the PostgreSQL server is reachable. By default, Sigrid connects at 
  the standard port for PostgreSQL (5432).
- Passwords for various PostgreSQL users: `webapp_user`, `db_mgmt_user`, and `import_user`.

The Helm charts provides SQL scripts to initialize the database. It is the responsibility of the 
on-premise customer to run these scripts (using `psql`). They are NOT executed by the Helm chart.
In case of managed PostgreSQL, these scripts might need to be adapted to take care of specifics 
of the managed PostgreSQL provider. The scripts are in the `sigrid-stack/files` directory, which 
can be obtained by pulling the Helm chart. The relevant files are `sigriddb-init` and `authdb-init`. 

IMPORTANT: When running the init scripts, take care to first replace the password placeholders with 
real passwords.

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

The on-premise version of Sigrid only supports single-sign-on (SSO); it does not maintain users by itself.
Therefore, a connection to an identity provider (IdP) is mandatory and needs to be configured in the Helm chart.

The only supported protocol for directly connecting to Sigrid is OpenID Connect.
Consequently, it is best if an IdP compatible with OpenID Connect is available (e.g., [Okta](https://www.okta.com), 
[Microsoft Entra](https://www.microsoft.com/en-us/security/business/microsoft-entra), or [Auth0](https://auth0.com)).
[SIG's documentation](usermanagement.md#2-using-single-sign-on-sso-with-an-identity-provider-idp) largely applies with exception of the redirect URI.

Note that for on-premise deployments, using LDAP or SAML is only possible via a bridge such as [Keycloak](https://www.keycloak.org) or
[Dex](https://dexidp.io). The latter is provided by Sigrid's Helm chart as an option.
Therefore, [SIG's documentation](usermanagement.md#2-using-single-sign-on-sso-with-an-identity-provider-idp) for connecting hosted Sigrid to an IdP does not apply.

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

Please note that many identity providers (IdPs) allow customization of the information included in the OpenID Connect (OIDC) identity token. Sigrid requires that this token contains the user's email address, first name, and last name.
If you are utilizing Dex as your IdP bridge, the redirect URI should be set to `https://YOUR-DOMAIN.COM/dex/oauth2/callback`.

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

#### Step 3: Bootstrap a Sigrid Admin

Sigrid limits which users have access to which systems. To be able to configure user permissions you will need a user 
that has the admin role. You can configure the first admin user by configuring the Helm chart:
```yaml
global:
  onPremise:
    administrators: 
      - "email@customer.com" 
```
Upon login the user with the matching email account will be granted the admin role. Once you have a user with the admin
role you will be able to use the Sigrid-UI to give grant other accounts the admin permission as well.

Please note that removing email addresses from this list does **NOT** remove the admin role. Use the standard user
management functionality of Sigrid to add/remove admin accounts after the initial setting up of Sigrid.

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

Sigrid uses an S3-compatible object store to transfer analysis results from CI/CD jobs to Sigrid.
Hence, access to an S3-compabible object store is mandatory. This might be Amazon's S3, or a 
compatible store such as [MinIO](https://min.io). Providing (access to) an object store is the 
responsibility of the on-premise customer; no object store is provided by the Helm chart.

In the Helm chart, two things need to be configured:
- (F.1) A secret to allow access to the object store.
- (F.2) Configuration for the Kubernetes jobs that import analysis results.

### (F.1) Secret to allow access to the object store

A secret for accessing the object store can be configured in the usual way:

```yaml
inbound-api:
  config:
    importJob:
      objectStoreSecret:
        create: true
        data:
          AWS_ENDPOINT_URL: "https://minio.my-company.com"
          AWS_FORCE_PATH_STYLE: true  # Do not use bucket-specific hostnames
          AWS_REGION: "eu-east-1"
          AWS_ACCESS_KEY_ID: ""
          AWS_SECRET_ACCESS_KEY: ""
```

As usual, the Helm chart creates the secret if you set `inbound-api.config.importJob.objectStoreSecret.create`
to true. Alternatively, you can provide the secret yourself, in which case the configuration should look like:

```yaml
inbound-api:
  config:
    importJob:
      objectStoreSecret:
        create: false
        secretName: "example name"
```

Note that this secret is not mandatory. In case authentication is already provided through other means (e.g. 
Pod/Workload Identity, IAM roles for service accounts, etc.), no secret is needed at all.

### (F.2) Configuration for the Kubernetes analysis results import jobs.

Sigrid creates [Kubernetes jobs](https://kubernetes.io/docs/concepts/workloads/controllers/job/) 
that import analysis results. These jobs read analysis results from the object store and store them 
in Sigrid's database. Several configuration parameters need to be provided. These jobs are 
created dynamically at runtime, by Sigrid itself (not by the Helm chart), whenever it receives a 
trigger from a CI/CD pipeline.

These jobs are created from a template that is configurable in the Helm chart, using the 
following configuration:

```yaml
inbound-api:
  config:
    importJob:
      serviceAccount:
        # -- Specifies whether a service account for import jobs should be created
        create: true
        # -- Annotations to add to the service account
        annotations: {}
        # -- The name of the service account to use.
        # If not set and create is true, a name is generated using the fullname template
        name: ""
      jobAnnotations: {}
      podAnnotations: {}
      retries: 3
      autoRemoveEnabled: true
      autoRemoveInterval: "60s"
      maxDuration: "3h"
      postgresSecret:
        create: true
        data:
          url: ""
          username: ""
          password: ""
```

With this configuration, whenever triggered, Sigrid tries 3 times to create a and successfully 
run an import job. Successful runs are automatically removed from the cluster 
(`autoRemoveEnabled: true`) after 60 seconds (`autoRemoveInterval: "60s"`). A job can run for at 
most 3 hours (`maxDuration: "3h"`). If needed, you can set annotations on the job resource, the 
pod resource for this job, or both. Finally, the Helm chart can create a service account 
(`serviceAccount.create: true`), or use an existing one (`serviceAccount.create: false`), in 
which case the name needs to be provided (`serviceAccount.name: "some name"`).

Last but not least, the import jobs need access to database `sigriddb`, with user `import_user`. 
The secret to hold credentials can either be created by the Helm chart (`postgresSecret.create: 
true`) or be provided externally (`postgresSecret.create: false` and `postgresSecret.secretName: 
"some name"`). Either way, it needs to be an opaque secret with entries `url`, `username`, and 
`password`.

#### (F.2.1) Optional: Configuring resource allocation for analysis results import jobs

The kubernetes jobs that Sigrid creates have no default resource (cpu/memory) requests/limits. To ensure the healthy 
operating of import jobs we recommend to set default resource requests/limit and create overrides on a per-system basis
as needed.

Sigrid offers three ways to configure resource requests/limits:
1. **Default resources**: Default resource requests/limits set on all jobs.
2. **System resources**: Resource requests/limits set only for jobs of a matching system.
3. **Dynamic resources**: Resource requests/limits set through the API when triggering an analysis results import. 

Method 1 and method 2 can be configured by admins using the Helm chart when installing or upgrading Sigrid:
```yaml
inbound-api:
  config:
    importJob:
      # -- Default resources allocated to import jobs
      defaultResources:
        requests:
          cpu: 500m
          memory: 5Gi
        limits:
          memory: 5Gi
      # -- Per system overrides for resource allocation.
      systemResources:
        company-system: # Format {customer}-{system name}
          requests:
            cpu: 1000m
            memory: 10Gi
          limits:
            memory: 10Gi
        company-system-2:
          requests:
            cpu: 1000m
            memory: 15Gi
          limits:
            memory: 15Gi
```
Sigrid performs a merge overwrite on resources which means that system specific resource requests/limits 
are merged with the defaults and overwrite any already present cpu/memory requests/limits.

Method 3 reduces the need for an admin to set system specific overwrites but must be explicitly enabled. To prevent
runaway resource consumption a maximum amount of cpu/memory that is requested through the API can be configured.
```yaml
inbound-api:
  config:
    importJob:
      # -- When set to true allows resource allocation overrides to be sent through the API. This feature allows users to
      # dynamically specify resource allocation instead of needing admins to update systemResources/defaultResources.
      allowResourceOverride: true
      # -- Maximum resource quantities that are allowed to be set through the API.
      maxResourceOverride:
        cpu: 1000m
        memory: 10Gi
```
In the above example no more than `1000m` cpu and `10Gi` memory may be dynamically allocated using the API. The values 
are used for both cpu/memory requests and cpu/memory limits.

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

# Runbook: Sigrid On-Premise Installation

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This documentation provides guidance on how to begin configuring on-premise Sigrid, serving as a helpful starting point.

<sig-toc></sig-toc>

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- You have access to Software Improvement Group DockerHub.

## Prepare for installation 

### (A) Prepare container images 

1. Get access to DockerHub from SIG.
   - Please ask your SIG Project Lead/contact person.
   - Provide an email address.
   - An existing DockerHub account will be invited or a new one created.
2. To log in to DockerHub as a Helm registry and pull the Helm chart, you need to create a Personal Access Token.
3. If your deployment is entirely air-gapped please perform the next two steps, otherwise you can continue at "Prepare helm chart".
4. Pull all container images required:

   from https://hub.docker.com/orgs/softwareimprovementgroup/repositories:
     - softwareimprovementgroup/ai-explanation-service
     - softwareimprovementgroup/auth-api-db-migration
     - softwareimprovementgroup/auth-api
     - softwareimprovementgroup/quality-model-service
     - softwareimprovementgroup/sigrid-api-db-migration
     - softwareimprovementgroup/sigrid-api
     - softwareimprovementgroup/sigrid-frontend
     - softwareimprovementgroup/sigrid-multi-analyzer
     - softwareimprovementgroup/sigrid-multi-importer
     - softwareimprovementgroup/survey-service  

   and the following public images:
     - nginxinc/nginx-unprivileged
     - redis:7.2.4-alpine
     - haproxy:2.9.4-alpine
5. Tag the downloaded containers with their tag from DockerHub (e.g. 1.0.2025013).
6. Re-tag and push the containers to your internal container registry.

### (A) Prepare helm chart 

1. Helm Login: `helm registry login registry-1.docker.io -u <username> -p <personal_access_token>`
2. Pull the latest helm chart: `helm pull oci://registry-1.docker.io/softwareimprovementgroup/sigrid-stack --version <latest tag>`
3. Store the helm chart under your version control making sure not to use clear text secrets, certificates and passwords in your helm.
4. Use Kubernetes-native secrets, either managed directly in Kubernetes or via an external tool that creates and updates these secret objects.

### (B) Prepare DNS (sub)domain

1. Create a (sub)domain to use for your Sigrid deployment.
2. Create a TLS certificate and store it securely in Kubernetes.

### (C) Prepare PostgreSQL

1. In the helm chart directory, there are two initialization scripts.
2. Using `psql`, run the two database initialization scripts that are found in sigrid-stack/files in the exact following order:
- sigriddb-init
- authdb-init
3. Replace passwords in the init scripts with ones you want to use and store them. You will need to provide them in the Helm charts at a later stage. 
4. Store the passwords securely in Kubernetes.

### (D) Prepare Identity Provider

When an OIDC compatible Identity Provider is available:
1. Create an OIDC integration in your Identity Provider.
2. Provide redirect URI (also called "login callback URL"). This is always `https://YOUR-SIGRID_DOMAIN.COM/rest/auth/login/oauth2/code/sigridmfa`, where `YOUR_SIGRID_DOMAIN.COM` is a placeholder for your (sub)domain on which the deployment of Sigrid will be hosted.
3. Create a secret and store it securely in Kubernetes.

### (E) Prepare an RSA keypair for the signing of UWT tokens

This part will soon become obsolete in a newer Sigrid release. 
1. Create a 2048-bit RSA keypair: `openssl genrsa -out uwt_signing_key.pem 2048`
2. Store the certificate securely in Kubernetes.

### (F) Prepare access to an S3-compatible object store 

1. Create a machine user in your object store.
2. Create an S3 bucket for importing analysis results.
3. Give the machine user access to read and write access to the bucket.
4. Store all relevant information in Kubernetes.

### (G) Optional: Prepare connection to source code repositories 

1. Register an OAUTH Application on every source code repository (server) you expect to connect to.
2. Store all relevant information in Kubernetes (client_id, client_secret).

## Sigrid Installation

### Create your deployment's values file

1. Your values file is a subset of the full helm chart. To make it manageable we've created an example-values.yaml which contains example values for everything that needs to be set.
2. Make a copy of example-values.yaml. E.g. custom-values.yaml.
3. Fill in the custom-values.yaml file.

Some sections of the values file are self-explanatory, while others may need additional context. Additionally, not all configurable values are included in the example. For a complete list of values that can be overridden, refer to the original Helm chart. 

Your copy of example-values.yaml however is enough to get a complete Sigrid deployment running. What do you need to know?

#### global:
```
ImageTag: "1.0.20250109"
```
Provide the tag of the containers you want to use.
It is important that the tag matches the tags used in Sigrid's Helm chart: all components of Sigrid must always use the same version.
```
onPremise: customer: "company"
```
Provide a technical shortname for your company/team.
This will eventually be displayed in the address bar of Sigrid like so `https://YOUR-SIGRID_DOMAIN.COM/company`. 
At a later stage, it needs to be provided as a "CUSTOMER" environment variable to the analysis job in your CI pipeline. 
```
onPremise: administrators: - admin@company.com
```
Provide an email address to bootstrap the very first user in Sigrid.
The email address should match the user's email in the connected IdP.
Note that this initial admin user will have full access to the entire portfolio. Once Sigrid is fully configured, you can invite another person as an Admin and, if desired, remove or demote the initial admin user to a regular user.
```
imagePullSecrets:
```
This only needs to be provided if your internal container registry requires authentication or if you’re pulling SIG containers from DockerHub directly. 

#### nginx:

If your deployment is air-gapped, adjust the values below.

```
image: registry: ""
image: repository: ""nginxinc/nginx-unprivileged""
```
 Provide full URL to your registry and container image.
```
image: tag: "mainline-alpine"
```
Provide the tag you used to push this image to your registry. 

#### auth-api:

These values can be retrieved using the GUI or .well-known endpoint of your IdP.

```
config.oauth2.resourceServer.data.issuer-uri: "https://my-idp.example.com" 
config.oauth2.resourceServer.data.jwk-set-uri: "https://my-idp.example.com/jwks.json 
config.oauth2.provider.sigridmfa.issuer-uri: "https://my-idp.example.com" 
```

#### sigrid-api:

No further context required.

inbound-api:

No further context required.

### *-service: 

The secrets provided below are configured to allow the Sigrid API to communicate with downstream APIs. If these secrets are modified, please ensure that they are updated across all three services, as they are associated with a single user.

```
config: secret: data: username: "example"
config: secret: data: password: "example" 
```

#### config.redis:

The secrets provided below are configured to allow Sigrid to communicate with Redis. 
They will work as is but can be modified.

```
redis: data: password: "example-password" 
redis: data: sentinel-password: "example-password" 
```
If you want to use the use a self-provided redis server, also adjust host: ""

## Install helm chart
We assume that your Kubernetes cluster is ready and that you have created a namespace. There are several ways to install a Helm chart. One common method is as follows: `helm upgrade --install <deployment-name> <helm-chart-path> -n <namespace> --values <values-file-path>`

For example, to install the Sigrid deployment, you can use: `helm upgrade --install sigrid-onprem ./sigrid-stack -n sigrid --values ./sigrid-stack/custom-values.yaml`

## Check your Deployment
In the unlikely event that the custom values file is filled in correctly the very first time, then proceed to "Setup a test analysis pipeline"

- Monitor your deployment to see if any pods or services have problems starting
- If so, please tail the logs and see what’s going on.
- Remedy the error by adjusting the custom values file.

If you’re using command line to install the helm chart you can repeat the command from earlier.

Once your deployment is running the ‘administrator’ provided in your custom-values should be able to login to Sigrid.

You can now start inviting more people to Sigrid if so desired.

## Setup a test analysis pipeline

### Create a Sigrid Token

- Login to Sigrid.
- Under User Settings, create a Sigrid Token.

### Setup your project
...

### Verify a succesful analysis

- Monitor any importer pods on your deployment, once it’s finished the analysis and import to Sigrid is done.
- Login to Sigrid and verify you can now see a system.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

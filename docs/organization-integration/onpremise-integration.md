# Sigrid on-premise integration

Most of this documentation refers to the software-as-a-service version of Sigrid, which can be accessed via [sigrid-says.com](https://sigrid-says.com) and is used by the vast majority of Sigrid users. However, SIG also offers an on-premise version of Sigrid. This document covers everything you need to integrate Sigrid on-premise in your environment. It also covers the functional differences between the SaaS version and the on-premise version, though these differences are relatively minor.

<sig-toc></sig-toc>

## High-level overview

From a deployment perspective, on-premise Sigrid consists of two "parts":

- **Sigrid** is the Sigrid web application, which you access from your browser.
- **Sigrid CI** runs within your development platform (e.g. GitHub). It performs the analyses and then publishes the results to Sigrid.

<img src="../images/onpremise-overview.png" width="600" />

- Sigrid on-premise is based on [Docker containers](https://en.wikipedia.org/wiki/Docker_%28software%29). There are two types of containers:
  - Application containers that should be deployed permanently in a [Kubernetes](https://en.wikipedia.org/wiki/Kubernetes) cluster, based on a [Helm chart](https://helm.sh) that is provided by SIG.
  - Analysis containers that run from a build pipeline within your development platform. These analysis containers may also be started on Kubernetes, but that is not a requirement. Supported development platforms are listed in [development platform integration](#development-platform-integration).
- SIG provides the necessary images through a container registry. The section [obtaining Sigrid on-premise](#obtaining-sigrid-on-premise) contains more information on how you can obtain and update these Docker containers.
- Authentication is based on your identity provider, using [OpenID Connect](https://openid.net/developers/how-connect-works/). Alternatively, [SAML](https://en.wikipedia.org/wiki/SAML_2.0) or [LDAP](https://en.wikipedia.org/wiki/Lightweight_Directory_Access_Protocol) are also supported, through [Dex](https://dexidp.io/).
- Analyses are triggered from a build pipeline. The analysis results are then imported into a Postgres database, so they can be viewed in Sigrid.
- Large files are stored in an [S3-compatible object store](https://aws.amazon.com/s3/).

Some Sigrid on-premise features are *optional*:

- The Open Source Health feature requires outbound internet access. Sigrid needs to connect to external sources to check for the latest vulnerability data for open source libraries. If you do not allow outbound internet access, the Open Source Health feature is not available. The rest of Sigrid is unaffected.
- When viewing detailed analysis results, Sigrid displays relevant source code files within Sigrid. For this to work, a web-accessible code storage needs to be available. This integrates with Sigrid via [OAuth](https://oauth.net/2/). For this to work, the identity provider used for Sigrid authentication and for the code storage needs to be the same. For viewing source code within Sigrid, you need to provide a development platform that is integrated with the same identity provider as Sigrid itself. The view source functionality is optional, without this integration the rest of Sigrid is unaffected.

## Obtaining Sigrid on-premise

The Docker containers that form Sigrid on-premise are distributed via [DockerHub](https://hub.docker.com). You will receive an account that allows you to access the container registry. 

<img src="../images/onpremise-dockerhub.png" width="500" /> 

As explained above, Sigrid consists of several Docker containers. The container `sigrid-multi-analysis-import` will run directly in your development platform's continuous integration pipelines, all other containers are deployed to your Kubernetes cluster. These steps are explained in more detail in the following sections.

### Updating Sigrid on-premise to a new version

SIG releases the Sigrid Docker containers based on a [continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery) process. This means that changes are immediately released once they have successfully passed through the development process. We advise our clients on the best way to develop and operate their software, so we try to adhere to the same best practices that we recommend our clients. 

This does not necessarily mean you need to *immediately* pull the Docker containers after every release. However, you need to pull the latest versions of the Docker containers at least once a month. SIG does not provide support for versions of the Docker containers over a month old. Updating frequently reduces the "delta" between the current version and the new version, thereby reducing update risk. Once a month is merely the *minimum* update frequency, we actually recommend you update as frequently as possible.

Although Sigrid consists of several Docker containers, you will need to update them collectively. It is theoretically possible to update some containers without updating other containers, but this gets complicated very quickly and we don't recommend this way of working to our on-premise clients. So when you update Sigrid on-premise, you will need to update all Docker containers to the same version.

This also means SIG does not back-port any changes to older versions: If you want to access new features or bugfixes, you will need to update the Docker containers to the latest version. 

### Updating your environment

In addition to updating Sigrid itself, you will also need to periodicially update your environment in which Sigrid runs. SIG uses the following support policy for infrastructure component versions:

- For Kubernetes, we support the latest 2 major versions. You can track the Kubernetes version history in [this overview](https://kubernetes.io/releases/).
- For Postgres, we also support the latest 2 major versions. You can track the Postgres version history in [this overview](https://www.postgresql.org/support/versioning/).

## Deploying Sigrid into a Kubernetes cluster

SIG will provide you with a [Helm Chart](https://helm.sh) to configure and install Sigrid on-premise. A Postgres database needs to be set up separately.

## Identity provider integration

Sigrid on-premise integrates with your identity provider through [OpenID Connect](https://openid.net/developers/how-connect-works/). You can either use an identity provider that "natively" supports OpenID Connect, or you can use middleware like [Dex](https://dexidp.io) that allows your identity provider to integrate with other systems. The installation of Dex is an optional feature of the Sigrid Helm chart. Alternatively, [KeyCloak](https://www.keycloak.org) can also be used to connect Sigrid to different identity providers, however this should be installed separately.

Locate the `sigrid-stack.auth-api` section in your Helm Chart's `values.yaml` file. Update the configuration properties so that they refer to your identity provider. 

## Development platform integration

In the on-premise version of Sigrid CI, the analysis runs as part of your continuous integration pipeline. The instructions for Sigrid CI depend on your development platform, and are virtually identical to the "normal" Sigrid CI instructions in this documentation. The key change is that you will need the `sigrid-multi-analysis-import` Docker container instead of the "normal" `sigrid-ci` Docker container.

## Functional/technical differences in Sigrid on-premise

- The on-premise Sigrid distribution is single tenant. You cannot create your own "tenants", all systems and analyses will end up in your portfolio. That said, you can still use Sigrid’s user management to define which people should have access to which systems.
- You are required to use the [development platform integration](#development-platform-integration) to publish your source code to Sigrid. SFTP uploads and manual uploads are not supported.
- [Multi-repo systems](systems.md#sigrid-view-is-based-on-business-applications) are not supported. You are responsible for publishing source code from your development platform to Sigrid.
- The on-premise Sigrid distribution does not support scheduling. It is assumed that analyses are performed from your continuous integration pipeline.
- The "view source" feature will show the *current* state of the file in your development platform, which might be different from the version of the file that was analyzed by Sigrid.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

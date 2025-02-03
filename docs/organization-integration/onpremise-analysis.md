# Sigrid on-premise: Analysis configuration

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

<sig-toc></sig-toc>

## Prerequisites

Your development platform will need access to the [Sigrid on-premise Docker containers](onpremise-integration.md#obtaining-sigrid-on-premise).

Each system to be analyzed needs an analysis configuration in the form of a file called
`sigrid.yaml` in the root directory of the system. Typically, this configuration is maintained by
the developers responsible for the system and consequently is not discussed here. Developers are
referred to the [analysis configuration reference](../reference/analysis-scope-configuration.md).

Sigrid's analyses require access to an S3-compatible object store. This can be Amazon's 
implementation, or an on-premise equivalent that supports Amazon's S3 API, such as [MinIO](https://min.io) or 
[Ceph](https://ceph.com).

Sigrid's analysis image includes [s5cmd](https://github.com/peak/s5cmd) to access 
the object store, which is based on the official Amazon S3 SDK. Because it is based on the 
official Amazon S3 SDK, it supports all authentication methods that Amazon provides. Typically, 
in a CI/CD environment, the AWS S3 SDK uses [environment variables](https://docs.aws.amazon.
com/cli/latest/userguide/cli-configure-envvars.html) 
to hold an access key. Consequently, typically the following environment variables need to be set:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ENDPOINT_URL` (when using a private S3-compatible object store)

## Configuring pipeline jobs

For on-premise solutions, we expect that source code is analyzed in a job in a CI/CD pipeline. 
In this document, we use GitLab as the example CI/CD environment. As analysis is based on a 
Docker image, any CI/CD environment that can run Docker containers will do.

The following GitLab job illustrates how to run an analysis:

```yaml
sigrid-publish:
  image:
    # Pulls from the private part of SIG's registry at Docker Hub; you may need to log in first, or replace this with the image name as cached in your internal registry:
    name: "softwareimprovementgroup/sigrid-multi-analyzer:1.0.20250123"
  variables:
    # These are all environment variables. For defaults, see the table below.
    # Note that typically, all environment variables marked as "shared" in the table
    # below would be set globally in the CI/CD environment:
    CUSTOMER: "company_name"
    SYSTEM: "$CI_PROJECT_NAME"
    SIGRID_URL: "https://sigrid.my-company.com"
    SIGRID_CI_TOKEN: "secret"
    BUCKET: "some-bucket"
    AWS_ENDPOINT_URL: "https://minio.my-company.com"
    AWS_ACCESS_KEY_ID: "some-id"
    AWS_SECRET_ACCESS_KEY: "also-secret"
    AWS_REGION: "us-east-1"
    SIGRID_SOURCES_REGISTRATION_ID: "gitlab-onprem"
  script:
    - "run-analyzers --publish"
```

Note that the image name contains an explicit Docker image tag (`1.0.20250123` in this example). 
It is important that the tag matches the tags used in Sigrid's Helm chart: all components of 
Sigrid must always use the same version. SIG recommends using an environment-wide variable 
instead of hardcoding the tag.

In GitLab, a CI/CD pipeline job with an `image` property starts the named Docker image, mounts a 
directory into it where it (automatically) checks out the source code of the current project, 
and runs the command(s) provided in the `script` tag. Other CI/CD environments provide a similar 
structure, although details may differ:
- Start a container.
- Ensure the source code of the project is available in it.
- Run the provided script inside the container (thus overriding the image entrypoint).

The `run-analyzers` script takes one optional command line parameter:
- `--publish`: run all analyses, persist analysis results in Sigrid, show analysis results on 
stdout and set exit code.
- `--publishonly`: run all analyses and persist analysis results in Sigrid.
- None: run analyses but do not persist analysis results (only show analysis results on stdout and
set exit code).

### Sigrid CI environment variables

Sigrid CI is configured with environment variables. The following table lists all 
environment variables with their defaults, if any. All that do not have a default value are
required. We distinguish two types of environment variables:
- Shared: these typically have the same value across different CI/CD projects for the same 
  Sigrid deployment. SIG recommends to configure these as variables managed by the CI/CD 
  environment (often called "secrets").
- Non-shared: these typically differ across projects.

| Variable                       | Shared? | Default   |
|--------------------------------|---------|-----------|
| CUSTOMER                       | Yes     |           |
| SYSTEM                         | No      |           |
| SIGRID_URL                     | Yes     |           |
| SIGRID_CI_TOKEN                | Yes     |           |
| BUCKET                         | Yes     |           |
| AWS_ENDPOINT_URL               | Yes     | (AWS)     |
| AWS_REGION                     | Yes     | us-east-1 |
| AWS_ACCESS_KEY_ID              | Yes     |           |
| AWS_SECRET_ACCESS_KEY          | Yes     |           |
| TARGET_QUALITY                 | No      | 3.5       |
| SIGRID_SOURCES_REGISTRATION_ID | Yes     | (auto)    |

Notes:
- `CUSTOMER`: this is the name of the Sigrid tenant as set in Sigrid's Helm chart when Sigrid was
  deployed. In Sigrid, this is always a lowercase string matching regex `[a-z][a-z0-9]`.
- `SYSTEM`: the name of this system (a lowercase string matching `[a-z][a-z0-9-]`). The default is 
  the project name of the current CI/CD project (e.g., the pre-configured `$CI_PROJECT_NAME` 
  variable in GitLab).
- `SIGRID_URL`: (sub-)domain where this Sigrid on-premise deployment is hosted, e.g. 
  `https://sigrid.mycompany.com`.
- `SIGRID_CI_TOKEN`: a personal access token created in Sigrid's UI.
- `BUCKET`: name of the bucket in which analysis results are stored.
- `AWS_ENDPOINT_URL`: URL at which an S3-compatible object store can be reached. Defaults to Amazon AWS 
  S3 endpoints.
- `AWS_REGION`: the region in which the bucket with name `S3_BUCKET` is located. For MinIO, this 
  is `us-east-1` unless a different region is configured in MinIO.
- `AWS_ACCESS_KEY_ID`: ID of the access key to authenticate to the S3-compatible object store. 
  This key should give access to the bucket named by `S3_BUCKET`.
- `AWS_SECRET_ACCESS_KEY`: the key whose ID is `AWS_ACCESS_KEY_ID`.
- `SIGRID_SOURCES_REGISTRATION_ID`: the ID of the OAuth client registration provided in `values.yaml` of Sigrid's Helm chart.

## Getting import job status and logs

When running an analysis in an on-premise deployment of Sigrid, from time to time it might be needed to inspect the status and/or logs of Kubernetes jobs started by Sigrid. There are three endpoints available for this purpose:

- `GET https://sigrid.your-domain.com/rest/inboundresults/imports/{partner}/{customer}/{system}`: returns an array of import jobs for the given system.
- `GET https://sigrid.your-domain.com/rest/inboundresults/imports/{partner}/{customer}/{system}/{job}`: returns the status of the given job ID.
- `GET https://sigrid.your-domain.com/rest/inboundresults/imports/{partner}/{customer}/{system}/{job}/logs`: returns the job logs of the given job ID (with Content-Type `text/plain`).

These endpoints are part of [Sigrid's external API](../integrations/sigrid-api-documentation.md), and consequently are called in the same way, using an [authentication tokens](../organization-integration/authentication-tokens.md) as bearer token.  

Assuming your token is stored in an environment variable called `SIGRID_CI_TOKEN`, the endpoint can be invoked using [`curl`](https://curl.se/) on Linux or MacOS like so:

```shell
curl -H "Authorization: Bearer $SIGRID_CI_TOKEN" https://sigrid.your-domain.com/rest/inboundresults/imports/{partner}/{customer}/{system}
```

where `{partner}`, `{customer}` and `{system}` are placeholders.

Or the equivalent for PowerShell:

```powershell
Invoke-RestMethod -Headers @{"Authorization" = "Bearer $Env:SIGRID_CI_TOKEN"} -Uri "https://sigrid-onprem.k8s.sig.eu/rest/inboundresults/imports/{partner}/{customer}/{system}" | Format-Table
```

The `GET /rest/inboundresults/imports/{partner}/{customer}/{system}` endpoint returns an array of job statuses for the given system, as JSON: 

<details markdown="1">
  <summary>Example response</summary>

```json
[
  {
    "name": "EXAMPLE-NAME",
    "status": "Failed",
    "creationTime": "2025-01-10T11:58:09Z",
    "startTime": "2025-01-10T11:58:09Z",
    "completed": 0,
    "running": 0,
    "ready": 0,
    "failed": 4,
    "conditions": [
      {
        "type": "Failed",
        "status": "True",
        "reason": "BackoffLimitExceeded",
        "message": "Job has reached the specified backoff limit",
        "lastProbeTime": "2025-01-10T12:01:13Z",
        "lastTransitionTime": "2025-01-10T12:01:13Z"
      }
    ]
  }
]
```

The `name` property of the `metadata` object is the name of the job that can be used to retrieve job details and logs with the `GET /rest/inboundresults/imports/{partner}/{customer}/{system}/{job}` endpoint and `GET /rest/inboundresults/imports/{partner}/{customer}/{system}/{job}/logs` endpoint. The endpoints discussed in this section are thin wrappers around the [equivalent endpoints of the Kubernetes API](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/#JobStatus), see the Kubernetes documentation for a detailed discussion of the response properties. 

</details>

The `GET /rest/inboundresults/imports/{partner}/{customer}/{system}/{job}` endpoint returns a job status object for the given job name, as JSON: 

<details markdown="1">
  <summary>Example response</summary>

```json
{
  "name": "EXAMPLE-NAME",
  "status": "Failed",
  "creationTime": "2025-01-10T11:58:09Z",
  "startTime": "2025-01-10T11:58:09Z",
  "completed": 0,
  "running": 0,
  "ready": 0,
  "failed": 4,
  "conditions": [
    {
      "type": "Failed",
      "status": "True",
      "reason": "BackoffLimitExceeded",
      "message": "Job has reached the specified backoff limit",
      "lastProbeTime": "2025-01-10T12:01:13Z",
      "lastTransitionTime": "2025-01-10T12:01:13Z"
    }
  ],
  "pods": [
    {
      "name": "EXAMPLE-NAME-POD-NAME",
      "status": "Failed",
      "creationTime": "2025-01-10T12:00:44Z",
      "startTime": "2025-01-10T12:00:44Z",
      "reason": null,
      "containerStatus": {
        "image": "docker.io/softwareimprovementgoup/sigrid-multi-importer:1.0.20250109",
        "imageID": "...",
        "name": "sigrid-importer",
        "ready": false,
        "started": false,
        "state": {
          "type": "terminated",
          "reason": "Error",
          "startedAt": "2025-01-10T12:00:45Z",
          "finishedAt": "2025-01-10T12:01:10Z",
          "exitCode": 1
        }
      },
      "conditions": [
        {
          "type": "PodReadyToStartContainers",
          "status": "False",
          "reason": null,
          "message": null,
          "lastProbeTime": null,
          "lastTransitionTime": "2025-01-10T12:01:12Z"
        },
        ...
      ]
    },
    ...
  ]
}
```

The endpoints discussed in this section are thin wrappers around the [equivalent endpoints of the Kubernetes API](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/#JobStatus), see the Kubernetes documentation for a detailed discussion of the response properties. 

</details>


## Manually publishing a system to Sigrid

It is also possible to *manually* start an analysis, and then publish the analysis results to Sigrid. You can use this option when your system doesn't have a pipeline, or when you need to import a system in Sigrid ad-hoc.

We recommend you integrate Sigrid CI into your pipeline. This ensures the results you see in Sigrid are always "live", since the analysis will run after every commit. It also allows for developers to receive Sigrid feedback directly in their pull requests. 
{: .warning }

You can run the analysis and publish the analysis results using the same Docker container. If you run Sigrid CI ad-hoc, you will still need to provide the [environment variables](#sigrid-ci-environment-variables). Since there are quite some environment variables, it's easiest to use Docker's `--env-file` option for this. This option is explained in the [Docker documentation](https://docs.docker.com/reference/cli/docker/container/run/).

The following example shows how to start an ad-hoc analysis for a system located in a local `/mysystem` directory:

    docker run \
      --env-file sigrid-ci-config.txt \
      -v /mysystem:/tmp/sources \
      -ti softwareimprovementgroup/sigrid-multi-analyzer:1.0.20250123 \
      --publish
      
This requires you to have access to the [Sigrid on-premise Docker containers](onpremise-integration.md#obtaining-sigrid-on-premise).
      
The version tag (`1.0.20250123`) should match your version of Sigrid on-premise. 

### Optional: connection to source code repositories
To set up the Helm charts, please follow the instructions provided [here](onpremise-kubernetes.md#g-optional-connection-to-source-code-repositories).

For manual system publishing, you need to supply additional environment variables beyond those mentioned [here](onpremise-analysis.md#sigrid-ci-environment-variables).

Please provide the following environment variables:

- **`SOURCES_API_BASE_URL`** (required):  
  Description: The entry point for the API of the source code repository.  
  Example: `https://github.example.com/api/v3` 
- **`SOURCES_PROJECT_SLUG`** (required):  
  Description: The project slug identifies your project within your CI/CD environment. It typically appears in URLs displayed in your browser, representing the part that follows the server address.   
  Example: `Software-Improvement-Group/sigridci`
- **`SOURCES_REF`** (optional):  
  Description: The branch name for the source view (defaults to 'main' if not provided).  
  Example: `patch_20250123`

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

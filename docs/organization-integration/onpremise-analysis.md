# Sigrid on-premise: Analysis configuration

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

Your development platform will need access to the [Sigrid On-Premise Docker containers](onpremise-integration.md#obtaining-sigrid-on-premise).

Each system to be analyzed requires an analysis configuration file named `sigrid.yaml` in the root directory. 
If no file is provided, this configuration is automatically generated (not stored in Sigrid or the pipeline). 
Creating a `sigrid.yaml` is only needed when developers want more control over the content of the analysis. 
Typically, this configuration is maintained by the developers responsible for the system. 
Developers can refer to the [analysis configuration reference](../reference/analysis-scope-configuration.md).

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
    # Pulls from the private part of SIG's AWS ECR registry; you may need to log in first, or replace this with the image name as cached in your internal registry:
    name: "571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:$SIGRID_VERSION"
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

Note that the image name contains a reference to the Docker image tag (`$SIGRID_VERSION` in this example). 
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

### Sigrid-Multi-Analyzer environment variables

Sigrid-Multi-Analyzer is configured with environment variables. The following table lists all 
environment variables with their defaults, if any. When provided with a default, you can override 
them, but you're not required to do so unless needed in your situation. All variables are required 
except `SIGRID_CA_CERT` and `AWS_CA_BUNDLE`, which are only required when using custom certificates 
for Sigrid and S3 bucket storage.

We distinguish two types of environment variables:
- Shared: these typically have the same value across different CI/CD projects for the same Sigrid 
  deployment. SIG recommends configuring these as variables managed by the CI/CD environment (often 
  called "secrets").
- Non-shared: these typically differ between projects and should be configured individually in each pipeline.

Using Shared Variables in Pipelines
- Using shared variables directly in the pipeline can be cumbersome.  
  It's easier to either store all shared variables at a higher level in your CI/CD project hierarchy or use a template for them and include it in your pipeline.  
  **Important:** Even when using templates, **do not put secrets in plain text**. Store sensitive values as project-level variables so they remain masked.  
  Only the `SYSTEM` variable needs to be defined in the project pipeline itself.

Example: Using a GitLab CI/CD template to store shared environment variables:
```yaml
variables:
  SYSTEM: "$CI_PROJECT_NAME"
include:
  - local: 'path/to/your/template.yml'
```

| Variable                       | Required | Shared? | Sensitive | Default   |
|--------------------------------|----------|---------|-----------|-----------|
| CUSTOMER                       | Yes      | Yes     | No        |           |
| SYSTEM                         | Yes      | No      | No        |           |
| SIGRID_CA_CERT                 | No       | Yes     | No        |           |
| SIGRID_URL                     | Yes      | Yes     | No        |           |
| SIGRID_CI_TOKEN                | Yes      | Yes     | Yes       |           |
| SIGRID_VERSION                 | Yes      | Yes     | No        |           |
| BUCKET                         | Yes      | Yes     | No        |           |
| AWS_ENDPOINT_URL               | Yes      | Yes     | No        | (AWS)     |
| AWS_REGION                     | Yes      | Yes     | No        | us-east-1 |
| AWS_ACCESS_KEY_ID              | Yes      | Yes     | Yes       |           |
| AWS_SECRET_ACCESS_KEY          | Yes      | Yes     | Yes       |           |
| AWS_CA_BUNDLE                  | No       | Yes     | No        |           |
| SIGRID_SOURCES_REGISTRATION_ID | Yes      | Yes     | No        | (auto)    |

Notes:
- `CUSTOMER`: this is the name of the Sigrid tenant as set in Sigrid's Helm chart when Sigrid was
  deployed. In Sigrid, this is always a lowercase string matching regex `[a-z][a-z0-9]`.
- `SYSTEM`: the name of this system (a lowercase string matching `[a-z][a-z0-9-]`). The default is 
  the project name of the current CI/CD project (e.g., the pre-configured `$CI_PROJECT_NAME` 
  variable in GitLab).
- `SIGRID_CA_CERT`: Path to Sigrid's certificate `my_sigrid_cert.pem`.
- `SIGRID_URL`: (sub-)domain where this Sigrid On-Premise deployment is hosted, e.g. 
  `https://sigrid.mycompany.com`.
- `SIGRID_CI_TOKEN`: a personal access token created in Sigrid's UI.
- `SIGRID_VERSION`: specifies the version tag of the Sigrid-Multi-Analyzer container.
  Ensure that the version matches the version used for the Sigrid web application you have deployed in Kubernetes.
- `BUCKET`: name of the bucket in which analysis results are stored.
- `AWS_ENDPOINT_URL`: URL at which an S3-compatible object store can be reached. Defaults to Amazon AWS 
  S3 endpoints.
- `AWS_REGION`: the region in which the bucket with name `S3_BUCKET` is located. For MinIO, this 
  is `us-east-1` unless a different region is configured in MinIO.
- `AWS_ACCESS_KEY_ID`: ID of the access key to authenticate to the S3-compatible object store. 
  This key should give access to the bucket named by `S3_BUCKET`.
- `AWS_SECRET_ACCESS_KEY`: the key whose ID is `AWS_ACCESS_KEY_ID`.
- `AWS_CA_BUNDLE`: Path to your S3 Bucket's certificate `my_s3bucket_cert.pem`.
- `SIGRID_SOURCES_REGISTRATION_ID`: the ID of the OAuth client registration provided in `values.yaml` of Sigrid's Helm chart.

#### Using Custom Certificates in Your Pipeline

To use custom certificates in your pipeline, copy them directly into the desired path, define them as string variables, or use CI/CD project variables, then pass their paths to the analyzer image. For example:

```yaml
sigrid-publish:
  image:
    name: "softwareimprovementgroup/sigrid-multi-analyzer:$SIGRID_VERSION"
  variables:
    SYSTEM: "$CI_PROJECT_NAME"
    SIGRID_CA_CERT: "my_sigrid_cert.pem"
    AWS_CA_BUNDLE: "my_s3bucket_cert.pem"
  script:
    - echo $MYSIGRID_CERT > $SIGRID_CA_CERT
    - echo $MY_S3_CERT > $AWS_CA_BUNDLE
    - "run-analyzers --publish"
```


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
        "image": "571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-importer:1.0.20260107",
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

We recommend you integrate Sigrid-Multi-Analyzer into your pipeline. This ensures the results you see in Sigrid are always "live", since the analysis will run after every commit. It also allows for developers to receive Sigrid feedback directly in their pull requests. 
{: .warning }

You can run the analysis and publish the analysis results using the same Docker container. If you run Sigrid-Multi-Analyzer ad-hoc, you will still need to provide the [Sigrid-Multi-Analyzer environment variables](#sigrid-multi-analyzer-environment-variables). Since there are quite some environment variables, it's easiest to use Docker's `--env-file` option for this. This option is explained in the [Docker documentation](https://docs.docker.com/reference/cli/docker/container/run/).

The following example shows how to start an ad-hoc analysis for a system located in a local `/mysystem` directory:

    docker run \
      --env-file sigrid-ci-config.txt \
      -v /mysystem:/tmp/sources \
      -ti softwareimprovementgroup/sigrid-multi-analyzer:$SIGRID_VERSION \
      --publish
      
This requires you to have access to the [Sigrid On-Premise Docker containers](onpremise-integration.md#obtaining-sigrid-on-premise).
      
The version tag (`$SIGRID_VERSION`) should match your version of Sigrid on-premise. 

### Optional: connection to source code repositories
To set up the Helm charts, please follow the instructions provided [here](onpremise-kubernetes.md#g-optional-connection-to-source-code-repositories).

> **Note:** The following environment variables are only required for manual system publishing and are not part of the standard Sigrid-Multi-Analyzer environment variable table above.  
> They are used to connect to external source code repositories when publishing a system manually.

For manual system publishing, you need to supply additional environment variables beyond those mentioned [here](onpremise-analysis.md#sigrid-multi-analyzer-environment-variables).

Please provide the following environment variables:

- **`SOURCES_API_BASE_URL`** (required, manual publishing only):  
  Description: The entry point for the API of the source code repository.  
  Example value: `https://github.example.com/api/v3` 
- **`SOURCES_PROJECT_SLUG`** (required, manual publishing only):  
  Description: The project slug identifies your project within your CI/CD environment. It typically appears in URLs displayed in your browser, representing the part that follows the server address.   
  Given the project's repository URL: `https://github.example.com/Software-Improvement-Group/sigridci`
  Example value: `Software-Improvement-Group/sigridci`
- **`SOURCES_REF`** (optional, manual publishing only):  
  Description: The branch name for the source view (defaults to 'main' if not provided).  
  Given the project's repository branch: https://github.example.com/api/v3/repos/Software-Improvement-Group/sigridci/branches/patch_20250123
  Example value: `patch_20250123`

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

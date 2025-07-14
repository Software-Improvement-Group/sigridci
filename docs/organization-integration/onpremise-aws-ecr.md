# Detailed instructions for accessing and using SIG's AWS ECR

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This documentation offers useful examples and context on how to use SIG's Elastic Container Registry, hosted on Amazon Web Services (AWS ECR).

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- You have access to Software Improvement Group [AWS ECR registry](571600876202.dkr.ecr.eu-central-1.amazonaws.com/).
- AWS CLI version 2.x. is available on the client that will pull be used to pull Sigrid's container images and helm chart.


## Logging in to AWS ECR and pulling the latest helm chart

The below script provides and example on how to authenticate and download the latest Sigrid Helm Chart from SIG's AWS ECR.

```bash
SIGRID_DOWNLOAD_REGION="eu-central-1"
SIGRID_DOWNLOAD_REGISTRY="571600876202.dkr.ecr.${SIGRID_DOWNLOAD_REGION}.amazonaws.com"
HELM_REPOSITORY_NAME="softwareimprovementgroup/sigrid-stack"
HELM_REPOSITORY_URI="${SIGRID_DOWNLOAD_REGISTRY}/${HELM_REPOSITORY_NAME}"
export AWS_ACCESS_KEY_ID="AKIAEXAMPLE" # Please replace with the one provided by SIG
export AWS_SECRET_ACCESS_KEY="EXAMPLESECRET" # Please replace with the one provided by SIG
aws ecr get-login-password --region $SIGRID_DOWNLOAD_REGION | docker login --username AWS --password-stdin $SIGRID_DOWNLOAD_REGISTRY
LATEST_TAG=$(aws ecr describe-images --repository-name $HELM_REPOSITORY_NAME --region $SIGRID_DOWNLOAD_REGION --query 'sort_by(imageDetails,&imagePushedAt)[-1].imageTags[0]' --output text)
helm pull oci://$HELM_REPOSITORY_URI --version $LATEST_TAG
```

## Using your own container registry

When this script is executed, it will pull the latest Sigrid images from the AWS ECR registry.
The script uses the AWS CLI to get a login password for the ECR registry and then logs in to the registry using Docker.
After that, it pulls the specified images with the given version.

```bash
SIGRID_DOWNLOAD_REGION="eu-central-1"
SIGRID_DOWNLOAD_REGISTRY="571600876202.dkr.ecr.${SIGRID_DOWNLOAD_REGION}.amazonaws.com"

export AWS_ACCESS_KEY_ID="AKIAEXAMPLE" # Please replace with the one provided by SIG
export AWS_SECRET_ACCESS_KEY="EXAMPLESECRET" # Please replace with the one provided by SIG

VERSION="1.0.20250603" # Please replace with the desired container image version
aws ecr get-login-password --region $SIGRID_DOWNLOAD_REGION | docker login --username AWS --password-stdin $SIGRID_DOWNLOAD_REGISTRY
IMAGES=(
  softwareimprovementgroup/ai-explanation-service
  softwareimprovementgroup/auth-api-db-migration
  softwareimprovementgroup/auth-api
  softwareimprovementgroup/quality-model-service
  softwareimprovementgroup/sigrid-api-db-migration
  softwareimprovementgroup/sigrid-api
  softwareimprovementgroup/sigrid-frontend
  softwareimprovementgroup/sigrid-multi-analyzer
  softwareimprovementgroup/sigrid-multi-importer
)
for IMAGE in "${IMAGES[@]}"; do
  docker pull $SIGRID_DOWNLOAD_REGISTRY/$IMAGE:$VERSION
done
```

## Pulling images directly from SIG's AWS ECR Registry using automated ECR login password refresh

AWS ECR passwords expire after 12 hours. Therefore, a scheduled refresh can be implemented for Sigrid On-Premises deployments. This approach automatically refreshes the ECR registry password to maintain continuous access to container images.

Note: this is only required when no internal container registry (cache) is used, or to automate the refreshing of images in your internal container registry.

Additional Prerequisites
- Access credentials for this user stored in a Kubernetes secret. e.g.`sig-customer-access-secret`
- Kubernetes cluster with RBAC enabled.

### Update your deployment's values file to enable the key rotation service

Add imagePullSecrets and ecrRepository into global.

```
global:
  
  imagePullSecrets:
    - name: sigrid-ecr-image-pull-secret

  onPremise:
    ecrRepository:
          enabled: true
          sigCustomerAccessSecret:
            data:
              AWS_ACCESS_KEY_ID: "AWS_ACCESS_KEY_ID"
              AWS_SECRET_ACCESS_KEY: "AWS_SECRET_ACCESS_KEY"
```
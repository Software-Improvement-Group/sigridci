# Detailed instructions for accessing SIG's AWS ECR

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This documentation offers useful examples and context on how to use SIG's AWS ECR.

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- You have access to Software Improvement Group [AWS ECR registry](https://571600876202.dkr.ecr.eu-central-1.amazonaws.com/).
- AWS CLI version 2.x. is available on the client that will pull be used to pull Sigrid's container images and helm chart.


## Logging in to AWS ECR and pulling the latest helm chart
<details>
<summary>Detailed description for pulling the latest helm chart</summary>

The below script provides and example on how to authenticate and download the latest Sigrid Helm Chart from SIG's AWS ECR.

```bash
SIGRID_DOWNLOAD_REGION="eu-central-1"
SIGRID_DOWNLOAD_REGISTRY="5012345678901.dkr.ecr.${SIGRID_DOWNLOAD_REGION}.amazonaws.com"
HELM_REPOSITORY_NAME="softwareimprovementgroup/sigrid-stack"
HELM_REPOSITORY_URI="${SIGRID_DOWNLOAD_REGISTRY}/${HELM_REPOSITORY_NAME}"
export AWS_ACCESS_KEY_ID="AKIAEXAMPLE" # Please replace with the one provided by SIG
export AWS_SECRET_ACCESS_KEY="EXAMPLESECRET" # Please replace with the one provided by SIG
aws ecr get-login-password --region $SIGRID_DOWNLOAD_REGION | docker login --username AWS --password-stdin $SIGRID_DOWNLOAD_REGISTRY
LATEST_TAG=$(aws ecr describe-images --repository-name $HELM_REPOSITORY_NAME --region $SIGRID_DOWNLOAD_REGION --query 'sort_by(imageDetails,&imagePushedAt)[-1].imageTags[0]' --output text)
helm pull oci://$HELM_REPOSITORY_URI --version $LATEST_TAG
```
</details>

## Using your own container registry

<details>
<summary>Detailed description for manually pulling the latest Sigrid container images</summary>

When this script is executed, it will pull the latest Sigrid images from the AWS ECR registry.
The script uses the AWS CLI to get a login password for the ECR registry and then logs in to the registry using Docker.
After that, it pulls the specified images with the given version.

```bash
SIGRID_DOWNLOAD_REGION=eu-central-1
SIGRID_DOWNLOAD_REGISTRY=5012345678901.dkr.ecr.${SIGRID_DOWNLOAD_REGION}.amazonaws.com
export AWS_ACCESS_KEY_ID="AKIAEXAMPLE" # Please replace with the one provided by SIG
export AWS_SECRET_ACCESS_KEY="EXAMPLESECRET" # Please replace with the one provided by SIG
VERSION=1.0.20250603 # Please replace with the desired container image version
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
</details>

## Pulling images directly from SIG's AWS ECR Registry using automated ECR login password refresh
<details>
<summary>Detailed procedure for automated AWS ECR login password refresh</summary>

AWS ECR passwords expire after 12 hours. Therefore, a scheduled refresh can be implemented for Sigrid On-Premises deployments. This approach automatically refreshes the ECR registry password to maintain continuous access to container images.

Note: this is only required when no internal container registry (cache) is used, or to automate the refreshing of images in your internal container registry.

Additional Prerequisites
- Access credentials for this user stored in a Kubernetes secret. e.g.`sig-customer-access-secret`
- Kubernetes cluster with RBAC enabled.

### Store AWS Credentials in Kubernetes
Create a Kubernetes secret with the IAM user's credentials.
For example, this can be done by using a YAML file and kubectl, but some Kubernetes cluster orchestration tools also allow you to create secrets via a GUI.
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: sig-customer-access-secret
  namespace: {{ .Release.Namespace }} # namespace where sigrid onprem is/will be deployed.
type: Opaque
data:
  AWS_ACCESS_KEY_ID: #provided by SIG
  AWS_SECRET_ACCESS_KEY: #provided by SIG
```

### Update your deployment's values file to enable the key rotation service
```
global:
  imagePullSecrets:
    - name: ecr-image-pull-secret

ecrRepository:
  enabled: true
  iamUserName: "sig_ecr_example_user"
  sigCustomerAccessSecretName: sig-customer-access-secret
```
</details>

## The AWS ECR key rotation service
<details>
<summary>Detailed description of the AWS ECR key rotation service</summary>

The ECR key rotation service serves to:

1. Generate temporary ECR authentication tokens periodically.
2. Create Kubernetes image pull secrets with these tokens.
3. Ensure continuous access to AWS ECR container repositories.

The ECR key rotation solution consists of several Kubernetes resources:

| Resource | Purpose |
| -------- | ------- |
| ServiceAccount | Provides identity to the CronJob |
| Role | Defines permissions for secret management |
| RoleBinding | Associates the Role with the ServiceAccount |
| ConfigMap | Contains the key rotation script |
| CronJob | Executes the key rotation script on a schedule |

<img src="../images/onpremise-ecr-access-key-rotation.png" width="80%" />


1. Service Account (ecr-key-rotation-sa.yaml)
Creates a Kubernetes identity for the CronJob:
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ecr-key-rotation-sa
  namespace: {{ .Release.Namespace }} # namespace where sigrid onprem is/will be deployed.
```

2. Role (ecr-key-rotation-role.yaml)
Defines permissions to manage secrets and jobs:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list", "create", "delete"]
  - apiGroups: ["batch"]
    resources: ["jobs"]
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

3. RoleBinding (ecr-key-rotation-role-binding.yaml)
Links the Role to the ServiceAccount:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
subjects:
  - kind: ServiceAccount
    name: ecr-key-rotation-sa
roleRef:
  kind: Role
  name: eks-sigrid-onprem-ecr-key-rotation-role
```

4. ConfigMap (ecr-key-rotation-configmap.yaml)
Contains the shell script(rotate_ecr_keys.sh) that performs the ECR key rotation process:
  - Gets a temporary ECR authentication token
  - Creates a Docker config JSON
  - Creates/updates a Kubernetes secret containing this config
```yaml
apiVersion: v1
kind: ConfigMap
data:
  rotate_ecr_keys.sh: |-
    # Configuration
    # Sets up variables for Kubernetes API interaction
    # Uses the Kubernetes service account token for authentication
    # Reads namespace from the service account mount
    K8S_SECRET_NAME=ecr-image-pull-secret
    APISERVER=https://kubernetes.default.svc
    SERVICEACCOUNT=/var/run/secrets/kubernetes.io/serviceaccount
    NAMESPACE=$(cat ${SERVICEACCOUNT}/namespace)
    TOKEN=$(cat ${SERVICEACCOUNT}/token)
    CACERT=${SERVICEACCOUNT}/ca.crt
    # Uses AWS CLI to retrieve an ECR authentication token
    # The token is valid for 12 hours from generation
    # Combines "AWS:" with the password and base64 encodes it (Docker authentication format)
    PASSWORD=$(aws ecr get-login-password --region $SIGRID_DOWNLOAD_REGION)
    BASE64_ENCODED_CREDENTIALS=$(echo -n "AWS:${PASSWORD}" | base64 | tr -d '\n')
    # Creates a JSON definition for a Kubernetes secret
    # The secret is of type kubernetes.io/dockerconfigjson (special type for Docker registry credentials)
    # The value of .dockerconfigjson is a base64-encoded Docker config JSON
    # The format matches Docker's config.json structure with registry auth credentials
    cat >/tmp/create_secret.json <<EOT
    { "apiVersion": "v1",
      "kind": "Secret",
      "metadata": {
        "name": "${K8S_SECRET_NAME}"
      },
      "type": "kubernetes.io/dockerconfigjson",
      "data": {
        ".dockerconfigjson": "$(echo -n "{\"auths\":{\"$SIGRID_DOWNLOAD_REGISTRY\":{\"auth\":\"$BASE64_ENCODED_CREDENTIALS\"}}}" | base64 | tr -d '\n')"
      }
    }
    EOT
    # Uses curl to directly interact with the Kubernetes API
    # First deletes the existing secret (if present)
    # Creates a new secret with fresh credentials
    # Uses the service account token for authentication
    # Uses the CA certificate to validate the API server's identity
    echo "Deleting old secret..."
    curl -s --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" "${APISERVER}/api/v1/namespaces/${NAMESPACE}/secrets/${K8S_SECRET_NAME}" -X DELETE
    echo "Creating new secret..."
    curl -s --cacert ${CACERT} --header "Authorization: Bearer ${TOKEN}" "${APISERVER}/api/v1/namespaces/${NAMESPACE}/secrets" -X POST -d @/tmp/create_secret.json -H 'Content-Type: application/json'
```
#### Important Technical Details:
  - Double Base64 Encoding: The script base64-encodes the entire Docker config JSON, which already contains a base64-encoded auth string.
  - Direct API Interaction: Uses curl instead of kubectl, allowing it to run without kubectl installed.
  - In-Cluster Authentication: Uses the service account token and CA certificate for secure API interaction.

5. CronJob (ecr-key-rotation-cronjob.yaml)
The CronJob resource schedules and executes the key rotation process:
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ecr-key-rotation
  namespace: {{ .Release.Namespace }} # namespace where sigrid onprem is/will be deployed.
spec:
  schedule: "0 */11 * * *"  # At 0 minute past every 11th hour, because token is valid for 12h.
  concurrencyPolicy: Forbid
  failedJobsHistoryLimit: 3
  successfulJobsHistoryLimit: 3
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: ecr-key-rotation-sa
          restartPolicy: OnFailure
          containers:
            - name: ecr-key-rotation
              image: public.ecr.aws/aws-cli/aws-cli:2.24.6  # Using AWS CLI image as base
              imagePullPolicy: IfNotPresent
              env:
                - name: SIGRID_DOWNLOAD_REGISTRY
                  value: 571600876202.dkr.ecr.eu-central-1.amazonaws.com
                - name: SIGRID_DOWNLOAD_REGION
                  value: eu-central-1
                - name: AWS_ACCESS_KEY_ID
                  valueFrom:
                    secretKeyRef:
                      name: # Kubernetes secret name where access key id is stored
                      key: AWS_ACCESS_KEY_ID
                - name: AWS_SECRET_ACCESS_KEY
                  valueFrom:
                    secretKeyRef:
                      name: # Kubernetes secret name where secret access key is stored
                      key: AWS_SECRET_ACCESS_KEY
              command:
                - /bin/sh
                - -c
                - date; /app/rotate_ecr_keys.sh
              resources:
                requests:
                  cpu: 100m
                  memory: 128Mi
                limits:
                  memory: 128Mi
              volumeMounts:
                - name: script
                  mountPath: /app
          volumes:
            - name: script
              configMap:
                name: ecr-key-rotation-script
                defaultMode: 0555
```
</details>
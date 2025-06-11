
### Manual AWS ECR login password refresh and pulling images own registry
<details>
<summary>Detailed procedure for Manual AWS ECR login password refresh</summary>
1. Once the script is executed, it will pull the latest Sigrid images from the AWS ECR registry.
The script uses the AWS CLI to get a login password for the ECR registry and then logs in to the registry using Docker. 
After that, it pulls the specified images with the given version:

```bash
SIGRID_DOWNLOAD_REGION=eu-central-1
VERSION=1.0.20250603 # Replace with the desired version
SIGRID_DOWNLOAD_REGISTRY=5012345678901.dkr.ecr.${SIGRID_DOWNLOAD_REGION}.amazonaws.com
export AWS_ACCESS_KEY_ID="provided by SIG"
export AWS_SECRET_ACCESS_KEY="provided by SIG"
AWS_STDERR_FILE="/tmp/.aws-ecr-get-login-stderr"
PASSWORD=$(aws ecr get-login-password --region $SIGRID_DOWNLOAD_REGION)
echo $PASSWORD | docker login --username AWS --password-stdin $SIGRID_DOWNLOAD_REGISTRY 2> $AWS_STDERR_FILE > /dev/null
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

### Automated AWS ECR login password refresh and pulling images from Sigrid ECR registry during Sigrid On-Premises deployments
<details>
<summary>Detailed procedure for automated AWS ECR login password refresh</summary>
AWS ECR passwords expire after 12 hours. Therefore, a scheduled refresh can be implemented for Sigrid On-Premises deployments. This approach automatically refreshes the ECR registry password to maintain continuous access to container images. Note: this is only required when no internal container registry (cache) is used, or to automate the refreshing of images in your internal container registry.
Prerequisites
- An AWS IAM user with ECR access permissions, SIG will provided that.
- Access credentials for this user stored in a Kubernetes secret
- Kubernetes cluster with RBAC enabled
- AWS CLI version 2.x

The ECR key rotation system serves to:

1. Generate temporary ECR authentication tokens periodically
2. Create Kubernetes image pull secrets with these tokens
3. Ensure continuous access to AWS ECR container repositories

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
6. Store AWS Credentials in Kubernetes
Create a Kubernetes secret with the IAM user's credentials:
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

### Update your deployment's values file
```
global:
  imagePullSecrets:
    - name: ecr-image-pull-secret
```
</details>
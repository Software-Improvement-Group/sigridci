# Sigrid on-premise: Analysis with Gerrit and Jenkins

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

This page shows how to run Sigrid-Multi-Analyzer in a Jenkins job for Gerrit, and how to receive Sigrid's feedback in Gerrit changes. It builds on the general [analysis configuration](onpremise-analysis.md), which describes the environment variables and certificates.

## Source code in Sigrid

Sigrid shows an *Open in external VCS* button, which opens the file in Gerrit's Gitiles plugin, instead of showing the file itself, see [source code links](onpremise-kubernetes.md#source-code-links-for-azure-devops-server-and-gerrit).

## Setup

Gerrit has no CI pipelines of its own, so the analysis runs in a Jenkins job. Use a Jenkins plugin for Gerrit, such as
[Gerrit Trigger](https://plugins.jenkins.io/gerrit-trigger), to start the job for every change. The plugin also provides
the change details, so you don't have to hard-code them. Variable names differ per plugin and version, so check the
`env` output of a test build.

Gerrit uses its own variables for feedback, instead of `CICD_COMMENT_TOKEN`:

| Variable | Description |
|---|---|
| `GERRIT_BASE_URL` | The base URL of your Gerrit server, starting with `https://`. Setting it makes Sigrid-Multi-Analyzer treat the job as a Gerrit pipeline. |
| `GERRIT_REPO` | The repository name as used within Gerrit. |
| `GERRIT_BRANCH` | The target branch of the change. Usually provided by the Gerrit plugin. |
| `GERRIT_CHANGE_ID` | The Change-Id of the change, starting with `I`. Usually provided by the Gerrit plugin. Without it, no comment is posted. |
| `GERRIT_USER` | A dedicated Gerrit service account that posts the comment. Don't use an administrator account. |
| `GERRIT_PASSWORD` | The HTTP password of that account, stored as a Jenkins credential. Token-based authentication is not supported. |
| `GIT_SSL_CAINFO` | The CA certificate for cloning from Gerrit, only if Gerrit uses a private CA. |
| `SIGRID_GERRIT_CA_CERT_PATH` | The CA certificate for posting the comment, only if Gerrit uses a private CA. |

The other variables, such as `CUSTOMER`, `SYSTEM`, `SIGRID_URL` and `SIGRID_CI_TOKEN`, are the same as for any other
platform. No `SIGRID_SOURCES_REGISTRATION_ID` is needed, because Sigrid links to Gerrit instead of fetching files.

Example `Jenkinsfile`, running Sigrid-Multi-Analyzer as a pod on Kubernetes with a CA certificate from a ConfigMap:

{% raw %}
```groovy
pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: sigrid-multi-analyzer
    image: 571600876202.dkr.ecr.eu-central-1.amazonaws.com/softwareimprovementgroup/sigrid-multi-analyzer:1.0.20261104
    command: ["sleep"]
    args: ["infinity"]
    resources:
      requests:
        cpu: "1"
        memory: 8Gi
      limits:
        memory: 8Gi
    volumeMounts:
    - name: custom-cert
      mountPath: /etc/custom-certs
      readOnly: true
  volumes:
  - name: custom-cert
    configMap:
      name: my-ca-bundle
'''
      defaultContainer 'sigrid-multi-analyzer'
    }
  }
  environment {
    CUSTOMER = 'company_name'
    SYSTEM = 'my-project'
    SIGRID_URL = 'https://sigrid.my-company.com'
    SIGRID_CI_TOKEN = credentials('SIGRID_CI_TOKEN')
    SIGRID_CA_CERT = '/etc/custom-certs/root-ca.pem'
    GIT_SSL_CAINFO = '/etc/custom-certs/root-ca.pem'
    SIGRID_GERRIT_CA_CERT_PATH = '/etc/custom-certs/root-ca.pem'
    GERRIT_BASE_URL = 'https://gerrit.my-company.com'
    GERRIT_REPO = 'my-project'
    // GERRIT_BRANCH, GERRIT_CHANGE_ID and GERRIT_REFSPEC come from the Gerrit plugin
  }
  stages {
    stage('Analyze') {
      steps {
        sh 'git clone "$GERRIT_BASE_URL/$GERRIT_REPO.git" .'
        sh 'git fetch origin "$GERRIT_REFSPEC" && git checkout FETCH_HEAD'
        withCredentials([usernamePassword(credentialsId: 'gerrit-sigrid', usernameVariable: 'GERRIT_USER', passwordVariable: 'GERRIT_PASSWORD')]) {
          sh '/usr/local/bin/run-analyzers --publish'
        }
      }
    }
  }
}
```
{% endraw %}

The job checks out the patch set of the change (`GERRIT_REFSPEC`), so the feedback is about the change, not about the
target branch. Replace the image tag with the Sigrid version of your deployment. A Docker agent works as well, as long
as it runs the Sigrid-Multi-Analyzer image. For the Gerrit side, such as the Gitiles plugin, see
[Sigrid CI for Gerrit](../sigridci-integration/gerrit.md).

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

# Automated Database Initialization

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- Make sure you have the latest Sigrid helm chart (>=0.4.14)

If you're not pulling `softwareimprovementgroup/sigrid-integration-onprem` directly from our ECR, make sure to pull it from ECR and push it to your local registry for deployment.
{: .attention }

## Enabling Automated Database Initialization
This feature enables automated initialization of the Sigrid databases during deployment.

By default, the Helm chart includes the required SQL scripts but does not execute them automatically. In a standard on-premises setup, customers are expected to run these scripts manually using psql. The scripts are located in the sigrid-stack/files directory of the Helm chart and include sigriddb-init and authdb-init.

To automate this process, set global.onPremise.postgresInit to true in your Helm values. When enabled, the initialization service will execute the database setup as part of the deployment.

To use this feature, you must provide:
 - PostgreSQL management credentials
 - The PostgreSQL server hostname
 - Pre-generated credentials for Sigrid's database users

After successful initialization, the initialization service is no longer required and can be disabled again in the Helm values.
{: .attention }

Below is an example configuration:

{% raw %}
```yaml
global:
  imageRegistry: "my-registry.example.com"
  imageTag: "1.0.20260309"
  hosts:
    - host: "my-sigrid.example.com"
      tls:
        enabled: true
        secretName: "my-tls-secret"
  onPremise:
    customer: "company"
    administrators:
      - "admin@company.com"
    postgresInit:
      enabled: true
      image:
        repository: "softwareimprovementgroup/sigrid-integrations-onprem"
        tag: "1.0.20260309"
      secrets:
        create: true
        secretName: "postgres-init-secret"
        data:
          PGPASSWORD: "" # Postgres root password
          DB_MGMT_USER_PASSWD: ""
          DB_MGMT_USER_PASSWD: ""
          IMPORT_USER_PASSWD: ""
          OSH_KB_UPDATER_PASSWD: ""
          LICENSES_USER_PASSWD: ""
          METRICS_USER_PASSWD: ""
          READONLY_USER_PASSWD: ""
          WEBAPP_USER_PASSWD: ""
          AUTH_DB_MGMT_USER_PASSWD: ""
          AUTH_DB_READONLY_USER_PASSWD: ""
          AUTH_DB_WEBAPP_USER_PASSWD: ""
          ## TEAM_SUFFIX: ""
      customCertificates:
        enabled: true
        certificates:
          create: true
          name: "ldap-group-sync-custom-certs"
          data:
            mysigridcert.pem: |
              -----BEGIN CERTIFICATE-----
              ...... INTERMEDIATE CERTIFICATE CONTENT (if any)
              -----END CERTIFICATE-----
              -----BEGIN CERTIFICATE-----
              ......
              -----END CERTIFICATE-----
            myldapcert.pem: |
              -----BEGIN CERTIFICATE-----
              .....
              -----END CERTIFICATE-----
```
{% endraw %}

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
# Sigrid LDAP Group Sync

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- Make sure you have the latest Sigrid helm chart (>=1.0.20260223)

If you're not pulling `softwareimprovementgroup/sigrid-integration-onprem` directly from our ECR, make sure to pull it from ECR and push it to your local registry for deployment.
{: .attention }

## Enabling LDAP Group Sync
The Sigrid LDAP Group Sync is enabled in the global section of your Sigrid On-Premise deployment configuration.

Enable `global.onPremise.ldapGroupSync` and provide all required LDAP connection values; notably, `SIGRID_UM_TOKEN` is a Sigrid User Management API token from a user with Admin access to Sigrid.

Below is an example configuration:

```yaml
global:
  imageRegistry: "my-registry.example.com"
  imageTag: "1.0.20260223"
  hosts:
    - host: "my-sigrid.example.com"
      tls:
        enabled: true
        secretName: "my-tls-secret"
  onPremise:
    customer: "company"
    administrators:
      - "admin@company.com"
    ldapGroupSync:
      enabled: true
      image:
        repository: "softwareimprovementgroup/sigrid-integrations-onprem"
        tag: "1.0.20260223"
      cronJobschedule: "0 * * * *" # Cronjob schedule in cron format. For example every hour.
      config:
        SIGRID_UM_URL: "https://my-sigrid.example.com"
        SIGRID_UM_CUSTOMER: "onprem"
        SIGRID_LDAP_URL: "ldap://ldap.example.com:389"
        SIGRID_LDAP_BIND_DN: "cn=read-only-admin,dc=example,dc=com"
        SIGRID_LDAP_USER_DN: "dc=example,dc=com"
        SIGRID_LDAP_USER_QUERY: "objectclass=inetOrgPerson"
        SIGRID_LDAP_GROUP_DN: "dc=example,dc=com"
        SIGRID_CA_CERT: /etc/ssl/certs/custom/mysigridcert.pem
        LDAP_CA_CERT: /etc/ssl/certs/custom/myldapcert.pem
      secrets:
        create: true
        secretName: "ldap-group-sync-secret"
        data:
          SIGRID_UM_TOKEN: "" # Sigrid User Management API token
          SIGRID_LDAP_BIND_PASSWORD: "" # LDAP bind password
      customCertificates:
        enabled: true
        certificates:
          create: true
          name: "ldap-group-sync-custom-certs"
          data:
            mysigridcert.pem: |
              -----BEGIN CERTIFICATE-----
              .....
              -----END CERTIFICATE-----
            myldapcert.pem |
              -----BEGIN CERTIFICATE-----
              .....
              -----END CERTIFICATE-----
```

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
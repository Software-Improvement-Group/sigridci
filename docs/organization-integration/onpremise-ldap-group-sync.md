# Sigrid LDAP Group Sync

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.
- Make sure you have the latest Sigrid helm chart (>=0.4.11)

If you're not pulling `softwareimprovementgroup/sigrid-integration-onprem` directly from our ECR, make sure to pull it from ECR and push it to your local registry for deployment.
{: .attention }

## Scenarios
This integration, once enabled will do the following

- LDAP group + Sigrid group both exist → 🔁 Membership is synchronized
- LDAP user in that group not in Sigrid → ✔️ User is created as SSO user
- LDAP group removed but still in Sigrid → ❌ Group is deleted from Sigrid
- User removed from LDAP group → ❌ User removed from Sigrid group (via full membership overwrite)

Optional flag `--override-groups`
- Force-replace all Sigrid user groups with LDAP groups → Replaces all user group memberships with those from LDAP

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
      #args: ["--override-groups"]
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

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.
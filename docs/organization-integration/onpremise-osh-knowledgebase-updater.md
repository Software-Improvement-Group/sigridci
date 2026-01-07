# Open Source Health knowledge base for Sigrid On-Premise

This documentation covers on-premise Sigrid. It is not applicable for cloud-based Sigrid.
{: .attention }

## Prerequisites

- You should have already read the other Sigrid On-Premise documentation.
- All pre-requisites from our public documentation are met.

## Introduction

Sigrid continuously measures and reports on the quality, security, and maintainability of software systems. Part of this capability is **Open Source Health (OSH)**, which focuses on identifying open source dependencies and assessing whether these dependencies are affected by known vulnerabilities.

In **Sigrid SaaS deployments**, OSH results are determined by consulting public and vendor-maintained vulnerability knowledge sources. However, for **Sigrid On-Premise deployments**, this is usually not possible. On-premise environments are commonly isolated from the internet or restricted by security and compliance requirements, which prevents access to external vulnerability databases.

As a result, Sigrid On-Premise cannot rely on public knowledge sources to determine vulnerabilities in open source dependencies.

To enable OSH in on-premise environments, Sigrid provides a dedicated **Open Source Health knowledge base**.

Accurate OSH results depend on continuously updated vulnerability database. Without access to such knowledge, OSH findings cannot be produced.

## OSH knowledge base for On-Premise deployments

For Sigrid On-Premise, the vulnerability database is provided through a **local OSH knowledge base**.

The OSH knowledge base is delivered as a **separate, optional container** that maintains a curated set of vulnerability data. During analysis, Sigrid queries this local knowledge base instead of public sources.

Key characteristics:

- **Optional component**  
  The OSH knowledge base is optional, but required if you want OSH findings in an on-premise deployment.
- **Independent versioning**  
  The OSH knowledge base container does not need to be on the same version as the other Sigrid containers.
- **Regular updates required**  
  Vulnerability data evolves rapidly. To ensure accurate and relevant OSH results, the knowledge base must be kept up to date.
- **Standard update process**  
  Updating the OSH knowledge base container follows the same process as updating other containers in the Sigrid deployment.

It is strongly recommended to update the OSH knowledge base container daily, if possible.
{: .attention }

## Creating the OSH knowledge base user

This step is only necessary when setting up the OSH knowledge base for Sigrid On-Premise deployments completed before 2026. Newer deployments already have this user, as it is created by sigriddb-init during the initial PostgreSQL database setup.
{: .attention }

Run the following commands on your PostgreSQL database:

```yaml
CREATE USER osh_kb_updater_user WITH
    PASSWORD '${OSH_KB_UPDATER_PASSWD}'
    CREATEROLE
    NOINHERIT
    ;
GRANT CONNECT, TEMP ON DATABASE sigriddb TO osh_kb_updater_user;
GRANT USAGE ON SCHEMA osh_knowledge_base TO osh_kb_updater_user;
-- For tables existing in osh_knowledge_base, grant SELECT, INSERT, UPDATE
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA osh_knowledge_base TO osh_kb_updater_user;
-- For sequences existing in osh_knowledge_base, grant SELECT, INSERT, UPDATE
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA osh_knowledge_base TO osh_kb_updater_user;
```

## Enabling the OSH knowledge base updater

The OSH knowledge base updater is enabled in the global section of your Sigrid On-Premise deployment configuration.

Add the following configuration to the `global` section:

```yaml
global:
  onPremise:
    oshKbUpdater:
      enabled: true
      updaterImage:
        repository: softwareimprovementgroup/osh-kb-updater
        tag: 1.0.20260106 # e.g. use Renovate to update this tag regularly
      pgHost: "postgres.example.com"
      pgSecretName: "osh-kb-updater-job-postgres-secret" # secret containing the password for the database user
      pgSecretPasswordKey: "" # 
      cronJobschedule: "0 9 * * *" # by default the cronjob will trigger at 9:00 UTC
```

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid-Multi-Analyzer. Users in Europe can also contact us by phone at +31 20 314 0953.
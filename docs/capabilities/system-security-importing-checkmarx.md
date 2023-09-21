# Importing Checkmarx security findings into Sigrid

**Note: This documentation does not yet completely describe how to export Checkmarx results using your CI platform, but it does provide pointers for doing so. Please contact SIG support if you need help getting up and running.**

Sigrid allows you to import your security findings into Sigrid so you can use Sigrid as single source of truth for all software quality needs.\
Imported findings will show up in the Security Findings page in Sigrid.

## Prerequisites

* A valid Checkmarx subscription (either hosted/on demand or on-premise) configured to run scans on the system that you want to import.
* A Sigrid subscription that includes security.

## Running scans with Checkmarx

Sigrid does not specify how you run your scans. This can be on-demand in your pipeline, or on a regular schedule. For setting up Checkmarx and running scans, please use the [Checkmarx SAST documentation](https://checkmarx.com/resource/documents/en/34965-46398-sast-user-guide.html).

## Importing results into Sigrid

Checkmarx results can be exported using the tool [CxFlow](https://github.com/checkmarx-ltd/cx-flow) provided by Checkmarx. Use CxFlow to export results into the `SARIF` format. This export file should then be placed in a `.sigrid` folder in the root of your codebase and pushed to Sigrid. It will then be automatically processed when you push your code to Sigrid.

- [CxFlow download page](https://github.com/checkmarx-ltd/cx-flow/releases)
- [CxFlow documentation](https://github.com/checkmarx-ltd/cx-flow/wiki/)

Below is a sample CxFlow configuration file that can be used. It should be tailored to your situation, but the export format should be Sarif. the [CxFlow wiki](https://github.com/checkmarx-ltd/cx-flow/wiki/Configuration) documents available configuration options.

This can be executed in a CI pipeline. CxFlow provides [tutorials to integrate with various CI platforms](https://github.com/checkmarx-ltd/cx-flow/wiki/Tutorials). The simplest version is running e.g.: `java -jar cx-flow.jar --spring.config.location=cxflow-config.yml --scan --cx-project=<project> -- app=<app> --f=<codebase>`

```yml
server:
  port: 8982
logging:
  file:
    name: cxflow.log

cxflow:
  bug-tracker: Sarif
  bug-tracker-impl:
    - Sarif
  branches:
    - main
  filter-severity:
  filter-category:
  filter-cwe:
  filter-status:

checkmarx:
  version: 9.0
  username: <your Cx username>
  password: <your Cx password>
  client-secret: 014DF517-39D1-4453-B7B3-9930C563627C
  base-url: <Your Cx installation URL>
  team: /CxServer
  url: ${checkmarx.base-url}/cxrestapi
  #WSDL Config
  portal-url: ${checkmarx.base-url}/cxwebinterface/Portal/CxWebService.asmx
  sdk-url: ${checkmarx.base-url}/cxwebinterface/SDK/CxSDKWebService.asmx
  portal-wsdl: ${checkmarx.base-url}/Portal/CxWebService.asmx?wsdl
  sdk-wsdl: ${checkmarx.base-url}/SDK/CxSDKWebService.asmx?wsdl
  app: <your application name>
```
*File: cxflow-config.yml*
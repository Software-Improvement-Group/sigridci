Integrating Sigrid CI with Mendix Pipelines
===========================================

This documentation covers cloud-based Sigrid. For on-premise Sigrid, refer to the section about
[on-premise analysis configuration](../organization-integration/onpremise-analysis.md).
{: .attention }

This document describes integrating Sigrid with [Mendix Pipelines](https://docs.mendix.com/developerportal/deploy/mendix-pipelines/), 
which is a continuous integration pipeline built into the Mendix Platform.

## Prerequisites

- You are using Mendix Pipelines for your project.
- You would like to trigger the Sigrid analysis from within Mendix Pipelines.
- You have a [Sigrid](https://qsm.mendix.com) user account.
- You have created an [authentication token using Sigrid](../organization-integration/authentication-tokens.md).
- You have created a Personal access (PAT) token using the [Mendix user settings](https://user-settings.mendix.com/link/developersettings)

## On-boarding your system to Sigrid

On-boarding is done automatically when you first run Sigrid CI. As long as you have a valid token, you will receive 
the message *system has been on-boarded to Sigrid*. Subsequent runs will then be visible in both your CI environment 
and [sigrid-says.com](https://sigrid-says.com). 

## Configuration

@@@TODO

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you 
may have after reading this documentation or when using Sigrid.

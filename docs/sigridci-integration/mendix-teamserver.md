# QSM (Sigrid-says.com)for Mendix customers using the Teamserver

This document describes use cases for customers that are using the central Mendix Teamserver.

please note: When the customer is not using the team server but they are in a "Bring Your Own Git" scenario then the below does not apply. Then please refer to [Mendix for GitHub](mendix-github-actions.md) or [Mendix for Gitlab](mendix-gitlab.md) 

## Control the onboarding of a Teamserver based app
Onboarding a new Mendix system is normaly done via [addon.mendix.com](https://addon.mendix.com). In some cases customers would like to take onboarding in their own hands. Examples can be automation or bulk onboarding. In those cases customers can trigger an QSM Onboarding that will add a new Mendix system to an existing Sigrid. By default the mainline of the Mendix system will be scanned once a day. The scan will provide both maintainability, OSH and security findings for QSM customers. AQM customers will only see maintainability results. The onboarding will generate a status email to the user specified in the payload.

## On demand scanning of a Teamserver based app
Trigger a QSM run for an already onboarded system. This is useful when a customer would like to trigger a new run for certain day. The trigger can be a step in an automated pipeline or just a developer that is interested in updated results for the mainline. There will be no email, the 'on demand' scan will overwrite the previous scan results in Sigrid.


### 1. Trigger an QSM Onboarding of a Teamserver based app

POST `/qsm/{customer}`

#### Info
Note that this endpoint requires a [SIGRID CI Authentication token](../organization-integration/authentication-tokens.md) that is valid for {customer}. 
##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
    - `Content-Type: application/json`
##### Body
Json object with the following fields:

    - appId : to be used to identify the Mendix app. 

    - appName : to be used as system name in Sigrid. You can use the Mendix project name, it will be converted to a Sigrid system name.

    - mendixToken : we prefer the Mendix PAT [Personal Access Token](https://warden.mendix.com) MX model read only. There is support for the old API Key. In case of an API Key, the userName should match the key

    - userName : to be used to send status email, not relevant for authentication in case of PAT
    

#### Example request
```bash
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER -H 'Content-Type: application/json' -d '{ "appId" : "01234567-89ab-cdef-0123-456789abcdef", "appName" : "mendixsystemname", "userName" : "user@sig.eu", "mendixToken" : "123456-abcdef" }'
```
---

### 2. Trigger a QSM run for an already onboarded system

POST `/qsm/{customer}/{system}`

#### Info
Note that this endpoint requires a [SIGRID CI Authentication token](../organization-integration/authentication-tokens.md) that is valid for {customer}.
##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
##### Body
Should remain empty
    

#### Example request
```bash
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER/SYSTEM
```

## Combining both the Teamserver and a CI pipeline to scan any branch against mainline

We see that some of our customers use the Mendix Team sever to store the Mendix apps and they also use a separate CI pipeline connected the teamserver to do automated 'pipeline' tasks. This is called the 'bring your own pipeline' scenario. Some of these customers would like to scan any branch in QSM and not only scan the default mainline.

In those cases the following hybrid setup will work. The trick of this hybrid set up is that the daily clone of the mainline de facto serves as a SigridCI --publish step.

- 1. QSM Sigrid-says.com will pull a daily clone from the team server busines as usual. It scans by default the mainline for both maintainability, open source health and security. 

- 2. In the CI pipeline the customer only needs to add the SigriCI step to scan any branch against the above 'published' mainline for maintainability results.

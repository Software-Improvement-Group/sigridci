# Sigrid API for Mendix customers using the Teamserver

This document describes 2 use cases to trigger Sigrid for customers that are using the central Mendix Teamserver.

please note: When the customer is using the Bring Your Own Git scenario then the below does not apply. please refer to [Mendix for GitHub](mendix-github-actions.md)

## Control the onboarding
Onboarding a new Mendix system is normaly done via [addon.mendix.com](https://addon.mendix.com). In some cases customers would like to take onboarding in their own hands. Examples can be automation or bulk onboarding. In those cases customers can trigger an QSM Onboarding that will add a new Mendix system to an existing Sigrid. By default the mainline of the Mendix system will be scanned once a day. The scan will provide both maintanability, OSH and security findings for QSM customers. AQM customers will only see maintainability results. The onboarding will generate a status email to the user specified in the payload.

## On demand scanning
Trigger a QSM run for an already onboarded system. This is useful when a customer would like to trigger a new run for certain day. The trigger can be a step in an automated pipeline or just a developer that is interested in updated results for the mainline. There will be no email, the 'on demand' scan will overwrite the previous scan results in sigrid-says.com


### 1. Trigger an QSM Onboarding

POST `/qsm/{customer}`

#### Info
Note that this endpoint requires a [SIGRID CI Authentication token](authentication-tokens.md) that is valid for {customer}. 
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
Note that this endpoint requires a [SIGRID CI Authentication token](authentication-tokens.md) that is valid for {customer}.
##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
##### Body
Should remain empty
    

#### Example request
```bash
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER/SYSTEM
```

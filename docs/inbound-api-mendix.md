## Triggers for Mendix customers

This document describes 2 use cases where Mendix customers can trigger Sigrid in the AQM/QSM context. 

Trigger an QSM Onboarding workflow is about adding a new Mendix system to an existing Sigrid. By default the mainline of the Mendix system will be scanned once a day. The scan will provide both maintanability and OSH and security findings.


Trigger a QSM run workflow for an already onboarded system. This is useful when a customer would like to trigger a new run for certain day. The 'on demand' run will overwrite the previous scan for maintainability, OSH and security.



### 1. Trigger an QSM Onboarding workflow

POST `/qsm/{customer}`

#### Info
Note that this endpoint requires a Sigrid Access Token that is valid for {customer}. 
##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
    - `Content-Type: application/json`
##### Body
Json object with the following fields:

    - appId (to be used to identify the Mendix app)

    - appName (to be used as system name in SigridYou can use the Mendix project name, it will be converted to an acceptable system name)

    - mendixToken (we prefer the PAT but also support the old API Key. In case of an API Key, the userName should match the key)

    - userName ( to be used to send email notifications, not relevant for authentication in case of PAT)
    

#### Example request
```
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER -H 'Content-Type: application/json' -d '{ "appId" : "01234567-89ab-cdef-0123-456789abcdef", "appName" : "mendixsystemname", "userName" : "user@sig.eu", "mendixToken" : "123456-abcdef" }'
```
---

### 2. Trigger a QSM run workflow for an already onboarded system

POST `/qsm/{customer}/{system}`

#### Info
Note that this endpoint requires a Sigrid Access Token that is valid for {customer}.
##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
##### Body
Should remain empty
    

#### Example request
```
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER/SYSTEM
```

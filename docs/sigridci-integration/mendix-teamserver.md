# QSM (Sigrid-says.com)for Mendix customers using the Teamserver

This document describes use cases for customers that are using the central Mendix Teamserver.

please note: When the customer is not using the teamserver but they are in a "Bring Your Own Git" scenario then the below does not apply. Then please refer to [Mendix for GitHub](mendix-github-actions.md) or [Mendix for Gitlab](mendix-gitlab.md) 

Onboarding a new Mendix system is normaly done via [addon.mendix.com](https://addon.mendix.com). By default the mainline of the Mendix system will be scanned once a day. The scan will provide both maintainability, OSH and security findings for QSM customers. AQM customers will only see maintainability results. The onboarding will generate a status email to the user specified in the payload.

## Trigger a QSM Onboarding of a Teamserver based app
In some cases customers would like to take onboarding of a teamserver based app in their own hands. Examples can be automation or bulk onboarding or specify a specific branch. In those cases customers can trigger an QSM Onboarding that will add a new Mendix system to an existing Sigrid. 


### Technical details about the required post message for onboarding a system

POST `https://sigrid-says.com/rest/inboundresults/qsm/{customer}`

#### Info
Note that this endpoint requires a [SIGRID CI Authentication token](../organization-integration/authentication-tokens.md) that is valid for {customer}. 

##### Headers
    - 'Authorization: Bearer YOUR_TOKEN'
    - `Content-Type: application/json`
##### Body


```json
{
    "userName": "[email address]", // to be used to send email notifications, not relevant for authentication in case of PAT
    "mendixToken": "[use a Mendix PAT with model read only rights]", // For legacy projects on Teamserver-SVN an API key is also supported
    "appId": "[a UUID]",
    "appName": "[the app name]",
    "teamServerBranch": "[the name of a specific branch]" // leave empty or omit alltogether to use mainline
}
```    

#### Example request
```bash
curl --header 'Authorization: Bearer YOUR_TOKEN' -X POST https://sigrid-says.com/rest/inboundresults/qsm/CUSTOMER -H 'Content-Type: application/json' -d '{ "appId" : "01234567-89ab-cdef-0123-456789abcdef", "appName" : "mendixsystemname", "userName" : "user@sig.eu", "mendixToken" : "123456-abcdef", "teamServerBranch" : "some_branch" }'
```

This request will return the following response:
```json
{
    "customerName": "customer",
    "systemName": "mendixsystemname-branch-some-branch"
}
```

Note that the system name is a concatenation of the app name, the word `branch` and the branch name, with unsupported characters replaced or removed. In case of omitting the `teamServerBranch` or leaving it empty, the system name would be `mendixsystemname`.

---

## Trigger a QSM run for an already onboarded system
This is useful when a customer would like to do an 'on-demand' trigger for certain day. The trigger can be a step in an automated pipeline or just a developer that is interested in updated results for the mainline. There will be no email, the scan will overwrite the previous scan results in Sigrid.

### Technical details about the required post message for triggering a run

POST `https://sigrid-says.com/rest/inboundresults/qsm/{customer}/{system}`

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

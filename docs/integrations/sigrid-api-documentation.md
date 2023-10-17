Sigrid API documentation
========================

In addition to [Sigrid CI](../README.md), Sigrid also provides a more general-purpose REST API that you can use to obtain analysis results from Sigrid. This allows you to integrate data from Sigrid into your workflow. 

## General usage

- The Sigrid API base URL is `https://sigrid-says.com/rest/analysis-results/api/v1`. 
- Authentication for the Sigrid API uses the same [authentication tokens](../organization-integration/authentication-tokens.md) that are used by Sigrid CI. Your token's permissions are based on your user account, so the token can access the same systems that you can. 
- You need to pass the authentication token to each request in the HTTP header `Authorization: Bearer {SIGRID_CI_TOKEN}`.
- All end points will return HTTP status 401 if the token is invalid, or if the token is not authorized to access the portfolio and/or system.
- All end points return JSON and therefore return a Content-Type of `application/json`.

The following example shows how to call the Sigrid API using `curl`:

```
curl -H 'Authorization: Bearer {SIGRID_CI_TOKEN}' https://sigrid-says.com/rest/analysis-results/api/v1/maintainability/{customer}
```

In the example, `{customer}` refers to your company's Sigrid account name, and `{SIGRID_CI_TOKEN}` refers to your authentication token.

### Including deactivated and/or excluded systems

In Sigrid's web-based user interface, several portfolio (customer) level dashboards by default 
hides deactivated systems and excluded systems. The filter panel on the right hand side provides 
two toggles to override this behavior:

<img src="../images/dashboard-toggles.png" width="202" />

A system can be deactivated, or excluded from dashboards, in the metadata settings page:

<img src="../images/metadata-deactivate.png" width="843" />

Sigrid's REST API mimics this behavior, as follows:
* All portfolio-level endpoints by default do not include deactivated nor excluded systems in 
  their responses.
* Deactivated systems can be included in the response by adding a boolean query parameter 
  `hideDeactivatedSystems` and set it to `false`, `no`, or `0`. For instance, `GET 
  /api/v1/maintainability/{customer}&hideDeactivatedSystems=false` includes deactivated systems 
  in the response.
* Excluded systems can be included in the response by adding a boolean query parameter
  `hideExcludedSystems` and set it to `false`, `no`, or `0`. For instance, `GET
  /api/v1/maintainability/{customer}&hideExcludedSystems=false` includes development-only systems
  in the response.

## Available end points

* [Maintainability ratings](#maintainability-ratings)
* [Security and reliability findings](#security-and-reliability-findings)
* [Vulnerable libraries in Open Source Health](#vulnerable-libraries-in-open-source-health)
* [System metadata](#system-metadata)
* [System lifecycle management](#system-lifecycle-management)
* [System objectives](#system-objectives)

### Maintainability ratings

Maintainability ratings for a given customer are available via three endpoints:
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/maintainability/{customer}`: system-level maintainability ratings for all systems of the given customer the current user has access to.
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/maintainability/{customer}/{system}`: system-level maintainability ratings for the given system of the given customer.
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/maintainability/{customer}/{system}/components`: component-level maintainability ratings for the given system of the given customer.

The parameter `{customer}` refers to your Sigrid account name. 

<details>
  <summary>Example response</summary>

```json
{
    "customer": "my-sigrid-account-name",
    "systems": [
        {
            "system": "my-system-name",
            "customer": "my-sigrid-account-name",
            "maintainability": 5.24,
            "maintainabilityDate": "2022-02-08",
            "allRatings": [
                {
                    "maintainability": 4.96,
                    "maintainabilityDate": "2022-02-06"
                }
            ]
        }
    ]
}
```
</details>

The top-level `maintainability` and `maintainabilityDate` refer to the *current* state of each system. The `allRatings` array contains a list of all *historic* measurements, which can be used for reporting or trend information.

### Security and reliability findings

Sigrid's REST API provides two endpoints to get security or reliability findings for a system:
* Security findings: `GET https://sigrid-says.com/rest/analysis-results/api/v1/security-findings/
  {customer}/{system}`
* Reliability findings: `GET https://sigrid-says.
  com/rest/analysis-results/api/v1/reliability-findings/{customer}/
  {system}`

The parameters `{customer}` and `{system}` refer to your Sigrid account name and system ID respectively. 

<details>
  <summary>Example response</summary>

```json
[
    {
        "id": "00000000-0000-0000-0000-0000005d9c1e",
        "href": "https://sigrid-says.com/my-sigrid-account/my-system/-/sigrid-security/00000000-0000-0000-0000-0000005d9c1e",
        "firstSeenAnalysisDate": "2019-09-18",
        "lastSeenAnalysisDate": "2019-09-18",
        "firstSeenSnapshotDate": "2019-05-04",
        "lastSeenSnapshotDate": "2019-05-04",
        "filePath": "helloworld.py",
        "startLine": 12,
        "endLine": 23,
        "component": "frontend",
        "type": "",
        "cweId": "CWE-12345",
        "severity": "LOW",
        "impact": "LOW",
        "exploitability": "LOW",
        "severityScore": 2.0,
        "impactScore": 1.2,
        "exploitabilityScore": 0.8,
        "status": "FALSE_POSITIVE",
        "remark": "Test test test",
        "toolName": null,
        "isManualFinding": true,
        "isSeverityOverridden": true,
        "weaknessIds": [
            "CWE-12345"
        ]
    }
]
```
</details>

### Vulnerable libraries in Open Source Health

A list of all third-party libraries used is available for a given system, or for all systems for a customer, using the following endpoints:
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/osh-findings/{customer}?vulnerable=<choose one of true or false according to the explanation below>`: get all third-party libraries for all systems the current user has access to for the given customer.
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/osh-findings/{customer}/{system}?vulnerable=<choose one of true or false according to the explanation below>`: get all third-party libraries for the given system and customer.

The path parameters `{customer}` and `{system}` refer to your Sigrid account name and system ID respectively. The `vulnerable` URL query parameter is optional and defaults to `false`. The meaning is as follows:
- `?vulnerable=false` or no query parameter: the endpoint returns the full list of third-party libraries detected by Sigrid for the given customer/system(s), including lists of known vulnerabilities per library if any. 
- `?vulnerable=true`: the endpoint returns only those third-party libraries detected by Sigrid for the given customer/system(s) that have at least one known vulnerability. 

The response format is based on the CycloneDX format for an [SBOM (software bill of materials)](https://en.wikipedia.org/wiki/Software_bill_of_materials). 

<details>
  <summary>Example response for a single system</summary>

```json
{
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "version": 1,
    "metadata": {
        "timestamp": "2022-03-17T09:58:34Z",
        "tools": [
            {
                "vendor": "Software Improvement Group",
                "name": "Sigrid",
                "externalReferences": [
                    {
                        "type": "other",
                        "url": "https://sigrid-says.com/my-sigrid-account-name/my-system-id/-/open-source-health"
                    }
                ]
            }
        ]
    },
    "components": [
        {
            "group": "",
            "name": "yui",
            "version": "2.8.0r4",
            "purl": "pkg:npm/yui@2.8.0r4",
            "type": "library",
            "bom-ref": "pkg:npm/yui@2.8.0r4"
        }
    ],
    "vulnerabilities": [
        {
            "bom-ref": "pkg:npm/yui@2.8.0r4",
            "id": "CVE-2010-4710",
            "ratings": [
                {
                    "score": 4.3,
                    "severity": "medium",
                    "method": "CVSSv3"
                }
            ],
            "description": "Cross-site Scripting"
        }
    ]
}
```
</details>

The endpoint that returns third-party vulnerabilities for all systems for the given customer returns an array of SBOMs, one for each system as follows:
```
{
    "customer" : "sig",
    "exportDate" : "2022-07-12",
    "systems" : [ {
        "customerName" : "sig",
        "systemName" : "bch",
        "sbom" : {
            ...                   // Same as the response format in the single-system case
        }
    ]
}
```

More information on the SBOM format and the various fields is available from the [CycloneDX SBOM specification](https://github.com/CycloneDX/specification).

### System metadata

System metadata can be viewed and updated using the following three endpoints:
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/system-metadata/{customer}/{system}`: get metadata of the given system of the given customer.
- `GET https://sigrid-says.com/rest/analysis-results/api/v1/system-metadata/{customer}`: get metadata of all systems of the given customer.
- `PATCH https://sigrid-says.com/rest/analysis-results/api/v1/system-metadata/{customer}/{system}`: update metadata of the given system of the given customer.

The path parameters `{customer}` and `{system}` refer to your Sigrid account name and system ID respectively.

<details>
  <summary>Example system-level `GET` and `PATCH` response format</summary>

The response format of both system-level endpoints (`GET` and `PATCH`) is as follows:
```json
{
  "displayName" : "User-friendly system name",
  "divisionName" : "Division name",
  "teamNames" : [ "My Team" ],
  "supplierNames" : [ "Supplier 1", "Supplier 2" ],
  "lifecyclePhase" : "EOL",
  "inProductionSince" : 2012,
  "businessCriticality" : "HIGH",
  "targetIndustry" : "ICD9530",
  "deploymentType" : "PUBLIC_FACING",
  "applicationType" : "ANALYTICAL",
  "softwareDistributionStrategy": "DISTRIBUTED",
  "remark" : "A remark",
  "externalID" : "ab12345",
  "isDevelopmentOnly" : false,
  "technologyCategory": "MODERN_GENERAL_PURPOSE"
}
```
</details>

<details>
  <summary>Example customer-level response</summary>

The response format of the customer-level endpoint (`GET https://sigrid-says.com/rest/analysis-results/api/v1/system-metadata/{customer}`) is as follows:
```json
[
  {
    "customerName": "foo",
    "systemName": "bar",
    "displayName" : "User-friendly system name",
    "divisionName" : "Division name",
    "teamNames" : [ "My Team" ],
    "supplierNames" : [ "Supplier 1", "Supplier 2" ],
    "lifecyclePhase" : "EOL",
    "inProductionSince" : 2012,
    "businessCriticality" : "HIGH",
    "targetIndustry" : "ICD9530",
    "deploymentType" : "PUBLIC_FACING",
    "applicationType" : "ANALYTICAL",
    "softwareDistributionStrategy": "DISTRIBUTED",
    "remark" : "A remark",
    "externalID" : "ab12345",
    "isDevelopmentOnly" : false,
    "technologyCategory": "MODERN_GENERAL_PURPOSE"
  }
]
```
</details>

All properties can be null except for `supplierNames` and `teamNames` (which are always an array, but possibly empty), and `isDevelopmentOnly` (which is always true or false).

For the `PATCH` endpoint, please take the following into account:
- Only users with admin rights are allowed to change metadata.
- A `PATCH` endpoint requires a body as well as a `Content-Type` header. This is best illustrated with the example below.
- The `Content-Type` header needs to be set to `application/merge-patch+json` or `application/json`. The former is the official one, the latter behaves exactly the same. 

```shell
$ curl 'https://sigrid-says.com/rest/analysis-results/api/v1/system-metadata/{customer}/{system}' -X PATCH \
    -H 'Content-Type: application/merge-patch+json' \
    -H 'Authorization: Bearer {SIGRID_CI_TOKEN}' \
    -d '{
  "supplierNames" : [ "Supplier 1" ],
  "remark" : null,
}'
```

This example request _replaces_ the list of supplier names with the list consisting of one single supplier name (`Supplier 1`). It also _removes_ the remark. Next to this, it
leaves all metadata as-is. For instance, if the external ID before executing this request is `ab12345`, after this request it still is. 

### Metadata fields

The metadata fields are described by the following table. Note that the setting for `deploymentType` is used to assess impact of security findings.

|Path                          |Type     |Description                                                                                                                               |
|------------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------|
|`displayName`                 |`String` |The display name of the system. Must be between 0 and 60 characters. Can contain blanks: true|
|`divisionName`                |`String` |The name of the division this system belongs to. Must be between 0 and 60 characters. Can contain blanks: true|
|`supplierNames`               |`Array`  |Array of the names of the suppliers for this system|
|`inProductionSince`           |`Number` |The year the system went into production. Cannot be later than the current year, must be at least 1960|
|`businessCriticality`         |`String` |Importance of the system in terms of the effects of it not being available on the user's business. Must match any of the following values (case-sensitive): CRITICAL, HIGH, MEDIUM, LOW|
|`lifecyclePhase`              |`String` |The phase of its lifecycle the system is in. Must be an industry identifier from the table of lifecycle phase identifiers below (case-sensitive)|
|`targetIndustry`              |`String` |The industry in which the system is normally used. Must be an industry identifier from the table of target industry identifiers below (case-sensitive)|
|`deploymentType`              |`String` |The way in which the system is typically deployed. Must be an industry identifier from the table of deployment types below (case-sensitive)|
|`applicationType`             |`String` |The type of the system. Must be an industry identifier from the table of application types below (case-sensitive)|
|`softwareDistributionStrategy`|`String` |The type of the software distribution strategy. Must be one of the distribution strategy identifiers from the table below (case-sensitive)|
|`isDevelopmentOnly`           |`Boolean`|If true, the system is not shown as part of customer's portfolio, in the UI this is known as the "Excluded from dashboards" toggle|
|`remark`                      |`String` |Remark(s) about the system as (possibly empty) free-format text. Must be between 0 and 300 characters. Can contain blanks: true|
|`externalID`                  |`String` |Allow customers to record an external identifier for a system. free-format text. Must be between 0 and 60 characters. Can contain blanks: true|

<details>
  <summary>Software distribution strategies</summary>

The software distribution strategy identifiers have the following meaning:

|`softwareDistributionStrategy` identifier|Software Distribution Strategy|
|---------------------------|----------------------|
|NOT_DISTRIBUTED|Software is not distributed to third parties|
|NETWORK_SERVICE|Software is not distributed, but is available to third parties as a network service (e.g. SaaS)|
|DISTRIBUTED|Software is distributed to third parties (e.g. as on-premise solution or device software)|

</details>

<details>
  <summary>Lifecycle phases</summary>

The lifecycle phase identifiers have the following meaning:

|`lifecyclePhase` identifier|System lifecycle phase|
|---------------------------|----------------------|
|INITIAL|Initial development (pre-production)|
|EVOLUTION|Evolution (post-production)|
|MAINTENANCE|Servicing and maintenance|
|EOL|End-of-life (in production but minimal maintenance)|
|DECOMMISSIONED|Decommissioned / Phased out (no longer in production)|

</details>

<details>
  <summary>Target industries</summary>

The target industry phase identifiers have the following meaning:

|`targetIndustry` identifier|Industry|
|----------|--------|
|ICD0500|Oil & Gas|
|ICD1750|Industrial Metals & Mining|
|ICD2350|Construction & Materials|
|ICD2710|Aerospace & Defense|
|ICD2730|Electronic & Electrical Equipment|
|ICD2750|Industrial Engineering|
|ICD2770|Industrial Transportation|
|ICD2790|Support Services|
|ICD2797|Industrial Suppliers|
|ICD3350|Automobiles & Part|
|ICD3500|Food & Beverage|
|ICD3700|Personal & Household Goods|
|ICD4500|Health Care|
|ICD5300|Retail|
|ICD5500|Media|
|ICD5700|Travel & Leisure|
|ICD6500|Telecommunications|
|ICD7500|Energy|
|ICD7577|Water|
|ICD8300|Banking|
|ICD8500|Insurance|
|ICD8630|Real Estate Investment & Services|
|ICD8700|Financial Services|
|ICD9530|Software & Computer Services|
|ICD9570|Technology hardware & equipment|
|SIG2200|Legal Services|
|SIG1200|Research|
|SIG1000|Government|
|SIG1100|Education|

</details>

<details>
  <summary>Deployment types</summary>

The deployment type identifiers have the following meaning:

|`deploymentType` identifier|Deployment Type|
|---------------------------|---------------|
|PUBLIC_FACING|A system that is accessible by users through the public internet|
|CONNECTED|A system that interacts with a public-facing system via the network. The system is not accessible via the public internet|
|INTERNAL|A system that can only be reached by users via VPN or the company intranet. The system has no interaction with public-facing systems|
|PHYSICAL|A system that can only be reached by users with access to a physical location. The system cannot be reached from an internal network and has no interaction with public-facing systems|

</details>

<details>
  <summary>Application types</summary>

The possible application types are as follows:

|`applicationType` identifier|
|----------------------------|
|PROCESS_CONTROLLER|
|TRANSACTION_PROCESSING|
|RESOURCE_MANAGEMENT|
|CASE_MANAGEMENT|
|DESIGN_ENGINEERING_DEVELOPMENT|
|ANALYTICAL|
|AUTHENTICATION_AND_PORTALS|
|COMMUNICATION|
|FUNCTIONAL_APPLICATIONS|
|KNOWLEDGE_AND_DOCUMENT_MANAGEMENT|
|PERSONAL_PRODUCTIVITY_APPLICATIONS|

</details>

<details>
  <summary>Technology categories</summary>

The possible technology categories are as follows:

|`technologyCategory` identifier|
|-------------------------------|
|AGGREGATE|
|BPM|
|CUSTOMIZATION|
|CONFIGURATION|
|DATABASE|
|DSL|
|EMBEDDED|
|LEGACY|
|LOW_CODE|
|MAINFRAME|
|MODERN_GENERAL_PURPOSE|
|SCIENTIFIC|
|SCRIPTING|
|SDI|
|TEMPLATING|
|WEB|

</details>

### System lifecycle management

Sigrid allows you to deactivate a given system.

The endpoint that enables such deactivation is:

- `PATCH https://sigrid-says.com/rest/analysis-results/api/v1/systems/{customer}/{system}`: enables setting the deactivation date for a system as the instant when this endpoint was called.

The request format is:

```json
{"deactivateNow": <deactivate_now>}
```

where the placeholder, `<deactivate_now>` can assume the following values:

- `{"deactivateNow": false}` : when setting the boolean value `deactivateNow` to false, the system will be viewed by Sigrid as being active, so, setting this value to false effectively marks a system as active and re-activates a previously deactivated system;

- `{"deactivateNow": true}` : when this value is true, the deactivation date for the system will be set using `Instant.now()` representing the current instant when the endpoint was called. This effectively deactivates a system from the moment the endpoint was called;

The response format on a successful request is, as an example, for SIG's `bch` system:

```json
{
    "name": "bch",
    "deactivationDate": "2017-12-03T00:00:00Z"
}
```

If the request body is not in the expected format, the returned response status will be: `400 BAD REQUEST`.

### System objectives

Sigrid allows you to define quality objectives for a system. This helps to set some realistic and feasible expectations per system, considering both the system's business context and its current technical state: business-critical systems using modern technologies require more ambitious targets than legacy systems.

<img src="../images/sigrid-objectives.png" width="500" />

Once you have defined quality objectives in Sigrid, you can [use these targets in Sigrid CI](../reference/client-script-usage.md#defining-quality-targets). You can also retrieve a system's objectives and corresponding targets via the API:

    GET https://sigrid-says.com/rest/analysis-results/api/v1/objectives/{customer}/{system}/config
    
This end point will return the following response structure:

    {
      "MAINTAINABILITY": 4.0,
      "NEW_CODE_QUALITY": 3.5,
      "OSH_MAX_SEVERITY": "LOW",
      "TEST_CODE_RATIO": 0.8
    }

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

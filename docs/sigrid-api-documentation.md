Sigrid API documentation
========================

In addition to [Sigrid CI](../README.md), Sigrid also provides a more general-purpose REST API that you can use to obtain analysis results from Sigrid. This allows you to integrate data from Sigrid into your workflow. 

## General usage

- The Sigrid API base URL is `https://sigrid-says.com/rest/api/clients`. 
- Authentication for the Sigrid API uses the same [authentication tokens](authentication-tokens.md) that are used by Sigrid CI. Your token's permissions are based on your user account, so the token can access the same systems that you can. 
- You need to pass the authentication token to each request in the HTTP header `Authorization: Bearer {SIGRID_CI_TOKEN}`.
- All end points will return HTTP status 401 if the token is invalid, or if the token is not authorized to access the portfolio and/or system.
- All end points return JSON and therefore return a Content-Type of `application/json`.

The following example shows how to call the Sigrid API using `curl`:

```
curl -D -  -H 'Accept: application/json' -H 'Authorization: {SIGRID_CI_TOKEN}' https://sigrid-says.com/rest/api/clients/{customer}
```

In the example, `{customer}` refers to your Sigrid account name, and `{SIGRID_CI_TOKEN}` refers to your authentication token.

## Available end points

### Maintainability ratings

`GET https://sigrid-says.com/rest/api/clients/{customer}`

Returns the maintainability ratings for all systems in your portfolio. The parameter `{customer}` refers to your Sigrid account name. 

Example response:

```
{
    "name": "my-sigrid-account-name",
    "systems": [
        {
            "name": "my-system-name",
            "clientName": "my-sigrid-account-name",
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

The top-level `maintainability` and `maintainabilityDate` refer to the *current* state of each system. The `allRatings` array contains a list of all *historic* measurements, which can be used for reporting or trend information.

### Security findings

`GET https://sigrid-says.com/rest/api/clients/{customer}/{system}/enrichedFindings`

Returns all security findings for the specified system. The parameters `{customer}` and `{system}` refer to your Sigrid account name and system ID respectively. 

Example response:

```
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

### Vulnerable libraries in Open Source Health

`GET https://sigrid-says.com/rest/api/clients/{customer}/{system}/open-source-health/vulnerable`

Returns all vulnerable open source libraries known to Sigrid. The output format is based on the [SBOM (software bill of materials)](https://en.wikipedia.org/wiki/Software_bill_of_materials) standard. The parameters `{customer}` and `{system}` refer to your Sigrid account name and system ID respectively. 

Example response:

```
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

More information on the SBOM format and the various fields is available from the [SBOM specification](https://github.com/CycloneDX/specification).

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

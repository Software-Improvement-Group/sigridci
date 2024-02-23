Adding business context to a system using metadata
==================================================

Adding business context to Sigrid makes it easier to interpret the results. For example, a below-market average maintainability rating of 2 stars might seem like a problem, but this depends entirely on the context. If the system is no longer actively maintained and will be decommissioned by the end of the year (i.e., its lifecycle phase is end-of-life, or EOL for short), such a rating might be perfectly acceptable. But if that system is new, uses modern technology, and is business critical, such a rating would be considered a red flag. In both cases the technical conclusion is identical, it's the context that determines the urgency.

Regarding ***Objectives***, see [our Objectives page](../capabilities/objectives.md)

This context information is called *metadata* in Sigrid. Adding metadata can be done in 4 different ways:

### Option 1: Adding metadata in Sigrid

This is by far the simplest approach: in Sigrid, simply go to the system settings option in the menu and select the "metadata" option. 

<img src="../images/metadata-ui.png" width="600" />

Note the screenshot only shows part of the metadata page. The full page contains options related to the context in which the system is being developed, such as *Business criticality*, *Lifecycle phase*, and *Deployment type*. All possible options can also be seen on the [Sigrid API metadata end point page](../integrations/sigrid-api-documentation.md#system-metadata).

They can be set with a drop-down menu. 

<img src="../images/metadata-lifecycle-phase-menu.png" width="400" />


<img src="../images/help-button.png" class="inline" /> The "?" help buttons explain the meaning of the different types of settings.

### Option 2: Using the Sigrid API to add metadata

The [Sigrid API end point for metadata](../integrations/sigrid-api-documentation.md#system-metadata) allows you to add metadata programmatically. This is less accessible than using the Sigrid user interface, but has the advantage that it can run automatically. This is typically used when you need to synchronize metadata from another system to Sigrid, and you want this to run in an automated way.

### Option 3: Adding metadata from a YAML file in your repository

As an alternative to using the API, you can also create a YAML file called `sigrid-metadata.yaml` in the root of your repository. The contents of this file are then used to update the metadata when the analysis runs. This is similar to using the API, but allows you to manage your Sigrid metadata as part of the repository in your version control system.

The following examples shows an example of a `sigrid-metadata.yaml` file:

```
metadata:
  displayName: "MyBank back-end"
  externalDisplayName: "MyBank component"
  divisionName: "My division"
  teamNames:
    - "My Team"
  supplierNames:
    - "Supplier 1"
    - "Supplier 2"
  lifecyclePhase: EOL
  inProductionSince: 2012
  businessCriticality: HIGH
  targetIndustry: ICD9530
  deploymentType: PUBLIC_FACING
  applicationType: ANALYTICAL
  externalID: ab12345
  isDevelopmentOnly: false
  remark: "Some notes"
```

The [Sigrid API documentation](../integrations/sigrid-api-documentation.md#system-metadata) contains descriptions of the various fields. Note that the semantics are the same: only fields present in `sigrid-metadata.yaml` are updated, others are left as-is. For example, the following `sigrid-metadata.yaml` file would _update_ the external ID and remove the current remark:

```
metadata:
  externalID: "ab12345"
  remark: null
```

The contents of the YAML file will be used to update the metadata whenever you publish your system to Sigrid. If you run Sigrid CI *without* publishing, i.e. when you run it for a branch or pull request, the metadata does *not* get updated. This ensures that publishing code and publishing metadata behave in a consistent way.

### Option 4: Adding metadata via Sigrid CI parameters

Metadata can also be configured by passing the metadata values as parameters when running Sigrid CI. This will dynamically generate the YAML file from option 3, but does not require you to commit this YAML file to your repository. 

- For all platforms, you can define environment variables to the Sigrid CI run. The name of the environment variables is the lowercase version of the metadata fields listed above. For example, defining the `applicationType` field in the YAML is equivalent to defining an environment variable named `applicationtype` as a Sigrid CI parameter.
- When using the Sigrid CI GitHub Action published to GitHub Marketplace, you can also provide these fields as input parameters instead of environment variables. The names are again lowercase, so the input parameter would be named `applicationtype`.

Note you can use the YAML file or environment variables, but not both. 

## System metadata fields and corresponding allowed values

The system metadata taxonomy used in Sigrid for adding business context to a system has a set of allowed values per field that need to match so that the context is correctly validated.

Each of the fields presented below can only assume a single value from the list of possible values shown:

| **Field name**                 | **Values**                                                                                                                                                                                                                                                                                                                      |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Software Distribution Strategy | "NOT_DISTRIBUTED", "NETWORK_SERVICE", "DISTRIBUTED"                                                                                                                                                                                                                                                                             |
| Application Type               | ["PROCESS_CONTROLLER","TRANSACTION_PROCESSING","RESOURCE_MANAGEMENT",<br>"CASE_MANAGEMENT","DESIGN_ENGINEERING_DEVELOPMENT","ANALYTICAL",<br>"AUTHENTICATION_AND_PORTALS","COMMUNICATION","FUNCTIONAL_APPLICATIONS",<br>"KNOWLEDGE_AND_DOCUMENT_MANAGEMENT","PERSONAL_PRODUCTIVITY_APPLICATIONS"]                               |
| Deployment Type                | ["PUBLIC_FACING","CONNECTED","INTERNAL","PHYSICAL"]                                                                                                                                                                                                                                                                             |
| Target Industry                | ["ICD0500","ICD1750","ICD2350","ICD2710",<br>"ICD2730","ICD2750","ICD2770","ICD2790",<br>"ICD2797","ICD3350","ICD3500","ICD3700",<br>"ICD4500","ICD5300","ICD5500","ICD5700",<br>"ICD6500","ICD7500","ICD7577","ICD8300",<br>"ICD8500","ICD8630","ICD8700","ICD9530",<br>"ICD9570","SIG2200","SIG1200","SIG1000",<br>"SIG1100"] |
| Business Criticality           | ["CRITICAL","HIGH","MEDIUM","LOW"]                                                                                                                                                                                                                                                                                              |
| Lifecycle Phase                | ["INITIAL","EVOLUTION","MAINTENANCE","EOL","DECOMMISSIONED"]                                                                                                                                                                                                                                                                    |
| Technology Category            | ["AGGREGATE","BPM","CUSTOMIZATION","CONFIGURATION",<br>"DATABASE","DSL","EMBEDDED","LEGACY",<br>"LOW_CODE","MAINFRAME","MODERN_GENERAL_PURPOSE",<br>"SCIENTIFIC","SCRIPTING","SDI","TEMPLATING","WEB"]                                                                                                                          |                                                                                                         |

### Meaning of special values for metadata fields

While several of the fields shown in the table above have self-evident values, some do not. As a reference, you can find the meaning of such fields detailed below:

<details>
  <summary>Lifecycle phases</summary>
  <div markdown="1">

The lifecycle phase identifiers have the following meaning:


|`lifecyclePhase` identifier|System lifecycle phase|
|---------------------------|----------------------|
|INITIAL|Initial development (pre-production)|
|EVOLUTION|Evolution (post-production)|
|MAINTENANCE|Servicing and maintenance|
|EOL|End-of-life (in production but minimal maintenance)|
|DECOMMISSIONED|Decommissioned / Phased out (no longer in production)|

</div>

</details>

<details>
  <summary>Target industries</summary>
  <div markdown="1">

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

</div>

</details>


<details>
  <summary>Deployment types</summary>
  <div markdown="1">

The deployment type identifiers have the following meaning:


|`deploymentType` identifier|Deployment Type|
|---------------------------|---------------|
|PUBLIC_FACING|A system that is accessible by users through the public internet|
|CONNECTED|A system that interacts with a public-facing system via the network. The system is not accessible via the public internet|
|INTERNAL|A system that can only be reached by users via VPN or the company intranet. The system has no interaction with public-facing systems|
|PHYSICAL|A system that can only be reached by users with access to a physical location. The system cannot be reached from an internal network and has no interaction with public-facing systems|

</div>

</details>

### Additional metadata fields

Besides the fields shown above, there is support for several additional fields to enrich the metadata of a given system.
These additional fields are free-text fields, in the sense that their values are not part of a specific set of values. However, there are some restrictions on the possible set of values for each of the fields, which are detailed in the table below:

| **Field name**      | **Values**                                                                                                                                         |
|---------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Display Name        | Free-text field containing the display name for the system (max. 60<br>characters long)                                                            |
| External Display Name| Free-text field containing the display name for the system (max. 60<br>characters long)                                                            |
| Division Name       | Free-text field containing the name of the division <br>this system is associated with (max. 60 characters long)                                   |
| Team Names          | A list where each element is a free-text field detailing the name(s)<br>of the team(s) that are involved with the system (max. 60 characters long) |
| Supplier Names      | A list where each element is a free-text field detailing the name(s)<br>of the supplier(s) of the system (max. 60 characters long)                 |
| In Production Since | Date in format YYYY detailing the year since the system is in <br>production (cannot be in the future)                                             |
| Is Development Only | Boolean value categorizing the system as being development only<br>or not                                                                          |
| Remark              | Free-text field containing any remarks about the system                                                                                            |

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

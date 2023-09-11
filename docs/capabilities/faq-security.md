Sigrid Security: Frequently Asked Questions
===========================================

This FAQ specifically covers Sigrid's security functionality. Also check the [Sigrid FAQ](faq.md) for more information about Sigrid in general.

## Security findings (ex. Open Source Health)

### Is it possible that Sigrid creates new findings without us changing the code?

Yes, in some cases. We are continuously extending our security knowledge base. Therefore, new findings are sometimes discovered in existing code. It might seem as a deterioration of the system's security. But actually it is a more accurate assessment of *security risk* in the system. 

### What statuses can security findings have?
See [Different statuses of security findings](system-security.md#different-statuses-of-security-findings).

### How does the automatic detection of "Fixed" findings work?
The status of a finding is automatically updated based on its "fingerprint". If a fingerprint is no longer found, the issue will be set to *Fixed*. If a new fingerprint is found, it will become a new finding.

The finding fingerprint is a calculated identifier based on multiple characteristics of the finding: analysis tool, rule, file name, and the line of code where the finding was located combined with the line before and after it. 

We use this approach to reduce the amount of busywork. Findings are automatically resolved to avoid situations where people fix something in the code, but then forget to update the finding in Sigrid. Moreover, multiple overlapping findings will automatically be merged if they have the same fingerprint. This means automatic deduplication, which is important for keeping the findings as actionable as possible.

### What are the risk thresholds for determining whether a risk is low-medium-high?
Findings are mapped on a scale from 0-10 based on a *CWE-CVSS* benchmark comparison. See the [explanation on CVSS in the security page](system-security.md#context-and-meaning-of-cvss-security-metrics-from-asset-to-risk) and [its different levels in Sigrid](system-security.md#cvss-scores-in-sigrid).

## Open Source Health

### Does Sigrid support transitive dependencies?
Yes. This is configurable. Scanning transitive dependencies is preferable from a security perspective, as vulnerabilities in transitive dependencies may be equally problematic as vulnerabilities in direct dependencies. However, it does introduce nuances: transitive dependencies might not actually be callable because they are somehow inactive. As a steering mechanism it may seem unfair to some teams, since the transitive dependencies are not within their direct control. 

Therefore, scanning transitive dependencies can be enabled or disabled in [the analysis configuration](../reference/analysis-scope-configuration.md#open-source-health). 

### Why does the finding list count certain findings twice?

The findings list indicates *compliance*. Sometimes a single finding on a vulnerable library has multiple vulnerabilities in multiple categories (e.g. injection and XXE). In that case these are counted separately in the list. However, despite the finding appearing in multiple categories, it is still the same finding. It only counts as a single finding towards the total, and resolving the finding will resolve it towards all categories.

### What technology is Open Source Health based on?

Open Source Health is proprietary SIG technology where we combine 20+ different ecosystems. Examples are *Sonatype OSS Index*, *NVD*, *Google OSV*, and the *GitHub Security Advisory API*. Depending on the technology, this will analyze dependency management files (e.g. `pom.xml` or `package.json`), library source files (e.g. `jquery-3.6.1.js`), and binary library files (e.g. `log4j.jar`).

Open Source Health offers the option to create an SBOM (Software Bill Of Materials) report, either through the Sigrid user interface or [through the Sigrid API](../reference/sigrid-api-documentation.md#vulnerable-libraries-in-open-source-health).

### Does SIG filter when resolving our system's dependencies?

SIG can filter dependency checks for internal dependencies to avoid exposing internal names, but they must be configured manually by SIG. [See the Open Source Health paragraph in our scope configuration document](../reference/analysis-scope-configuration.md#open-source-health). Please inform SIG of such dependencies and their name conventions before onboarding.

### Why are some Open Source vulnerabilities missing a CVE?

SIG gathers data from multiple ecosystems. Most of these ecosystems link library vulnerabilities to CVEs, but some provide their own data that is not connected to CVEs.

### What are the risk thresholds that determine low-medium-high risk?

They are shown as a mouseover on the Open Source Health page in the top tile that summarizes risks. See the [open-source health page](system-open-source-health.md#navigating-the-overview-page).

### I previously marked a security finding in an open source library as a false positive, but now it is back?

Open Source Health produces security findings for the version of the open source library you are currently using. If you update the version, but that new version still contains the same issue, the finding will automatically be reopened. If you update the open source library to a version that no longer contains the issue, the security finding in Sigrid will automatically be marked as *"Fixed"*.
    

### We have a lot of (new) security findings. What should we do first?
Please see [elaboration on such strategies in the system-level security page](system-security.md#a-general-typical-strategy-for-processing-security-findings), or [specifically the paragraph on filtering security findings](system-security.md#filtering-results-for-false-positives-starting-with-open-source-vulnerabilities).

### To what extent does SIG provide consultancy for security findings?

This depends on your agreement with SIG, which can differ per system: 

- **Fully automated findings:** You will always receive frequent new findings from the scan tools built into Sigrid. Much expertise of SIG is constantly going into the selection and configuration of these tools and the rules they apply. This includes the smart software that provides as much useful information about the finding, including links to various resources with more information. 
- **Manual refinement:** This service provides interpretation, selection and enrichment of  tool findings by SIG experts. SIG experts remove false positives as much as possible. Where necessary, risk levels are changed. In addition, the SIG experts add remarks to the findings, with interpretation details and when relevant some mediation advice.
  - How far does SIG advisory go when it comes to findings refinement?
    - We offer first tier security coaching for findings. This means we do the most what we can from our side through the finding remarks. In addition, clients can ask questions in scheduled workshop moments or through e-mail. 
    - The model is that training of personnel and second tier hands-on security coaching is to be organised by the client. When required, SIG can assist.
    - In case you believe that remarks can be more helpful: please  provide examples of where you believe this is the case. We want to offer useful guidance as well as we can.
- **Manual code review:** This service provides reviewing design, configuration and code for findings that cannot be detected by scan tools - typically involving the interpretation of logic, in context. The results are added into the Sigrid finding workflow.

### What about security risk assessment and threat modeling?

These should indeed be considered requisites for dealing with security findings effectively. Please see our elaboration [on the system security page](system-security.md#threat-modeling-as-a-requisite-for-interpreting-security-findings).

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.


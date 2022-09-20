Sigrid Security: Frequently Asked Questions
===========================================

This FAQ specifically covers Sigrid's security functionality. Also check the [Sigrid FAQ](faq.md) for more information about Sigrid in general.

### How do you track if a finding has been fixed?

Finding status is automatically updated based on  its "fingerprint". If a fingerprint is no longer found, the issue will be set to Fixed. If a new fingerprint is found, it will become a new finding. A fingerprint is calculated from multiple fields: analysis tool, rule, file name, and the ine of code where the finding was located, combined with the line before and after it. 

### What status can findings be in?

- **Raw:** Initial status when a finding is first created by Sigrid.
- **Refined:** Indicates a finding has been interpreted by an expert.
- **False positive:** Indicates the finding is invalid, and does not actually pose any risk.
- **Will fix:** Indicates the finding should be fixed. This is different from the "refined" status, in that some findings must be fixed while others can remain open as the risk is deemed acceptable.
- **Fixed:** The finding no longer poses any risk. This status can be assigned by Sigrid if a previous finding is no longer found in subsequent scans. 

### Is it possible that new findings are created without changing the code?

Yes, in some cases. SIG is continuously extending our security knowledge base, which means that new findings are sometimes discovered in existing code. This can feel unfair to some teams, but it's important to realize that Sigrid indicates *risk* in the system. In other words, when a new finding is found it doesn't necessarily mean the team did something wrong, it simply means a new risk was discovered and needs to be addressed.

### Does Sigrid support transitive dependencies?

Yes, but this is configurable. Scanning transitive dependencies is preferable from a security perspective, as vulnerabilities in transitive dependencies are equally problematic as vulnerabilities in direct dependencies. However, to some teams this can see unfair, as the transitive dependencies are not within their control. 

Therefore, scanning transitive dependencies can be enabled or disabled in [the analysis configuration](analysis-scope-configuration.md). 

### Why are findings counted double sometimes in the finding list?

The finding list is to indicate compliance. Sometimes a single finding on a vulnerable library has multiple vulnerabilities in multiple categories (e.g. injection and XXE). In that case these are counted separately in the list, but as one in the totals dashboard.

### What technology is Open Source Health based on?

Open Source Health is proprietary SIG technology where we combine 20+ different ecosystems. Examples are Sonatype OSS Index, Google OSV, and GitHub security advisories. Depending on the technology, this will analyze dependency management files (e.g. `pom.xml` or `package.json`), library source files (e.g. `jquery-3.6.1.js`), and binary library files (e.g. `log4j.jar`).

Open Source Health offers the option to create an SBOM (Software Bill Of Materials) report, either through the Sigrid user interface or [through the Sigrid API](https://github.com/Software-Improvement-Group/sigridci/blob/main/docs/sigrid-api-documentation.md#vulnerable-libraries-in-open-source-health).

### Why are sometimes Open Source vulnerability entries without a CVE?

As indicated in the previous question, SIG gathers data from multiple ecosystems. Most of these ecosystems link library vulnerabilities to CVEs, but some provide their own data that is not connected to CVEs.
    
### To what extent does SIG provide consultancy for security findings?

This depends on your agreement with SIG, which can differ per system: 

- **Fully automated findings:** You will always receive frequent new findings from the scan tools built into Sigrid. Much expertise of SIG is constantly going into the selection and configuration of these tools and the rules they apply. This includes the smart software that provides as much useful information about the finding, including links to various resources with more information. 
- **Manual refinement:** This service provides interpretation, selection and enrichment of  tool findings by SIG experts. SIG experts remove false positives as much as possible. Where necessary, risk levels are changed. In addition, the SIG experts add remarks to the findings, with interpretation details and when relevant some mediation advice.
  - How far does SIG advisory go when it comes to findings refinement?
    - We offer first tier security coaching for findings. This means we do the most what we can from our side through the finding remarks. In addition, clients can ask questions in scheduled workshop moments or through e-mail. 
    - The model is that training of personnel and second tier hands-on security coaching is to be organised by the client. When required, SIG can assist.
    - In case you believe that remarks can be more helpful: please  provide examples of where you believe this is the case. We want to offer useful guidance as well as we can.
- **Manual code review:** This service provides reviewing design, configuration and code for findings that cannot be detected by scan tools - typically involving the interpretation of logic, in context. The results are added into the Sigrid finding workflow.

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.


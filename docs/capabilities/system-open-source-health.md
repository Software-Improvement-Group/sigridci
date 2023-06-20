# System-level Open Source Health

## Analyzing security findings: Open Source Health example
If you click on the finding, the source code of the finding will be shown with its details. 
<img src="../images/system-security-maven-finding-detail-sshd-search.png" width="600" />

In case that the relevant line is not highlighted in yellow (this sometimes occurs in package management files), you can search within the file with cmd+f/ctrl+f. By default your browser takes precedence for this shortcut and therefore will try to search the page. You therefore need to move mouse focus to the left pane by clicking on the source code area or tabbing to the element first. You can use regular expressions if you wish so. 

On the right side of the page, all details surrounding the finding are shown. If available, the relevant *CWE* will be shown. This is part of the authoritative list of weakness types known as the *"Common Weakness Enumeration"* by MITRE [MITRE CWE website](https://cwe.mitre.org/). The CWE link in the security finding will refer you to the [OWASP CRE page](https://www.opencre.org/) of which SIG has been an active contributor. It is an open source, OWASP supported reference knowledge base that links all sorts of relevant, authoritative security reference documents and their explanations. 

With the buttons in the top right, you can edit the finding or show the code in the  *"Code Explorer"*, which will show you code context. See also [Code Explorer](code-explorer.md). 

<img src="../images/system-security-pom-dependency-edit-finding.png" width="300" />

In this case, because this is an automatically scanned dependency by [Open Source Health](system-open-source-health.md), e.g. changing its status to "false positive" will not necessarily remove the finding indefinitely. As long as the OSH tooling finds the same result, it will return. See also [this specific case in the Security FAQ](faq-security.md#i-previously-marked-a-security-finding-in-an-open-source-library-as-a-false-positive-but-now-it-is-back).

An audit trail can be seen when clicking the *"Show Audit Trail"* button. In case of changes, multiple entries will be shown with their respective usernames and dates.

<img src="../images/system-security-audit-trail.png" width="300" />
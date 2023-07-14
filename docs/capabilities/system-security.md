# System-level Security

System-level security is one of the detailed technical views under *Findings*. This may be available for your system. It depends on which capabilities have been activated specifically for your system or portfolio. 

## Reaching the Security page
You can reach the system-level security view in different ways: Via the top menu, clicking a capability on the System or Portfolio *Overview* pages, or clicking on a system from the Portfolio security view. See  [the system-level Overview page](system-overview.md#navigating-to-capabilities), [navigating from the portfolio-level Overview page](portfolio-overview.md#navigating-to-capabilities) or [navigating from the portfolio security view](portfolio-security.md#moving-from-portfolio-level-to-system-level).

The tooling underlying this analysis is updated as often as possible. Therefore it may be possible that [new findings are found even when code is unchanged (link to FAQ)](faq-security.md#is-it-possible-that-sigrid-creates-new-findings-without-us-changing-the-code).


## Navigating the Security Overview
The security overview page shows a summary of findings, their change, age and estimated severity. In this example, 

<img src="../images/system-security-overview.png" width="600" />

The different elements in this page are:
* *Findings* shows a count of *the current number of findings*. Below it is the number of changes, based on the source code comparison period. This range be changed in the top right as usual. The note *"Also showing ... resolved findings and ... informational findings"* means that on top of this number, more findings are shown below. This is relevant for estimating activity surrounding these findings, such as fixing security findings or marking them as *false positive*. 
* *Activity* shows a breakdown of this number. A mouseover on the *Activity* barchart will show the following:

<img src="../images/system-security-activity-mouseover.png" width="300" />

* The *Findings Age* tile gives an indication how long findings are known. 


### The scoring system with CVSS: background
* The *CVSS Severity* tile summarizes a breakdown of findings according to CVSS severity ratings. A mouseover on the barchart will show the exact number of findings. A mouseover on the CVSS severity benchmark shows the CVSS security score and the number of findings with that severity. *CVSS* (*Common Vulnerability Scoring System*) is a security-industry standard on a 0-10 scale, developed by [NIST](https://nist.gov/), specifically its [National Vulnerability Database(NVD)](https://nvd.nist.gov/). CVSS scores are based on a benchmark of expert judgements and a well-defined calculation that estimates risk (see [NIST's current 3.1 calculator](https://nvd.nist.gov/vuln-metrics/cvss/v3-calculator/) or a [calculation preview of the to-be-released CVSS 4.0](https://www.first.org/cvss/calculator/4.0/)). Note that version 2 did not include a *"Critical"* vulnerability category.


### CVSS scores in Sigrid
<img src="../images/system-security-cvss-mouseover.png" width="500" />

<img src="../images/filter-2.png" class="inline" /> The CVSS map adjusts to the filter that you may have used.

Based on the CVSS score of findings, they are marked and colored ranging from "Information", "Low", "Medium", "High", "Critical".
<img src="../images/system-security-icon-information1.png" class="inline" /> *Information*: a CVSS score of "0". These include anti-patterns that may not have a direct security impact but can still be significant. 

<img src="../images/system-security-icon-low1.png" class="inline" /> *Low*: CVSS score between 0 and 3.9.

<img src="../images/system-security-icon-medium1.png" class="inline" /> *Medium*: CVSS score between 4 and 6.9.

<img src="../images/system-security-icon-high1.png" class="inline" /> *High*: CVSS score >between 7 and 8.9. 

<img src="../images/system-security-icon-critical1.png" class="inline" /> *Critical*: CVSS score 9 or higher. 



## Different statuses of security findings
These are the different statutes of findings. The status *"Fixed"* will be applied automatically if a finding is resolved. See [FAQ:Fixed issues are auto-detected](faq-security.md#how-does-the-automatic-detection-of-fixed-findings-work). The other statuses can be set. They are similar to those used for [system maintainability refactoring candidates](system-maintainability.md#refactoring-candidates). 
* *"Raw"* means "not yet verified" where *"Refined"* ones mark that a finding has been confirmed manually. Inversely, a finding can be set as *"False positive"*. 
* *"Will fix"* signals the intention to fix it, while *"Risk Accepted"* does not.

## Different possible grouping of security findings
Different views can be selected in the left menu. security models. The menu selector on the left you to easily toggle between the different models in one view. 

<img src="../images/system-security-grouping-finding-status-ex-background.png" width="250" />

Note that here, the menu's category in bold is the currently chosen grouping. Therefore, below, under the column *"Description"*, different statuses are shown. Because *"Grouping"* means that Sigrid will show you a summary, the number of findings are shown on the right column under *"Findings"*, such as [C]1, [H]1, [M]99+ and [I]99+. These abbreviate the severity of the findings based on their CVSS score, and their count. You can click on those for a listing of the detailed findings. See also the [CVSS elaboration above](#the-scoring-system-with-cvss).

In the Grouping menu in the top left under *"Finding"*, the following types of grouping can be set:

* *"Activity"* groups according to *"New"*, *"Recurring"* or *"Resolved"*.
* *"Origin"* refers to the originating tool of the finding.
* *"Severity"* orders on level of severity (based on CVSS).
* *"Status"* lists the statuses as [mentioned above](#different-statuses-of-security-findings).
* *"Type"* shows a specific list of vulnerabilities. This is especially useful for technical analysis, since sometimes, a whole category/type of findings may be set to *"False positive"*. 
* *"Weakness"* orders on type of weaknesse (based on [MITRE's *CWE* database](https://cwe.mitre.org/)). Weaknesses are defined somewhat higher level than *"Type"*. 

<img src="../images/system-security-grouping-location-ex-background.png" width="250" />

In *"Location"*, either *"Component"* or *"File"* grouping can be chosen. The Component group follows the maintainability grouping in components. Findings may fall outside of that grouping because of exclusions. Then they will show under the *"Other"* component. Examples might be binaries or package manager configuration files, which would be excluded for maintainability analysis and therefore not fall into a component for the purpose of maintainability calculations. 

<img src="../images/system-security-grouping-model-ex-background.png" width="250" />

Under *"Model"*, different Models can be used to map findings on. This is in practice mostly a matter of preference or specific auditing requirements. Next to popular security models, SIG has developed its own model based on the ISO 25010 standard, which can also be chosen. These are based on the [SIG Evalution Criteria Security][https://www.softwareimprovementgroup.com/wp-content/uploads/SIG-Evaluation-Criteria-Security.pdf].

### A note on seeing the same file/finding multiple times
* **A specific finding** is counted once, but it may be visible in multiple views. This could be because e.g. there is certain overlap in classification of the model that you have chosen as a view. 
* **A specific line** may be counted multiple times if it refers to multiple *CWEs*: a count is applied for each possible security risk. See also [security FAQ elaboration on multiple views of the same finding](faq-security.md#why-does-the-finding-list-count-certain-findings-twice).  


## Analyzing security findings
You can group and sort the detailed view of security findings. The sorting offers you the following.  

<img src="../images/system-security-sorting-menu.png" width="150" />

Below an example of a list of detailed findings. 

<img src="../images/system-security-overview-no-grouping-sorting-status.png" width="600" />

In the top left you can see that the findings are not grouped. Therefore each finding is shown individually. Below, the *"Grouping"* menu under *"Sorting"*, sorting is set to CVSS severity. Therefore the highest risk findings are shown above. Note that for example the first two findings are Maven dependencies. These originate from [Open Source Health](system-open-source-health.md). 

If Remarks have been registered, they can be seen in the far right column with a mouseover or clicking on the text balloon. An example of a mouseover is shown here. 
<img src="../images/system-security-osh-remark-mouseover.png" width="500" />

If you click on the finding, the source code of the finding will be shown with its details. Details such as Status, finding age, Origin (scanning tool), File location, Remarks (if available) or audit trail are all viewable here.
<img src="../images/system-security-security-os-inj-example-detail.png" width="600" />

In the left panel, the specific line is highlighted in yellow, where a possible vulnerability may exist (in this case, OS injection). For details on e.g. the right panel, see [Open Source Health-analysis section](system-open-source-health.md#analyzing-security-findings-open-source-health-example). Extra information such 

## Analyzing security findings: Dependency example (based on Open Source Health)
As above, starting from the findings overview: if you click on the finding, the source code of the finding will be shown with its details. 
<img src="../images/system-security-maven-finding-detail-sshd-search.png" width="600" />

In case that the relevant line is not highlighted in yellow (this sometimes occurs in package management files), you can search within the file with cmd+f/ctrl+f. By default your browser takes precedence for this shortcut and therefore will try to search the page. You therefore need to move mouse focus to the left pane by clicking on the source code area or tabbing to the element first. You can use regular expressions if you wish so. 

On the right side of the page, all details surrounding the finding are shown. 

## Changing a finding's status and audit trail

<img src="../images/edit-inverted.png" class="inline" /> In the top right, the *Edit Finding* button allows you to change e.g. its Status and Severity 

In this case, because this is an automatically scanned dependency by [Open Source Health](system-open-source-health.md), e.g. changing its status to "false positive" will not necessarily remove the finding indefinitely. As long as the OSH tooling finds the same result, it will return. See also [this specific case in the Security FAQ](faq-security.md#i-previously-marked-a-security-finding-in-an-open-source-library-as-a-false-positive-but-now-it-is-back). The same holds for the *"Remark"*. Findings by *Open Source Healt*h* automatically add the type of vulnerability and vulnerability (CVE) reference. Remarks can also be adjusted manually. Any user can edit remarks or other characteristics. This could also be a SIG consultant, depending on your specific Sigrid agreement. 

An audit trail can be seen when clicking the *"Show Audit Trail"* button. In case of changes, multiple entries will be shown with their respective usernames and dates.

<img src="../images/system-security-audit-trail.png" width="400" />

## CWE and its link with CRE (Common Requirement Enumeration)
If available, the relevant *CWE* will be shown. *CWEs* are part of the authoritative list of weakness types known as the *"Common Weakness Enumeration"* by MITRE [MITRE CWE website](https://cwe.mitre.org/). The *CWE* link in the security finding will refer you to the [OWASP Common Requirement Enumeration (CRE) page](https://www.opencre.org/). This will show the CWE in context. SIG has been an active and proud contributor to this project in close collaboration with the world's application security authority [*OWASP* (Open Worldwide Application Security Project)](https://owasp.org/). *CRE* is an open source security reference knowledge base, [a nexus between *OWASP's* initiatives](https://owasp.org/projects/#owasp-projects-the-sdlc-and-the-security-wayfinder) and relevant, authoritative security reference documents originating in [MITRE](https://www.mitre.org/), [NIST](https://www.nist.gov/) and [ISO](https://www.iso.org/). 

An example of openCRE is shown below.

<img src="../images/opencre-example-cwe308.png" width="600" />

## Linking to Code Explorer
On the top right you can show the code in the *"Code Explorer"*, which will show you the code's context and related findings. See also [Code Explorer](system-code-explorer.md). 

<img src="../images/system-security-pom-dependency-edit-finding.png" width="400" />

## Your strategy for processing security findings

In general, processing scan findings includes cleaning the results from false positives, adding priority, and writing explanations or recommendations. You may take different strategies that depend a lot on organizational context.

* Probably you want to start with *"Open Source Health"* because they are regularly high-risk and urgent, yet relatively easy to solve. That has a high return on your efforts. Also, grouping the same libraries/frameworks may be favorable because you only need to go through release notes once. This might be harder if you need to cross teams to do that.
  * Any occurring *possible legal risks* (e.g. GPL) are important to discuss with your legal department. These legal license risks tend to apply only in specific cases, e.g. when you have modified the source code. SIG explicitly cannot help you with legal advice. 

* To get an *overview* of findings and to be able to make quick exclusions of false positives, it may be useful to order security findings by *component/file* [see above](#different-grouping-of-security-findings). A file-view may expose e.g. test-code, and a component-view may show that many files may lay in a certain functional domain (e.g. deployment). This may lead to a lot of exclusions and a cleaner overview of security findings. In the *File view* you can export findings as a spreadsheet. In case of very large lists of findings it may be advantageous to browse and filter in a spreadsheet editor, and then go back and exclude them (by groups). 
  * A tactic during sprints is to use a kind of *Boy Scout* approach, where you compare findings for files while you are modifying them. This tends to be efficient because you are already working in/analyzing the code. You may consider to make this part of the Definition of Done.
* *Prioritizing by severity* is the typical approach, and this is faithful to agile practices (assuming you choose the action with the highest return first). This way you move from urgent to less urgent findings.
* Prioritizing based on grouping by patterns means that you may exclude or solve many findings in one go. There are indeed cases when a whole class of findings can be excluded because for some reason the findings are not applicable or can be resolved in one place.

### SIG consultancy helping with security
Depending on your agreement with SIG, security expertise consultancy may be available. See also [this question in the security FAQ](faq-security.md#to-what-extent-does-sig-provide-consultancy-for-security-findings).







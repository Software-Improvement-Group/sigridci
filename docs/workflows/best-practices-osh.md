# Best Practices for Open Source Health (OSH)

<!-- 
- TODOs 
  - consider how to use context/meta-information to refine policies?
  - make sure duplication is avoided as much as sensible by cross-referencing to sections.

-->

<details>
<summary>Input documents used</summary>
Proposed goal: The Sigrid documentation should be the single source [of truth] of knowledge about Sigrid, the quality models, and SIG Best Practices, thus replacing most of these documents.

Exceptions are SIG and customer confidential information and slidedecks that are (really) needed for presentations.
This means that examples that are derived from customer systems, or that expose internal detail about the benchmark need to be written down elsewhere (for now in the wiki).
 
- [Sigrid documentation](https://docs.sigrid-says.com/)
- [Internal software development guidelines from SIG Development team](https://softwareimprovementgroup.atlassian.net/wiki/spaces/ISMS/pages/50314183293/ISMS+P16.+Software+Development)
- OSH model slides (Open with Powerpoint--New from template)
  - there are almost no explanatory slides for OSH in the PPT slide templates (only one overview and 2 templates for findings)
- ["How to interpret OSH findings" wikipage](https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings)
  - See also the License Risk Evaluation Framework slide at the bottom of the wiki page: [OSH interpret results wikipage](https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings)
- ["OSH quality model" wiki page](https://softwareimprovementgroup.atlassian.net/wiki/spaces/DEL/pages/50594021377/Open+Source+Health+Quality+Model) 
- [Sigrid guidance for producers](https://docs.sigrid-says.com/reference/quality-model-documents/open-source-health.html)
   - we should be consistent with this; e.g. when setting default targets?
- [Library Management Practices](https://softwareimprovementgroupcom.sharepoint.com/:p:/r/sites/Internalprojects/SEF/Shared%20Documents/Input/20200526_LibraryManagementBestPractices.pptx?d=w2d1b408f0aab4c6182fcd3f055020926&csf=1&web=1&e=LMfkRh)
- [DPA V4 documentation](https://softwareimprovementgroupcom.sharepoint.com/:p:/r/sites/Deliveryprojects/P20140006BestPracticeEvaluationFramework/Shared%20Documents/Training/2023-DPA-V3-V4-introduction-long.pptx?d=w8b589f9f0eaf4201b2e1d5d7299b7e17&csf=1&web=1&e=tigu97) 
- ...
  
---
</details>  

> NOTE: This document is a collection of the knowledge that we have accumulated within SIG on the best practices for achieving Open Source Health. Its purpose within SIG is to have all this knowledge documented in one place, such that we have a shared base as consultants, and also a document that we can share with customers that are in search of concrete advice on how to get things in place for healthy open source usage. 


## Introduction

The purpose of this document is to provide concrete and actionable guidelines, hints and tips on how to achieve healthy use of open source libraries in your application. 
This covers how to get started, how to stay in control, and how to act when health deteriorates. 
Where applicable, we explain how Sigrid can be used to achieve this.



## OSH Jobs to be done

The guidelines and best practices have been structured based on the concept of 'jobs to be done': the idea is to look at the actual tasks that stakeholders need to conduct, and provide them with help to do those tasks. Jobs can embed/refer to other tasks.

These jobs have been grouped in three categories: first some incidental jobs; typically tasks that are required to start up a healthy open source usage in development, that may need to be revisited or updated on a regular basis. Secondly the various types of tasks that are needed to ensure continued health of libraries (note that even when application code is not actively maintained for a while, the health of open source libraries may diminish!). And thirdly a set of practical tasks in handling libraries as a developer.


#### Incidental Jobs
1. Define OSH related policies
2. Implement usage of a package manager
3. Improving portfolio and system-level OSH
4. Setting up Sigrid OSH


#### Ensuring health of libraries

5. Scan the software for issues
6. Handling detected vulnerabilities
7. Handling detected license issues
8. Handling detected lack of freshness
9. _Handling detected lack of activity_ (TBD)

#### Handling libraries

9. Updating a library [New library version available]
10. Adopting a new library
11. When a library does not support requirements
12. When a bug is detected in a library
13. _Compatibility break_ (TBD)

## The OSH model
The SIG Open Source Health model is described in the following places:
- The Sigrid documentation contains the [OSH guidance for producers](https://docs.sigrid-says.com/reference/quality-model-documents/open-source-health.html)
- Wiki page "How to interpret OSH findings"
- "OSH quality model" wiki page
- And now the guide for producers is also in the Sigrid documentation
- [And would benefit from a nice integration..]
- The benchmark risk categories should inform (be consistent with) the methodology, similar for the guidance for producers.


## Guidelines for Jobs to be done:
In this section, we are describing guidelines, hints and tips on how to achieve healthy use of open source libraries in your application. Where applicable, we explain how Sigrid can be used to achieve this.


### 0. General guidelines for your application development
There are a number of topics to consider that are not directly related to which libraries you use, but how you organize the development of the application itself.

The following guidelines should be considered as compliance rules for framework and library management (comply or explain):​

#### Keep application source code separate from frameworks/libraries​.
1. _Do not change the source code of used frameworks/libraries._
2. _Do not add project or organization specific headers._ 
    > [LB: to what??? to the source code of libraries or frameworks?]​
3. _Use only a single version of each library or framework​._


#### Regression tests and maintainability of the application code are key to updating frameworks/libraries​
If it is hard to update a library, chances are the problem lies in your codebase.​
1. _Keep module coupling and component independence low_, to make it easier to change code implementation (such as dealing with new versions of a library) while keeping the same behavior/requirements.
1. _Develop, maintain and run regression tests._ These help to identify breaking changes in updates.​​


### 1. Define OSH related policies for development
There are a number of policies on how to address open source libraries during development. For most of these policies, minimal requirements should be set for all teams; individual teams may agree on more stringent rules. 
1. _Declare which libraries are allowed to be used_
   - Create an _allow-list_. This list requires CISO approval. The allowlist must be reviewed regularly (a few times per year): define when this review will happen.
   - For determining whether to include libraries, see the criteria defined in the section [Adopting a new library](#adopting-a-new-library).
2. _Define the usage of a package manager_: this requires choosing preferably one per technology 
   > (+communicate to developers, + embedding in the pipeline?). 
3. _Set the thresholds for library risks_ that are (not) acceptable: this is applicable to all types of risks. 
   - These goals can be set in the [Sigrid objectives](#TBD)
   - Goals for the amount of and allowed types of vulnerabilities
   - Goals for library freshness. e.g. in terms of time since a new version has been released, or the maximum number of versions you may stay behind.
4. _Define how frequent to check for risks_ such as vulnerabilities and other risks in open source libraries
5. _Define how fast new vulnerabilities have to be resolved_; this will depend on the criticality. See the section on [Handling detected vulnerabilities](#6-handling-detected-vulnerabilities) for details.



### 2. Implement usage of a package manager
- depends on technology: do we have suggestions?
- what if your technology does not come with a package manager?


### 3. Improving portfolio and system-level OSH
- In case a package manager is not used, or only partially, this is a good topic to start with, since it will make the other improvement steps easier, faster, and less error-prone.
> TODO: should we advise to compile a portfolio-level overview of which libraries are used, and conduct an assessment of each library (independent of its context) regarding the risks? it can make sense (and it is a practice at some organizations) to have a set of 'approved'/white-listed libraries--sometimes only those are allowed to be used.
- First focus on vulnerabilities
  - do a threat analysis to prioritize the systems that are most risk-prone to security attacks
    - e.g. public-facing systems first 
    - systems dealing with the most sensitive data
  - Focus on removing all high risk vulnerabilities first
- Secondly, consider legal risks due to licenses: 
  - This is often an important part of due diligence when a product or organisation is being considered for take-over.
  > TODO are there any heuristics on where best to start/what to prioritize? 
- For the other properties: 
  - investigate the risks of heavily outdated and perhaps no longer maintained libraries: Make sure to look at the product lifecycle, end-of-support date and maintenance activity. 
  - Do an impact analysis and plan the needed effort to mitigate the risks. This can be -a series of- updates, or complete replacement of a library. 
  - ​​Opensource dependencies can be compared in terms of activity on tools like [https://www.openhub.net/](https://www.openhub.net/)​
  - Looking at the bug reports of inactive libraries, and the fixed bugs or improvements of outdated libraries can give good information of the relevance of updating.
- When many libraries require (multiple or major) version updates, the level of test coverage of a system can be used to prioritize systems that involve fewer risks for undetected defects due to incompatible updates.  

- Where to start/how to tackle OSH techdebt incrementally
  

### 4. Setting up Sigrid OSH
-  Define  Sigrid objectives
  - Portfolio/System



### 5. Scan the software for health issues
- Frameworks and libraries should be scanned frequently (preferably daily, but no less than every 3 months) to make sure there are no severe vulnerabilities in them.
- Use Sigrid to continuously review libraries:
  - For existence of known vulnerabilities.
  - For acceptable license
  - For up-to-date-ness (freshness)
- When to use the scan results: 
  - Do triaging during refinement. You need to decide if libraries need to be updated during the upcoming sprint, either because vulnerabilities have been found or because the team agrees it is falling too far behind the latest version. 
  Likely actions:
    - [Updating a library](#updating-a-library) 


### 6. Handling detected vulnerabilities
Security risks of a certain framework or library should be determined based on at least the following aspects: 
​- The severity level of known vulnerabilities for the artifact​
- The mission of the components where the framework or the library will be applied​: Non mission critical / ​Mission ​critical
- The outside visibility: ​External Facing or Distributed​ 
  > [? is this the right classification?]
  - public facing systems need to be tackled first, and should not have any  vulnerabilities of risk category _high_ and higher.

When a vulnerability is found, it will be remediated within a specified time period.
  The table below is a suggestion how to specify this, depending on the criticality of the system:
  | CVSSv3 Range | Label | Remediation Deadline Critical | Remediation Deadline Regular |
  | --- | --- | --- | --- |
  | 9.0 – 10.0 | Critical | Within 1 working day | Within 1 working day | 
  | 7.0 – 8.9 | High | Within 14 days | Within 30 days |
  | 4.0 – 6.9 | Medium | Within 60 days | Within 90 days |
  | 0.1 – 3.9 | Low | Within 1 year | Within 1 year |
  > TODO: check that the above table makes sense, especially the added last column..

- If no remediation is available, do a risk assessment which will have one of 3 outcomes:
  - If we find that the vulnerability does not pose any actual risk, we will ‘allowlist’ it. This requires CISO approval. This allowlist will be reviewed as part of the half-yearly measurement cycle.
  - We will mitigate the risk in some other way. If, for example, we do not want to allowlist. the entire library because of its importance but the vulnerability is limited to a single method, we can test for the use of that method and fail the pipeline in that case.
  - [In](http://3.in/) extreme cases, we will shut down the application until the vulnerability is resolved.
  - note: when addressing the vulnerabilities of a specific library by updating to a newer version, that always also improves the freshness
  
### 7. Handling detected license issues
- Libraries must have an acceptable license.
  - This may be a paid license or an acceptable open-source license. [Company] maintains a list of common licenses used in free and open-source software (FOSS); if a library has a license listed as acceptable, it can be used. Otherwise, see if an alternative is available, or contact the [applicable role] to discuss whether the license is acceptable.
- See also the License Risk Evaluation Framework slide at the bottom of the wiki page: [OSH interpret results wikipage: https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings](https://workflowy.com/#/c9c4745b6b6b)
- Note that the risk depends on the context: 
  - e.g. when developing open-source software, more licenses are acceptable.
  - it also depends on how you use a library: it is sometimes needed/a solution to wrap the library in an executable component that can be used by calling, instead of becoming a part of the codebase.

### 8. Handling detected lack of freshness
- The teams are responsible for keeping libraries reasonably up to date: 
  - small library updates can be updated as part of regular maintenance; 
  - larger updates (e.g. major versions or frameworks) should be planned explicitly as part of a development sprint.



### 9. Updating a library
There can be several reasons to consider updating a library.

Checklist before updating:
- Does it have open issues?​
- Is the license (still) compatible?​
  - --> [Handling detected license issues](#handling-detected-license-issues)
- Does it contain optimizations for performance, maintainability, functionality?​
  - ? not sure why this is exactly asked?
- Is the new version compatible?  ​
- How mature is the version?​
- Is it stable enough?​

Always Manage libraries with a package manager (don’t mix third party code with first party code)​

- compatibility break
  - Compatibility breaks can be caused by the framework/library no longer supporting the technologies used in the system.​
  - Analyze the impact and consider the following things:​
  - What is the impact of updating the system to make it compatible?​
  - Are there alternatives of the library?​
  - Are the technologies used still relevant for the future of the system?​

- when is postponing updates a good idea?
  - The longer you postpone updating, the bigger the eventual pain. As your system grows and evolves, the costs and risks of upgrading an old library increase. Such an accumulation of maintenance debt may lead to a much larger effort than in the case of smaller incremental updates.​
  - For core functionalities, it is a good idea to stay on a stable version of the library. ​Being an early adopter of a new version comes with some risks. Bugs are common in immature versions of libraries as they are not thoroughly tested. Although you have the opportunity to contribute, by testing and potentially providing solutions to bugs you encounter in open source libraries, it might be a better practice to wait until the library becomes more mature.​​
  - Don’t go for the ”If it ain’t broke, don’t fix it” strategy​
    - This strategy implies that you don’t update unless you have to. You stay with the current version of the third-party library until you notice something wrong in your application, no matter how often the vendor publishes an update. ​
    - Whilst easier in the short term, with this strategy you will end up with a system which depends on outdated and unmaintained libraries, where you can't use some other libraries since they require a newer version of that library which you can't upgrade and at some point. You may lose the ability to fix some issues at all.​


### 10. Adopting a new library
- checklist:
  - Does it have open issues?​
  - Is the license acceptable?​
    - Libraries must have a license acceptable to <org>.  <org> maintains a list of common licenses used in free and open-source software (FOSS); if a library has a license listed as acceptable, it can be used. 
  - How is the code quality of the library? 
  - Does it contain optimizations for performance, maintainability, functionality?​
  - Is the new version compatible?  ​
  - How mature is the version?​
  - Is it stable enough?​
  - Are many people using it (e.g. check github stars)

  
### 11. When a library does not support requirements
Basic rule: libraries should not be modified or customised: ​One of the main benefits of libraries/frameworks, is that they provide functionality without the duty of maintaining it. ​With customizing, you lose this benefit while being dependent on the changes that the community makes!​

If no other solution is feasible and a modification is absolutely required (or: the costs of alternative solutions are very high), the source code should be 'adopted' (if permitted by its license) and put into a designated area in a version control system. The modification should be documented so that it can be re-applied whenever a newer version of the library is made available.

### 12. When a bug is detected in a library
During development, while testing your application code, you may find out there is a bug in a library.
- If the bug has already been fixed in a newer version of the library, then consider updating ([Updating a library])
- You may be able to wrap the relevant library call(s) with extra code that corrects or hides the bug.
- Or you can look at the code of the library and develop a bug fix: 
  - you can temporarily use the [modified library](#modify library) while merging back the bug fix into library (be aware of the license). Once the community has accepted the fix, remove the local code​
  - Or you can wait until a new version that includes the bug fix has been published and [update](#updating-a-library) 





## Where OSH/Sigrid fits in your workflow (going-concern)
> see [https://docs.sigrid-says.com/workflows/agile-development-process.html#where-does-sigrid-fit-in-scrum-rituals](https://docs.sigrid-says.com/workflows/agile-development-process.html#where-does-sigrid-fit-in-scrum-rituals)
- Refinement:
  - triaging OSH issues
- Sprint Planning
- Programming:
  - using a library
  - update a library
  - add a new library
  - modify a library
- Code Review:
  - [When do you see the impact of the changes? when merging after the review?]
- Sprint retrospective: 
  - make sure you have actually addressed the findings you set out to fix in your sprint planning.
  
## Frequently Asked Questions

Q: why not adopt a ‘if it ain’t broke, don’t fix it’ strategy for updating libraries?

A:

---

Q: Why it is a good idea to see every library as a backlog item? 

A: Make developers aware of the risks & effort.

---

Q: How does Sigrid OSH collect its information?

A: First, the entire codebase is scanned for configuration files of common dependency management systems (e.g., Nuget, Maven, NPM) to find explicitly managed dependencies.​

Information about each managed dependency is then queried from public sources to determine the version currently used, the date of this version, the number and date of the newest published version, information about its license, and whether it is known to contain security vulnerabilities.​

In addition, the entire codebase is scanned for unmanaged dependencies following some heuristics:​
- JavaScript files are scanned for a version identifier in their name of contents. If found, it is assumed third-party and looked up in public databases to determine freshness, license and vulnerabilities.​
- The contents of Windows DLL files and Java JAR files are considered third-party and are scanned for name and version number and then looked up in public databases to determine freshness, license and vulnerabilities.​

---
Q: 

A: 

---
Q: 

A: 

---
Q: 

A: 

---


## Input: List of Best practices
> TODO: distribute these over the various JTBD?

> The following list comes from the _Library Management Practices_ deck: can these all/mostly be moved to specific JTBDs?


- Use tooling to automate managing the updates​ --> this is one of the OSH topics
  - Integrate tools in the development pipeline​​​
- Embed library management in the development process​
  - Review frameworks/libraries as close as possible at the start of iterations​
  - If you cannot embed this in development iterations, use a standalone schedule for updates (< once a month)​
  - When using stabilization branches, only update for critical fixes ​
  - Don’t mix updating and adding functionality in the same tickets, so you can rollback updates.​
- Try to avoid multiple versions of the same library, as they add the same effort as a separate library​​
- Consider each library/framework as a backlog item, and make it the responsibility of developers​
  - Avoiding use of multiple versions of the same framework/library​
  - Preventing using multiple frameworks/libraries for the same functionalities ​
  - Re-estimating effort and creating visibility in growing technical debt of outdated frameworks/libraries​​


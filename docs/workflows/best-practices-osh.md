# Best Practices for Open Source Health (OSH)

<!-- 
- TODOs 
  - consider how to use context/meta-information to refine policies?
-->

<details>
<summary>Input documents used</summary>
Proposed goal: The Sigrid documentation should be the single source [of truth] of knowledge about Sigrid, the quality models, and SIG Best Practices, thus replacing most of these documents.

Exceptions are SIG and customer confidential information and slidedecks that are (really) needed for presentations.
 
- [Sigrid documentation](https://docs.sigrid-says.com/)
- [Internal software development guidelines from SIG Development team](https://softwareimprovementgroup.atlassian.net/wiki/spaces/ISMS/pages/50314183293/ISMS+P16.+Software+Development)
- OSH model slides (Open with Powerpoint--New from template)
  - there are almost no explanatory slides for OSH in the PPT slide templates (only one overview and 2 templates for findings)
- ["How to interpret OSH findings" wikipage](https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings)
  - See also the License Risk Evaluation Framework slide at the bottom of the wiki page: [OSH interpret results wikipage](https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings)
- ["OSH quality model" wiki page](https://softwareimprovementgroup.atlassian.net/wiki/spaces/DEL/pages/50594021377/Open+Source+Health+Quality+Model) 
- [OSH guidance for producers](https://softwareimprovementgroupcom.sharepoint.com/:w:/s/Internalprojects/InnovationBenchmarkingOSH/EdGZrGAK4C1AmEERkHFyxlQB5KUyWuYZTnGgjmuv8ewUsw?email=lodewijk.bergmans%40softwareimprovementgroup.com&e=4%3avx2p7i&at=9)
   - we should be consistent with this; e.g. when setting default targets?
- [Library Management Practices](https://softwareimprovementgroupcom.sharepoint.com/:p:/r/sites/Internalprojects/SEF/Shared%20Documents/Input/20200526_LibraryManagementBestPractices.pptx?d=w2d1b408f0aab4c6182fcd3f055020926&csf=1&web=1&e=LMfkRh)
- ... 
---
</details>  


## General best practices
>TODO: not sure what the source of this is: can these all be moved to specific JTBDs?

General best practices, considered as compliance rules for framework and library management are stated as follows:​
- Separate application source code from frameworks/libraries​
- Do not change the source code of used frameworks/libraries
​- Do not add project or organization specific headers ​
- Use a single version of a library or framework​
- Regression tests and maintainability are key to updating frameworks/libraries​
- If it’s hard to update, chances are the problem lies in your codebase.​
- Low module coupling and component independence make it easier to change code implementation while keeping the same behavior/requirements.​
- Regression tests help to identify breaking changes in updates.​​
- Use tooling to automate managing the updates​
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


## OSH Jobs to be done
> Note: 'Library Management Practices' proposes these situations: new version / low activity / vulnerability detected / bug detected / functionality missing / compatibility break; perhaps add the latter? 

***TODO: not yet consistent with the guidelines list!!***

#### Incidental Jobs
1. Define OSH related policies
2. Improving portfolio OSH
   > note: when addressing the vulnerabilities of a specific library by updating to a newer version, that always also improves the freshness
3. Implement usage of a package manager
4. Setting up Sigrid OSH

#### Going concern Jobs

5. Scan the software for issues
6. Updating/adopting/introducing/modifying a library
7. Handling detected vulnerabilities
8. Handling detected license issues
9. Handling detected lack of freshness


## The OSH model
  - This is described in the following places:
    - OSH model slide for an overview (partial)
    - wiki page "How to interpret OSH findings"
    - "OSH quality model" wiki page
    - And now the guide for producers is also in the Sigrid documentation
  - [And would benefit from a nice integration..]
  - The benchmark risk categories should inform (be consistent with) the methodology, similar for the guidance for producers.


## Guidelines for Jobs to be done:
> make sure these are consistent with the guidance for producers


### 1.Define OSH related policies
- Which libraries are allowed
- the use of a package manager
- how frequent to check for vulnerabilities and other risks in open source libraries
- goals for library freshness
  - (max number versions you may stay behind)
- how fast new vulnerabilities have to be resolved (depending on the criticality)


### Improving portfolio OSH

### Implement usage of a package manager
- depends on technology: do we have suggestions?
- what if your technology does not come with a package manager?


### Setting up Sigrid OSH:
-  Define  Sigrid objectives
  - Portfolio/System



### Adopting/introducing a new library
- checklist:
  - Does it have open issues?​
  - Is the license compatible?​
  - Does it contain optimizations for performance, maintainability, functionality?​
  - Is the new version compatible?  ​
  - How mature is the version?​
  - Is it stable enough?​
  - Are many people using it (e.g. check github stars)
  - How is the code quality of the library? 
  
- 3rd party libraries are not to be modified.
  - Avoid custom versions of frameworks or libraries. ​One of the main benefits of libraries/frameworks, it provides functionality without the duty of maintaining it. ​With customizing, you lose this benefit!​
  - If no other solution is feasible and a modification is required, the source code should be 'adopted' (if permitted by its license) and put into a designated area in a version control system. The modification should be documented so it can be re-applied whenever a newer version of the library is made available.


### Scan your software for health issues
- Frameworks and libraries should be scanned frequently (preferably daily, but no less than every 3 months) to make sure there are no severe vulnerabilities in them.
- Use Sigrid to continuously review libraries:
  - For existence of known vulnerabilities.
  - For acceptable license
  - For up-to-date-ness (freshness)
- When to use the scan results: 
  - do triaging during refinement [You need to decide if libraries need to be updated during the upcoming sprint, either because vulnerabilities have been found or because the team agrees it is falling too far behind the latest version. ]
Likely actions:
- [Updating a library](Updating a library) 

### Updating a library
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


### Bug detected in a library:
During development, while testing your application code, you may find out there is a bug in a library.
- If the bug has already been fixed in a newer version of the library, then consider updating ([Updating a library])
- You may be able to wrap the relevant library call(s) with extra code that corrects or hides the bug.
- Or you can look at the code of the library and develop a bug fix: 
  - you can temporarily use the modified library [modify a library] while merging back the bug fix into library (be aware of the license). Once the community has accepted the fix, remove the local code​
  - Or you can wait until a new version that includes the bug fix has been published and update [update library]


### Handling detected vulnerabilities
- Security risks of a certain framework or library should be determined based on at least two aspects: 
  - ​1) The severity level of known vulnerabilities for the artefact​
  - 2) The mission of the components where the framework or the library will be applied​ 
    - Non mission critical / ​Mission ​critical / ​External Facing or Distributed​
- public facing systemen eerst--> 0 (x risk) vulnerabilities
- When a vulnerability is found, it will be remediated within a time period according to below table [not here]
- If no remediation is available, [Company] will do a risk assessment which will have one of 3 outcomes:
  - If we find that the vulnerability does not pose any actual risk, we will ‘allowlist’ it. This requires CISO approval. This allowlist will be reviewed as part of the half-yearly measurement cycle.
  - We will mitigate the risk in some other way. If, for example, we do not want to allowlist. the entire library because of its importance but the vulnerability is limited to a single method, we can test for the use of that method and fail the pipeline in that case.
  - [In](http://3.in/) extreme cases, we will shut down the application until the vulnerability is resolved.
  
### Handling detected license issues
- Libraries must have an acceptable license.
  - This may be a paid license or an acceptable open-source license. [Company] maintains a list of common licenses used in free and open-source software (FOSS); if a library has a license listed as acceptable, it can be used. Otherwise, see if an alternative is available, or contact the [applicable role] to discuss whether the license is acceptable.
- See also the License Risk Evaluation Framework slide at the bottom of the wiki page: [OSH interpret results wikipage: https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings](https://workflowy.com/#/c9c4745b6b6b)
- Note that the risk depends on the context: 
  - e.g. when developing open-source software, more licenses are acceptable.
  - it also depends on how you use a library: it is sometimes needed/a solution to wrap the library in an executable component that can be used by calling, instead of becoming a part of the codebase.

### Handling detected lack of freshness
- The teams are responsible for keeping libraries reasonably up to date: 
  - small library updates can be updated as part of regular maintenance; 
  - larger updates (e.g. major versions or frameworks) should be planned explicitly as part of a development sprint.
- Improving portfolio OSH
- how to make investment decisions
- Where to start/how to tackle OSH techdebt incrementally
  - public facing systems first: focus on removing all high risk vulnerabilities
  - Make sure to look at the product lifecycle, end-of-support date and maintenance activity. Do an impact analysis and plan the needed effort to mitigate the risks. ​​Opensource dependencies can be compared in terms of activity on tools like [https://www.openhub.net/](https://www.openhub.net/)​

### Guidelines for Sigrid-specific Jobs to be done


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
  
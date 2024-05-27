# Guidelines for healthy use of Open Source

<!-- 
- TODOs 
  - consider how to use context/meta-information to refine policies?
  - Check that the benchmark risk categories and the guidance for producers should be consistent with the methodology & guidelines: so same scales etc.
  - Make sure we are aligned with DPA v4! (can we refer to it?)
  - and with the guidance for producers
  - we have to explicitly address: what if we did not reach 4 stars -> then look at the underlying measurements
  - check consistent usage of the term third party library (marco: open-source dependency)
   - create an overall flow chart? (but not in mermaid..)
  - comments marijn:
     - Nog iets: onder het kopje 'When a library does not support requirements' staan redenen om een library te vervangen die allemaal los staan van OSH, maar die ook weer terugkomen on Vervolgens staat onder 'Replacing a library' een aantal redenen om te replacen die wel weer aan OSH vast zitten. Volgens mij is er eigenlijk 1 flow die neerkomt op 'Ik ben niet blij met mijn library vanwege whatever, dan 1) update 1a) pull request of issue aanmaken bij maintainer (noemen we nu nog niet) 2) vervangen 3) (if all else fails) adopteren.
    - Nog iets: in 'How to improve portfolio and system-level OSH' kunnen we volgens mij op een hoger niveau blijven. Nu beschrijven we daar bepaalde details die ook terugkomen in de 'Handling....' secties.
  - [Marco]: I feel the text in "Structure and overview" and #### Be equipped for healthy open source usage can be merged. I find the text above that introduces this list very... informal, but at the same time not straightforward to understand.
-->

<!-- > NOTE for internal use: This document is a collection of the knowledge that we have accumulated within SIG on the best practices for achieving Open Source Health. Its purpose within SIG is to have all this knowledge documented in one place, such that we have a shared base as consultants, and also a document that we can share with customers that are in search of concrete advice on how to get things in place for healthy open source usage.  -->

<sig-toc></sig-toc>

## Introduction

The purpose of this document is to provide concrete and actionable guidelines, hints and tips on how to achieve healthy use of third party libraries and frameworks in your application. 
This covers how to get started, how to stay in control, and how to act when health deteriorates. 
Where applicable, this document explains how Sigrid can be used to achieve this.


### Structure and overview

The guidelines and best practices have been structured based on 'jobs to be done': the idea is to look at the actual tasks that stakeholders need to conduct, and provide them with help to do those tasks. Jobs can embed, or refer to, other jobs.

These jobs have been grouped in three categories: first some general guidelines for conducting healthy open source usage in development, that help to get started, and may need to be revisited or updated on a regular basis. Secondly the various types of tasks that are needed to ensure continued health of libraries (note that even when application code is not actively maintained for a while, the health of open source libraries may diminish!). And thirdly a set of practical tasks in handling libraries as a developer.


#### Be equipped for healthy open source usage
1) [Define OSH-related policies](#1-define-osh-related-policies-for-development)  
2) [How to improve portfolio and system-level OSH](#2-how-to-improve-portfolio-and-system-level-osh)  
3) [General guidelines for your application development](#3-general-guidelines-for-your-application-development)

#### Ensuring your open source stays healthy
4) [Scan the software for issues](#4-scan-the-software-for-health-issues)  
5) [Handling vulnerabilities](#5-handling-vulnerabilities)  
6) [Handling license issues](#6-handling-license-issues)  
7) [Handling lack of freshness](#7-handling-lack-of-freshness)  
8) [Handling lack of activity](#8-handling-lack-of-activity)  

#### Handling libraries
9) [Updating a library](#9-updating-a-library)  
10) [Selecting a new library](#10-selecting-a-new-library)  
11) [When a library does not meet the requirements](#11-when-a-library-does-not-meet-requirements)  
12) [Replacing a library](#12-replacing-a-library)  
13) [Reviewing a library](#13-reviewing-a-library)  

A word of caution: The guidelines and steps that follow are intended to be helpful in making decisions and taking proper actions; since every application context is unique, these guidelines and steps should never replace logical thinking, taking your unique situation into account!
{: .attention }

### About the SIG Open Source Health (OSH) model
The SIG Open Source Health model is described here in the documentation: [OSH guidance for producers](../reference/quality-model-documents/open-source-health.md).

<!-- And more internal details for SIG are here (since some proprietary info):
- Wiki page ["How to interpret OSH findings" wikipage](https://softwareimprovementgroup.atlassian.net/wiki/spaces/SSM/pages/50317951024/How+to+interpret+Open-Source+health+findings).
  > Is this now redundant?
- Wiki page ["OSH quality model" wiki page](https://softwareimprovementgroup.atlassian.net/wiki/spaces/DEL/pages/50594021377/Open+Source+Health+Quality+Model).  -->



## Be equipped for healthy open source usage

This section prescribes a typical way of working for ensuring healthy open source usage; in specific situations, you may adapt this approach, but it is best to follow a comply-or-explain approach.



### 1. Define OSH related policies for development
There are a number of policies on how to address open source libraries during development. For most of these policies, minimal requirements should be set for all teams; individual teams may agree on more stringent rules. 

#### Policy I: Define the usage of a package manager
Choose the package manager(s) to be used, at least per system, preferably shared across the organization. Depending on the technologies that are used, you may need multiple package managers.

The package managers need to be integrated in your CI/CD pipeline.
{: .attention }

#### Policy II: Set the thresholds for library risks
Set the thresholds for library risks that are (not) acceptable: this is applicable to all types of risks. Set these goals in the [Sigrid objectives](../capabilities/portfolio-objectives.md). 
  > SIG advises the following objectives: 
  >  - _No library vulnerabilities_: having vulnerabilities of medium or higher risk is generally not acceptable as a goal, and since there are relatively few low-risk vulnerabilities in practice, a 'clean sweep' of all vulnerabilities is preferred.
  >  - _No unacceptable licenses_; for a typical context this means no licenses that come with obligations or restrictions for commercial usage (see the [OSH Guidelines for producers](../reference/quality-model-documents/open-source-health.md) for more details.). In Sigrid these are classified as no-risk, and include the MIT, BSD, and Apache licenses.
  >  - _Ensure overall OSH quality rating is 4.0 stars[^1] or more_. *NOTE: OSH benchmarked star ratings are a new Sigrid feature that will be released in May 2024*  

#### Policy III: Define how frequent to check for risks
Preferably check daily for vulnerabilities and quarterly for other OSH risks. See section [4. Scan the software for health issues](#4-scan-the-software-for-health-issues) for more details.  

#### Policy IV: Define how fast new vulnerabilities have to be resolved
This will depend on the criticality. See the section on [Handling vulnerabilities](#5-handling-vulnerabilities) for details.  

#### Policy V: Declare which libraries should not be checked
   - This is useful when a library has properties that cause Sigrid to signal a risk, but that risk is a false positive. 
   - Create an _ignore-list_. This list requires CISO approval. The ignore-list must be reviewed regularly (a few times per year): define when this review will happen.
    > **Sigrid How to:** _To achieve this in Sigrid, the library to ignore must be added in the scope file_
  
Do note that if a library is put on the ignore-list since the reported vulnerability is a false positive, that does not necessarily mean that the other types of risk for that library should be ignored as well.
{: .attention }

#### Policy VI: (Optional) Define a shared permitted-list
A shared list of libraries that have been reviewed and approved for usage can be useful (and in some organizations required). 
  - This list can have an advisory role, functioning as a list of libraries that have already been checked, and are likely already in use. It can also have the role of a clearance list, where developers have only permission to use libraries from the permitted-list, and must seek approval for libraries that are not on that list. 
  - For determining whether to include libraries, see the criteria defined in the section [10. Selecting a new library](#10-selecting-a-new-library).  



### 2. How to improve portfolio and system-level OSH
Especially when a system or portfolio is new in Sigrid, at the system and portfolio level there can be an abundance of OSH related issues that need to be fixed; this section provides some advice on how to tackle all those jobs incrementally, starting with the most critical and high-ROI topics first; Sigrid is designed specifically to help you focus on the highest priority issues.

- In case no package manager is used, or not for all libraries (all technologies), it makes a lot of sense to start with the -extended- use of a package manager. This it will make all other improvement steps easier, faster, and less error-prone.
- The next step is to focus on vulnerabilities, since these threaten your application security in the short term:
   - Start with a quick threat analysis to prioritize the systems that are most risk-prone: this means the system where attacks would have the most impact, and the highest likelihood of an attack. In particular for systems with [business-criticality](../organization-integration/metadata.md#system-metadata-fields-and-corresponding-allowed-values) that is `CRITICAL` OR `HIGH` and systems containing privacy-sensitive data or transactions, the impact will be high. The likelihood is determined by the attack surface and exposure: so especially systems with a [deployment type](../organization-integration/metadata.md#meaning-of-special-values-for-metadata-fields) that is `PUBLIC_FACING` will have a higher likelihood.
   - Focus on removing all critical and high risk vulnerabilities first, continue with the remaining vulnerabilities.
- Consider legal risks due to unacceptable licenses:
   - The highest priority are libraries that are used in an application without the proper rights; for example libraries that do not allow commercial use (if you are a commercial organization). Some of those require paying a license fee; which is the most straightforward means of addressing the issue.
   - A next category to consider are the copy-left licenses, which require the application that uses those libraries to be distributed with the same license (and e.g. also made open-source). Depending on your situation, using copyleft licenses carries the risk of not complying with license obligations, leading to consequences such as the obligation to distribute the source code and legal disputes. The main way of addressing legal risk due to unacceptable licenses is by [replacing the library with another one](#12-replacing-a-library).
- For the other properties: 
   - investigate the risks of heavily outdated and perhaps no longer maintained libraries: look at the product lifecycle, end-of-support date and maintenance activity to verify that there is a real need for [replacing the library](#12-replacing-a-library).
   - Do an impact analysis and plan the needed effort to mitigate the risks. This can be -a series of- [updates](#9-updating-a-library), or complete [replacement of a library](#12-replacing-a-library). 
   - ​​Open source libraries can be compared in terms of activity on tools like [https://www.openhub.net/](https://www.openhub.net/)​
   - Looking at the bug reports of inactive libraries, and the fixed bugs or improvements of outdated libraries can give good information of the relevance of [updating](#9-updating-a-library).

When many libraries require (multiple or major) version updates, the level of test coverage of a system can be used as an additional factor for prioritization: systems with high test coverage have a lower risk of running into defects at run-time due to incompatible updates.  
  

### 3. General guidelines for your application development

There are a number of topics to consider that are not directly related to the libraries themselves, but to the way you organize the development of the application itself.
The following guidelines should be considered as compliance rules for framework and library management:​

#### Keep application source code separate from frameworks/libraries​.
1. _Do not change the source code of used frameworks/libraries_: depending on the technology used, you often do not need source code at all, but will use binaries of the libraries.
1. _Only a single version of each library or framework​ should be used directly_: Also, do not have copies of the same library installed. It may well be that one or more of your libraries is importing another version of the same library that your application uses; such indirect use is mostly out of scope.
<!--  This discussion is perhaps too detailed/nuanced?
   Note that in some cases, you can have a library _L1_ that requires _M_, and a library _L2_ that requires another version of _M_; in such cases you may not be able to influence this (depending on what your package manager allows), but at least ensure your application code does not directly rely on multiple versions of the same library.
  [Note Asma] Point 3 sounds like transitive dependency management, what are the best practices there to handle those in a package manager? Also at which lvl of transitivity do we stop caring? 
  LB:  indeed in some package managers you actually do have influence over the versions of indirect dependencies, discuss this. exercising influence over this makes sense for security purposes, but otherwise its impact *should* be encapsulated.
-->

#### Regression tests and maintainability of the application code are key to updating frameworks/libraries​
If it is hard to update a library, chances are the problem lies in your codebase.​

- _Keep module coupling and component independence low_, to make it easier to change code implementation (such as dealing with new versions of a library) while keeping the same behavior/requirements.
- _Develop, maintain and run regression tests._ These help to identify breaking changes in updates.​​



## Ensuring your open source stays healthy
This section describes guidelines, hints and tips on how to maintain healthy use of open source libraries in your application. Where applicable, we explain how Sigrid can be used to achieve this.


### 4. Scan the software for health issues

For timely handling of open source health risks, there are two concerns:

- _Risks that appear due to changes in the code_: these need to be signalled as soon as possible (short feedback loops make it much more efficient to make changes); doing the scanning as part of the CI/CD pipeline using `sigridci` addresses this.
  - The risks that are detected are best addressed immediately, _before_ merging the new code.
- _Risks that appear due to changes in the ecosystem over time_: these require regular scans, even when the application code does not change. For this category:
  - Vulnerabilities require frequent scanning: preferably daily, at least every 2 weeks.
  - The other OSH properties are less volatile and urgent, and monthly to quarterly scanning is sufficient for those.

OSH analysis is conducted whenever Sigrid receives an update through [Sigrid CI](../sigridci-integration/development-workflows.md), or in the form of a new snapshot [upload](../organization-integration/upload-instructions.md). Hence, for systems that are inactive, new vulnerabilities in the ecosystem are not visible in Sigrid. Regularly do a forced update (or upload) to ensure your code is scanned again.
{: .attention }

A good time to triage scan results is during refinement for the next sprint: You need to decide to address the detected risks during the upcoming sprint, or possibly create a backlog item. In some cases, the detected risk is considered a false positive, or acceptable risk that can be ignored. The most common mitigation will be [updating a library](#9-updating-a-library). 

<!-- See also [Where OSH fits in your workflow](#where-oshsigrid-fits-in-your-workflow-going-concern) for details on how to integrate library handling in your workflow. -->


### 5. Handling vulnerabilities

#### When to remediate vulnerabilities
Security risks, and hence the urgency of fixing a vulnerability, of a certain framework or library should be determined based on at least the following aspects: 

* The severity level of the detected vulnerabilities for the artifact​.
* The connectedness of the specific application: in particular the category `public facing` is the group of systems for which vulnerabilities need to be resolved most urgently. This information can be specified in the [Sigrid metadata](../organization-integration/metadata.md) as the _deployment type_; all non-public facing categories (`connected`, `internal` and `physical`) are referred to below as `local`.

Additional considerations for prioritizing vulnerability handling can also be business criticality, lifecycle phase and the privacy sensitivity of the data that an application handles.

When a vulnerability is found, it must be remediated within a specified time period.
The table below is a proposal how fast you should resolve vulnerabilities, depending on the risk level and the connectedness of the system:

| CVSSv3 Range | Risk Label | Remediation Deadline Public facing | Remediation Deadline Local |
|-----|-----|-----|-----|
| 9.0 – 10.0 | Critical | Within 1 working day | Within 14 days | 
| 7.0 – 8.9 | High | Within 14 days | Within 30 days |
| 4.0 – 6.9 | Medium | Within 30 days | Within 60 days |
| 0.1 – 3.9 | Low | Within 60 days | Within 90 days |


#### How to remediate vulnerabilities

The primary means of remediating a vulnerability is to update the library: in most cases, vulnerabilities (especially critical ones) are only published once a patch is available in a new version of the library. See section [9. Updating a library](#9-updating-a-library) for more details. Do check that the vulnerability is indeed solved in the newer version of the library.

If no such remediation is available, do a risk assessment which will have one of these outcomes:
- If the vulnerability does not pose any actual risk, ‘allow-list’ it: that means you allow the specific vulnerability for this library/application to be present. This requires approval from a CISO or other applicable role. This _allowlist_ will be reviewed as part of a half-yearly measurement cycle. 
- The risk can be mitigated in some other way. If, for example, the vulnerability is limited to a single method in the library that is not called by our application. You can then test for the use of that method and fail the pipeline in that case, to prevent future accidental risks.  
- The library can be replaced, or no longer used, completely; see [12. Replacing a library](#12-replacing-a-library) for more details.
- In extreme cases, you may need to shut down the application until the vulnerability is resolved.



### 6. Handling license issues 

SIG assesses whether a license is generally considered a risk for use within commercial software. Contact an IT lawyer to discuss license risks specifically for the code analyzed as well as the way it will be used.
{: .attention }

Usually, license risks will appear whenever a library is scanned for the first time; either because the application is scanned for the first time, or the library has just been introduced.


#### Assess the license risk
- Libraries must have an acceptable license. This may be a paid license or an acceptable open-source license. 
- Maintain a list of common licenses used in free and open-source software (FOSS); if a library has a license listed as acceptable, it can be used. Otherwise, see if an alternative is available, or contact the responsible in your organization to discuss whether the license is acceptable.
- Note that the actual risk of using a library with a certain license depends on the context: 
  - e.g. when developing open-source software, licenses that require you to make your code available as open source are acceptable, where this is not acceptable for closed-source development.
  - It also depends on how you distribute a library:
    1. **Distribute modified code**: Distribute the source code of the library, after making changes to it.
    1. **Distribute linked libraries**: As linked libraries, not the actual source code.
    1. **Linked libs through network**: As linked libraries that are called through the network.
    1. **Internal use only**: As libraries that are used internally only.

The following table shows how various types of licenses are (not) suitable for different distribution policies, and explains how these common licenses are mapped to general risk levels. But do note that if your distribution model is clear, and the value listed for the particular license-distribution model is 'ok' in the table, then your actual licensing risk is minimal:


| Risk level | License category | Common licenses | Distribute modified code | Distribute linked libraries | Linked libs through network | Internal use only |
|------------|------------------|-----------------|------------------------|---------------------------|------------|-------------------------|
| none     | permissive       | Apache / MIT / BSD| Ok | Ok | Ok | Ok |
| low      | Weak copy-left   | LGPL / MPL / CC-BY-ND | prohibited | Ok | Ok | Ok |
| medium   | Strong copy-left | GPL | prohibited | prohibited | Ok | Ok |
| high     | Viral            | AGPL / CC-BY-NC / EUPL | prohibited | prohibited | prohibited | Ok |
| critical | Commercial       | EULA / non-OSS / custom | prohibited | prohibited | prohibited | prohibited |



#### Possible actions
Depending on the circumstances, one or more of the following actions can be taken to remediate detected licensing issues
* Ensure that libraries with commercial licenses are properly registered and paid for. 
* (When applicable) Add a license to the shared list of acceptable licenses (this may involve an approval process).
* (When applicable) Adjust the distribution model of the application to avoid violating the terms of the library license. For example, distribute linked libraries instead of (modified) source code.
* Stop using a library with unacceptable licensing conditions: in practice this requires [Replacing a library](#12-replacing-a-library).



### 7. Handling lack of freshness

Lack of freshness occurs when there is a newer version of a library available, but that version is not used in the application.

Development teams are responsible for keeping libraries up-to-date to a recent version: this may be part of [How to remediate vulnerabilities](#how-to-remediate-vulnerabilities), to make sure that bug fixes and improvements are incorporated, for compatibility with other libraries, or to ensure that future updates will not be too complicated or require a large effort all at once.

The remedy for lack of freshness is always [Updating a library](#9-updating-a-library), possible exceptions are:

- the newer version has a vulnerability for which a fix is not available (very rare)
- the newer version is not compatible with other libraries.
<!-- this actually also overlaps with 'updating a library', but maybe still good to have these 2 sentences here? -->


### 8. Handling lack of activity
Lack of activity in the development of a library is not an urgent problem, but it is a long-term concern, in particular since it precludes detecting and patching security vulnerabilities. 
This issue cannot be resolved by application developers, except by [Replacing a library](#12-replacing-a-library).


<!-- 
### 8.5 Handling insufficient package management [OPTION]

> NOTE: perhaps a few lines about what it can mean when you have package managers in use, but still score insufficiently.

- This may be due to e.g. Java JARs or javascript source files that have been copied directly into your code base. 
- perhaps you also use libraries that are not part of an ecosystem that is handled by the package manager
- perhaps you use libraries for a technology that does not have an (adequate/acceptable) package manager
... -->



## Handling your libraries


### 9. Updating a library
There can be several reasons for updating a library: 
- _Urgent reasons_: when a vulnerability is detected in a library that has been resolved in a new version, or a bug has been resolved in a newer version.
- _Hygiene_: ensure that the version of a library that you use does not fall behind too much, since that will make your life as a developer harder.

Updating to a newer version will always also improve the freshness rating. Using a package manager, updates may be installed automatically, or require updating the version constraints in the configuration file (sometimes called 'manifest') of the package manager.

The _effort involved in updating_ a library can be estimated based on the release notes, and also [semantic versioning](https://semver.org/): here are some rules of thumb w.r.t. the effort needed for updating:
- a security patch: typically less than 1 hour
- a minor version update: also typically less than 1 hour
- a major version update: an average of 1 day; the effort _can_ be substantial, depending on the amount of breaking changes, which are typically described in the release notes.

One important factor is how well the automated test suite for the application (unit tests and/or system tests) will cover all possible cases: a need for manual testing can add substantial time to the above efforts.

_Scheduling library updates:_
- Small library updates (security patches and minor version updates) can be updated as part of regular maintenance. 
- Larger updates (e.g. major versions or frameworks) should be planned explicitly.

> _Ground rule: never postpone updating_
  - The longer you postpone updating, the bigger the eventual pain. As your system grows and evolves, the costs and risks of upgrading an old library increase. Such an accumulation of maintenance debt may lead to a much larger effort than in the case of smaller, incremental updates.​
  - if a new, stable version comes out: don't wait, start testing. If it is really core and really important, already start testing with release candidates.
  - Do _not_ adopt the "If it ain’t broke, don’t fix it" strategy​
    - This strategy implies that you do not update unless you *have to*. You stay with the current version of the third-party library until you notice something wrong in your application, no matter how often the vendor publishes an update. ​
    - Whilst easier in the short term, with this strategy you will end up with a system that depends on outdated and unmaintained libraries, where you cannot use some other libraries since they require a newer version of that library which you cannot upgrade and at some point. You may lose the ability to fix some issues at all.​
  - Only when a new version breaks the behavior of the application, postponing may be warranted.



### 10. Selecting a new library
The main criterion for selecting a new library is when a non-trivial amount of commonplace behavior is needed within the application: implementing such behavior from scratch is typically more time-consuming and error-prone than predicted, hence reuse from an (open source) library may be the better option. 
 
Often, libraries are part of an ecosystem, or work within a certain application framework, such as Eclipse, or Apache, where it makes a lot of sense (consistency, frictionless compatibility) to pick a library from the same ecosystem, unless it violates any of the other recommendations provided in this document (e.g. you adopted a library that is no longer maintained, etc.). 

See section [Reviewing a library](#13-reviewing-a-library) for a detailed checklist of properties to consider before selecting a new library.

A more extensive discussion of selecting (including reviewing) open source libraries can be found in this [talk](https://portal.gitnation.org/contents/is-it-the-one-how-to-select-an-open-source-library).



### 11. When a library does not meet requirements

There are several possible cases where a library does not support the needs and requirements:

- _Its Open Source Health has unacceptable risks_. 
- _Functional mismatch_: a library is missing features that cannot easily be added on top, or the implementation of the library is based on assumptions or choices that are incompatible with the ones in the application.
- _Bug in library implementation_: typically detected after a library has been adopted, so the cost of switching is non-negligible.
- _Compatibility break_: a library does not (or no longer) work well together with another library or the application itself, due to changes in the APIs of involved components.

The basic rule is that _library implementations should not be modified or customized_: ​One of the main benefits of libraries and frameworks, is that they provide functionality without the duty of maintaining it. After customizing a library implementation, you lose this benefit while being dependent on the changes that the community makes.​

How to address failing requirements:

- First, check whether a newer version of the library may solve the issue, then consider updating ([Updating a library](#9-updating-a-library)); you may also wait a bit until a fix is being released, especially when the issue is being worked on.
- If the issue is a bug or lacking feature, you can file an issue at the maintainer of the library. 
- If the issue is a bug or lacking feature, you can also look at the implementation of the library and develop a fix: 
   - You may be able to wrap the relevant library call(s) with extra code that corrects or hides the bug.
   - Alternatively, you can temporarily use the modified library while merging back the bug fix into the library (be aware of the license, and make sure you have clearance from your employer to do so). Once the community has accepted the fix, you can update and remove the local code​.
- Consider whether another library that implements similar functionality is available, and the costs of adopting that library are acceptable. Check [Replacing a library](#12-replacing-a-library) for more details.
- If no other solution is feasible and a modification is absolutely required (or: the costs of alternative solutions are very high), the source code can be forked and put into a designated area in a version control system. In this case carefully consider the possible legal ramifications, e.g. should you make the modified version open source as well. The modification should be documented so that it can be re-applied whenever a newer version of the library is made available.



### 12. Replacing a library
There can be multiple reasons that require discarding a library and replacing it with another; see [11. When a library does not meet requirements](#11-when-a-library-does-not-meet-requirements) for such situations.

In _most_ cases, rebuilding a common functionality is not the best option: just assume that doing that will take much more time than expected, and will also require you to maintain the code in the future. So looking for an alternative library is most likely the best choice, unless there is only very specific and limited behavior that you need now (and in the foreseeable future).

See section [10. Selecting a new library](#10-selecting-a-new-library) for guidelines on how to pick a new library.

One major concern when replacing a library with a new one is that a new library will most likely come with a new API; this means that all the locations in the application that use that library may need to be identified and adjusted. This can be more than just the identifiers of method calls, but also the data types that are passed back and forth to the library API can be different, which _may_ impact the calling code substantially. An approach in this case can be to wrap the new library and in this way provide an interface that is equal, or more similar, to the previous library.



### 13. Reviewing a library
Whenever choosing a new library or updating to a new version, consider the following review criteria:
1. What are the known vulnerabilities?
2. Is the license acceptable?​ (and/or is the library in the shared permitted-list). See also [6. Handling license issues](#6-handling-license-issues).
3. Is an updated version compatible with the previous version?  ​(release notes should indicate any breaking changes)
4. Is the code quality (esp. maintainability) of the library acceptable (>3.0 stars)? 
5. How mature is the version?​ (e.g. an x.0 version tends to be a bit more immature). Are there still -relevant- open issues? Use a stable version unless there is a real reason not to do so. An example might be that a Release Candidate fixes a vulnerability, and you do not want to wait for the stable version to come out.
6. Is the library actively maintained (also discussed [here](../reference/quality-model-documents/open-source-health.md#activity) ) in the Guidance for Producers), preferably by multiple developers?
7. Are there enough users of the library? (check for example the number of downloads, or amount of GitHub stars).

---

<!-- - compatibility breaks
  - Compatibility breaks can be caused by the framework/library no longer supporting the technologies used in the system.​
    - e.g. if the libraries are using newer language versions? 
  - Analyze the impact and consider the following things:​
     - What is the impact of updating the application to make it compatible?​
     - Are there alternatives of the library?​
     - Are the technologies used still relevant for the future of the system?​ -->
<!-- check this text by marijn:
You were using a (deprecated) method that is no longer available. Your IDE will likely make you aware of this.
A nastier version is that you weren't using the library correctly and the new version is less forgiving but without alarms going off.
The library needs transitive dependencies that have become incompatible with needs of other libraries -->


<!-- 
## Where OSH/Sigrid fits in your workflow (going-concern)  
#### [ROUGH DRAFT]

tasks to do repeatedly:
- scan for issues (daily/..)
- remediate vulnerabilities (depends on urgency)
- remediate other OSH findings ()
- revisit 'allow-list' and 'permitted-list' (with CISO, half-year basis)
  

> see [workflows/agile-development-process.html#where-does-sigrid-fit-in-scrum-rituals](../workflows/agile-development-process.md#where-does-sigrid-fit-in-scrum-rituals)
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
  -->
<!--   
## Frequently Asked Questions  [ROUGH DRAFT]

Q: why not adopt a ‘if it ain’t broke, don’t fix it’ strategy for updating libraries?

A:

---

Q: Why it is a good idea to see every library as a backlog item? 

A: Make developers aware of the risks & effort.

---

Q: How does Sigrid OSH collect its information?

A: First, the entire codebase is scanned for configuration files of common dependency management systems (e.g., NuGet, Maven, NPM) to find explicitly managed libraries.​

Information about each library is then queried from public sources to determine the version currently used, the date of this version, the number and date of the newest published version, information about its license, and whether it is known to contain security vulnerabilities.​

In addition, the entire codebase is scanned for unmanaged libraries following some heuristics:​
- JavaScript files are scanned for a version identifier in their name of contents. If found, it is assumed third-party and looked up in public databases to determine freshness, license and vulnerabilities.​
- The contents of Windows DLL files and Java JAR files are considered third-party and are scanned for name and version number and then looked up in public databases to determine freshness, license and vulnerabilities.​

---
Q: 

A: 

---
Q: 

A: 

---
- Objection: Yes, this is a known vulnerability, but we don't even know whether it is actually exploitable, we may not be using the vulnerable method.
  - SIG opinion: in 90% of the cases, it takes less time to update, than to figure out whether you are vulnerable or not. So just do it. The other 10% contains frameworks that are used everywhere, or a major update, or systems that have no test code and a rigid pre-release manual testing setup). Those 10% can do the investigation into whether they are actually vulnerable.
- Objection: Updating is hard because we need to manually re-test our entire system / get approval / wait for the next quarterly release / are not using a package manager
  - SIG opinion: You have bigger problems than outdated libraries. Update the most important vulnerable dependencies, and invest in test automation and your development process.
- Objection: It is a bad practice to be on the latest version all the time, they tend to be unstable and contain bugs.
  - SIG opinion: Agree (although it is not that bad in practice). This is why we do not recommend to have everything green for Freshness, and everything less than 1 month not updated is still green.

--- -->

<!-- 
## Input: List of Best practices
> TODO: distribute these over the various JTBD?

> The following list comes from the _Library Management Practices_ deck: can these all/mostly be moved to specific JTBDs?


- Use tooling to automate managing the updates​ → this is one of the OSH topics
  - Integrate tools in the development pipeline​​​
- Embed library management in the development process​
  - Review frameworks/libraries [updates?] as close as possible at the start of iterations​ → during backlog refinement?
  - If you cannot embed this in development iterations, use a standalone schedule for updates (< once a month)​
  - When using stabilization branches, only update for critical fixes ​
  - Don’t mix updating and adding functionality in the same tickets, so you can roll back updates.​
- 
- Consider each library/framework as a backlog item, and make it the responsibility of developers​
  - Avoiding use of multiple versions of the same framework/library​, as they add the same effort as a separate library​​
  - ?? Re-estimating effort and creating visibility in growing technical debt of outdated frameworks/libraries​​ -->

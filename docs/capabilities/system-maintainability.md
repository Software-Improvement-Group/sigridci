# System-level maintainability
The maintainability view is available for all systems by default. 
You can reach this view in different ways: Via the top menu, or clicking an a capability on the System or Portfolio *Overview* pages. See the [system-level Overview page](system-overview.md#navigating-to-capabilities) or [portfolio-level Overview page](portfolio-overview.md#navigating-to-capabilities).

<img src="../images/system-maintainability-menu-ex-architecture.png" width="250" />

The definition of what a system is, what it is comprised of, and how it is configured, are detailed in the pages on [systems within Sigrid](../organization-integration/systems.md) and the [analysis scope configuration documentation page](../reference/analysis-scope-configuration.md).

## 4 different views in the Maintainability tab 
The maintainability section on the system level has 4 views: 
1. The *Overview* tab brings the main metrics together. 
2. The *Component Dependencies* tab visualizes architectural layering and connections.
3. The *Refactoring Candidates* tab groups and prioritizes code that does not meet 4 star quality. 
4. The [*Delta quality*](system-delta-quality.md) view shows the impact of new code changes on the system for the selected period.

## Maintainability overview
The overview page is shown below. 
* The system’s (configured) architecture is visible in the top right. This is based on the system’s scope configuration (see [the page on scope configuration](../reference/analysis-scope-configuration.md)). 
* The main code changes are visible at the bottom.
* The (change in) system metrics are in the top left. 

<img src="../images/system-maintainability.png" width="600" />

Below a detailed view of the metrics. 
<img src="../images/help-button.png" class="inline" /> A mouse-over on the "?" help icon explains what constitutes the overall maintainability rating. The maintainability score consists of several sub-metrics that range from 1 to 5 stars, with the range 0.5 to 5.5.Please be aware that the overall score is not an average of the submetrics. For a general introduction on these metrics, see the section on [our approach](../getting-started/approach.md).

For technical details on maintainability metrics, see [Maintainability Evaluation Criteria](https://www.softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability.pdf) on our website. Or a broader overview on our [Reference page on our quality models](../reference/sig-quality-models.md).

Below the metrics overview, there is a shortcut to the *Refactoring candidates* [link on this page](system-maintainability.md#refactoring-candidates). This can also be reached by the Maintainability tab. 

### Technical Monitor and Code Explorer
 
The “*Technical monitor*” button above the system rating brings you to an alternative (one might say, “legacy”) view of all the maintainability metrics and underlying source code. Its functionality and views will eventually be moved to Sigrid. Generally, its source code-level view is available in Sigrid in the [Code Explorer](system-code-explorer.md). 

<img src="../images/technical-monitor-shortcut.png" width="200" />

Because the views, filters and sorting abilities between the "*Technical monitor*" and "*Code Explorer*" are different, please see [a deserved elaboration on the Technical monitor on the Code Explorer page](system-code-explorer.md#the-technical-monitor). 

## Component Dependencies
The *Component Dependency* view visualizes the dependencies between your application’s main components. The components follow from the system’s configuration.

<img src="../images/system-component-dependencies.png" width="600" />

### Meaning of the dependencies
The arrows denote call direction within the code; a number on top of an arrow indicates the count of dependencies (that is, >1). Note that only calls will be shown that are identifiable as code dependencies (“static”). This excludes dependencies that may occur in production because of communication to frameworks or resources that are not explicitly defined in the source code. 

### Visualization options and filters
Different types of dependency antipatterns can be shown by toggling *”Visualize component entanglement”*. 

<img src="../images/system-component-dependencies-visualize-toggle.png" width="450" />

Once activated, a legend will appear at the bottom describing the different types. 

<img src="../images/system-component-dependencies-legend.png" width="600" />

The legend’s colors denotes the severity of the antipattern: 

* **Layer bypassing dependency:** an architectural layer appears to be bypassed; a component has both a direct and indirect (“transitive”) dependency to another component.
* **Indirect cyclic dependency:** a set of components (>2) does not have direct cyclic dependencies, but the communication lines between the involved components form a cycle.
* **Cyclic dependency:** code within 2 components appear to “depend on each other”.

For details on their specifics, see the [Reference page on our quality models](../reference/sig-quality-models.md), specifically the [Maintainability Guidance for Producers (on the SIG website)](https://softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability-Guidance-for-producers.pdf).

If you click on an arrow in the graph, a page will appear where you can inspect the individual dependencies from- and to the selected components.

<img src="../images/system-component-dependencies-call-details.png" width="600" />

Note that the calls are shown for the direction of the arrow that you clicked at. If you want to inspect cyclic dependencies, also inspect the dependencies in the other direction.

<img src="../images/system-component-dependencies-call-details-mouseover-path.png" width="300" />

A filename mouseover shows you the full path. Clicking on the file name will bring you to its source code.

### Annotations
The annotation menu can present different data on top of the components. 

<img src="../images/system-components-annotation-ex-toggle.png" width="150" />

This may include e.g. code volume in PM/PY (person-month or person-year equivalent).

### Filtering
On the left-hand side column, you can filter dependencies per component and/or file level. This will show you a more detailed view of dependencies.

<img src="../images/system-component-dependencies-file-selection.png" width="600" />

## Refactoring candidates
This view lists the top 100 findings per metric.  

<img src="../images/system-refactoring-candidates.png" width="600" />

Clicking on a metric will expand the list, prioritized by the “severity” of the violation. This is a good approximation of technical risk. The order/prioritization of the findings cannot be changed, but their status can be. The default status is *“Raw”*. This is meant in the sense of “not yet curated by hand”. Setting another status may help you to filter findings. A finding can be set to *“Prioritize”* or *“Accept risk”*.  

<img src="../images/system-refactoring-candidates-3dots-status.png" width="300" />

Setting a finding to *“Prioritize”* will show as *“Will fix”*

<img src="../images/system-refactoring-candidates-status-set.png" width="250" />

When you set a finding to *“Accept Risk”*, its status will change to *“Risk accepted”* and the finding will be hidden by default. 

<img src="../images/filter-2.png" class="inline" /> Findings with *“Risk accepted”* can still be viewed by using the filter. By default the filter is set to *“Will fix”* and *“Raw"* only. 

The relevant filter is shown below.

<img src="../images/system-refactoring-candidates-filters-risk-accepted.png" width="150" />


### Ordering of refactoring candidates

Refactoring candidates are sorted by risk impact. This is shown as maintainability risk categories, color coded as green-yellow-orange-red from lowest- to highest risk. Within each category, code is sorted by code volume (since volume is the common denominator for the maintainability metrics). [See for more details the technical documentation](../reference/sig-quality-models.md).

As an example, the risk categories for *Unit complexity* as shown at the top of the page:

<img src="../images/system-refactoring-candidates-unit-complexity-risk-profile.png" width="600" />

The exception in this ordering is *Duplication*, where no different degrees of risks are used for the rating calculation. They are ordered by *duplicate size*, where a duplicate may appear more than 3 times, in 1 or multiple files. This is visible next to the file names in the columns "*Same file*" and "*Same component*".

The risk impact ordering is a good indication for prioritization of findings, but it may need a case-by-case analysis. Context is a defining factor, which is discussed below. 

### Dealing with Refactoring candidates

Being refactoring *candidates* should be taken literally. It is not to say that every candidate *needs* to be resolved. No system is technically perfect (or it is not for long). Every metric has tolerances for violations of the risk categories, and these violations may be defendable. 

The decision to refactor is essentially a cost-benefit trade-off. As a simplification this is determined by:
* The size of the **problem**
* The amount of **effort** to resolve that
* Expected **benefits** (like its "*future value*")

Questions to ask yourself dealing with refactoring candidates include:

**Problem** 
* Does this piece of code cause trouble to me or other developers? E.g. is this a long `switch` statement scoring badly for unit complexity, but it is perfectly readable in context?
  * How likely is it that this code will need (frequent) modification in the future?
  * Is this problem likely to grow? A "*mistake waiting to happen*"? For example, could this maintainability "*tarnish*" evolve into a security flaw?   
* How important/critical is this code in context of the system? Do we value its stability more than technical elegance?
  * To what extent is this code guarded against undesirable behavior (being well tested and contained)? And is this in sufficient proportion to the code's importance?

**Effort**
* How difficult is this to refactor? Am I confident in its unit-/integration tests?
  * Are there technical limitations, or design choices, that limit our ability to change code into a more maintainable form? Can a case be made that consistency trumps technical cleanliness? 
  * Is it efficient to change this code right now when I am already looking at it?
* Can it even be placed outside of the source code (this may be true for e.g. static referennce lists)?

**Benefits**
* What is the "*opportunity cost*" of refactoring this as opposed to "the next best thing" you could spend your time on (such as bugfixing/building new functionality)? 
* Could I gain an extra advantage by refactoring now, e.g. by improving unit tests? 

### Sigrid as part of the Agile development process
For an elaboration of using and prioritizing maintainability findings within the development process, [see the elaboration in the Agile development process document](../workflows/agile-development-process.md#for-maintainability-focus-on-technical-debt-that-is-affecting-you-right-now)

## Investigating system maintainability rating state and -changes 

A typical approach and different options to investigate what is going on in terms of maintainability metrics are described below. Getting an initial overview is discussed here in most detail. The options to further analyze have their own respective pages and paragraphs and are referred in the text. 

* **Getting an overview:** the [Maintainability Overview (see above)](#maintainability-overview) is the place to start. The different metrics give a quick breakdown of system characteristics (such as Volume or Duplication). For a background on maintainability, [see "*Our approach*" section under "*Getting Started*"](../getting-started/approach.md). 
You can find the [technical details of maintainability metrics under "*References*"](../reference/sig-quality-models.md).

With the default treemap view, as an example, a large drop in "*Component independence*" may lead you to filter on change in that metric specifically over the chosen time period. With the following menu:

<img src="../images/system-overview-treemap-menu-change-component-independence.png" width="600" />

This results in the following overview colored by rating change impact on a green-to-red color scale:

<img src="../images/system-overview-treemap-component-independence-change.png" width="600" />

To get an insight into the point of time of large changes, it may be useful to turn the default treemap into a trendline (change in the "*Chart*" drop-down menu) to see approximate when large changes have taken place. As an example, distinguishing between different metrics ("*System properties*"):

<img src="../images/system-overview-trend-system-properties.png" width="600" />

Assuming that this has been your first step into maintainability analysis, you can do several things next:

* **System architecture**: Architectural details can be analyzed in the [Component Dependencies view](#component-dependencies). For more details, [see the Architecture Quality page](architecture-quality.md) or [see "*References*" for its separate technical document](../reference/sig-quality-models.md). *Architecture Quality* does not count towards the maintainability rating.  
  * You may be triggered by an architecture-level rating change or have suspicions of architectural problems based on experience. You might experience that certain components or files are hard to maintain because they are inter-related or (tightly) coupled in complex ways. For example, when design-level changes have unpredictable effects, when small changes propagate errors/faults, when a change in one component makes integration tests fail in another part of the system. 
* **Triggered by a specific maintainability rating change**: you may be interested in understanding the cause of a specific change. There are several ways to analyze this deeper: 
  * **Delta quality**: In case of a recent change, the *Delta quality* view shows you how and where recent code modifications/additions have affected the maintainabilty rating. 
  * **Refactoring candidates**: In case code steps over certain risk thresholds ("*a violation*"), it will show up in the *Refactoring Candidates* [see Refactoring Candidates paragraph above](#refactoring-candidates). There may be several trade-offs in deciding whether and when to refactor [see relevant paragraph above on dealing with refactoring candidates](#dealing-with-refactoring-candidates). 
    * As an exception, there might be no "*Component Entanglement*" violations visible while its rating is below 4-star rating. That can be the case if there are no architectural violations to resolve, but when the number of components and their connections are higher than the benchmark. This would be visible in the [Component Dependencies view](#component-dependencies) (but **not** in the *Architecture Quality* view, since they are not directly related). 
    * For *Duplication* and unit metrics, clicking on a *Refactoring candidate* will show the affected code highlighted in context of this one file. 
  * **Code Explorer**: You may reach the *Code Explorer* from a finding in the *Refactoring candidates* list or the detailed file list from the *Delta quality* view. there you can go to the *Code Explorer* to see the unit/file/component in context of the codebase. The Code Explorer is also a good place to start if you suspect specific maintenance hotspots and want to understand the details. [See the *Code Explorer* page](system-code-explorer.md). An advantage of the Code Explorer is that it can also show per file/unit whether it contains other risky constructs, e.g. regarding security. 
  * **Using the Technical Monitor**: The strength of the *"Technical Monitor"* (accessible from the maintainability overview page) is making detailed comparisons between snapshots and filtering by technologies [discussed as part of the Code Explorer page](system-code-explorer.md#the-technical-monitor).



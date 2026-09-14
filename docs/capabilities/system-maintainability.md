# System-level maintainability

You can reach this view via the left menu on system level > quaity aspects > maintainability. See the [system-level Overview page](system-overview.md#navigating-to-capabilities).

<img width="210" height="200" alt="New_maintainability_views" src="../images/Maintainability-overview-deltaquality.png" />


The definition of what a system is, what it is comprised of, and how it is configured, are detailed in the pages on [systems within Sigrid](../organization-integration/systems.md) and the [analysis scope configuration documentation page](../reference/analysis-scope-configuration.md).

## 2 different views in the Maintainability tab 
The maintainability section on the system level has 3 views: 
1. The *Overview* tab brings the main metrics together. 
2. The [*Delta quality*](system-delta-quality.md) view shows the impact of new code changes on the system for the selected period.

## Maintainability overview
The overview page is shown below. 
* The system’s (configured) architecture is visible in the top right. This is based on the system’s scope configuration (see [the page on scope configuration](../reference/analysis-scope-configuration.md)). 
* The main code changes are visible at the bottom.
* The (change in) system metrics are in the top left. 

<img width="1294" height="881" alt="New_Maintainability_system_view" src="https://github.com/user-attachments/assets/1a58c05a-5179-4d41-8257-b882ba179794" />

In the above picture, the test code ratio might not be obvious at a glance, the displayed percentage is calculated as the ratio of "test code lines" to "production code lines". 
As an example, if there are 120 lines of test code and 100 lines of production code, the test code ratio would be:

(Number of test code lines / Number of production code lines)*100 = (120/100)*100 = 120%.

Note that this number is not the same as "test coverage", as it measures exclusively the size of the unit tests corresponding to the production code units that were present in the code upload. Our experience indicates that having a 100% test code ratio roughly translates to having 80% test coverage which is an empirical benchmark seen in practice that offers the best balance between practicality and assurance of code correctness.

The maintainability score consists of several sub-metrics that range from 1 to 5 stars, with the range 0.5 to 5.5.Please be aware that the overall score is not an average of the submetrics. A mouse-over on the individual metrics explains what they measure in short. For a general introduction on these metrics, see the section on [our approach](../getting-started/approach.md).

For technical details on maintainability metrics, see [Maintainability Evaluation Criteria](https://www.softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability.pdf) on our website, or [Maintainability Guidance for Producers (on the SIG website)](https://softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability-Guidance-for-producers.pdf).

Below the metrics overview, there is a shortcut to the *Refactoring candidates* [link on this page](system-maintainability.md#refactoring-candidates). This can also be reached by the Maintainability tab. 


### Sigrid as part of the Agile development process
For an elaboration of using and prioritizing maintainability findings within the development process, [see the elaboration in the Agile development process document](../workflows/agile-development-process.md#for-maintainability-focus-on-technical-debt-that-is-affecting-you-right-now)

## Investigating system maintainability rating state and -changes 

A typical approach and different options to investigate what is going on in terms of maintainability metrics are described below. Getting an initial overview is discussed here in most detail. The options to further analyze have their own respective pages and paragraphs and are referred in the text. 

* **Getting an overview:** the [Maintainability Overview (see above)](#maintainability-overview) is the place to start. The different metrics give a quick breakdown of system characteristics (such as Volume or Duplication). For a background on maintainability, [see "*Our approach*" section under "*Getting Started*"](../getting-started/approach.md). 
You can find the [technical details of maintainability metrics under "*References*"](../reference/sig-quality-models.md).

With the default treemap view, as an example, a large drop in *Component independence* may lead you to filter on change in that metric specifically over the chosen time period. With the following menu:

<img src="../images/system-overview-treemap-menu-change-component-independence.png" width="600" />

This results in the following overview colored by rating change impact on a green-to-red color scale:

<img src="../images/system-overview-treemap-component-independence-change.png" width="600" />

To get an insight into the point of time of large changes, it may be useful to turn the default treemap into a trendline (change in the *Chart* drop-down menu) to see approximate when large changes have taken place. As an example, distinguishing between different metrics (*System properties*):

<img src="../images/system-overview-trend-system-properties.png" width="600" />

Assuming that this has been your first step into maintainability analysis, you can do several things next:

* **System architecture**: Architectural details can be analyzed in the [Component Dependencies view](#component-dependencies). For more details, [see the Architecture Quality page](architecture-quality.md) or [see the "*References*" page for its separate technical document](../reference/sig-quality-models.md). *Architecture Quality* does not count towards the maintainability rating.  
  * You may be triggered by an architecture-level rating change or have suspicions of architectural problems based on experience. You might experience that certain components or files are hard to maintain because they are inter-related or (tightly) coupled in complex ways. For example, when design-level changes have unpredictable effects, when small changes propagate errors/faults, when a change in one component makes integration tests fail in another part of the system. 
* **Triggered by a specific maintainability rating change**: you may be interested in understanding the cause of a specific change. There are several ways to analyze this deeper: 
  * **Delta quality**: In case of a recent change, the *Delta quality* view shows you how and where recent code modifications/additions have affected the maintainabilty rating. 
  * **Refactoring candidates**: In case code steps over certain risk thresholds ("*a violation*"), it will show up in the *Refactoring Candidates* ([see the Refactoring Candidates paragraph above](#refactoring-candidates)). There may be several trade-offs in deciding whether and when to refactor ([see the relevant paragraph above on dealing with refactoring candidates](#dealing-with-refactoring-candidates)). 
    * As an exception, there might be no *Component Entanglement* violations visible while its rating is below 4-star rating. That can be the case if there are no architectural violations to resolve, but when the number of components and their connections are higher than the benchmark. This would be visible in the [Component Dependencies view](#component-dependencies) (but **not** in the *Architecture Quality* view, since they are not directly related). 
    * For *Duplication* and unit metrics, clicking on a *Refactoring candidate* will show the affected code highlighted in context of this one file. 
  * **Code Explorer**: You may reach the *Code Explorer* from a finding in the *Refactoring candidates* list or the detailed file list from the *Delta quality* view. there you can go to the *Code Explorer* to see the unit/file/component in context of the codebase. The Code Explorer is also a good place to start if you suspect specific maintenance hotspots and want to understand the details. [See the *Code Explorer* page](system-code-explorer.md). An advantage of the Code Explorer is that it can also show per file/unit whether it contains other risky constructs, e.g. regarding security. 


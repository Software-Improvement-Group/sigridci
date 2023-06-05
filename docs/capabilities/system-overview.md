# System-level overview

This section describes the main functionalities and typical uses/analysis questions on the system level, looking at details and root causes of system quality findings. 

For the portfolio-level view, see [the portfolio-level overview](portfolio-overview.md).

## Main capabilities

This section describes the quality aspects / tabs that you will encounter in Sigrid.

<img src="../images/system-overview-top-bar.png" width="600" />

### Maintainability
The maintainability section on the system level has 4 views: 
1. The *Overview* tab brings the main metrics together. 
2. The *Component Dependencies* tab visualizes architectural layering and connections.
TODO
3. The *Refactoring Candidates* tab groups and prioritizes code that does not meet 4 star quality. 
TODO
4. The *Delta quality* view shows the impact of new code changes on the entire portfolio for the selected period. By default it is grouped per system. 

Within *Delta quality*, there are three tabs available :
* **New code**: this shows the code quality of newly added files. 
* **Changed code**:this shows the quality of existing files in which a change has been made, and 
* **New & changed code**: this shows the balance of all changed- and added code quality. 
The information can be filtered and sorted by metadata (such as supplier, team, or division) by using the filter button <img src="../images/filter-2.png" width="25" />.

*New code* tends to give you the best indication of whether new development is creating high quality software. For *Changed code*, quality effects may be limited unless deliberate refactoring/renovation has been done.

### Objectives
Please see [Objectives](objectives.md).

## Analysis questions for system development progress/planning views
To gauge development progress and expected remaining work to be done, you are interested in indications of how predictable code development is. For viewing progress and predicting planning, example analysis questions are:

* For a particular system, where are technical debt and code quality moving towards? Is that what we are expecting?
* If we extrapolate progress, does it seem likely that we can meet (planning) objectives? How much (unforeseen) technical renovations will we need to take into account?

## Analysis questions for system detail views
Moving deeper into code details, to know what to focus development efforts on, example analysis questions are:

* Does the code show our craftsmanship? Can we explain why code changes are hard when the business asks us for faster delivery?
* In terms of technical debt, are we reaching quality goals? What should be prioritized on the backlog?
* How well are we generally doing securing our systems? Where is this concerning? Are we actually exposed? Are there accepted risks that we accept as a business or false positive findings that we may ignore?


### System quality overview
Quality goals can be assesed in the Overview tab. You can reach this either by starting with a portfolio view and then selecting a system from the system list. Or start at the system view and move to the Overview tab.

<img src="../images/system-overview-tab-objectives.png" width="600" />

The status of quality goals are shown in the System Objective Overview on the right (see also [Objectives](../getting-started/objectives.md)). This is binary: either the objective is met or not. 

Since a period of time has been selected, the change within this period is shown. On the right side (Delta) a change will be noted by an equal sign, upward arrow, or downward arrow. Details of changes in objectives are shown in the Quality Overview bar on the top. 

On the left, system details can be edited. Clicking on the edit button will bring you to the [metadata](../organization-integration/metadata.md) page. This will allow, and influence, filtering on these metadata fields, such as "Division" or "Business criticality".

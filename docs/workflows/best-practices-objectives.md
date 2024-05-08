# Guidelines for using Objectives

<sig-toc></sig-toc>


## Introduction

The purpose of this document is to provide concrete and actionable guidelines, hints and tips on how to successfully use portfolio and system level objectives in Sigrid.


### Structure and overview

The guidelines and best practices have been structured based on 'jobs to be done': the idea is to look at the actual tasks that stakeholders need to perform, and provide them with help to do those tasks. Jobs can embed, or refer to, other jobs.

<!--  another, obvious form of structuring the contents in this document is in a (simple) design pattern format, which is centered around a problem to be addressed. That format can provide more structure, and allows for (1) putting a problem into a context, (2) adding details, special cases and practical suggestions without cluttering the main message.
> base structure could be: name - problem - solution - (implementation in Sigrid) - consequences 
--> 

### Why you should set objectives

While nobody is fundamentally against building good software, doing that in practice is not always easy. A common problem is that for most organizations, building software isn't their goal in life, rather, it is a means to an end. For new features, it is typically (reasonably) clear how they contribute to these organizational goals. For any technical improvement work, a lot less, so technical improvements take a back seat to feature work. The result is a vicious cycle of increasing technical debt and a growing backlog of technical work. Sigrid aims to break that cycle by making quality measurable and creating a clear connection to these organizational goals. This allows technical improvements to enter in a fair competition with feature work and have a fair chance of winning.

Of course, there is no one answer to the question 'how good does my application need to be?'. This depends on various aspects, such as whether or not the application is accessible over the internet (security is more important for public facing systems), or lifecycle stage it is in (newly developed applications should be maintainable, for end-of-life applications this is less important).

The goal of objectives is to decide for each application how good it needs to be and to record the outcome of those decisions in Sigrid. By evaluating the gap between the current quality of your applications and the objective, you don't just learn where quality is lacking, but also where it is hurting your organization the most. That is why you should set objectives. A quick side note: Sigrid supports creating objectives for different categories of applications so you don't have to configure each individual app.

### Objectives and team autonomy

Sometimes, setting quality standards in a top-down way meets with resistance from teams, as they feel it clashes with the autonomy they desire. In most cases, it doesn't. At the core of Sigrid are generic engineering best practices that most engineers would subscribe to. Most engineers are happy to delegate the work of enforcing/monitoring these best practices to Sigrid so they can focus on the more sophisticated engineering challenges that are specific to their product. We consider Sigrid best practices to be an enabler for more specific engineering tasks.

As for autonomy, that is not absolute to begin with. Even the most autonomous teams work within the financial and strategic constraints of their organization. There is no reason such constraints should not exist when it comes to engineering. In many situations, teams will appreciate having explicitly agreed upon quality standards, so they have leverage when discussing the trade-off between quality and e.g. new feature requests.

The picture below depicts the hybrid model that we recommend. It aims to strike a middle ground between a top-down model that leaves teams with very little autonomy to address problems as they see fit and the fully autonomous model where management has very little control even if that would benefit the teams.

<img src="../images/hybrid-model.png" width="700" />

## Using software quality objectives: jobs to be done

As stated, the goal of objectives is to decide for each application how good it needs to be and to record the outcome of those decisions in Sigrid. This is easier said than done, not because of the actions to be performed in Sigrid, but because of the organization required. All stakeholders need to be involved and aligned which works differently in each organization. Because of this, the first job two jobs are about making sure that the initial scope (1) is meaningful but not too big to establish a workable governance structure (2). Once this has been done, the objective setting can take place, followed by monitoring and reviewing both the objectives themselves and the governance process established around. The latter may trigger enlarging the scope. This is the list of jobs, the following sections describe them in more detail:

1. [Identify a scope](#1-identify-a-scope) - a set of applications for which it make sense to set objectives
1. [Establish Governance Structure](#2-establish-governance-structure) - Set up a governance structure to oversee the objective-setting process.
1. [Set objectives](#3-set-objectives) - decide how good systems need to be
    1. [Configure Metadata](#31-configure-metadata) - helps slice and dice the portfolio
    2. [Identify Relevant Organizational Goals](#32-identify-relevant-organizational-goals) - what does the organization want to achieve? 
    3. [Link Goals to Objectives](#33-link-goals-to-objectives) - establish the quality level required to meet the goals
    4. [Configure Objectives](#34-configure-objectives) - Configure the Objectives to reflect the outcome of the previous steps
1. [Document and train](#4-document-and-train) - ensure everyone involved knows what is expected of them
1. [Monitor Objectives](#5-monitor-objective-status) - Keep track of adherence and correct if needed.
1. [Review Objectives and Governance](#6-review-objectives-and-governance) - Make sure objectives reflect the current situation and the process works.

### 1. Identify a scope
To be sure, setting objectives for a single system has value. But in most situations, business value isn't provided by a single system so setting objectives for just one system does not help to meaningfully improve things. At the same time, going through this exercise for the whole organization in one go can be impractical. So, it helps to identify a meaningful set of systems to set objectives for. While identifying a workable scope isn't an exact science, workable scopes have certain characteristics:
- A limited amount of people needs to be involved to make decisions
- The selected systems support a limited, coherent set of business processes and/or a limited/coherent set of organizational goals.

Typically, divisions or departments are a good starting point (although in large organizations, these might still be quite big). A technology platform (e.g. a low code platform) can be a useful scope because they often exist to accelerate development to decrease the time to market, which is a useful goal to base objectives on. The downside is that they typically support a variety of business processes which makes that less usable as a source of a limited, coherent set of organizational goals.

### 2. Establish governance structure
It needs to be clear who gets to decide what. Typically, the decision making involves engineering leaders (e.g. architects, lead developers, etc.). For the day-to-day management, different models are possible. Some organizations prefer a dedicated cross-functional team responsible for defining, reviewing objectives and interacting with engineering teams regularly. Others add this to the existing engineering leadership roles.

It is important to raise awareness with all stakeholders that meeting objectives is a serious concern that may have impact on the feature planning. The best practice is to allow teams and product/project owners/managers to come to a balanced priority setting themselves, but an escalation path needs to be provided to resolve conflicts if they arise.

### 3. Set objectives

Good objectives have the following characteristics:
- **Indisputable** All teams agree on the objectives unanimously to avoid discussions​
- **Relevant** Related to the context and the company objectives, e.g., impact on time-to-market​
- **Achievable** Being realistic given the numbers and timelines, and allowing prioritization on impact​
- **Modifiable**  Objectives should be continuously evaluated, refined, and become stricter along the maturity of the process​
- **Actionable**  Not meeting an objective should lead to concrete actions

The following sections describe how to get there.

#### 3.1 Configure metadata
First off, configuring metadata is essential for effective use of Sigrid, not just objective setting. We describe it here because it is essential for objective setting. With metadata, context can be added to help set meaningful objectives for certain categories of systems. As an example, security requirements for a system might be stricter for systems that are public-facing than for systems that can only be accessed through an internal network. [This page](../organization-integration/metadata.html) explains how to do this in Sigrid.

#### 3.2 Identify relevant organizational goals

First off, this section is not about actually _creating_ organizational goals. It assumes organizational goals to be present in some shape or form. It is about identifying those goals that can be reached through software. Typical examples of such goals include:
- Increase revenue
- Reduce time-to-market
- Lower costs
- Increase (product/service) quality
- Increase customer satisfaction

Often, goals link to each other. Increasing revenue might be achieved in part by increasing customer satisfaction, for example. In general, it helps to be as specific as possible. Also, don't rule out goals too early because they seem unrelated to software.

#### 3.3 Link goals to objectives

The goal of linking goals to objectives is to create a view on software quality that is shared by technical and non-technical stakeholders. It is to ensure that the objectives that will be configures in the next step are considered an organization concern as opposed to a purely technical concern.

The following table indicates how the technical concerns measured in Sigrid connect to typical organizational concerns:

| Organizational Concerns ➡ / Technical Concerns ⬇ | Market Adaptability | Time to Market | Availability | Cost Efficiency | Security | Compliance | Scalability |
|----------|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|:----------:|
| Open-Source Health | x | | | | x | x | |
| Maintainability | x | x | | x | |  | x |
| Security | | | x | | x | x | |
| Architecture Quality | x | x | x | x |  | | x |


The goal of this table is to facilitate the exercise of linking technical objectives to organizational concerns. It does not imply that the technical concerns listed fully cover the organizational concerns they link to. As an example, the 'security' concern,which is in Sigrid, is important to address the organizational concern 'security', but so are various measures against social engineering, which are not in Sigrid.

#### 3.4 Configure objectives

Our recommended approach is to set an ambitious baseline of [portfolio-level objectives](../capabilities/portfolio-objectives.md) and define exemptions as needed. For each technical concern, a separate best practice document within the Sigrid documentation provides our recommended (set of) objective(s). Since these recommended objectives assume well-written code in modern technologies, they are sometimes difficult to achieve for existing systems. For these systems, exemptions can be made either by configuring conditional portfolio objectives or [system-level objectives](../capabilities/objectives.md). Some examples:
- Mainframe code may be held to a lower maintainability standard by using a conditional objective based on the Technology category
- An older Java system might be held to a lower architecture standard by setting a system-level objective.

Make sure to add a rationale to each objective.

### 4. Document and train

Everyone involved in and affected by the objective-setting process needs to know how it works and what is expected of them. Obviously, the objectives that are set and the rationale provided are a starting point but at least two more things are needed:
- Teams need to be made aware of the objectives, their rationale and what is expected of them
- The process of [monitoring](#5-monitor-objective-status) and [review](#6-review-objectives-and-governance) need to be documented in a place that is accessible to all stakeholders. If an existing process framework is in place, the process can be made part of that framework. Examples include SAFe or an ISO based ISMS (Information Security Management System) or QMS (Quality Management System).
Specifically, it is important that an escalation path exists if not enough priority is given to meeting objectives.

### 5. Monitor objective status

Use Sigrid to monitor progress towards objectives and track system quality over time. More details can be found in the the documentation on [portfolio-level objectives](../capabilities/portfolio-objectives.md) and [system-level objectives](../capabilities/objectives.md). Leverage the reporting and analytics capabilities of Sigrid to generate insights into trends, identify areas for improvement, and make data-driven decisions. Regularly communicate progress updates to stakeholders to keep them informed and engaged.

Note that most of the work can and should be done in the teams. If the objective-setting process has been done correctly, each team understands and subscribes to the objectives that have been set, so they can plan, monitor, and perform corrective action themselves. 

### 6. Review objectives and governance

Conduct periodic reviews of objectives, especially ones that allow for exemptions to global objectives, to ensure ongoing alignment with organizational priorities and evolving organizational needs. Adjust objectives and policies as necessary based on feedback, lessons learned, and changes in the operating environment with the responsible teams. 

Conduct periodic reviews of your objective-setting process based on feedback and lessons learned. Solicit input from stakeholders on how to improve the process, streamline workflows, and enhance governance practices. Be open to adopting new tools and methodologies that can help optimize the objective-setting process and drive better outcomes.

Both the objectives themselves as well as the governance should be reviewed as often as needed, but at least twice per year. It is often useful to combine both types of reviews because they can inform each other, e.g. an objective might not be met because the work necessary could not be prioritized.

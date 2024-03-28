# Guidelines for using Objectives

<!-- 
- TODOs 
  
-->

<details>
<summary>Input documents used</summary>
Proposed goal: The Sigrid documentation should be the single source [of truth] of knowledge about Sigrid, the quality models, and SIG Best Practices, thus replacing most of these documents.

Exceptions are SIG and customer confidential information and slide decks that are (really) needed for presentations.
This means that examples that are derived from customer systems, or that expose internal detail about the benchmark need to be written down elsewhere (for now in the wiki).
 
- [Sigrid documentation](https://docs.sigrid-says.com/)
- [Portfolio objectives training](https://softwareimprovementgroupcom.sharepoint.com/:p:/r/sites/CustomerSuccessManagement/Shared%20Documents/General/Feature%20rollout/Portfolio%20Objectives/Objectives%20Training%20ppt%20.pptx?d=w17f5a45ac6154d4499518a6282b2492d&csf=1&web=1&e=zzwrKo)
- ...
  
---
</details>  

## Table of contents:
<sig-toc></sig-toc>


## Introduction

The purpose of this document is to provide concrete and actionable guidelines, hints and tips on how to successfully use portfolio and system level objectives in Sigrid.


### Structure and overview

The guidelines and best practices have been structured based on 'jobs to be done': the idea is to look at the actual tasks that stakeholders need to perform, and provide them with help to do those tasks. Jobs can embed, or refer to, other jobs.

These jobs have been grouped in three categories: first some general guidelines for conducting healthy open source usage in development, that help to get started, and may need to be revisited or updated on a regular basis. Secondly the various types of tasks that are needed to ensure continued health of libraries (note that even when application code is not actively maintained for a while, the health of open source libraries may diminish!). And thirdly a set of practical tasks in handling libraries as a developer.

<!--  another, obvious form of structuring the contents in this document is in a (simple) design pattern format, which is centered around a problem to be addressed. That format can provide more structure, and allows for (1) putting a problem into a context, (2) adding details, special cases and practical suggestions without cluttering the main message.
> base structure could be: name - problem - solution - (implementation in Sigrid) - consequences 
--> 

### The thinking behind objectives

While nobody is fundamentally against building good software, doing that in practice is not always easy. A common problem is that for most organizations, building software isn't their goal in life, rather, it's a means to an end. For new features, it's typically (reasonably) clear how they contribute to these organizational goals. For any technical improvement work, a lot less, so technical improvements take a back seat to feature work. The result is a vicious cycle of increasing tecnnical debt and a growing backlog of technical work. Sigrid aims to break that cycle by making quality measurable and creating a clear connection to these organizational goals. This allows technical improvements to enter in a fair competition with feature work and prevail.

Of course, there's no one answer to the question 'how good does my application need to be?'. This depends on various aspects, such as whether or not the application is accessible over the internet (security is more important for public facing systems), or lifecycle stage it is in (newly developed applications should be maintainable, for end-of-life applications this is less important).

The goal of objectives is to decide for each application how good it needs to be and recording the outcome of those decisions in Sigrid. By evaluating the gap between the current quality of your applications and the objective, you don't just learn where quality is lacking, but also where it's hurting your organization the most. That's the thinking behind it. A quick sidenote: Sigrid supports creating objectives for different categories of applications so you don't have to configure each individual app.

### Objectives and team autonomy

It shouldn’t. At the core of Sigrid are generic engineering best practices that most engineers would subscribe to. Most engineers are happy to delegate the work of enforcing/monitoring these best practices to Sigrid so they can focus on the more sophisticated engineering challenges that are specific to their product. Sigrid best practices are an enabler for more specific engineering tasks.

As for autonomy, that is not absolute to begin with. Even the most autonomous teams work within the financial and strategic constraints of their organization. There is no reason such constraints should not exist when it comes to engineering. In many situations, teams will appreciate having explicitly agreed upon quality standards, so they have leverage when discussing the trade-off between quality and e.g. new feature requests.

[Picture of a hybrid model]

## Using Software Quality Objectives: Jobs to be Done

1. Identify a scope - a set of applications for which it make sense to set objectives
1. Set objectives - decide how good systems need to be
    1. Configure Metadata - helps slice and dice the portfolio
    1. Identify Relevant Organizational Goals - what does the organization want to achieve? 
    1. Link Goals to Objectives - establish the quality level required to meet the goals
1. Monitor objectives and take action - decide on what to do in case objectives aren't met
1. Maintain objectives - things change. Make sure this is reflected in the objectives

### Identify a scope
To be sure, setting objectives for a single system has value. But in most situations, business value isn't provided by a single system so setting objectives for just one system does not help to meaningfully improve things. At the same time, going through this exercise for the whole organization can be impractical. So, it helps to identify a meaningful set of systems to set objectives for. While identifying a workable scope isn't an exact science, workable scopes have certain characteristics:
- A limited amount of people needs to be involved to make decisions
- The selected systems support a single business process (or a limited, coherent set) and/or a limited/coherent set of business goals.
- The amount of teams involved is somewhere between 1 and 5

Typically, divisions or departments are a good starting point (although in large organizations, these might still be quite big). A technology platform (e.g. a low code platform) can be a useful scope because they often exist to accelerate development to decrease the time to market, which is a useful goal to base objectives on. The downside is that they typically support a variety of business processes which makes that less usable as a source of a limited, coherent set of business goals.

### Set Objectives
- **Indisputable** All teams agree on the objectives unanimously to avoid discussions​
- **Relevant** Related to the context and the company objectives, e.g., impact on time-to-market​
- **Achievable** Being realistic given the numbers and timelines, and allowing prioritization on impact​
- **Modifiable**  Objectives should be continuously evaluated, refined, and become stricter along the maturity of the process​
- **Actionable**  Not meeting an objective should lead to concrete actions

#### Configure Metadata
With metadata, context can be added to help set meaningful objectives for certain categories of systems. As an example, security requirements for a system might be stricter for systems that are public-facing than for systems that can only be accessed through an internal network. [This page](https://docs.sigrid-says.com/organization-integration/metadata.html) explains how to do this.

#### Identify Relevant Organizational Goals

First off, this section is not about actually _creating_ organizational goals. It assumes organizational goals to be present in some shape or form. It's about identifying those goals that can be reached through software. Typical examples of such goals include:
- Increase revenue
- Reduce time-to-market
- Lower costs
- Increase (product/service) quality
- Increase customer satisfaction

Often, goals link to each other. Increasing revenue might be achieved in part by increasing customer satisfaction, for example. In general, it helps to be as specific as possible. Also, don't rule out goals too early because they seem unrelated to software.

#### Link Goals to Objectives

[Table that links organizational concerns to technical objectives]


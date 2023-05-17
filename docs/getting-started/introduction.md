Getting started with Sigrid
===========================================

# About this guide 
This document acts  as a user guide for Sigrid. This covers:
* **Context and background.** This page dedicates some words to our vision developing and offering Sigrid. A high-level overview of its goals and functionality.  
Other pages will discuss:
* [Roles and usage](roles-and-usage.md) The main roles/typical users that Sigrid supports. These range from management/architects to developers. They typically have different needs for views/detail (roughly from portfolio/trend to code detail view). 
  + **Analysis scenarios.** We discuss typical analysis needs or use cases and the steps can you take to get there.

## Sigrid, why you need it
Sigrid is a fact-supported cost-saver, risk-management aid and a technical-debt prioritization tool that can be used to improve quality at all system levels. 

It does that by providing you the data to steer business decisions and make technical improvements.

## Sigrid, how we see it 
We know that most organizations rely on software to run their business. Software, and taking control of it, is therefore at the center of business decisions.
* To make confident business decisions in this context, you need to be confident about the internals (the health) of your software landscape. We will provide you with the data to get that insight, and make informed decisions. The type of data accommodates the organizational context. Therefore, functionality focuses on:
  + Seeing trends of the portfolio of software as a whole.
  + Bringing together many types of technical health (such as maintainability, security, architecture).
  + Offering transparency on IT quality, which evokes accountability and makes code contributors proud of their work.

## What can you use Sigrid for?
As SIG’s software quality assurance platform, Sigrid provides a *single source of truth* of software health. This helps you steer decision-making while you buy, build, maintain and modernize your software. We call this ‘bit to boardroom insights’. These decisions will range from high-level system lifecycle decisions (e.g., renewal, decommissioning) to code-level recommendations (e.g., what to refactor and upgrade) to improve and smoothen out patterns that may slow down or endanger your business.

Sigrid visualizes your software landscape according to various technical quality aspects, into a single solution. *Quality* here is understood as characteristics of technical health (or technical debt). This includes terms defined and understood in the ISO 25010 standard, such as maintainability and security. Bringing these aspects together broadens your overview of your software landscape, which helps you expose possible technical risks. 

<img src="../images/portfolio-systems.png" width="600" />
Example of a portfolio overview. For an elaboration of the relation between systems and their repositories, see [systems](../organization-integration/systems.md).

## How does Sigrid work?
Essentially, Sigrid’s insights are based on source code analysis. Analyses are run on the code “as is”, so without actually running the system. This is known as *static analysis*, as opposed to *dynamic analysis*. Dynamic analysis of software is more typically done by the developers themselves, because it requires a simulation of how a system will behave in operation.

Sigrid recognizes, calculates and prioritizes code characteristics that indicate software health. Such as whether the code contains design anti-patterns (undesirable constructs), whether the code contains security flaws (or imported, external code contains those).  

For maintainability (the relative ease of code maintenance) Sigrid results in metrics that are benchmarked. Those are elaborated on in [maintainability](maintainability.md).


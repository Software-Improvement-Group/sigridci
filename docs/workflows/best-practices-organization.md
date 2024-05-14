# Guidelines on how to organize for quality software

<sig-toc></sig-toc>

## Introduction

The purpose of this document is to provide concrete and actionable guidelines on how organizations should set themselves up to achieve high-quality software. We are aware that many models, ideas, frameworks and the like are available on this topic which makes it a difficult one to discuss because we risk adding yet another ingredient to the already long list. The way we handle this is twofold:
- First, a lot of content on this topic focusses on speed and alignment whereas we focus on quality.
- Second, we do not aim to introduce yet another model. Rather, we identify three different levels of decision making that are present in almost all organizations and describe what they are expected to do and what they should expect from each other.

## Three levels of decision making

Having consulted with many organizations, we have identified three levels of decision making that need to be involved to achieve high quality software, structurally. These are:
- The team level
- The engineering level
- The management level

### Team Level​
The role of teams in the creation of high quality software is obvious: they actually create it. They have three main instruments to leverage their craftsmanship when it comes to creating quality software: peer reviews, tests that run in the pipeline (both functional and non-functional such as Sigrid CI) and hygiene features present in the IDE. The main inputs are quality guidelines set by the team themselves, engineering leaders and management, including objectives set in Sigrid. In reaching their quality goals, teams may identify impediments that they cannot address themselves (or that aren’t effectively/efficiently addressed by the team). These are communicated to engineering leaders or management for resolution. Team members are the core players at this level with engineering leaders (team leads, tech leads, architects) in a supporting role.​

### Engineering Leader Level​
Engineering leaders address engineering challenges that are bigger than a single ticket, may transcend teams and have the ability to significantly improve the quality of the software (or ensure that software-to-be-built is of good quality) but are not directly related to feature work. Examples include threat modelling and subsequent mitigations, major refactoring/rearchitecting, but also agreeing on standards for non-functional requirements and how to implement them. Triggers for this loop can be concerns raised by the team that they cannot address themselves, standards that need to be met, operational problems (e.g. poor performance) or antipatterns spotted by engineering leaders (team leads, tech leads, architects) themselves. They are the core players, supported by the team members and higher-level managers.​

### Management Level​
This loop is about answering the question, is the organization in control of the quality of the software it produces? Drivers can be multiple: compliance requirements, an identified need to improve quality across the board, gaining a competitive advantage by having great software are examples we’ve seen in practice. Existing methods include traditional IT Governance frameworks such as ITIL and COBIT but I'm not sure we often see that in practice. These frameworks have a strong process focus as opposed to Sigrid, which focusses on the software itself. Since there is no entrenched practice, there's not something we can easily tap into. This loop typically involves higher level managers supported by engineering leaders.​

### How to identify each level
Of these levels, **teams** are typically the easiest to identify, because they exist as such.

**Management** can be harder because many organizations, especially larger ones, have multiple layers of management and not all of them are relevant in our context. Typically though, management represents the (strategic) organizational goals and has a budget responsibility. They are accountable for the outcomes of software development and as such, are concerned with topics like cost, speed and risk. While this accountability ultimately lies with a CEO, the concerns can also be represented by a product owner or project manager.

**Engineering leadership** is typically the hardest one to identify because it's of the three the least established and exists in various forms and to varying degrees. Engineering leadership is typically involved in (higher-level) solution design, technology choices or threat analyses. Job titles may include tech lead, architect. Engineering leadership may exist in teams and organize virtually through Communities of Practice, Guilds or Chapters. In other cases, separate engineering leadership roles or teams exist, such as enterprise architects, security specialists or Centers of Excellence.

## What is needed from each level

Typically, nobody in an organization is opposed to building quality software. Rather, investing in software quality often loses out to other topics, typically features and bugs. The shift that needs to take place is that organizations allow for a fair competition to take place between feature work and technical improvements. This is not just a matter of 'the business should allow us to work on improvements instead of pushing for features'. There is a responsibility from teams and engineers to properly shape and quantify the work they think needs to be done so a fair assessment can be made. Also, teams need to accept the need for standards. In areas like security and legal, it is not practical or desirable for individual teams to assume full responsibility for these aspects. 

We consider these key ingredients of a healthy engineering culture:
- Management and engineering leads remove impediments for teams
- Management recognizes the need for technical improvements in general and takes proposals into consideration
- Teams and Engineering shape and quantify technical improvements so they can be taken in consideration
- Management and engineering leads set (well-motivated) standards for teams but give them autonomy otherwise
- Teams accept the need for standards

This picture shows the interactions and responsibilities of the different levels:

<img src="../images/organization-levels-interaction.png" width="700" />

## Strategies to ensure technical improvements

For the different levels to understand their responsibilities in producing quality software is one thing, to ensure that technical improvements are indeed happening is another. In this section, we present some strategies that make technical improvements part of the regular workflow. These strategies are generically applicable in the sense that they can be applied in an existing development process, whatever that process might be. We have seen these strategies work for customers and/or used them ourselves. Also, you can mix-and-match strategies and switch strategies over time as you learn more or circumstances change.

In [another section](#embedding-technical-improvements-in-existing-frameworks), we discuss how to embed technical improvements in existing frameworks such as SAFe or SCRUM.

### A hands-on tech lead
A hands-on tech lead is a person that oversees the technical state of a certain codebase and makes improvements themselves (the hands-on part). This person can be part of a team but can also work for multiple teams that share the same codebase. In the latter case, they might be part of a platform team.

The obvious advantage of this approach is that things will get done as this person is by design relatively immune to feature pressure. In the case of a shared codebase, they mitigate the risk that no single team feels responsible for the technical state of the code. 

There are also disadvantages. Not all codebases are big or important enough to dedicate a person to the job of keeping them healthy. The person should operate in such a way that they are seen as enabling the team(s) as opposed to being seen as an impediment. To make this happen, they cannot fly solo but need to identify a technical improvement backlog with the team(s) and work with them from time to time. This requires a certain level of people skills in addition to technical skills which makes it a very senior role.

### Set a target percentage
Teams can agree on a target percentage of their capacity that should be spent on technical improvements. This is an effective way to make sure technical work happens. The downside is that it does require some discipline in the team. A product owner (or whoever sets functional priorities) should respect an agreement even when under functional pressure. Team members should clearly articulate the work the want to do as part of that percentage and not treat it as a 'do whatever' category. 

### Applying the [boy scout rule](https://www.oreilly.com/library/view/97-things-every/9780596809515/ch08.html)
This is something you can (and should) always do. The main downside is that boy scouting only works for small, localized improvements. Bigger, more structural improvements need to be planned explicitly. If not, small changes may take a disproportional amount of time which can cause a team to unnecessarily be perceived as slow.

### Piggyback on features
Generally speaking, technical improvements, at some level, enable feature work to happen, or happen more quickly. In some cases, a clear connection can be made between a technical improvement and a desired feature: if we do technical improvement X first, developing feature Y will go faster. This can help 'sell' bigger technical improvements of which there is agreement that they need to be done at some point, but no agreement at which point exactly. 

The downside is that this may require careful stakeholder management, especially if the feature being piggybacked on is highly anticipated.

### Quality sprints
In a way, this is a version of the [target percentage](#set-a-target-percentage) strategy. But instead of setting a percentage and managing that as a going concern, a sprint (or another flavor of iteration) is used as a way to dedicate time to technical work. The advantage is that the whole team can focus on technical improvements and pick up bigger items.

The main disadvantage of this method is that it may create a 'moral hazard' in regular sprints, teams might focus exclusively on features (or feel forced to do so) under the assumption that any technical debt they may introduce is taken care of during the quality sprint.

A way to mitigate this is to not have a regular '1 out of X' cadence for quality sprints, but have the team decide on the need to have one based on the technical improvement backlog. This obviously requires a fair amount of team discipline and maturity.

## Embedding technical improvements in existing frameworks
Organizations may have implemented a framework to organize their software development. While the [strategies presented](#strategies-to-ensure-technical-improvements) are universally applicable, it may help to explain how to organize for quality software within these frameworks, using its concepts and jargon.

- [Agile/Scrum](../workflows/agile-development-process.md)
- [Scaled Agile Framework]() (SAFe)
- [Team Topologies]()
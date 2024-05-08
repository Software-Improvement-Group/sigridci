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
- The maangement level

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



## Strategies

- Dedicated tech lead (hands-on!)
- Target percentage
- Boyscouting
- Piggyback on features
- Quality sprints





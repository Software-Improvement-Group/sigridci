# Sigrid workflow for developers

As a developer, you will be interacting with other stakeholders (e.g. see a [description of the the agile development workflow](agile-development-process.md) during your day-to-day work. While providing your unique perspective on the codebase as someone who actually writes the code and implements the necessary features.

As a project evolves, a lot of its details can change over time, like the teams who work on it, the scope and requests from customers. Your task as a developer then becomes managing all these aspects together.


## Set your quality objectives
Sigrid can help you balance these aspects, by allowing you (i.e. the team) to define [objectives for non-functionals](../capabilities/objectives.md) (e.g. test code coverage, state of open-source libraries used, etc.). And then providing you with information that will help you to track progress towards those objectives as part of your process. The responsibility of setting objectives lie more with [managers](manager.md), [Product Owners](product-owner.md) and [architects](architect.md),

Either way, it is important to align with other stakeholders on code quality objectives. Regardless of whether you are extending existing code with new functionalities, improving non-functionals or adding new features to an existing codebase. Sigrid allows you to define objectives across several distinct capabilities which can then be monitored by yourself, as a developer, and by your fellow colleagues, to ensure that you and your entire team are moving in the right direction.
Setting such objectives should make the lives easier for future colleagues (including your future self) in a way that they can work with a more maintainable codebase.

## Sigrid integrated into your pipeline

Developers in modern software development teams tend to work with agile processes. The cornerstone of such processes is adhering to the mantra: _release early and often_. What this means is that the development process has become much more nimble, supported by an infrastructure (notably tests) that enables developers to release small batches of working code very often. In such a fast-paced environment, ensuring the quality of your code can be a complex task. Sigrid [fits into your CI developer workflow](../sigridci-integration/development-workflows.md) by [integrating with your development platform](../sigridci-integration/integration.md), [supporting current technologies](../reference/technology-support.md). In this way you can use Sigrid’s feedback in the CI as input for your normal code review process. 

## Manage code quality over time 

You know that there is no such thing as perfect code. Code quality exists in a context, both social and technical, in which the technologies you choose and the teams you work with can change during the lifetime of a project. It is okay to accept that the code is not in the state where you want it to be _today_. But you would want to see the needle moving in the right direction over time.
Sigrid offers you timelines on your code quality, allowing you to look at newly added and/or modified code over a certain period of time, so you and your team are in complete control over the quality of your code. For most of this insights, you might start at the [system code quality overview](../capabilities/system-overview.md), specifically the [system maintainability overview](../capabilities/system-maintainability.md), comparison [code quality changes](../capabilities/system-delta-quality.md), checking the [security overview](../capabilities/system-security.md) and [open source scan overview (*Open Source Health*)](../capabilities/system-open-source-health.md).

Sigrid also supports you in prioritizing fixing technical debt by "promoting maintainability findings" into a (markdown) template that can easily be added to your JIRA, Github, or Gitlab boards, for full transparency and control of your development process in a top-down fashion. [This is available in the Code Explorer](../capabilities/system-code-explorer.md#assisting-in-planning-with-issue-tracker-text).
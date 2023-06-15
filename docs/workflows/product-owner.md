# Sigrid workflow for product owners

As a product owner, you face a constant challenge to prioritize your sprint backlog. On one hand, you represent the voice of the customer and need to delivery as much customer value as possible, every single sprint. But on the other hand, you're also working with your team to ensure the non-functional aspects. If you *only* focus on adding more and more functionality at the expense of everything else, your productivity will eventually slow to a crawl as everyone gets increasingly overwhelmed by technical debt.

<img src="../images/po-priorities.png" width="600" />

Sigrid can help you to balance these aspects, by allowing you to define objectives for non-functional quality, and then providing you with information that will help you to track progress towards those objectives as part of your process. 

## Define shared objectives and make them part of your definition of done

[Sigrid's objectives](../capabilities/objectives.md) allow you to define clear quality goals. These goals will help you to keep non-functionals top-of-mind: It shows whether requirements are met, and allows for constructive feedback during sprint planning, daily stand-ups, and sprint reviews. This allows you to keep your product in great shape, all as part of your regular development process.

## Prioritize the issues that matter most

It is impossible to fix every single issue, especially if you've been working on a system for years and some degree of technical debt has started to accumulate. The solution for addressing technical debt is twofold. First, let's focus on *preventing* new technical debt. After all, it doesn't make sense to start fixing issues if the very next day you reintroduce a bunch of new ones. It won't be possible to prevent technical debt altogether, but at least you can try to control it. Adding [Sigrid CI](../sigridci-integration/development-workflows.md) allows you to use Sigrid's feedback during your code reviews, which makes this process explicit.

Preventing technical debt will help you in the long run, but it won't solve the existing problems. As said, solving them all is not possible, but we can prioritize the issues that have the biggest impact. You can use Sigrid's code explorer to prioritize technical debt during your sprint planning, in a way that functional tickets and technical debt are aligned instead of competing with each other. For example, it doesn't make sense to combine functional changes in component A with fixing technical debt in component B. Maybe component B hasn't been touched in years, so fixing technical debt over there isn't going to make anyone's life any better. But if you combine work on a component with technical debt in that same component, you both improve quality and also immediate create a benefit for the other people working on that component. 

## Report progress towards your objectives

[Objectives](../capabilities/objectives.md) are not only useful to the team, you can also use them to report progress to stakeholders outside of the team. To those people, concepts like software quality and non-functionals can be abstract, making it hard to explain *why* you are choosing to prioritize those issues. [Sigrid's dashboards](../capabilities/system-overview.md) help evaluate changes to the overall quality of the system. This allows you to determine whether you're on track to meet your objectives, or whether you need to pivot to prevent yourself from further trouble.

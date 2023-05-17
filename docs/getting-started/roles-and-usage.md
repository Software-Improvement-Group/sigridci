User roles and analysis scenarios in Sigrid
====================

# Where could Sigrid help me in my role?

Sigrid is aimed at organizational roles that deal with concerns around system health, code quality and their business consequences. Depending on your role you can answer different types of questions.

## Role: Executive/portfolio manager for portfolio/trend views: 
High-level overviews of the software landscape’s composition and quality help you take inventory of your landscape’s *health*, or *risk profile*. This gives direction to future plans. Example analysis questions:
* Is the portfolio balanced with business objectives and (enterprise) architecture roadmaps? 
* Do some systems appear to be in trouble while they should have a long life ahead of them?

To answer such questions, start in the portfolio view > tab *Overview*. Sigrid shows a dashboard with a quality overview of your entire portfolio, combining all quality characteristics. Based on the systems’ information, you can filter/zoom your portfolio into views that help you understand the details. 

<!-- SR I am reusing the same portfolio pic. Rather have consistency than minor variations in views-->
<!--SR relative path ../images/ does not seem to fit with the unit test -->
<img src="docs/images/portfolio-systems.png" width="600" />

Below, systems are grouped by lifecycle phase. A lifecycle phase is an indication of a system’s maturity and “adaptability needs”. They range from: initial development > Evolution > Servicing & maintenance > End-of-life. You will generally expect to see a higher maintainability for younger systems (Initial development and Evolution), because they have a long time of changes ahead of them. Lower code quality early on in a system’s life will hurt more over the long term than it would for a system that is already considered “end-of-life”. 

<!-- SR TODO from here -->

Portfolio Objectives 

Being able to set system-specific objectives can help you evaluate your system realistically based on your business context, as well as its current lifecycle phase. However, when you have many systems, setting objectives individually for each of them becomes impractical. It's important to prioritize and set stronger or weaker targets for certain systems, according to their importance for your business. Therefore, it is critical to be able to set objectives for a group of systems. This can be done via portfolio objectives. 

Portfolio Objective:  A type of objective that targets a group of systems based on similar metadata, aiming to provide an efficient and user-friendly experience that removes the need to set objectives individually for each system and better prioritization. (General rule) 


<img src="../images/portfolio-objectives-main-table.png" width="700" />


System Objective: A type of objective specific to an individual system within a portfolio that does not follow the general rule. When an objective is set at the system level, the system no longer follows the objective defined at the portfolio level.





How to define portfolio objectives? 

To define a portfolio objective, the user can click on the “Add Portfolio Objective” button on the top right of the screen:



Upon clicking the button, a pop-up will appear to guide you during the creation of a portfolio objective.

The pop-up will guide you towards configuring the portfolio objective:



There will be several dropdown menus available in the pop-up.


There will be a Capability dropdown, that allows the user to select the specific capability for which the portfolio objective will be defined.


Then, the Type dropdown, that allows the user to select a given objective type that is part of the capability selected in the previous step. In the example, we see that the Test Code Ratio is set as a type. This is due to the fact that Test Code Ratio is a type of objective that belongs to the Maintainability capability.


Finally, the last step allows for defining the actual value that we want our portfolio objective to be. 
This final field can be of two distinct types: either a free-text field, in the case of numeric objectives, or a dropdown containing a series of pre-defined values, that will be the allowed values for the given objective type.

Note also the indicator that the objective will apply to all systems in a given portfolio.


Finally, we have a free-text field called Rationale. This field can be used to add any additional details on why a given objective was set and add extra details regarding the values for ensuring full clarity to all involved stakeholders.





Importance of the Rationale field

One of the main goals of portfolio objectives is that they allow our customers to codify business objectives in Sigrid. 
A portfolio objective is not, exclusively, a technical objective, but, it’s also a business objective for our customers’ portfolio. 
An example can be as follows: consider a legacy modernization scenario, where older systems are being re-written in a more modern version of a given technology. And, let’s assume, that in order to guide that process, a quality standard is agreed upon by all stakeholders: a maintainability rating of 4.0 stars is enforced for all systems, to ensure that the re-write doesn’t degrade the existing quality.
Such a goal is an important business goal for the customer, and, now, with portfolio objectives, that business expectation can be seen and monitored through Sigrid.


Relation between system-level objectives and portfolio-level objectives

The system level and portfolio level objectives are closely related to each other, but, there are several important details to be aware of:


Portfolio level objectives are intended to be used across a wide range of the customer’s systems, and, are meant to be defined based on the metadata for these systems. In other words: the effectiveness and usefulness of portfolio level objectives will be directly related to the quality and level of granularity of the metadata.
In order for customers to define effective portfolio level objectives, they first need to define the “corresponding” metadata.


The portfolio-level objectives will act as a fallback in case no system-level objectives are defined, but, if they are, they will override the portfolio level ones.

Let’s understand the flow with a practical scenario:
As an admin, you target a subset of your systems, for which you set a high test code ratio percentage, such as, 90%. 
Then, during the day-to-day work, since one of these systems is being completely revamped, a system-level override is defined, that sets the test code ratio to only 70%, to be less strict.
From this point onwards, the system-level override will be the only one in effect, and this particular system will not be affected by the portfolio level target.
Once the developers finish their work, they no longer require the objective to be there, so, they remove it.
Upon removing it, the system-level override disappears and, simultaneously, the portfolio-level objective come into effect again, making the newly revamped system to be subjected to the higher quality standard set by the portfolio-level objective.




# Sigrid workflow for managers

The [portfolio dashboard](../capabilities/portfolio-overview.md) and [system-level dashboard](../capabilities/system-overview.md) in Sigrid provides you with insights to stay well informed about trends and changes in your software. An example is shown below. 

<img src="../images/manager-workflow-dashboard.png" width="600" />

Telling whether you are going the right direction requires goalsetting. This comparison you can make with [Sigrid Objectives (the specific non-functionals for code within Sigrid)](../capabilities/objectives.md#objectives-help-you-set-direction-and-compare-them-with-current-state). These technical objectives should naturally be in line with business characteristics such as *business criticality*, a system's *lifecycle stage*, or whether a system is web-exposed ("*deployment type*"). These can be set as [metadata](../organization-integration/metadata.md). 

Given the overlap in business interests with [Product Owners](product-owner.md) and [architects](architect.md), aligning with them will make you a more effective team, while for [developers](developer.md), objectives in Sigrid can help setting direction and should make their lives a bit easier.

Prioritizing improvement actions will depend on the input from all team members, but generally, security findings ([system level](../capabilities/system-security.md) have (and should) receive the highest urgency. This includes [possible vulnerabilities in imported code on a system level](../capabilities/system-open-source-health.md) (third party dependencies being scanned in Open Source Health). A portfolio view on [security](../capabilities/portfolio-security.md) and [Open Source Health](../capabilities/portfolio-open-source-health.md) tells you more about the general health of the landscape. 
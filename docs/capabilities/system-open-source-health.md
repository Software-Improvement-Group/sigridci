# System-level Open Source Health (OSH)
Sigrid runs a comprehensive analysis of open source software that is used in the source code. These are known here as “*Third party libraries*”. You can reach this via the top menu:
<img src="../images/system-top-bar-osh.png" width="300" />


## Navigating the overview page

The system level overview lists the third party libraries used in this system, categorized per risk area (columns on the right). On top, a trend line is shown counting changes over time. A summary of counts, changes and identified risks are shown in the top four panels. These (change) counts depend on the period that you have chosen in the top right corner. If only 1 snapshot is available, only the latest count will be provided.

<img src="../images/system-osh-top-bar-and-trendline.png" width="600" />

The default view shows a vulnerability count first:

<img src="../images/system-osh-chart-vulnerability-risk.png" width="300" />

The counts refer to number of findings in that category, and below the change in that count. An increase is shown in red, a decrease in green, and no change in blue.

All bar charts allow mouseovers that show the exact counts. For example, for vulnerabilities:

<img src="../images/system-osh-vuln-chart-mouseover-medium-ex-background.png" width="300" />

or 

<img src="../images/system-osh-vuln-chart-mouseover-high-ex-background.png" width="300" />

In this tile, different categories can be chosen by clicking on the bottom icons. In this case, *"Legal"* (the orange gavel) has been clicked and is therefore highlighted in higher contrast and a indicative dot. 

<img src="../images/system-osh-risk-barchart-bottom-icons.png" width="300" />

<img src="../images/help-corner-osh.png" class="inline" /> The help button in the right corner shows mouseovers for the respective categories.

If you change the category, the help mouseover will also change and provide you a relevant explanation. For example, for legal risks:

<img src="../images/system-osh-legal-help-mouseover.png" width="300" />


## Open Source Health scans for 6 different risk areas

“*Open Source Health*” scans for six different risk areas: 
<img src="../images/system-osh-icon-vulnerability.png" class="inline" /> **Known vulnerabilities:** publicly known and categorized vulnerabilities in a third-party dependency
<img src="../images/system-osh-icon-freshness.png" class="inline" />  **Freshness:** a measure of versioning compared to official/available versions. The count is the time difference with the date of the latest (publicly) available version. 
<img src="../images/system-osh-icon-activity.png" class="inline" />  **Activity:** an estimation of (lack of) community activity as the time passed since the last release.
<img src="../images/system-osh-icon-stability.png" class="inline" />  **Stability:** an estimate of stability by identifying seemingly unfinished versions such as alpha/beta/rc/0.x versions.
<img src="../images/system-osh-icon-dep-management.png" class="inline" />  **Management:** possible risk originating from dependencies in binaries (e.g. JARs for Java) instead of configurations in package managers.
<img src="../images/system-osh-icon-legal.png" class="inline" />  **Legal licenses:** third-party dependencies may have restricted licenses, that restrict how you can use it or e.g. obliges you to publish certain source code. This should always trigger a check by a legal expert. 

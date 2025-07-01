# System-level Open Source Health (OSH)

Sigrid scans your system for third-party libraries managed by supported package managers. In addition, Sigrid performs a best-effort scan to detect unmanaged ("raw") dependencies, such as JavaScript files, Java JARs and .Net DLLs that appear to be from third parties. The results of scanning these open source libraries are then shown in Sigrid's Open Source Health page.

## Reaching the OSH page
You can reach the Open Source Health information via the top menu if you are in System view already:

<img src="../images/system-top-bar-osh.png" width="600" />

Or you can click a capability on Portfolio *Overview* page, clicking on a system from the Portfolio Open Source Health view. See [the system-level Overview page](system-overview.md#navigating-to-capabilities), [navigating from the portfolio-level Overview page](portfolio-overview.md#navigating-to-capabilities) or [navigating from the portfolio security view](portfolio-open-source-health.md#moving-from-portfolio-level-to-system-level).

## Navigating the overview page
The system level overview lists the third party libraries used in this system, categorized per risk area (columns on the right). 
On the top left, the tile shows ratings based on the Open Source Health Quality Model, then a trend line is shown counting changes over time. 
A summary of counts, changes and identified risks are shown in four panels next to the ratings. These (change) counts depend on the period that you have chosen in the top right corner. If only 1 snapshot is available, only the latest count will be provided.

<img src="../images/system-osh-top-bar-and-trendline.png" width="600" />

### Open Source Health scans for six different risk areas

*Open Source Health* scans for six different risk areas: 

<img src="../images/system-osh-icon-vulnerability.png" class="inline" /> **Known vulnerabilities:** publicly known and categorized vulnerabilities in a third-party dependency.

<img src="../images/system-osh-icon-freshness.png" class="inline" />  **Freshness:** a measure of versioning compared to official/available versions. The count is the time difference with the date of the latest (publicly) available version. 

<img src="../images/system-osh-icon-activity.png" class="inline" />  **Activity:** an estimation of (the degree of) community activity, measured as the time that has lapsed since the last published release. 

<img src="../images/system-osh-icon-stability.png" class="inline" />  **Stability:** an estimate of stability by identifying seemingly unfinished versions such as alpha/beta/rc/0.x versions.

<img src="../images/system-osh-icon-dep-management.png" class="inline" />  **Management:** possible risk originating from dependencies in binaries (e.g. JARs for Java) instead of configurations in package managers.

<img src="../images/system-osh-icon-legal.png" class="inline" />  **Legal licenses:** third-party dependencies may have restricted licenses, that restrict how you can use it or e.g. obliges you to publish certain source code. This should always trigger a check by a legal expert. 

### Navigating the top tiles in the overview page 
The default views shows the Open Source Health Quality Model ratings first:

<img src="../images/system-osh-quality-model-ratings.png" width="300" />

You might notice that the tile does not include Stability. This metric is not used to the purpose of rating calculations, as our analyses show not bringing enough value when assessing the quality of third party open source dependencies.

Then, a tile shows the total number of dependencies for that system, and the latest scan date:

<img src="../images/system-osh-dependencies-count.png" width="300" />

Then, a vulnerability count:

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

## Filtering internal dependencies
Internal dependencies can be filtered manually, such that they will not be resolved with the Open Source Health APIs that Sigrid uses.
[Please see the Open Source Health paragraph in our scope configuration document](../reference/analysis-scope-configuration.md#open-source-health) or [this related question in the FAQ](../capabilities/faq-security.md#does-sig-filter-when-resolving-our-systems-dependencies).

## Attacking the findings list
Since there is a plausible possibility that open source vulnerabilities are actually exploitable problems, this is the place to start as a security fix backlog. Of course, context matters. And not every update is of equal difficulty. See [the prioritization section on the security page](system-security.md#filtering-results-for-false-positives-starting-with-open-source-vulnerabilities) for more considerations.

## Excluding risks

In general, we recommend you address Open Source Health risks by [updating your libraries as often and as fast as possible](../workflows/best-practices-osh.md#handling-your-libraries). 

However, there are situations in which it is impossible address a risk, and the only remaining option is to simply accept it. For example, some vulnerabilities are disputed. In that situation, "fixing" the risk is not possible, as there is no library version that removes the (disputed) vulnerability. Depicting those risks can lead to misinterpretation, as people looking at Sigrid without context have no way of knowing this vulnerability isn't as serious as it first seems. 

You can therefore exclude certain risks in the [Open Source Health configuration options](../reference/analysis-scope-configuration.md#exclude-open-source-health-risks). This includes situations where you want to exclude a certain finding for a library (e.g. license risk) while still wanting Sigrid to scan the library for other types of risk.

## How does Sigrid handle transitive dependencies?

The term "transitive dependencies" means the dependencies of your dependencies. By default, Sigrid will *not* report on transitive dependencies, and will only cover your direct dependencies. 

However, you can enable transitive dependency scanning in the [Sigrid configuration](../reference/analysis-scope-configuration.md#open-source-health). If you decide to enable this option, the transitive dependencies will *only* count towards your system's vulnerability risk and license risk. Other types of risk, like the freshness risk, do not apply to transitive dependencies. 

So why do some risks apply to transitive dependencies, but not others? The key difference is *who* is responsible for the risk. If your system contains security vulnerabilities in transitive dependencies, that's your problem, because your system is now vulnerable. Same for license risk. For something like freshness risk, that's *not* your problem, it's the problem of the people maintaining your direct dependency which is using the direct dependency.


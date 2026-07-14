# Portfolio-level Open Source Health

The Open Source Health overview page shows a summary of findings and estimated severity.  

<img width="1696" height="897" alt="New_Portfolio_OSH" src="https://github.com/user-attachments/assets/a6453fbf-cf66-4f54-a141-b8b2baf3e434" />

From left to right, the tiles read as follows:
* *Systems and libraries*: the totals of systems being scanned and the sum of identified (third party) libraries.
* *Systems with vulnerability/legal/freshness/.. risk*: the count of systems with at least 1 identified risk, ordered by risk category (e.g. *low*, *medium*, *high* or *critical*).
* *Libraries with vulnerability/legal/freshness/..risk*: the total count of libraries in each risk category, transcending systems. 

## 6 different risk areas
It is important to know how Open Source Health groups its findings. Open Source Health scans for 6 different risk areas. For an elaboration, please [see the relevant paragraph in the page describing system-level view of Open Source Health](system-open-source-health.md#open-source-health-scans-for-6-different-risk-areas). Risks are then classified and colored as <img src="../images/system-security-icon-low1.png" class="inline" /> *low*, <img src="../images/system-security-icon-medium1.png" class="inline" /> *medium*, <img src="../images/system-security-icon-high1.png" class="inline" /> *high*, or <img src="../images/system-security-icon-critical1.png" class="inline"> *critical* based on their *CVSS score*. See also [our elaboration on how CVSS works](system-security.md#context-and-meaning-of-cvss-security-metrics-from-asset-to-risk) and on [how risks are visualized in Sigrid](system-security.md#cvss-scores-in-sigrid).
The 6 categories are present on the bottom of the tiles that show the sum of number of risks.

<img src="../images/system-osh-risk-barchart-bottom-icons.png" width="400" />

<img src="../images/help-corner-osh.png" class="inline" /> The help button in the tile's upper right corner shows mouseovers for each category that you select.

In the bottom part of the screen, each system is shown with a summary of its counts: number of libraries and findings per category. For larger portfolios it may be useful to sort these on different characteristics. 

Sorting can be done per columns (here, "*Vulnerability*" as an example). The top right bottom for exporting the data as a spreadsheet may be useful for further analysis. 

<img src="../images/portfolio-open-source-health-sorting-columns-vulnerability-focus.png" width="400" /> 

## Filtering internal dependencies
Internal dependencies can be filtered manually, such that they will not be resolved with the Open Source Health APIs that Sigrid uses.
[Please see the Open Source Health paragraph in our scope configuration document](../reference/analysis-scope-configuration.md#open-source-health) or [this related question in the FAQ](../capabilities/faq-security.md#does-sig-filter-when-resolving-our-systems-dependencies).




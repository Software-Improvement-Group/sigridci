# Axis Dashboard definitions

This page defines the terms and metrics that have a specific meaning in Sigrid Axis Dashboard. The other pages link here when they use one of these terms.

## Portfolio, systems, and time

* <span id="portfolio"></span>**Portfolio:** All active systems of your organization in Sigrid. The page title says which portfolio you are looking at. A [portfolio filter](#portfolio-filter) narrows the metrics down to a group of systems in the portfolio.
* <span id="system"></span>**System:** One system in your portfolio, as onboarded in Sigrid; so a system can actually be subsystem or a micro-service. 
* <span id="period"></span>**Period:** The number of weeks that every metric on the page covers: **1 wk**, **4 wks** (the default), **13 wks**, or **All**. You choose it in the top bar, and it applies to all tabs. See [Navigating Axis Dashboard](navigating.md#1-period).
* <span id="last-complete-week"></span>**Last complete week:** A period always ends with the last complete week: the last full week, from Monday to Sunday, before the current week. The week that is still in progress is never included.
* <span id="previous-period"></span>**Previous period:** The period of the same length directly before the selected period. With a period of 4 weeks, the previous period is the 4 weeks before the last 4 weeks. All [changes](#change) compare a period with its previous period. The period **All** has no previous period.
* <span id="all"></span>**All:** The period that covers all measured weeks. It has no [previous period](#previous-period), so it shows no changes, no arrows, and no markers for a previous value.

## AI adoption

* <span id="ai-generated-code"></span>**AI-generated code:** Lines of code that Sigrid identified as written by an AI coding assistant.
* <span id="new-and-changed-code"></span>**New and changed code:** The lines of code that were added or changed in the period. This is the code your teams touched, not the complete code base of a system.
* <span id="ai-adoption"></span>**AI adoption:** The share of [new and changed code](#new-and-changed-code) that is [AI-generated](#ai-generated-code), over all systems and all weeks of the period. Sigrid adds up the lines of AI-generated code and the lines of all new and changed code before it divides them. It does not average weekly percentages. A system with no new or changed code in the period has no AI adoption.
* <span id="ai-adoption-stage"></span>**AI adoption stage:** The stage of a portfolio, or of a system, derived from its [AI adoption](#ai-adoption): *Exploring* (less than 10%), *Adopting* (from 10% up to 30%), *Scaling* (from 30% up to 60%), or *AI-native* (60% or more). A percentage exactly on the border between two stages belongs to the higher stage.
* <span id="ai-adoption-signal"></span>**AI adoption signal:** The quadrant of the AI adoption landscape that a system is in, derived from its [AI adoption](#ai-adoption) in the period and its [change](#change) against the [previous period](#previous-period). *Emerging*: low adoption, rising. *Accelerating*: high adoption, rising. *Stalled*: low adoption, not rising. *Regressing*: high adoption, not rising. High means above the middle of the adoption axis of your portfolio, so it is relative to your portfolio, not a benchmark value. Only the direction counts: a rise smaller than 2.5% still counts as rising. A system with no new or changed code in the previous period has no signal.
* <span id="ai-code-footprint"></span>**AI code footprint:** The share of all lines of code of the systems that is [AI-generated](#ai-generated-code), measured at the end of the period. It describes the whole code base, not only the code of the period.

## Speed

* <span id="pull-request-pr"></span>**Pull request (PR):** A request to merge a change into the main code of a system. Speed counts the pull requests that were merged.
* <span id="speed"></span>**Speed:** The number of [pull requests](#pull-request-pr) merged per developer per week, over all [active systems](#active-system-speed) and all weeks of the period. Sigrid adds up the pull requests and the developer-weeks before it divides them, so a busy week counts for more than a quiet one. A week of a system with an exceptional number of pull requests per developer, compared with all other system-weeks in the portfolio, is left out, because it would distort the metric. Written as PRs/dev/week.
* <span id="developer"></span>**Developer:** A person who merged code in a system in a week. For a portfolio, Sigrid counts every developer once per week, also when they work on several systems. For a [filtered portfolio](#portfolio-filter) this is not possible, so a developer who works on several of the selected systems counts once for each of them. For that reason the speed of a filtered portfolio cannot be compared with the market.
* <span id="core-developer"></span>**Core developer:** A [developer](#developer) who contributes regularly to your portfolio, as determined by Sigrid from the commit history. On the Speed tab you can calculate [speed](#speed) for core developers only, with the *Developers: core* switch.
* <span id="active-system-speed"></span>**Active system (speed):** A system is active for speed when it merged at least 5 pull requests in the 13 weeks ending with the last week of the selected period. This is the same for every period, so a short period does not shrink the set of systems. Systems that are not active are [inactive](#inactive). Speed is only available for systems where Sigrid has pull request data, which needs developer activity to be enabled for [Architecture Quality](../capabilities/architecture-quality.md).

## Output quality

* <span id="maintainability-rating"></span>**Maintainability rating:** The star rating that Sigrid gives to the maintainability of code. On the Output Quality tab it is the rating of the new and changed code of the period, shown with a ★. The [quality score](#quality-score) for maintainability is based on it.
* <span id="finding-density"></span>**Finding density:** The number of new security or reliability findings per thousand lines of changed code (findings/KLOC). A lower density is better. The [quality score](#quality-score) for security and reliability is based on it: 100 means no new findings.
* <span id="system-volume"></span>**System volume:** The size of a system in lines of code (LOC). It is the size of a bubble in the Output Quality landscape.
* <span id="code-changes"></span>**Code changes:** The amount of code a system touched in the period: the lines added, changed, or removed, in thousands of lines (KLOC). It is the size of a bubble in the [bubble chart](#bubble-chart) of the Dashboard tab, and the horizontal axis of the Output Quality landscape.
* <span id="output-quality"></span>**Output quality:** A score from 0 to 100 for the maintainability, security, and reliability of the [new and changed code](#new-and-changed-code) of the period. A higher score is better. Output quality does not describe the quality of the complete system. For that, see the quality ratings in Sigrid Core.
* <span id="quality-score"></span>**Quality score:** The score of one quality, maintainability, security, or reliability, for the code touched in the period. Sigrid compares the findings per changed line with the SIG benchmark of systems with a similar amount of change. A score of 0 is the worst in the benchmark, and a score of 100 means there are no findings. The overall output quality is the average of the scores that are available for your portfolio. A quality that Sigrid has no measurements for, for example because of a missing license, is left out. It is never counted as zero.
* <span id="active-system-output-quality"></span>**Active system (output quality):** A system is active for output quality when it changed at least 200 lines of code in the 13 weeks ending with the last week of the selected period. Systems that are not active are [inactive](#inactive).

## Zones and categories

* <span id="sig-benchmark"></span>**SIG benchmark:** The SIG benchmark is the reference data that SIG has built from many systems. Speed and output quality are compared with it, so that you can tell whether a value is low or high compared with the market.
* <span id="market-average"></span>**Market average:** The middle band of the [SIG benchmark](#sig-benchmark): from the 35th to the 65th percentile. A value in this band is *at market average*. A value below the band is *below market average*, and a value above it is *above market average*. 
* <span id="not-measured"></span>**Not measured:** A system that is active, but that has no value for the metric in the period, for example because it has no pull requests with developer data in a single week. A system that is not measured is counted, but it is not ranked. It is never shown as zero.
* <span id="inactive"></span>**Inactive:** A system with too little activity to be measured fairly: less than 5 pull requests (speed) or less than 200 changed lines of code (output quality) in the 13 weeks ending with the selected period. Inactive systems have no zone.
* <span id="signal"></span>**Signal:** The quadrant of the [bubble chart](#bubble-chart) that a system is in, for example *Higher speed, lower quality*. The list of systems shows it as a colored label. On the AI Adoption tab the signal is the [AI adoption signal](#ai-adoption-signal).

## Changes and trends

* <span id="change"></span>**Change:** How a metric moved compared with the [previous period](#previous-period). This is always shown as a percentage. If the underlying metric already is a percentage, change is shown as the percent point change in the percentages of each of the period. Output quality score is treated as if it is a percentage as well.
* <span id="stable"></span>**Stable:** A change smaller than 2.5% is stable. It is shown with a flat arrow, because small changes are normal fluctuation and not a trend. A system counts as changed when at least one of its metrics is increasing or decreasing.
* <span id="trend"></span>**Trend:** The line that shows how a metric developed over all measured weeks, independent of the selected [period](#period). Every point is the metric over the 4 weeks ending in that week, so one unusual week does not dominate. A week without data breaks the line. It is never drawn as zero.

## Page elements

* <span id="portfolio-filter"></span>**Portfolio filter:** A category that you select in one of the *Systems by ...* charts on the AI Adoption, Speed, or Output Quality tab, for example the *Scaling* stage or *Above market average*. While the portfolio filter is on, every metric on every tab is about the systems in that category only. The portfolio filter is a category, not a fixed list of systems. See [Navigating Axis Dashboard](navigating.md#2-portfolio-filter).
* <span id="bubble-chart"></span>**Bubble chart:** A chart in which every system is a bubble. The Dashboard tab compares systems on speed and output quality, with AI adoption as color intensity and the amount of [code changes](#code-changes) as the size of the bubble, see [The Dashboard tab](dashboard.md#3-system-landscape). The AI Adoption, Speed, and Output Quality tabs each have a landscape of their own.
* <span id="notice-and-alert"></span>**Notice and alert:** The two levels of the [Data availability](dashboard.md#5-data-availability) section. An **alert** means that no system has it. A **notice** means that fewer than half of the systems have a kind of data. The metrics that depend on that data are less representative in those cases.

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

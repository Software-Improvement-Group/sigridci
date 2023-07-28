# Our approach on maintainability: benchmarked code metrics offer perspective

Generally, to assess the quality of something, you need a sense of context. And each piece of software may have a widely different context. To put objective thresholds under code quality, at SIG we use technology-independent code measurements and compare those to a benchmark. A benchmark on quality is meaningful because it shows you an unbiased norm of how well you are doing. The context for this benchmark is "the current state of the software development market". This means that you can compare your source code to the code that others are producing and maintaining. 

To compare different programming technologies with each other, the metrics represent a type of abstractions that occur universally, like the volume of pieces of code and the complexity of decision paths within. In that way, system size can be normalized to "*person-months*" or "*person-years*", indications of amount of developer work done per time period. Those numbers are again based on benchmarks.  

Below a short video introduction of this approach. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/D_5SN4Q8cGI" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

Summarizing, Sigrid compares analysis results for your system against a benchmark of 10,000+ industry systems. This benchmark set is selected and calibrated (rebalanced) yearly to keep up with *the current state* of software development. "Balanced" here can be understood as a representative spread of the "system population". This will include anything in between old and new technologies, from anything legacy to modern JavaScript frameworks. In terms of technologies this is skewed towards programming languages that are now most common, because that best represents this *current state*. The metrics underlying the benchmark approach a normal distribution. This offers a sanity check of being a fair representation and allows statistical inferences on "the population" of software systems.

## Benchmarking maintainability from 1 to 5 stars

The code quality score compared to this benchmark is expressed in a star rating on a scale from 1 to 5 stars. It follows a 5%-30%-30%-30%-5% distribution. Technically, its metrics range from 0.5-5.5 stars. This is a matter of convention, but it also avoids a "*0*" rating score, because 0 is not a meaningful end on a quality scale. So the middle 30% exists between 2.5 - 3.5 and all scores within this range are scored as 3 stars, so market average. 

To be sure, so even though 50% necessarily is below average (3.0), 35% of systems will score below the 3-star threshold (below 2.5). And 35% of systems will score above the 3-star threshold (above 3.5). To avoid a suggestion of extreme precision, it is indeed helpful to think about these stars as ranges, such that 3.4 star would be considered "within the expected range of market average, on the higher end". Note that calculation rounding tolerances are always downwards, with a maximum of 2 decimals of precision. So 1.49 star will be 1.

## The system cloud: maintainability and system volume
One of the findings that the SIG maintainability benchmark consistently confirms is that system volume correlates negatively with maintainability. This generally applies to all sectors and technologies: large systems tend to be harder to maintain than smaller systems. This holds even if we take SIG model bias into account (where a higher system volume scores lower on maintainability because of e.g. increasing analysis/coordination efforts). From our experience we know that large systems can still score very well on a "code unit level" (the smallest unit of programming logic), but complexity increases quickly on an architectual level. As an illustration, a simplified visualization of what is commonly known as the "SIG cloud" is shown below. The X-axis is a logarithmic scale of system volume (in person-years) and the Y-axis represents the maintainability scale from 0.5-5.5 stars. 

<img src="../images/maintainability-benchmark-cloud.png" width="600" />

## Star ratings are predictive of speed and costs

By experience with its datasets of systems, SIG has gathered that there is a strong correlation, and cause-effect relationship, between this  star rating and development speed/system maintenance costs. For example, maintenance/ownership costs for 4-star systems are 2 times lower than for 2-star systems, and their development speed is up to 4 times faster.  See the graph below:

<img src="../images/maintainability-star-distribution.png" width="600" />

## Further reading and interpreting metrics

* **Approach and metric details**: To read on further about maintainability metrics and the benchmark approach, see the [Reference page on our quality models](../reference/sig-quality-models.md), specifically the [Maintainability Guidance for Producers (on the SIG website)](https://softwareimprovementgroup.com/wp-content/uploads/SIG-TUViT-Evaluation-Criteria-Trusted-Product-Maintainability-Guidance-for-producers.pdf).

* **Metrics in context**: Generally, whether a lower maintainability score such as a 2-star rating is an actual problem, depends on context. Considerations might be e.g. the balance between the system’s code change capacity (how easy you can make changes) and the expected business change demand (how much and how fast you need to change to get by). To aid you in setting this context, you can use Sigrid to set such metadata ([see the Metadata documentation page](../organization-integration/metadata.md)) and set specific system/portfolio quality objectives ([see the Objectives documentation page](../capabilities/objectives.md)). For aid in the area of development processes, see the "*Workflows*" documentation pages, [e.g. on using Sigrid within an Agile development process](../workflows/agile-development-process.md). 

* **Navigating/analyzing code quality**: Sigrid will help you navigate through- and analyze, all types of code quality findings. On a portfolio level, the place to start is the "*Portfolio Overview*" ([see Portfolio Overview documentation page](../capabilities/portfolio-overview.md)). Similarly, per system this is the "*System Overview*" ([see System Overview documentation page](../capabilities/system-overview.md)), specifically the Maintainability pages ([see Maintainability documentation page](../capabilities/system-maintainability.md)) and its sections on analyzing metrics ([e.g. its paragraph on analyzing metrics](../capabilities/system-maintainability.md#investigating-system-maintainability-rating-state-and--changes)).  


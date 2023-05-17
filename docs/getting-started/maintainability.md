Maintainability
===========================================

# Maintainability: benchmarked code metrics offer perspective
A benchmark on quality is meaningful because it shows you an unbiased norm of how well you are doing. For source code this means that you can compare it to the code that others are producing and maintaining.

Sigrid compares analysis results for maintainability against a benchmark of 10,000+ industry systems to give you that perspective. 

This benchmark set is selected and calibrated yearly to give a balanced view of the *current state of software development*. “Balanced” here can be understood as a representative spread of the “system population”. This will include anything in between old and new technologies. In terms of technologies this is skewed towards programming languages that are now most common. The metrics underlying the benchmark approach a normal distribution.

## Maintainability from 1 to 5 stars
The code quality score compared to this benchmark is expressed in maintainability stars on a scale from 1 to 5 stars. It follows a 5%-30%-30%-30%-5% distribution. Technically, its metrics range is from 0.5-5.5 stars. So the middle 30% exists between 2.5 - 3.5 and is scored as 3 stars, market average. 

So even though 50% necessarily is below average (3.0), 35% of systems will score below the 3-star threshold (below 2.5). And 35% of systems will score above the 3-star threshold (above 3.5). 

## Maintainability stars are predictive of speed and costs
By experience with its datasets of systems, SIG has gathered that there is a strong correlation, and cause-effect relationship, between this maintainability star rating and development speed/system maintenance costs. For example, maintenance/ownership costs for 4-star systems are 2 times lower than for 2-star systems, and their development speed is up to 4 times faster.  See the graph below:

<img src="../images/maintainability-star-distribution.png" width="600" />

## Interpretation of maintainability metrics depends on context
Whether a lower score, such as below a 3-star rating, is an actual problem, depends on context. SIG consultants will be happy to help out there. Considerations might for example be the balance between the system’s code change capacity (how easy you can make changes) and the expected business change demand (how much and how fast you need to change to get by).


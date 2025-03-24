SIG Security Quality Model 2025: Guidance for producers
=================================================================

<sig-toc></sig-toc>

## Introduction

Since 2020, SIG utilized the Security capability to get a grip on secure 
coding, and Sigrid proved its usefulness with prioritization according to the 
OWASP top-10 via the CVSS Severity Benchmark.
Nevertheless, the current way of reporting security findings in Sigrid 
is a challenge when IT leaders deal with large portfolio of applications: 
visualization and reporting proves less effective when having to prioritize 
across many applications.
SIG’s Security Quality model has been developed to fill this gap, adopting 
similar benchmarking methodologies used in other SIG Quality models.

This document outlines guidance and provides explanation to software
producers about the measurement method of SIG applied to source code. 
For the measurements SIG considers, the threshold measurement values are provided 
for scoring at the level of 4 stars.

## Model Definitions

The SIG Security Quality Model benchmark relies on the measurements we take and 
fit into the OWASP top-10: the set of security checks and findings outline 
security concerns and focus on the 10 most common, popular but relevant risks.
The rest of this document does not outline the details of each OWASP category,
(which can be found [here](https://owasp.org/Top10/)) but defines only the 
threshold at system-level for aggreated findings that are required to reach a 
4-star system rating. 

## Guidance for producers

For each OWASP top-10 category, the model associates a compliance
value based on the highest severity finding measured in that category. The 
severity categories considered in the calculations are according to CVSS. 
For a quick outline about the context and meaning of CVSS security metrics, 
[refer to this paragraph](../../capabilities/system-security.md#context-and-meaning-of-cvss-security-metrics-from-asset-to-risk).
Values are aggregated together and used to calculate a rating. 
The mapping between the aggregated value and ratings is non-linear and
benchmarked.  

As a general high-level guideline, SIG provides a non-exhaustive outlook as to
how many categories can have a certain severity, so that the system rates 4-stars:

| Critical | High      | Medium    | Low       | None/Info |
|----------|-----------|-----------|-----------|-----------|
| 1        | 0         | At most 2 | 0         | 8         |
| 0        | 0         | 0         | At most 3 | 8         |
| 1        | 0         | At most 2 | 0         | 7         |
| 0        | 0         | At most 4 | 0         | 7         |
| 0        | At most 3 | At most 1 | 0         | 7         |

These values should be seen as upper limit when combined together.
More in general, producers should strive to reduce higher severity findings
as much as possible.


## Contact and support

Feel free to contact SIG’s support department for any questions or issues 
you may have after reading this document, or when using Sigrid. 
Users in Europe can also contact us by phone at +31 20 314 0953.



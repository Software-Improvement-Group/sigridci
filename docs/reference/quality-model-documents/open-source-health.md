SIG Open Source Health Quality Model
=========================================

### Guidance for producers
December 7, 2023

<sig-toc></sig-toc>

# Introduction

Contemporary software development heavily relies on open source
third-party dependencies. Dependencies reduce the burden of spending
precious resources to implement tedious but important features, with the
benefit of relying on a wide community support that takes care of the
maintenance effort.

Nevertheless, using third-party open source dependencies also comes with
challenges and risks: daily, new security issues (vulnerabilities) found
in third-party packages might lead to exploits by malicious actors. The
nature of open source software development also comes with the risks of
lacking support, restrictive license usage, and more.

Since 2021, SIG utilized the Open Source Health capability to assess the
risks involved by using third-party open source dependencies. While the
risk assessment provided precious initial indication to stakeholders, it
did not provide how such risks compare with the market. SIG’s Open
Source Health Quality model has been developed to fill this gap,
adopting similar benchmarking methodologies used in other SIG Quality
models.

This document outlines guidance and provides explanation to software
producers about the measurement method of SIG applied to open source
third-party dependencies used in software products. For the measurements
SIG considers, the threshold measurement values are provided for scoring
at the level of 4 stars.

Throughout this document, the terms "package" and "dependency" refer to
third-party open source dependency integrated and used by a software
product.

# Model Definitions

The SIG Open Source Health Quality Model measurements are performed on
third-party open source dependencies.

Elements of a dependency that contribute to the measurements in the Open
Source Health Quality model are:

- Vulnerabilities
- Dependency Freshness
- License use
- Activity
- Management

As such, for each of the above SIG has associated a property, that is
captured by a metric. The rest of this document outlines the details and
thresholds for each of them.

# Guidance for producers

For each measurement, the values provided are the ones necessary to achieve
a 4-star rating. Minor variations in percentages or measurements could
produce small variation in the resulting ratings.

Note that these values are meant as guidance for software producers, and
are not meant to be strictly applicable, nor as a representation of what
SIG considers a best practice.

More in general, producers should strive to reduce risks measured by the
SIG Open Source Health Quality Model properties as much as possible.

## Vulnerabilities

Security vulnerabilities in open source dependencies pose a significant
threat to software integrity and security. The transparency of open
source development, while advantageous, makes code vulnerable by
potential exploitation. Code vulnerabilities in third-party open source
dependencies can lead to severe consequences, such as data breaches, or
compromised system functionality.

For the evaluation of the vulnerabilities property, the software
product’s third party vulnerable dependencies are categorized according
to the [CVSS v3](https://nvd.nist.gov/vuln-metrics/cvss) qualitative severity 
rating. CVSS is the industry de-facto standard for communicating the 
characteristics and severity of vulnerabilities. 
It is developed and maintained by the NIST.

To score a 4 stars rating for this property, a producer should aim to
have only low-risk vulnerabilities.

## Dependency Freshness

Maintaining the freshness of third-party dependencies not only helps
product security but also ensures its future-proofness. Third-party open
source dependency upkeep is a crucial activity for several reasons, and
this job is oftentimes postponed as not deemed necessary, or for lack of
resources. Consequences linked to lack of continuous dependency refresh
might lead to risks not only related to the security of a software
system (older dependencies are oftentimes vulnerable, for example), but
also with maintenance (a minor release update in a third party
dependency is less resource intensive than a major release update).

For the evaluation of the freshness property, SIG determines how much a
dependency is out-of-date by measuring how long a newer version has been
available.

To score a 4 stars rating for this property a producer should aim at
having:

- The percentage of dependencies that are out-of-date for more than 2
years should not exceed 17%.
- The percentage of dependencies that are out-of-date for more than 3,5
years should not exceed 16%.
- The percentage of dependencies that are out-of-date for more than 5
years should not exceed 7%.

## License use

Incorporating third-party open source dependencies in software products
automatically assumes accepting the license that comes with it. With
incompatible or restrictive licenses, software products might expose
themselves to legal risks. Such restrictive licenses may conflict with
the end-user, with the distribution method, or the business model, and
failure to comply with licensing terms can lead to legal repercussions.

Note that the information provided regarding the licenses used by
third-party open source dependencies and associated risks is for general
informational and risk evaluation purposes only. SIG is not a legal
entity, and as such the content does not represent legal advice. Doubts
or concerns about the legal implications of specific licenses should be
consulted with the legal department of one’s organization or from a
qualified legal professional. The accuracy and applicability of legal
information can vary and may require personalized legal guidance. SIG
disclaim any liability for actions taken based on this information.

For the evaluation of the license property, SIG measures the risks
associated with a dependency license. A brief, non-exhaustive outline of
licenses associated with open source dependencies, and risks evaluation,
is in the table below:

| Risk        | Non-exhaustive example of licenses                         |
|-------------|------------------------------------------------------------|
| High risk   | AGPL (GNU Affero GPL), CC-BY-NC-ND, CC-BY-NC, CC-BY-SA     |
| Medium risk | GPL (GNU General Public License), Mozilla, CC-BY-ND        |
| Low risk    | LGPL (GNU Lesser GPL), CDDL, Eclipse                       |
| No risk     | MIT, BSD, Apache                                           |

To score a 4 stars rating for this property, a system should have at
most four dependencies associated with low-risk licenses.

## Activity

Adopting third-party open source dependencies with an active support
community is important, as it significantly influences the reliability
and effectiveness of e.g. security patches, and timely issue resolutions
should it be needed. When a dependency starts to lack support, thus
maintenance, known vulnerabilities may never get addressed, and
compatibility issues may arise with natural software evolution. The
absence of community-driven updates compromises the future-proofness of
the dependency.

For the evaluation of the activity property, SIG determines a dependency
latest release date.

To score a 4 stars rating for this property a producer should aim at
having:

- The percentage of dependencies latest released more than 1,5 years ago
should not exceed 8,1%.
- The percentage of dependencies latest released more than 3 years ago
should not exceed 6%.
- The percentage of dependencies latest released more than 5 years ago
should not exceed 5,2%.

## Management

Effective third-party open source dependency management is crucial for
software development. Utilizing package managers streamlines most of the
operations around third-party dependencies, as they typically offer an
efficient, centralized version set-up, simplify dependency resolution,
and reduce risks of compatibility.

On the other hand, managing dependency manually increases the risks of
errors, version mismatches, or multiple versions of the same dependency
used at the same time in different parts of a software product.

For the evaluation of the management property, SIG measures unmanaged
third party open-source dependencies.

To score a 4 stars rating for this property, a system should have at
most 4,2% unmanaged dependencies.

## Contact and support
Feel free to contact SIG’s support department for any questions or issues 
you may have after reading this document, or when using Sigrid. 
Users in Europe can also contact us by phone at +31 20 314 0953.



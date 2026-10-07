# [Sigrid](https://sigrid-says.com) objectives check: ❌ Failed

- ⚠️   **Maintainability:** You are still below your objective of 4.0 stars.
- ⚠️  **Architecture:** Your changes introduced architecture issues.
- ❌️  **Open Source Health:** You have no medium-severity open source vulnerabilities.
- ❌️  **Security:** You did not meet your objective of having no 🟣 critical security findings.

#### Failed checks

| Risk | Finding | Details | Location | Actions |
|------|---------|---------|----------|---------|
| 🟣 | **Security** • A07:2025 - Authentication Failures | Hard coded password | Example2.java (line 5) | [Exclude file](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-files-and-directories-from-security-scanning) • [Exclude rule](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-security-rules) |
| 🟠 | **Architecture** • Cyclic dependency (Introduced) | Source: sigdelivery-sigrid-ci-example-dennis ▶ c.ts • Target: sigdelivery-sigrid-ci-example-dennis ▶ b.ts | c.ts | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#manually-removing-architecture-dependencies) |
| 🟠 | **Open Source Health** • `log4j-core` 2.17.0 contains known vulnerabilities. | Vulnerabilities: • [GHSA-6hg6-v5c8-fphq](https://nvd.nist.gov/vuln/detail/CVE-2026-34477) • [GHSA-vc5p-v9hr-52mj](https://nvd.nist.gov/vuln/detail/CVE-2025-68161) • [GHSA-8489-44mv-ggj8](https://nvd.nist.gov/vuln/detail/CVE-2021-44832) • [GHSA-3pxv-7cmr-fjr4](https://nvd.nist.gov/vuln/detail/CVE-2026-34480) | build.gradle | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks) |

**Detailed maintainability ratings**

| System property | System on 2026-10-02 | Before changes | New/changed code |
|-----------------|-------------------------------------------|----------------|------------------|
| Duplication | 5.5 | 5.5 | 0.5 |
| Unit Size | 5.5 | 5.5 | 0.7 |
| Unit Complexity | 5.5 | 5.5 | 0.5 |
| Unit Interfacing | 5.5 | 5.5 | 4.0 |
| Module Coupling | 5.5 | N/A | 5.4 |
| Component Independence | 0.5 | 0.5 | 5.4 |
| Component Entanglement | 1.9 | N/A | N/A |
| **Maintainability** | **3.4** | **2.6** | **1.6** |


----

[**View this system in Sigrid**](https://sigrid-says.com/aap/noot)

![© Software Improvement Group](https://sigrid-says.com/usage/matomo.php?idsite=6&rec=1&ca=1&e_c=sigridci.feedbackview&e_a=sigridci.feedbackview&e_n=sig-aap-noot)

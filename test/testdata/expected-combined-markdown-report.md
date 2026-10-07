# [Sigrid](https://sigrid-says.com) objectives check: ❌ Failed

- ⚠️   **Maintainability:** You are still below your objective of 4.0 stars.
- ⚠️  **Architecture (Beta):** Your changes introduced architecture issues.
- ❌️  **Open Source Health:** You have vulnerable open source libraries.
- ❌️  **Security:** You did not meet your objective of having no critical security findings.

#### Failed checks

Risk: 🟣 critical | 🔴 high | 🟠 medium | 🟡 low |

| Risk | Finding | Details | Location | Actions |
|------|---------|---------|----------|---------|
| 🟣 | **Security** • A07:2025 - Authentication Failures | Hard coded password | Example2.java (line 5) | [Exclude file](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-files-and-directories-from-security-scanning) • [Exclude rule](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#excluding-security-rules) |
| 🟠 | **Architecture** • Cyclic dependency (Introduced) | Source: sigdelivery-sigrid-ci-example-dennis ▶ c.ts • Target: sigdelivery-sigrid-ci-example-dennis ▶ b.ts | c.ts | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#manually-removing-architecture-dependencies) |
| 🟠 | **Open Source Health** • `log4j-core` 2.17.0 contains known vulnerabilities. | Vulnerabilities: • [GHSA-6hg6-v5c8-fphq](https://nvd.nist.gov/vuln/detail/CVE-2026-34477) • [GHSA-vc5p-v9hr-52mj](https://nvd.nist.gov/vuln/detail/CVE-2025-68161) • [GHSA-8489-44mv-ggj8](https://nvd.nist.gov/vuln/detail/CVE-2021-44832) • [GHSA-3pxv-7cmr-fjr4](https://nvd.nist.gov/vuln/detail/CVE-2026-34480) | build.gradle | [Exclude](https://docs.sigrid-says.com/reference/analysis-scope-configuration.html#exclude-open-source-health-risks) |

**Non-urgent findings**

These findings do not fail your objectives, but you might still want to look at them.

| Risk | Finding | Details | Location | Actions |
|------|---------|---------|----------|---------|
| 🔴 | **Maintainability** • Duplication (Introduced) | 74 duplicated lines across 2 occurrences | Example.java (line 41) • Example2.java (line 39) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 57 duplicated lines across 2 occurrences | Example.java (line 177) • Example2.java (line 162) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 49 duplicated lines across 2 occurrences | Example.java (line 246) • Example2.java (line 237) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 40 duplicated lines across 2 occurrences | Example.java (line 131) • Example2.java (line 110) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 17 duplicated lines across 2 occurrences | Example.java (line 3) • Example2.java (line 15) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 390 duplicated lines across 27 occurrences | Example2.java (line 318) • Example2.java (line 129) • Example.java (line 150) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 300 duplicated lines across 26 occurrences | Example2.java (line 318) • Example2.java (line 129) • Example.java (line 150) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 34 duplicated lines across 14 occurrences | Example.java (line 208) • Example2.java (line 155) • Example2.java (line 98) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 16 duplicated lines across 7 occurrences | Example.java (line 112) • Example.java (line 131) • Example.java (line 169) |  |
| 🔴 | **Maintainability** • Duplication (Introduced) | 19 duplicated lines across 12 occurrences | Example.java (line 209) • Example2.java (line 156) • Example.java (line 259) |  |
| ⚪️ | ... and 51 more findings | | | |


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

# SIG Guidelines for Tech Due Diligence: Reporting

## Reporting guidelines

Reporting is a critical phase of the Tech Due Diligence (Tech DD) engagement. Technical details are translated into actionable intelligence for the client.

This chapter provides guidelines on how to structure, communicate, and deliver findings to clients clearly, defensibly, and well-scoped to the tight timelines of Tech DD engagements.

## Knowing the audience

Since the target audience is typically a buy-side investing party that takes deal-related decisions under time pressure, there is no primary interest in deep technical material. Instead, they need:

- Red flags that could affect the deal
- High risk items for mitigation pre- or post-deal
- Cost implications of identified risks
- Prioritized recommendations

**Guideline:** ensure the report is centered around deal relevance. Every finding that is included should answer implicitly to _what does this mean for the acquisition or investment?_.

A typical pitfall is to get into the role of consulting or advising the target company’s development team. Instead, be an independent advisor to the buyer (the client). Maintain this perspective throughout the report.

## Report structure and focus

Reports based on Sigrid should roughly follow the following structure to maintain a clear narrative and a strong foundation in facts. Existing report structures should include the following concepts to fit in Sigrid results well:

- **Executive summary:** include the overall risk profile of the system or portfolio in scope. Include the most important findings relevant to the deal. Include recommendations at a high-level.
- **Chapters per finding area:** it helps to organize findings by quality aspects as assessed in Sigrid. Use separate chapters for instance for Maintainability and Open-Source Health, to clearly delineate the different analysis scopes and methodologies.
- **Scope and Methodology:** Sigrid analysis is based on standards (such as ISO 25010) and proven measurement methodologies. It is important to be clear on the approach taken, including scope. List which systems were in/out of scope. It helps to mention that the analysis was performed using an industry benchmark based on a dataset of over 400 billion lines of code. Include the approach for the various quality aspects in scope.
- **Cost and effort estimations:** where possible, translate findings into effort and cost implications. Use Sigrid’s data to support such estimates and be transparent about the assumption underlying any figures provided.
- **Prioritized actionable recommendations:** the report should include a clear overview of recommendations regarding Sigrid results. Make a distinction between:
  1. deal-critical issues,
  2. post-deal priorities, and
  3. longer-term improvement areas.

## Using Sigrid within reports

### Visualizations

The Sigrid platform provides extensive visualizations and allows drilling-down all the way to the code level for findings traceability. The various views and dashboards are valuable and can be used in reports but should not be treated as final deliverables as such.

Carefully integrate visualization into reports, and add clear interpretive statements for anything included, e.g., what does this score mean, why does it matter, and what should be done about it?

### Benchmarking

One of the core strengths of the Sigrid platform is its benchmarking capability. Results are compared to a dataset of over 400 billion lines of code. Within that benchmark, contextualize scores and ratings. An old system in an old technology may be performing well at market-average ratings, whereas a brand-new system in a modern technology should be held to higher standards.

See also the [Sigrid Results Interpretation Guide](./tech-dd-guide-interpretation.md).

### Showing examples

Avoid including extensive code samples in client-facing reports. Small, well-chosen illustrative examples can be effective, but lengthy code examples tend to lose non-technical readers. When in doubt, describe the pattern rather than showing the code.

An architecture overview, showing main components and how they connect, is usually a valuable insight. This visualization, available in Sigrid, can be an effective tool to show the simplicity, or complexity of a system.

**Important:** there may be legal implications to including code examples in reports for the client. Align with client and supplier to clarify whether code examples may be shared with the client or not.

### Integrations: Extracting Sigrid information

Apart from using the platform UI, it is possible to get results from Sigrid in additional ways:

- To generate (Powerpoint or Word) reports from Sigrid, see [Generating reports using Sigrid Report Generator](#generating-reports-using-sigrid-report-generator)
- To integrate directly with the Sigrid API:  
  [API docs](../integrations/sigrid-api-documentation.md)

## Tone, language, and confidentiality

Since reports are likely used in deal negotiations, avoid both overstating and understating risk. Sigrid’s strength is providing facts and evidence to support decision-making.

### Avoid

- Speculative language without supporting evidence.
- Absolute statements where nuance is warranted.
- Turning code measurement results into conclusions about the target team’s skills and expertise.

### Prefer

- _“Sigrid’s analysis indicates that x% of the codebase has elevated maintenance costs”_
- _“Based on the benchmark, …”_

## Confidentiality

Given the confidential nature of Tech DD engagements, be conservative with sharing code snippets, and sometimes even system and filenames. Come to clear agreements with the client and the target about what can, and cannot, be shared between the two parties.

## Final report delivery

As part of final reporting, it is important to prepare for pushback, especially when the target company gets to see the results or join reporting sessions. Be prepared to explain and defend the applied methodologies (structured models, ISO-standards, benchmarking).

Keep Sigrid reporting focused. Include only what is necessary to convey the key message. Resist the temptation to include every finding Sigrid shows.

## Tips and tricks

- Do not wait until the final report to communicate (preliminary) results with the client.
- Flag critical findings / red flags immediately. The client may need to act on the information immediately.

## Checklist for reporting

This applies to the areas in the Tech DD report that are associated with Sigrid.

- The executive summary is concise and decision-focused regarding Sigrid results.
- Scope and limitations are clearly stated.
- All findings are grounded in Sigrid data with interpretive context.
- Cost and effort implications are included where possible.
- Recommendations are prioritized based on deal relevance.
- Critical findings were communicated early during the engagement.
- Confidentiality agreements have been followed throughout (e.g., regarding source code or documentation snippets).

## Generating reports using Sigrid Report Generator

Sigrid offers the ability to generate reports based on preconfigured report templates or custom templates using predefined fields. To use this, please refer to the following GitHub page, which includes instructions on how to use this generator:

[Sigrid report generator on Github](https://github.com/Software-Improvement-Group/sigrid-report-generator)

The README document on GitHub contains examples of report layouts that can be generated, and their typical use-case.

Start with the default report template by omitting the `--layout` flag. Other layouts may be explored but can contain empty or incomplete pages.

### Using custom templates

As described on GitHub, custom PowerPoint template can be used with the slide generator. Refer to the instructions in the README to do so.

### Report generator limitations

Currently, cost estimation data (i.e., estimated maintenance effort, renovation effort, and technical debt) is experimental and not at the right maturity level to be used in final reporting. Avoid using these results. This includes the following fields listed on GitHub:

- `RENOVATION_EFFORT_PERCENTAGE`
- `RENOVATION_EFFORT_PY`
- `MAINTENANCE_FTE`
- `MAINT_RELATIVE`
- `TECHNICAL_DEBT_PERCENTAGE`
- `TECHNICAL_DEBT_PYT`
- `TECHNICAL_DEBT_SYSTEMS_CHART`
- `MARKER_MODERNIZATION_TECHNICAL_DEBT`
- `MODERNIZATION_TECHNICAL_DEBT_{parameter}`

## Partner White Label Template

As SIG partner, you will likely want to embed the Sigrid results in your own templated reports. SIG provides a sanitized version of the standard generated IT DD Report. This version is stripped of most of the SIG branding and allows partners to add logos and color schemes more easily.

Every slide in that report contains a comment section for the partner that provides additional information on the intended usage of the slide.

## Quick references

For deeper guidance, refer to the SIG Evaluation Criteria documentation and the Sigrid user manual:

- Software analysis and evaluation criteria: <https://www.softwareimprovementgroup.com/software-analysis/>
- [Sigrid user manual](../README.md)

---

This document is part of the SIG Partner Guidelines for Tech Due Diligence using Sigrid. For questions or feedback, please contact your SIG partner manager.
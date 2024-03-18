Sigrid release notes
====================

SIG uses [continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery), meaning that every change to Sigrid or the underlying analysis is released once our development pipeline has completed. On average, we release somewhere between 10 and 20 times per day. This page therefore doesn't list every single change, since that would quickly lead to an excessively long list of small changes. Instead, this page lists Sigrid and analysis changes that we consider noteworthy for the typical Sigrid user.

### March 11, 2024

- **Objectives:** The Portfolio Objectives page now allows you to drill-down, which helps you to determine which teams and systems are compliant versus non-compliant. 
- **User management:** It is now possible to use the Sigrid API for Sigrid user management. This allows for more automation and integration options. The [Sigrid API documentation](../integrations/sigrid-api-documentation.md) contains more information.
- **Technology support:** Improved support for Rust, including better automatic detection of test code.
- **Technology support:** Open Source Health now supports [Cargo](https://crates.io), which is typically used in combination with `crates.io` for dependency management in Rust systems.
- **Open Source Health:** Sigrid now supports CycloneDX SBOM version 1.5. Find out more about [importing your SBOM into Sigrid](../integrations/integration-sbom.md ).
- **Architecture Quality:** When using database technologies, stored procedures and tables are now handled differently in the architecture visualization. Previously, they looked the same visually. Separating stored procedure calls from data access, and using different colors, makes it easier to understand the system's architecture.

### February 26, 2024

- **On-premise:** The documentation for Sigrid on-premise is now also available from this documentation. This was previously covered by a series of PDF documents, but having all Sigrid documentation in a central location makes it easier to navigate.
- **User management:** Added support for user groups. This makes it significantly easier to manage Sigrid access for portfolios with large numbers of systems and/or large numbers of people. You can find more information on how to use user groups in [the extended user management documentation](../organization-integration/usermanagement.md).
- **User management:** It is now possible to change the default access rights for Single Sign-On Users. You can choose between no access (which is the default) or access to all systems. The latter is both more suitable and more convenient for organizations that have a culture of transparency, where everyone can see the entire Sigrid portfolio. This is an organization-level setting, so contact SIG support to discuss how to change this setting if you're interested.
- **Technology support:** Improved Kotlin dependency detection. This removes incorrectly detected dependencies to constructors.
- **Open Source Health:** Improved support for Maven properties.
- **Open Source Health:** The [SIG Open Source Health quality model](quality-model-documents/open-source-health.md) is now documented.

### February 12, 2024

- **Sigrid CI:** The output directory where Sigrid CI saves feedback is now a configurable. See the [options reference](client-script-usage.md) for details.
- **Open Source Health:** The Sigrid user interface now shows whether dependencies are direct or transitive (currently only for Maven and NPM). This is helpful when using the [transitive option for Open Source Health](analysis-scope-configuration.md#open-source-health), as it allows you to quickly determine a dependency's origin.
- **User management:** It is now possible to force MFA (Multi Factor Authentication) for Sigrid users. Contact SIG support for guidance on how to best introduce this option for existing Sigrid accounts. 

### January 29, 2024

- **Sigrid CI:** Sigrid CI now supports 41 additional technologies. The [technology support list](technology-support.md) has been updated to reflect the updated support.
- **Sigrid API:** You can now also use the API to retrieve Architecture Quality ratings. Refer to the [API documentation](../integrations/sigrid-api-documentation.md#architecture-quality-ratings) for more information.

### January 15, 2024

- **Objectives:** It is now possible to set portfolio objectives that consider technology, business context, lifecycle phase, and deployment type. This allows you to use Sigrid to define policies. For example, security requirements tend to be more strict for public-facing systems than for internal systems. Similarly, objectives tend to be more lenient for legacy systems, since they are approaching the end of their life cycle. You can use portfolio objectives to consider these aspects, so you can define objectives for your landscape without having to define them for every single system individually.
- **User management:** Sigrid now also supports Single Sign-On integration based on [OpenID Connect](https://auth0.com/docs/authenticate/protocols/openid-connect-protocol). This support is added in addition to the existing SAML-based integration support.
- **User management:** Your Sigrid administrators now have the ability to reset their users' MFA (multi factor authentication). Previously this could only be done by SIG support.
- **Technology support:** Updated support for various TypeScript frameworks. The number of TypeScript frameworks is pretty much infinite, so please reach out if you believe SIG does not adequately support your preferred framework.
- **Technology support:** Added support for new versions of [Poetry](https://python-poetry.org).
- **Technology support:** Added support for the Baan 4GL programming language.

### November 20, 2023

- **Dashboard:** It is now possible to view progress towards your portfolio objectives in two ways: Via the overall Sigrid portfolio dashboard (which already existed), and via the newly added "objectives" page. The latter gives you a more high-level overview of your overall objectives, without diving into the specifics regarding teams or systems. You can find more information in the [portfolio objectives documentation](..//capabilities/portfolio-objectives.md).
- **Open Source Health:** Sigrid is now able to import SBOM (Software Bill Of Materials) produced by other tools. The [SBOM standard](https://en.wikipedia.org/wiki/Software_supply_chain) is emerging as the de-facto standard for software supply chains. Sigrid was already able to *export* SBOM information, but it is now also able to *import* SBOMs. Instructions are available on how to [import SBOMs into Sigrid](../integrations/integration-sbom/md).

### November 6, 2023

- **Architecture Quality:** Architecture Quality is now part of the Sigrid base license! Don't miss our [Ask Me Anything](https://www.softwareimprovementgroup.com/events/sigrid-ask-me-anything/) session on November 23, which we'll use to answer questions about this new capability.
- **Architecture Quality:** Architecture Quality now includes an optional tree view. This can be used as a secondary way of navigating your architecture, in addition to the main architecture visualization. 
- **Architecture Quality:** Architecture Quality now has a search option. This allows you to quickly find system elements within your architecture, such as components, files, end points, or databases.

<img src="../images/aq-search.png" width="200" />

- **Architecture Quality:** The metric detail panel now includes the option to export the measurement results to Excel.
- **Open Source Health:** Sigrid can now identify the [Reciprocal Public License](https://opensource.org/license/rpl-1-5/). For commercial organizations using open source software, this license is seen as high risk due to its requirements.

### October 23, 2023

- **On-boarding:** It is now possible for all users to on-board additional systems to Sigrid. However, you might not be able to access the analysis results for your system in Sigrid until you have been given permission by your Sigrid administrator.
- **Technology support:** Added support for the [Elixir](https://elixir-lang.org) programming language.
- **Maintainability:** The maintainability overview page now shows system volume in lines of code, in addition to the system volume in person years that was already displayed. Person years is easier to interpret by non-technical users, but technical users asked to *also* show the lines of code as they find it easier to interpret this number.
- **Architecture Quality:** The [configuration options](analysis-scope-configuration.html#architecture-quality) for `grouping` now support regular expressions for more advanced/powerful configuration.

### October 9, 2023

- **Sigrid CI:** The Sigrid CI output for GitHub has been significantly improved:
  - First, Sigrid CI will now pass as long as your code improved *towards* your quality objectives. Previously, you had to *meet* your quality objectives for every single change. The old behavior can lead to frustration when you're maintaining legacy code and are trying to improve it: you can make significant improvements, but Sigrid CI would nevertheless fail your changes for not improving them *enough*. In retrospect this behavior is a bit too strict, especially in situations where the legacy code has significant technical debt but the quality objectives are very ambitious. The new behavior is much more encouraging in this type of situation, and the focus on incremental improvement also combines very well with an agile mindset.
  - We also changed the structure of the Sigrid CI feedback. The feedback now follows the structure of an agile retrospective; we first focus on what went well, then on what could be better. This means more focus on the actual changes, and less focus on previously existing technical debt. We have discussed and validated this with many developers and they found this way of communicating feedback to be more fair.
  - Finally, Sigrid CI feedback can now be displayed directly in the GitHub pull request, removing the need for additional clicks.
  - Refer to the [GitHub integration documentation](../sigridci-integration/github-actions.md) for more information on how to integrate the new output in your pipeline.
  - These improvements are initially provided for the Sigrid CI GitHub integration since it's the most used. Over the coming months, we will work towards bringing similar improvements to Sigrid CI integrations for other development platforms, prioritizing by usage.
  
<img src="../images/github-markdown.png" width="350" />

- **Technology support:** We have improved dependency detection for Kotlin. This means you might notice more dependencies for your Kotlin systems in Maintainability, Architecture Quality, and Code Explorer.
- **Architecture Quality:** The terminology for the Knowledge Distribution metric has been changed, to make it more clear what is actually measured and how these numbers should be interpreted.

### September 25, 2023

- **Security:** Added "External Integrations" category. Moved [OSH](../capabilities/osh-upload-instructions.md) and [REST API](../integrations/sigrid-api-documentation.md) pages there. Added [SAST (static analysis tooling)](../integrations/integration-security.md) explanation page. Specifically added separate pages for integration with [Checkmarx](../integrations/integration-security-checkmarx.md) and [Fortify](../integrations/integration-security-fortify.md).
- **Security:** Large additions in the [system security page](../capabilities/system-security.md), e.g. [filtering security results](../capabilities/system-security.md#filtering-results-for-false-positives-starting-with-open-source-vulnerabilities) and [prioritizing findings](../capabilities/system-security.md#prioritizing-security-findings). Also, a new section clarifying [the way that CVSS scores are calculated in Sigrid](../capabilities/system-security.md#context-and-meaning-of-cvss-security-metrics-from-asset-to-risk) and how they can be interpreted.
- **Security:** Clarified and added [third party findings options](../reference/analysis-scope-configuration.md#third-party-findings) in the scoping configuration page. Clarifications in the [technology support page](../reference/technology-support.md), e.g. added a [third party findings analyzer technology support table](../reference/technology-support.md#supported-security-analyzers).
- **Architecture Quality:** New [architecture quality](../capabilities/architecture-quality.md) options added, e.g. [grouping and annotating components](../capabilities/architecture-quality.md#grouping-and-annotating-components).
- **Documentation:** Fixed unclarities in the [self-service configuration](analysis-scope-configuration.md) page regarding component definitions and mapping test code when components are defined manually.

### August 28, 2023

- **Architecture Quality:** Sigrid can now identify and visualize dependencies that are considered undesirable. You can specify these dependencies in the [Sigrid configuration](analysis-scope-configuration.md#architecture-quality).
- **Configuration:** The React versus JavaScript configuration has been simplified, so that Sigrid's React analysis is now a superset of the JavaScript analysis. If you are using [self-service configuration](analysis-scope-configuration.md) these improvements are applied automatically, and there is no need to manually update the configuration.
  - Note: In case you formerly had both React and JavaScript in scope of Sigrid measurements and they were configured as separate technologies, then now you only the code together as part of JavaScript technology. This may have two effects for your maintainability metrics:
    - JavaScript volume in Person Months may have somewhat grown because different productivity factors between React and JavaScript are now equalized. The impact depends on the volume ratio React:JavaScript.
    - Call dependencies between React and JavaScript are now more accurate. Therefore you may seem more dependencies and this may result in a (slightly) lower module coupling score.   
- **Command line options:** `--include` is added to the command line options of `sigridci.py`. `--exclude` already allowed you to remove specific folders / files from the upload. With the addition of `--include` you can now narrow down the uploaded folders / files even more by specifying the set of folders / files to include.

### August 9, 2023

- **Objectives:** It is now possible to define objectives for *all* Sigrid capabilities, not just for Maintainability and Open Source Health. To do this, navigate to your system's dashboard, locate your objectives, and hit the edit button.
- **Technology support:** Added support for the [Dart](https://dart.dev) programming language, which is commonly used for creating apps in Google's [Flutter](https://flutter.dev) framework.

### July 31, 2023

- **Scope configuration:** The `sigrid.yaml` configuration file format has been registered with [SchemaStore.org](https://www.schemastore.org/json/). This means that IDEs such as [Visual Studio Code](https://code.visualstudio.com) or [JetBrains IDEs](https://www.jetbrains.com) will now provide content assist and indicate errors when you edit Sigrid configuration files. This both gives a productivity boost and reduces errors, since you can act on thise feedback right away when editing these files.
- **User management:** It is now possible to copy another user's permissions when creating a new users. This is generally more convenient than having to create existing permissions for the new user.
- **Documentation:** In this documentation, every section now has a "link" icon. Clicking this icon will copy the link to that particular section to your clipboard. This allows you to quickly share or store deeplinks to the documentation.

### July 24, 2023

- **Scope configuration:** It is now possible to use [self-service scope configuration](analysis-scope-configuration.md) in combination with [multi-repo systems](../sigridci-integration/development-workflows.md#combining-multiple-repositories-into-a-single-sigrid-system). Previously you could use one of these features or the other, but not both. Refer to [the configuration documentation](analysis-scope-configuration#configuring-multi-repo-systems) on how to manage this configuration.
- **Open Source Health:** Sigrid can now scan Maven dependency report files in addition to POM files. Refer to the [Open Source Health documentation](../capabilities/osh-upload-instructions) for more information on how and when this can be used.
- **Technology support:** Sigrid now supports [X++ for Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/dev-ref/xpp-language-reference).

### July 3, 2023

- **Open Source Health:** The [Python Poetry](https://python-poetry.org) dependency management tool is now supported by Sigrid. Refer to the [Open Source Health upload instructions](../capabilities/osh-upload-instructions) for more information.
- **Open Source Health:** When using Yarn, multiple versions for the same dependency would sometimes be reported. This has been changed so that only the version defined in `package.json` is reported by Sigrid.
- **User management:** Non-administrator users can now use the User Management page to see who "their" administrator is, which is helpful if they were not quite sure who to contact on their side (which is sometimes the case for very large portfolios).
- **Sigrid API:** It is now possible to [deactivate systems via the Sigrid API](../integrations/sigrid-api-documentation.md). Previously, this could only be done via the user interface.

### June 5, 2023

- **Architecture Quality:** Sigrid's Architecture Quality now matches technology support for maintainability, meaning that all 300+ technologies are now supported. You can find more information in our [technology support](technology-support.md) page.
- **On-boarding:** If Sigrid cannot detect the technologies during on-boarding, it would previously silently fail. This detection has been improved, so that these systems still appear in Sigrid.

### May 16, 2023

- **Security:** Sigrid now links to opencre.org, which is a content linking platform founded and built with a team at OWASP. Based on a Sigrid security finding, the user is taken to more information about the risk, about how to fix it, how to test for it, how to configure test tools, etc.
- **Code Explorer:** The Code Explorer is now always visible, even if there are no findings in the system. This is because many people use the Code Explorer to navigate the codebase, and this navigation is useful even without looking at findings.

### May 9, 2023

- **Portfolio dashboard:** System information has been added to the new dashboard, adding some more detail on top of the basic information displayed at the top of the page.
- **User management:** Sigrid users can now reset their own password. Previously, they had to ask either their administrator or someone at SIG support.

### May 2, 2023

- **Metadata:** In addition to the existing "division" and "supplier" metadata, a new "team" field has been introduced. This is useful for our largest clients, as this allows them to provide a team dashboard. 
- **Upload Unpacker:** Self-service on-boarding is now also supported for clients that use SFTP uploads. Previously, self-service was only possible for clients using Sigrid CI. This will help to further streamline our on-boarding process for clients that are unable to use Sigrid CI due to technical limitations or security restrictions on their side.

### April 24, 2023

- **Sigrid API:** The new Sigrid goals can also be retrieved using the API.
- **Siemens Polarion integration:** We now support SBOM integration between Sigrid and Siemens Polarion. This applies to both the components/libraries/dependencies and the associated vulnerabilities. 

### April 17, 2023

- **Portfolio/system dashboard:** The dashboards now display an indicator to show whether systems are using Sigrid CI. This information is also added to the filtering options, so you can easily determine which systems in your portfolio aren't using Sigrid CI yet.
- **Portfolio/system dashboard:** Similar to the above, an icon is shown if you use self-service scoping for the system (as opposed to using the standard configuration or a SIG-managed configuration).

## Contact and support

Feel free to contact [SIG's support department](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this document, or when using Sigrid or Sigrid CI. Users in Europe can also contact us by phone at +31 20 314 0953.

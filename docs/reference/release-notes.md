Sigrid release notes
====================

SIG uses [continuous delivery](https://en.wikipedia.org/wiki/Continuous_delivery), meaning that every change to Sigrid or the underlying analysis is released once our development pipeline has completed. On average, we release somewhere between 10 and 20 times per day. This page therefore doesn't list every single change, since that would quickly lead to an excessively long list of small changes. Instead, this page lists Sigrid and analysis changes that we consider noteworthy for the typical Sigrid user.

### July 31, 2023

- **Scope configuration:** The `sigrid.yaml` configuration file format has been registered with [SchemaStore.org](https://www.schemastore.org/json/). This means that IDEs such as [Visual Studio Code](https://code.visualstudio.com) or [JetBrains IDEs](https://www.jetbrains.com) will now provide content assist and indicate errors when you edit Sigrid configuration files. This both gives a productivity boost and reduces errors, since you can act on thise feedback right away when editing these files.
- **Documentation:** In this documentation, every section now has a "link" icon. Clicking this icon will copy the link to that particular section to your clipboard. This allows you to quickly share or store deeplinks to the documentation.

### July 24, 2023

- **Scope configuration:** It is now possible to use [self-service scope configuration](analysis-scope-configuration.md) in combination with [multi-repo systems](../sigridci-integration/development-workflows.md#combining-multiple-repositories-into-a-single-sigrid-system). Previously you could use one of these features or the other, but not both. Refer to [the configuration documentation](analysis-scope-configuration#configuring-multi-repo-systems) on how to manage this configuration.
- **Open Source Health:** Sigrid can now scan Maven dependency report files in addition to POM files. Refer to the [Open Source Health documentation](../capabilities/osh-upload-instructions) for more information on how and when this can be used.
- **Technology support:** Sigrid now supports [X++ for Dynamics 365](https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/dev-ref/xpp-language-reference).

### July 3, 2023

- **Open Source Health:** The [Python Poetry](https://python-poetry.org) dependency management tool is now supported by Sigrid. Refer to the [Open Source Health upload instructions](../capabilities/osh-upload-instructions) for more information.
- **Open Source Health:** When using Yarn, multiple versions for the same dependency would sometimes be reported. This has been changed so that only the version defined in `package.json` is reported by Sigrid.
- **User management:** Non-administrator users can now use the User Management page to see who "their" administrator is, which is helpful if they were not quite sure who to contact on their side (which is sometimes the case for very large portfolios).
- **Sigrid API:** It is now possible to [deactivate systems via the Sigrid API](sigrid-api-documentation.md). Previously, this could only be done via the user interface.

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

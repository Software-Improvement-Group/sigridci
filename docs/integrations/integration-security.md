# Importing your security tool findings into Sigrid

Sigrid allows you to import your security findings into Sigrid so you can use Sigrid as single source of truth for all software quality needs. Imported findings will show up in the Security Findings page in Sigrid.

## Importing - general process

Whichever security tool you use, the process of importing into Sigrid is largely the same:

1. **Security license needed:** A security license is needed to access Sigrid's security features. Contact your SIG account manager if you do not have one yet.
2. **Note on interchange format:** The preferred interchange format is [SARIF](https://sarifweb.azurewebsites.net/). Many security tools can export to this format. If your tool does not, and it is not explicitly supported otherwise, please contact SIG to see if we can add support.
3. **Run analysis**: How the security analysis is ran depends on your tool. SIG provides guidance for popular tools, but it is up to you to run your security tool and export its findings.
4. **Place findings alongside codebase**: The SARIF (or other) export should be placed in a `.sigrid` folder in the root of your repository and have a `.sarif` extension. Ideally this file is updated every time your security scan tool runs, either via scheduled scans or scans after a merge request. Choose the option that works best with your development workflow.
5. **Send findings to Sigrid**: 
   1. **Sigrid CI**: Because the export file is part of the codebase, it will be pushed to Sigrid along with the rest of the code if you use Sigrid CI with the publish workflow. You can also choose to explicitly push to Sigrid after updating the export file. 
   2. **SFTP / manual uploads**: Include the `.sigrid` folder with the `.sarif` file in your upload to SIG and its findings will be imported.

## Importing - specific tool support / instructions

Many tools that export SARIF will be supported with no or minimal extra effort from SIG, contact us to be sure. The below tools are guaranteed to work:

- [Fortify (SARIF format)](system-security-fortify.md)
- [Checkmarx (SARIF format)](system-security-checkmarx.md)

## Triaging findings: Which system is in control?
Security findings typically need to be processed and triaged to determine whether they are false positives, prioritized, etc. When importing external results, you can choose to either do the triage in your own tool, or in Sigrid which [also provides this feature](system-security.md#changing-a-findings-status-and-audit-trail). To ensure consistency, make an explicit choice which system is in charge of triage. Where possible, Sigrid respects already triaged findings during its import.

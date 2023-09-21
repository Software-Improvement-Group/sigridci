# Importing Fortify on Demand security findings into Sigrid

Sigrid allows you to import your security findings into Sigrid so you can use Sigrid as single source of truth for all software quality needs. Imported findings will show up in the Security Findings page in Sigrid.

## Prerequisites

- A valid Fortify subscription (either hosted/on demand or on-premise) configured to run scans on the system that you want to import.
- A Sigrid subscription that includes security.

## Running scans with Fortify

Sigrid does not specify how you run your scans. This can be on-demand in your pipeline, or on a regular schedule. For setting up Fortify and running scans, please use the Fortify documentation.

## Importing results into Sigrid

The Sigrid integration uses Fortify's [VunerabilityExporter](https://github.com/fortify/FortifyVulnerabilityExporter) tool to extract the findings from Fortify in the `SARIF` format. This Sarif export file should be placed in a `.sigrid` folder in the root of your codebase and pushed to Sigrid. It will then be automatically processed when you push your code to Sigrid.

To ensure compatibility with Sigrid, please use the provided Fortify `VulnerabilityExporter` configuration file. Place this configuration file in the `.sigrid` folder in your repository root: [Sigrid_Fortify_export.yml](#sigrid_fortify_exportyml).

Below are guidelines for specific CI platforms. If yours is not listed, it will still be possible to integrate Fortify with Sigrid using a similar approach.

### Github

This Github action extracts the latest findings from Sigrid, commits the export file and pushes it to Sigrid. Use it in conjunction with the SIG configuration for Fortify VulnerabilityExporter. 

1. Copy this Github action into your repository
2. Place [Sigrid_Fortify_export.yml](#sigrid_fortify_exportyml) into the `.sigrid` folder in your codebase.
3. Configure the following FOD secrets as repository or organization secrets [Github docs on secrets](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions):
   *  `FOD_TENANT` : Your Fortify on Demand tenant ID
   *  `FOD_USER` : Your Fortify on Demand username
   *  `FOD_PAT` : Your Fortify on Demand access token, this can be created via the Fortify web interface. [Fortify docs](https://www.microfocus.com/documentation/fortify-software-security-center/2010/SSC_Help_20.1.0/Content/SSC_UG/Gen_Auth_Tokens.htm)
   *  `FOD_RELEASE_ID` : The integer release ID of the system in Fortify. Find this by opening the release in Fortify and looking at the URL, for example: `https://emea.fortify.com/Releases/<release_ID>/Overview` 
4. Change the environment variables at the top of the script:
   * `FOD_BASE_URL`: Location where your Fortify installation runs, in this example it's emea.fortify.com
   * `SIGRID_CUSTOMER`: Your customer name as defined in Sigrid
   * `SIGRID_SYSTEM`: Your system name as defined in Sigrid.
5. Change the top section so that this action runs when you want, e.g. on a specific schedule or event. Default: Daily at 5:30 AM. [Github docs on triggering actions](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

Note that this action also includes the `sigrid-publish` workflow to push all code to Sigrid. This is optional if you are already using a separate action to push code to Sigrid, but pushing too often is not harmful.

{% raw %}
```yml
name: Import Fortify On Demand SAST Results into Sigrid
on:
  # Allow action to be triggered manually
  workflow_dispatch:
  # Run daily at 5:33 AM
  schedule:
    - cron: '33 5 * * *'

env:
  FOD_BASE_URL: "https://emea.fortify.com/"
  SIGRID_CUSTOMER: "examplecustomername"
  SIGRID_SYSTEM: "examplesystemname"

jobs:                                                  
  Export-Fortify-To-Sigrid:
    runs-on: ubuntu-latest
    permissions:
        actions: read
        contents: write
    steps:
       - uses: actions/checkout@v3
       # Pull SAST issues from Fortify and generate Sigrid-optimized SARIF output
       - name: Export Results from FoD
         uses: fortify/gha-export-vulnerabilities@v1
         with:
          export_config: ${{github.workspace}}/.sigrid/Sigrid_Fortify_export.yml
          fod_base_url: ${{ env.FOD_BASE_URL }}
          fod_tenant: ${{ secrets.FOD_TENANT }}
          fod_user: ${{ secrets.FOD_USER }}
          fod_password: ${{ secrets.FOD_PAT }}
          fod_release_id: ${{ secrets.FOD_RELEASE_ID }}
       - run: "mkdir -p .sigrid && mv ./fortify-sast.sarif .sigrid"
       - name: Display contents of .sigrid folder
         run: ls -R
         working-directory: .sigrid
       - name: Commit Fortify export to repository
         run: |
          git config --global user.name 'Fortify export'
          git add .sigrid/fortify-sast.sarif
          git commit -m "Automated Fortify export for Sigrid"
          git push
       # Optional: Directly push code to Sigrid, this will import the security findings, and also trigger a new maintainability analysis
       - name: Download Sigrid CI
         run: "git clone https://github.com/Software-Improvement-Group/sigridci.git sigridci"
       - name: Run Sigrid CI to upload code
         env:
           SIGRID_CI_TOKEN: "${{ secrets.SIGRID_CI_TOKEN }}"
         run: "./sigridci/sigridci/sigridci.py --customer ${{env.SIGRID_CUSTOMER}} --system ${{env.SIGRID_SYSTEM}} --source . --publish"
```
{% endraw %}
*File: .github/workflows/Fortify_export_to_Sigrid.yml*


### Gitlab / BitBucket

There are no detailed instructions at this time. However, the Fortify `VulnerabilityExporter` documentation explains how to enable the exporter for [Gitlab](https://github.com/fortify/FortifyVulnerabilityExporter/blob/main/USAGE.md#gitlab-integration) and [Bitbucket](https://github.com/fortify/FortifyVulnerabilityExporter/blob/main/USAGE.md#bitbucket-integration) Please use these instructions together with the [Sigrid_Fortify_export.yml](#sigrid_fortify_exportyml) export configuration file and ensure that the resulting SARIF file is committed to the `.sigrid` folder in the repository root. It can then be published to Sigrid alongside the code using the Sigrid CI integration for Gitlab or Bitbucket.


### Sigrid_Fortify_export.yml
Use this Fortify VulnerabilityExporter configuration to ensure compatibility with Sigrid:
{% raw %}
```yml
# See FortifyVulnerabilityExporter documentation for FoD connection settings and release selection

export: 
  from: fod
  to: json.github.sast

fod:
  release:
    embed:                                             # Load static scan summary as required for GitHub output
      - propertyName: staticScanSummary
        uri: /api/v3/scans/{currentStaticScanId}/summary 
  vuln:
    filterParam: scantype:Static                       # Have FoD return only static issues 
    embed:                                             # Also load details as required for GitLab output
      - subEntity: details
      - subEntity: recommendations
      - subEntity: traces

export.dir: ${GITHUB_WORKSPACE:${export.default.dir}}  # Unless overridden, use GITHUB_WORKSPACE if defined, otherwise default export dir
sarif.output: ${export.dir}/fortify-sast.sarif      # Define default output file location and name
json.github.sast.output:
  stdout: false                                        # Disabled by default to avoid vulnerability data being exposed through log files
  pretty: true                                         # Useful for debugging, disable for optimal performance
  file:   ${sarif.output}                              # Output file
  
  spring.config.activate.on-loader-plugin: fod

json.github.sast.filter.expr: vuln.scantype=='Static'
json.github.sast.format: 
  fields:
    "[$schema]": https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json 
    version: '2.1.0'
    runs:
      - tool:
          driver:
            name: 'Fortify on Demand'   
            version: SCA $[release.staticScanSummary?.staticScanSummaryDetails?.engineVersion?:'version unknown']; Rulepack $[release.staticScanSummary?.staticScanSummaryDetails?.rulePackVersion?:'version unknown']
            rules: $[vulnerabilityMappers.rules.get()]
        results: $[#check(vulnerabilityMappers.result.get().size()>1000, "GitHub does not support importing more than 1000 vulnerabilities. Please clean the scan results or update vulnerability search criteria.")?vulnerabilityMappers.result.get():{}]
  vulnerabilityMappers:
    rules.fields:
      id: $[vuln.checkId+'']
      name: $[vuln.category]
      shortDescription.text: $[vuln.category]
      fullDescription.text: $[#htmlToText(vuln.details?.summary)]
      help:
        text: $[#htmlToText(vuln.details?.explanation)+'\n\n'+#htmlToText(vuln.recommendations?.recommendations)+"\n\nFor more information, see "+vuln.deepLink]
      helpUri: $[vuln.deepLink]
      properties:
        tags: $[vuln.cwe?.split(",")]
        precision: $[(vuln.severityString matches "(Critical|Medium)") ? "high":"low" ]
        security-severity: $[{Critical:10.0,High:8.9,Medium:6.9,Low:3.9}.get(vuln.severityString)+'']
    result.fields:
      ruleId: $[vuln.checkId+'']
      message: 
        text: $[vuln.category]
      level: $[(vuln.severityString matches "(Critical|High)") ? "warning":"note" ]
      properties:
        tags: $[vuln.cwe?.split(",")]
      partialFingerprints:
        issueInstanceId: $[vuln.instanceId]
      locations:
        - physicalLocation:
            artifactLocation:
              uri: $[vuln.primaryLocationFull]
            region:
              startLine: $[vuln.lineNumber==0?1:vuln.lineNumber]
              endLine: $[vuln.lineNumber==0?1:vuln.lineNumber]
              startColumn: $[1]  # Needs to be specified as an expression in order to end up as integer instead of string in JSON
              endColumn: $[80]
      codeFlows: |-
        $[ 
          vuln.traces==null ? {}
            : 
            {{ 
                threadFlows: vuln.traces.![{
                  locations: traceEntries?.![{
                    location: {
                        message: {
                            text: #htmlToText(displayText).replaceAll("&nbsp;", " ")
                        },
                        physicalLocation: {
                            artifactLocation: {
                                uri: location
                            },
                            region: {
                                startLine: lineNumber
                            }
                        }
                    }
                  }] 
                }] 
            }} 
        ]
```
{% endraw %}
*File: .sigrid/Sigrid_Fortify_export.yml*

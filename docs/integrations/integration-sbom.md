# Importing SBOMs into Sigrid

[SBOM](https://en.wikipedia.org/wiki/Software_supply_chain) is an emerging standard for software supply chains. Sigrid is able to export SBOM information for your portfolio, either via the Sigrid user interface or via the [Sigrid REST API](sigrid-api-documentation.md).

However, Sigrid is also able to *import* SBOMs. The dependency and vulnerability information from these SBOMs will be shown alongside the information detected by Sigrid itself, allowing you to use Sigrid as a comprehensive overview that combines information from multiple sources.

There are various reasons on why you would consider to import existing SBOM information into Sigrid:

- You have internal SBOM information that is not accessible to Sigrid, and you want to feed this information into Sigrid to have a full overview.
- You are already using other tools that provide this SBOM information, and you would prefer to reuse the existing information rather than having Sigrid re-scan it.
- Sigrid does not support some of the technologies used in your portfolio.

In these scenarios, Sigrid will import the dependencies from your SBOM. It will then *enrich* your SBOM information with additional information that is not normally found in the SBOM, such as freshness information and benchmark risks. The enriched results are then added to Sigrid.

That said, note that in most situations you would *not* need this feature. Sigrid supports a [large number of technologies and open source ecosystems](../reference/technology-support.md), so in most cases Sigrid will be able to provide SBOM information for your systems without the need for importing additional files. This integration exists to offer additional flexibility for the scenarios listed above.

## What types of SBOM are supported?

Sigrid's SBOM import support is not based on specific tools, but on specific *standards*. One of the goals of SBOM is to provide a standardized structure for different tools to provide this type of information. There are two commonly used "flavors" of SBOM, and both are supported by Sigrid:

- [CycloneDX SBOM](https://cyclonedx.org/capabilities/sbom/)
- [SPDX SBOM](https://github.com/opensbom-generator/spdx-sbom-generator)

Both are able to export the SBOM information to a JSON file, which can then be imported by Sigrid.

## How to publish your SBOM to Sigrid

- Export your SBOM to a JSON file.
- Add this JSON file to a directory called `.sigrid` in the root of your repository.
- Publish your code to Sigrid as normal.
- Your provided SBOM information will now appear in Sigrid, alongside Sigrid's own information.

## Example

Let's say we have a Python system, and we want to use [CycloneDX Python](https://github.com/CycloneDX/cyclonedx-python) to create an SBOM and import that into Sigrid. This example is slightly contrived, as Sigrid is perfectly able to provide this information itself, but for the sake of simplicity let's say that's what we want to do. Let's also assume we're using GitHub and GitHub Actions.

The first step is to generate the SBOM. We don't want to store this file in our repository, as we want to generate the SBOM on-the-fly to make sure it reflects the current state of our code. That means it's probably the best choice to produce the SBOM as part of the build in GitHub Actions:

{% raw %}
```
mkdir .sigrid
cyclonedx-py environment -o .sigrid/sbom.json --output-format json
```
{% endraw %}

This will generate the JSON file in the correct directory. We can now follow the [Sigrid CI instructions for GitHub Actions](../sigridci-integration/github-actions.md) to publish our system to Sigrid, just like we did before. There are no special instructions or configurations to make Sigrid "see" the SBOM JSON file, this will happen automatically as long as you generate the file in the correct location.

## Combining the SBOM with Sigrid scanning

By default, Sigrid will combine both the dependencies from your SBOM *and* the dependencies it finds in your codebase. If needed, you can change this behavior so that Sigrid *only* shows the contents of your SBOM. This can be done in the [Sigrid configuration](../reference/analysis-scope-configuration.md#configuring-sbom-import).

## Contact and support

Feel free to contact [SIG's support team](mailto:support@softwareimprovementgroup.com) for any questions or issues you may have after reading this documentation or when using Sigrid.

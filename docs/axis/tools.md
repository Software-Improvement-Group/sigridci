# Sigrid Axis MCP tools reference

The Sigrid Axis MCP server gives an agent one Guardrails check that reads the code in your working tree, and tools that read what Sigrid Core found in a published system or write triage decisions back to it.

The skills call these tools for you. You need this page when you prompt the tools directly, restrict which ones a session sees, or debug a connection. For connecting the server, see [installation](installation.md).

## How tool names appear

This page writes the tools in dotted form, such as `guardrails.quality_check`. Clients display them differently. Claude Code shows `guardrails_quality_check`, and with the plugin it adds the prefix `mcp__plugin_axis_axis__`, which is also the prefix to use in a permission allowlist. Match on the tool, not on the exact string.

Every tool except `guardrails.quality_check` takes a `customer` and a `system`, the names in your Sigrid URL. The parameters below are the ones that shape the result.

## Tools at a glance

| Tool | Capability |
| --- | --- |
| `guardrails.quality_check` | [Guardrails](guardrails.md) |
| `maintainability.get_ratings` | [Auto-fix Agents](autofix-agents.md) |
| `maintainability.get_findings` | [Auto-fix Agents](autofix-agents.md) |
| `security.get_findings` | [Auto-fix Agents](autofix-agents.md) |
| `reliability.get_findings` | [Auto-fix Agents](autofix-agents.md) |
| `opensourcehealth.get_risks` | [Auto-fix Agents](autofix-agents.md) |
| `opensourcehealth.get_vulnerabilities` | [Auto-fix Agents](autofix-agents.md) |
| `get_finding` | [Auto-fix Agents](autofix-agents.md) |
| `update_finding_status` | [Auto-fix Agents](autofix-agents.md) |
| `architecture.get_internal` | [Auto-fix Agents](autofix-agents.md) |
| `architecture.get_external_dependencies` | [Auto-fix Agents](autofix-agents.md) |
| `architecture.get_worst_directories` | [Auto-fix Agents](autofix-agents.md) |

## Guardrails

`guardrails.quality_check` checks one file for maintainability and security issues. It returns the maintainability guidelines the file violates, with a severity and a line range per unit, plus a separate list of security findings. Both lists empty means a pass. It does not return a rating.

- `filename`: the original file name, including the extension, so the right language rules apply.
- `code_snippet`: the file's contents, exactly as written to disk, not a diff or a summary. For Java, pass a complete class that compiles, because the analyzer compiles it.

See [supported technologies](guardrails.md#supported-technologies).

## Maintainability

`maintainability.get_ratings` returns the current maintainability ratings, on a scale from 0.5 to 5.5 stars, where 3.0 is the market average and 4.0 is the target for new development.

- `component`: set to true for ratings per component instead of for the whole system.
- `technology`: set to true to add statistics per technology.

`maintainability.get_findings` returns the refactoring candidates for one [maintainability property](../reference/sig-quality-models.md), ranked by their weight in the rating. Each candidate has an `id` to pass to `update_finding_status`.

- `system_property`: one of `duplication`, `unitSize`, `unitComplexity`, `unitInterfacing`, `moduleCoupling`, `componentIndependence`, or `componentEntanglement`.
- `count`: how many candidates to return. The default is 20.
- `technology`: filter on a technology.
- `status`: the statuses to include. The default is all of them: `RAW`, `WILL_FIX`, and `ACCEPTED`.

## Security and reliability

`security.get_findings` returns open security findings, ranked by severity and then by exploitability, with CWE identifiers and file locations. `reliability.get_findings` does the same for reliability findings, such as error handling, concurrency, and resource management. Each finding has an `id` to pass to `get_finding` and `update_finding_status`. Both take the same parameters:

- `severity_min`: `LOW` (the default), `MEDIUM`, `HIGH`, or `CRITICAL`.
- `model`: the security model, one of `ow10`, `sigsec`, `5055sec`, `c25`, `pci4`, `owasvs4c`, `owasvs4s`, or `lcnc10`. For reliability, `sigrel` or `5055rel`. Leave it out for your organization's default.
- `path_prefix`: only findings under this file path. Long, specific prefixes work best.
- `limit`: at most 100. The default is 25.
- `status`: the statuses to include. By default, findings marked `FIXED` or `FALSE_POSITIVE` are left out.

## Open source health

`opensourcehealth.get_risks` returns open source dependency risks across six dimensions: vulnerability, freshness, legal, activity, stability, and management. It is the default tool for any question about open source health.

- `risk_dimension`: only these dimensions. A dependency matches if any of them is at or above `risk_min`.
- `risk_min`: `NONE`, `LOW`, `MEDIUM` (the default), `HIGH`, or `CRITICAL`.
- `limit`: at most 100. The default is 25.

`opensourcehealth.get_vulnerabilities` returns the known CVEs in your dependencies, ranked by CVSS score.

- `severity_min`: `LOW`, `MEDIUM` (the default), `HIGH`, or `CRITICAL`.
- `limit`: at most 100. The default is 25.

## Findings

`get_finding` looks up one finding by its id, typically one you saw earlier through one of the `get_findings` tools.

- `finding_id`: the `id` returned with the finding.
- `finding_type`: `security`, `reliability`, or `maintainability`.
- `system_property`: required when `finding_type` is `maintainability`.

`update_finding_status` sets the status or the remark of a finding, so Sigrid reflects the agent's decision. Open source health findings do not have a status, so this tool does not work for them.

- `finding_id`: the `id` returned with the finding.
- `status`: the new status, from the table below.
- `remark`: a note to attach to the finding.

You have to pass at least one of `status` and `remark`. The valid statuses depend on the type of finding:

| Finding type | Valid statuses |
| --- | --- |
| Maintainability | `RAW`, `WILL_FIX`, `ACCEPTED` |
| Security, reliability | `RAW`, `REFINED`, `WILL_FIX`, `FIXED`, `ACCEPTED`, `FALSE_POSITIVE` |

## Architecture

The architecture tools read Sigrid Core's dependency graph, which describes the baseline branch as Sigrid last analyzed it. Paths have to match Sigrid's own paths, which can differ from your local layout.

`architecture.get_internal` shows how the parts inside a directory relate: which parts call which, and how often.

- `path`: the directory. Leave it out for the system's top-level components.

`architecture.get_external_dependencies` lists the direct dependencies of a file or directory, what it calls and what calls it, to find the blast radius of a change. It returns one hop per call.

- `path`: the file or directory. This is required.
- `direction`: `incoming`, `outgoing`, or `all` (the default).

`architecture.get_worst_directories` returns up to 20 directories, ranked by structure rating, worst first. The ranking is weighted by volume, so a low rating on a large component outranks the same rating on a small one.

- `path`: rank the directories inside this path instead of across the whole system.
- `min_volume`: leave out directories at or below this volume in person-years. The default is 0.2. Lower it, for example to 0.01, to see leaf directories on a small system.

## Tool selection

Only the tools for the Sigrid capabilities your organization has enabled are available. If your organization has Maintainability and Security enabled, for example, you only see the tools for those.

To restrict the tools in a session further, pass the `X-Enabled-Tools` header with a comma-separated list of tool names:

```json
{
  "mcpServers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>",
        "X-Enabled-Tools": "guardrails.quality_check, security.get_findings"
      }
    }
  }
}
```

## Troubleshooting

Here are the problems we see most, and what solves them:

| Problem | Solution |
| --- | --- |
| "Server not found" | Check that your token is valid |
| "mcp-remote not found" | Run `npm install -g mcp-remote` |
| Connection fails in proxy mode | Check that the `--allow-http` flag is there |
| IntelliJ does not connect | Check where your OS keeps the MCP JSON file |
| "Bad Request: No valid session ID provided" | Restart the client, or turn the MCP server off and on again |
| The agent ignores the tools | Use a recent frontier model |
| The agent asks permission for every Sigrid tool after upgrading | [Update your permission allowlist](installation.md#2-update-your-permission-allowlists) |
| Sigrid On-Premise: connection refused or 401 | See below |

On Sigrid On-Premise, a refused connection or a 401 usually has one of three causes. Check that the URL uses your own Sigrid host, that the token was created in your on-premise Sigrid, and that your administrator has [enabled the MCP server](../organization-integration/onpremise-mcp.md) in the Helm chart.

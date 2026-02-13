# Sigrid MCP Integrations

Sigrid MCP integrations can be used to leverage Sigrid's capabilities from AI Coding Assistants, Agents and other MCP-based LLM tools.

- *Sigrid Guardrails MCP*: Leverage Sigrid's code analysis to safe guard AI Coding Assistants from introducing security and other quality issues
- *Sigrid Modernization Recipes MCP*: Use data from Sigrid to let AI Coding Agents perform large scale modernization tasks (coming soon)

## Sigrid Guardrails MCP

The Sigrid Guardrails MCP integration enables AI coding assistants and LLMs to leverage Sigrid's comprehensive code analysis capabilities during code generation. By embedding Sigrid directly into the AI agent workflow, this integration ensures that both newly generated and existing code is automatically evaluated for security vulnerabilities and quality issues.

This proactive approach allows AI coding agents to autonomously identify and resolve code issues in real-time, preventing quality problems at the point of generation rather than discovering them later in the development cycle through build pipeline failures or downstream processes.

### Supported Technology List for MCP

The currently supported technologies are:

- Java
- Python
- C/C++
- C#
- JavaScript
- TypeScript
- Kotlin
- Progress ABL
- PHP

Visit the [Technology Support](../reference/technology-support.md#list-of-supported-technologies) page for more details on supported technologies.

### Setup

- Step 1: Obtain a Sigrid Token — see the Sigrid docs on [authentication tokens](../organization-integration/authentication-tokens.md)
- Step 2: Configure MCP tool in your IDE or AI Coding Assistant
- Step 3: Tune agent instructions rules or policies for Sigrid MCP Guardrails to your needs
- Step 4: Pick a LLM with support for MCP tools (recommended: GPT-5, Claude 4 series, Gemini 2.5 series or higher)

### Configuration by IDE

| IDE | Connection Type | Configuration Method | Status |
| --- | --- | --- | --- |
| Cursor | Direct HTTP | MCP & Integrations panel | ✅ Fully Supported |
| VSCode w/ Github Copilot plugin | HTTP via GitHub Copilot | Agent mode → Tools menu | ✅ Supported |
| VSCode native | Proxy (mcp-remote) | MCP settings | ✅ Supported |
| Windsurf | Proxy (mcp-remote) | MCP settings | ✅ Supported |
| IntelliJ/PyCharm/WebStorm | HTTP via AI Chat | Manual JSON edit | ✅ Supported |

### Connection Types Explained

Direct HTTP

- Simplest configuration
- IDE connects directly to MCP server
- Used by: Cursor

HTTP via GitHub Copilot Extension
- Requires GitHub Copilot plugin
- Configuration through extension UI
- Used by: VSCode, IntelliJ family

Proxy (mcp-remote)
- Uses npx and mcp-remote package (install if needed through terminal with the command: npm install mcp-remote)
- Required when direct HTTP not supported
- Used by: Windsurf, VSCode

### Configuration Instructions

#### Cursor/Github Copilot Plugin

- Open IDE
- Click MCP & Integrations panel (left sidebar)
- Paste configuration:

```
{
  "mcpServers": {
    "SigridCode": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

#### VSCode

- Install Node (needed for the npx package)
- Install GitHub Copilot extension
- Connect your GitHub account
- In main screen of VSCode, click the settings icon on bottom left, select "Profiles"
- Click MCP Servers. If prompted to create a new file, say "Yes"

Add:
```
{
  "servers": {
    "SigridCode": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://sigrid-says.com/mcp",
        "--header",
        "Authorization: Bearer <your_sigrid_token>",
        "--allow-http"
      ]
    }
  }
}
```

- Save → Verify server appears in tools list

#### Windsurf

- Install Node
- Open MCP settings
- Add configuration:
```
{
  "mcpServers": {
    "SigridCode": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://sigrid-says.com/mcp",
        "--header",
        "Authorization: Bearer <your_sigrid_token>",
        "--allow-http"
      ]
    }
  }
}
```

- Restart Windsurf

#### Claude Code

- To add Sigrid MCP to Claude Code, run the following command:

```bash
claude mcp add SigridCode -- npx mcp-remote https://sigrid-says.com/mcp --header "Authorization: Bearer TOKEN" --allow-http
```

Replace `TOKEN` with your actual Sigrid API token.

- Restart Claude Code

#### IntelliJ/PyCharm/WebStorm

In the IDE, navigate to Tools > AI Assistant > Model Context Protocol (MCP) and add:

```
"mcpServers": {
    "CodeGuardrails": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://sigrid-says.com/mcp",
        "--header",
        "Authorization: Bearer <your_sigrid_token>",
        "--allow-http"
      ]
    }
```

Then, save the configuration and click the `Reconnect` arrow on the top of the configuration, and, if your Sigrid token is valid, you will be successfully connected to the MCP server.

### Using Sigrid Quality Gates with AI Coding Agents

AI-generated code quality varies significantly based on the instructions given. The Sigrid MCP provides guardrails that notify agents when code doesn't meet quality standards without requiring the system to be published to Sigrid first.

We recommend combining two elements:
1. **Code principles**: brief guidelines that help the agent write good code upfront
2. **Quality gate**: a mandatory check using Sigrid before completing any task

#### Recommended Prompt

Add this to your agent instructions (see [Where to Place These Instructions](#where-to-place-these-instructions)):

```
## Code Principles

Write maintainable code: single responsibility, small focused functions, clear naming, avoid duplication, simple control flow.
Write secure code.

## MANDATORY: Quality Gate

Before reporting ANY task as complete:

1. Run the Sigrid Code Quality Guardrails tool on all changed production code
2. Maintainability findings: accept if principles were followed, otherwise refactor
3. Security findings: fix if straightforward, otherwise flag to user

Do not skip this step.
```

For stricter workflows, add a rescan step: "If fixes were made, rescan to verify no new issues were introduced."

#### Where to Place These Instructions

Most AI coding agents respect instruction files in your repository. Refer to your agent's documentation for specifics.

| File | Supported by |
|------|--------------|
| `.cursor/rules/` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `.windsurfrules` | Windsurf |
| `CLAUDE.md` | Claude Code |
| `AGENTS.md` | Emerging convention (check agent support) |

For tools that support both global and project-level rules, prefer project-level to keep instructions versioned with your code.

#### Customizing for Your Codebase

The prompt above is a starting point. Consider these adjustments:

- **Framework conventions**: If your codebase follows specific design patterns (e.g., hexagonal architecture, Redux patterns), add them to the code principles section.
- **Check frequency**: You may prefer to run the quality gate with a different frequency, e.g. only before commits rather than after every task.
- **Direct invocation**: You can also ask the agent directly: "Run Sigrid on these files: ..."
- **Iterate from experience**: When the agent makes recurring mistakes, add a principle that addresses the pattern.

> **Tip**: Start with concise principles. Add explicit guidance only if the model struggles.

We advise to complement the MCP with Sigrid CI to catch architecture issues, vulnerable dependencies, and cross-file metrics.

### Troubleshooting

| Issue | Solution |
| --- | --- |
| "Server not found" | Verify token is valid |
| "mcp-remote not found" | Run npm install -g mcp-remote |
| IntelliJ not working | Check manual JSON file location for your OS |
| Connection fails | Ensure --allow-http flag is present (proxy mode) |
| Bad Request: No valid session ID provided | Restarting the client and/or simply enabling/disabling the MCP servers |
| AI Coding Assistant ignores MCP tool | Try one of the recommended LLMs: GPT-5, Claude 4 series, Gemini 2.5 series or higher |

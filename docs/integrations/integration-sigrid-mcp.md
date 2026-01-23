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
| IntelliJ/PyCharm/WebStorm | HTTP via GitHub Copilot | Manual JSON edit | ⚠️ Workaround only |

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
    "SigridCodeAnalyzer": {
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
claude mcp add sigrid -- npx mcp-remote https://sigrid-says.com/mcp --header "Authorization: Bearer TOKEN" --allow-http
```

Replace `TOKEN` with your actual Sigrid API token.

- Restart Claude Code

#### IntelliJ/PyCharm/WebStorm (Workaround)

⚠️ Not natively supported - [Open JetBrains issue](https://youtrack.jetbrains.com/projects/JUNIE/issues/JUNIE-461/MCP-Remote-Server-Support)

- Install GitHub Copilot plugin
- Manually edit: `~/.config/github-copilot/intellij/mcp.json`
- Use same configuration as Cursor/Github Copilot


### Rules and Policies

When exactly the AI Coding Assistant should reach out to Sigrid to receive feedback on Code Quality and Security can typically be defined as rules or policies in the AI Coding Assistant itself.
It is up to the user to define these rules and what kind of rules and policies are possible depends on the Coding Assistant that is used.

SIG sees different types of rules being used by users:
- Some users prefer to add Sigrid MCP into a workflow (e.g. when tagging @Sigrid in the prompt)
- Others prefer to run Sigrid for each and every piece of code that is generated, but have the AI Coding Assistant only focus on issues within the method they changed
- Others prefer to run Sigrid for each and every piece of code that is generated and have the AI Coding Assistant fix any issue that comes up in the change or in the vicinity of the change

SIG provides example instructions in its documentation, but it is up to the user (or organisation) to tweak those to the specific needs for a given system or given organisational context.
Ultimately it is the Large Language Model behind the AI Coding Assistant that based on the defined rules in the coding assistant decides that an MCP integration should be called.

Example Global Rule:

```
---
applyTo: "**"
---

# Project code quality and security best practices

- BEFORE finalizing any code change, the AI assistant MUST:
  - Run the Sigrid Code Quality Guardrails tool on the modified code
  - Review all findings from the analysis
  - Address any new or pre-existing security or maintainability issues in the scope of the current change(e.g. within the same method, function or procedure of the changed code)
  - Document any pre-existing issues that are out of scope
  - Only after completing these steps, present the final change to the user
- If any security or maintainability issues are found based on newly introduced or modified code, propose a fix for the issues using the results context from Sigrid.
- Immediately propose fixes for pre-existing maintainability issues in the scope of the code change with a refactoring to improve code quality, even if that increases the scope of the change.
- Always rescan the code after fixing the issues to ensure that the issues were fixed and that there are no newly introduced issues.
- Repeat this process until no issues are found.
- Always provide a valid code snippet to the Sigrid Code Quality Guardrails tool. For example: Do not just provide a method, but wrap it in a class.
```

Choose a workflow that works for you and your team: Some teams prefer to have every single code snippet analysed, other teams want to manually invoke the MCP server on very specific functions or snippets, some teams want to restrict to Java code, etc.
Sigrid MCP provides the code quality and security analysis, but it is up to the user, team or organisation to define the preferred interaction model in their Agentic IDE.

### Troubleshooting

| Issue | Solution |
| --- | --- |
| "Server not found" | Verify token is valid |
| "mcp-remote not found" | Run npm install -g mcp-remote |
| IntelliJ not working | Check manual JSON file location for your OS |
| Connection fails | Ensure --allow-http flag is present (proxy mode) |
| Bad Request: No valid session ID provided | Restarting the client and/or simply enabling/disabling the MCP servers |
| AI Coding Assistant ignores MCP tool | Try one of the recommended LLMs: GPT-5, Claude 4 series, Gemini 2.5 series or higher |

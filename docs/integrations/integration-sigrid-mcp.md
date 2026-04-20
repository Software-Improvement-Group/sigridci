# Sigrid MCP Integrations

Sigrid MCP integrations let AI coding tools use Sigrid's analysis while you work — catching security and quality issues as they're introduced, and driving down technical debt through guided refactoring.

- **[Sigrid Guardrails MCP](sigrid-mcp/guardrails.md)**: Leverage Sigrid's code analysis to safeguard AI Coding Assistants from introducing security and other quality issues
- **[Sigrid Modernization Recipes MCP](sigrid-mcp/recipes.md)**: Use data from Sigrid to let AI Coding Agents perform large-scale modernization tasks

## Installation

### Claude Code plugin (recommended)

The [Sigrid AI Toolkit](https://github.com/Software-Improvement-Group/sigrid-ai-toolkit) is a Claude Code plugin that automatically configures both the Sigrid MCP server and the associated skills. This is the easiest way to get started.

```
/plugin marketplace add git@github.com:Software-Improvement-Group/sigrid-ai-toolkit.git
/plugin install sigrid@sigrid-ai-toolkit
```

The installer will prompt for your Sigrid API token and store it securely in the system keychain.

- Step 1: Obtain a Sigrid Token — see the Sigrid docs on [authentication tokens](../organization-integration/authentication-tokens.md)
- Step 2: Run the two commands above in Claude Code
- Step 3: Follow the installer prompts

### Manual configuration (other IDEs)

For IDEs other than Claude Code, configure the MCP server manually:

- Step 1: Obtain a Sigrid Token — see the Sigrid docs on [authentication tokens](../organization-integration/authentication-tokens.md)
- Step 2: Configure the MCP tool in your IDE or AI Coding Assistant using the instructions below

#### Supported IDEs

| Tool | Connection Type | Configuration Method | Status |
| --- | --- | --- | --- |
| Cursor | Direct HTTP | MCP & Integrations panel | ✅ Fully Supported |
| VSCode w/ Github Copilot plugin | HTTP via GitHub Copilot | Agent mode → Tools menu | ✅ Supported |
| VSCode native | Proxy (mcp-remote) | MCP settings | ✅ Supported |
| Windsurf | Proxy (mcp-remote) | MCP settings | ✅ Supported |
| Claude Code | Proxy (mcp-remote) | CLI command | ✅ Supported |
| OpenCode | Direct HTTP | opencode.json | ✅ Supported |
| IntelliJ/PyCharm/WebStorm | HTTP via AI Chat | Manual JSON edit | ✅ Supported |

#### Connection types explained

**Direct HTTP**
- Simplest configuration
- IDE connects directly to MCP server
- Used by: Cursor

**HTTP via GitHub Copilot Extension**
- Requires GitHub Copilot plugin
- Configuration through extension UI
- Used by: VSCode, IntelliJ family

**Proxy (mcp-remote)**
- Uses `npx mcp-remote` (install globally first if needed: `npm install -g mcp-remote`)
- Required when direct HTTP not supported
- Used by: Windsurf, VSCode

#### Cursor / GitHub Copilot Plugin

- Open IDE
- Click MCP & Integrations panel (left sidebar)
- Paste configuration:

```json
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
```json
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

#### Visual Studio

- Connect your GitHub account and open GitHub Copilot
- At the bottom left, below the chat box, select "Agent" mode
- Click on the + button to add a new MCP server
- When prompted, enter the name "SigridCode", then add the URL as `https://sigrid-says.com/mcp`
- Choose "Additional headers" and add: `Authorization: Bearer <your_sigrid_token>`
- After saving/closing the window, if the token is valid, verify server appears in tools list

#### Windsurf

- Install Node
- Open MCP settings
- Add configuration:

```json
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

#### Claude Code (manual)

```bash
claude mcp add --transport http SigridCode https://sigrid-says.com/mcp --header "Authorization: Bearer <your_sigrid_token>"
```

Alternatively, using a proxy:
```bash
claude mcp add SigridCode -- npx mcp-remote https://sigrid-says.com/mcp --header "Authorization: Bearer <your_sigrid_token>" --allow-http
```

Replace `<your_sigrid_token>` with your actual Sigrid API token. Restart Claude Code after adding.

#### OpenCode

- Create or edit `opencode.json` in your project root:

```json
{
  "mcp": {
    "SigridCode": {
      "type": "remote",
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

- Restart OpenCode

#### IntelliJ / PyCharm / WebStorm

Navigate to Tools > AI Assistant > Model Context Protocol (MCP) and add:

```json
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

#### IBM Bob

Navigate to Settings (the cogwheel icon inside the Bob chat window) > MCP. Configure a global or project-specific MCP server:

```json
{
    "mcpServers":
    {
        "CodeGuardrails": {
            "type": "streamable-http",
            "url": "https://sigrid-says.com/mcp",
            "headers": {
              "Authorization": "Bearer <your_sigrid_token>"
            }
        }
    }
}
```

Note the **extra** outer brackets required for the configuration to validate successfully. Save the configuration and verify the connection on the settings page.

## Available tools reference

| Tool | Product | Description |
| --- | --- | --- |
| `code_quality_guardrails` | [Guardrails MCP](sigrid-mcp/guardrails.md) | Checks code for maintainability issues and security vulnerabilities |
| `sigrid_refactoring_candidates` | [Modernization Recipes MCP](sigrid-mcp/recipes.md) | Retrieves ranked refactoring candidates for a given maintainability property |
| `edit_sigrid_finding_status` | [Modernization Recipes MCP](sigrid-mcp/recipes.md) | Updates the status and remarks of a Sigrid finding |


### Troubleshooting

| Issue | Solution |
| --- | --- |
| "Server not found" | Verify token is valid |
| "mcp-remote not found" | Run npm install -g mcp-remote |
| IntelliJ not working | Check manual JSON file location for your OS |
| Connection fails | Ensure --allow-http flag is present (proxy mode) |
| Bad Request: No valid session ID provided | Restarting the client and/or simply enabling/disabling the MCP servers |
| AI Coding Assistant ignores MCP tool | Try one of the recommended LLMs: GPT-5, Claude 4 series, Gemini 2.5 series or higher |

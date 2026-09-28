---
redirect_from:
  - /integrations/integration-sigrid-mcp.html
---

# Installing Sigrid Axis

Sigrid Axis consists of the Sigrid Axis MCP server and a set of skills. Both follow open standards, so Axis works in any agentic tool that supports MCP and skills. Installing it means connecting the MCP server, installing the skills, and [adding the Guardrails instruction](#add-the-guardrails-instruction) to your repository. In Claude Code, a plugin does all three in one step.

## Prerequisites

- A Sigrid account with at least one system. The Guardrails check works on code that has not been published to Sigrid yet, but the other tools and skills read what Sigrid Core found in a published system.
- A Sigrid API token. See [authentication tokens](../organization-integration/authentication-tokens.md) for how to create one.
- Your Sigrid customer and system names, which you can read off the Sigrid URL: `sigrid-says.com/<customer>/<system>`.

## Install the Claude Code plugin

In Claude Code, the plugin configures the Sigrid Axis MCP server and the skills together. It also adds a hook that reminds the agent to run the Guardrails check before it reports a task done, so you don't have to add that instruction yourself. Run these commands:

{% include axis/plugin-install.md setup=true %}

What each one does:

1. The first command adds the `sigrid` marketplace from the [agent-integrations](https://github.com/Software-Improvement-Group/agent-integrations) repository.
2. The second installs the `axis` plugin. On first use, Claude Code asks for your Sigrid API token and stores it in your operating system's keychain.
3. The third runs the [`setup`](skills.md#setup) skill. Run it once in each repository you work in. It detects your Sigrid system from the repository, asks for what it cannot tell, and writes `.sigrid/profile.md`. Commit that file, so your team shares it.

We would also turn on auto-update, so you get new skills and fixes without reinstalling: run `/plugin`, go to **Marketplaces**, select **sigrid**, and choose **Enable auto-update**.

To check that the plugin works, ask for a Guardrails check on a file you changed recently:

```
Run the Sigrid guardrails quality check on <a file you changed recently>.
```

A clean file comes back with no findings, and that is a pass. See [configuration](configuration.md) for changing the token later and for the plugin options.

The plugin connects to `sigrid-says.com` only. For Sigrid On-Premise, see [connecting an AI coding assistant](../organization-integration/onpremise-mcp.md#connecting-an-ai-coding-assistant).
{: .attention }

## Use the skills in other agentic tools

The skills are plain `SKILL.md` files, the open format that most agentic tools read. You can find them in the `axis` directory of the [agent-integrations](https://github.com/Software-Improvement-Group/agent-integrations) repository. To use them in another tool:

1. Connect the Sigrid Axis MCP server by hand, as described below.
2. Install the skills the way your tool installs skills.
3. Run `setup`, or write `.sigrid/profile.md` yourself, to record your Sigrid system and change how the skills behave in your repository. See [the Sigrid profile](configuration.md#the-sigrid-profile).
4. [Add the Guardrails instruction](#add-the-guardrails-instruction) to your repository.

## Add the Guardrails instruction

Outside the Claude Code plugin, this step is required for Guardrails. The agent does not call the Guardrails check unless something tells it to, and in Claude Code the plugin's hook does that. Every other tool needs the instruction in its context file.
{: .attention }

Put this text in `AGENTS.md` at the root of your repository, which Cursor, GitHub Copilot, Devin, and most other agentic tools read at the start of every session. It is the same text the Claude Code hook adds:

{% include axis/quality-gate-prompt.md %}

This also applies when you connect the MCP server by hand in Claude Code, without the plugin, but there the file is `CLAUDE.md`. To adjust the instruction to your codebase, see [set up the quality gate](guardrails.md#set-up-the-quality-gate).

## Connect the MCP server by hand

Every agentic tool that supports MCP can connect to the Sigrid Axis MCP server directly. The snippets below name the server `axis`. Replace `<your_sigrid_token>` with your Sigrid API token in each of them.

| Tool | Connection type | Where to configure it |
| --- | --- | --- |
| Cursor | Direct HTTP | MCP & Integrations panel |
| VS Code with GitHub Copilot | Proxy (`mcp-remote`) | MCP settings |
| Visual Studio with GitHub Copilot | Direct HTTP | Agent mode, add MCP server |
| Devin Desktop | Direct HTTP | MCP settings |
| Claude Code | Direct HTTP | CLI command |
| OpenCode | Direct HTTP | `opencode.json` |
| IntelliJ, PyCharm, WebStorm | Proxy (`mcp-remote`) | AI Assistant MCP settings |
| IBM Bob | Direct HTTP | Bob settings, MCP |

A direct HTTP connection is the simplest: the tool talks to the MCP server itself. The proxy connection runs `npx mcp-remote` locally for tools that cannot connect over HTTP directly, so it needs Node. If `npx` cannot find it, install it globally first with `npm install -g mcp-remote`.

### Cursor

Open the **MCP & Integrations** panel in the left sidebar and paste this configuration:

```json
{
  "mcpServers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

### VS Code

To connect VS Code with GitHub Copilot:

1. Install Node, which the `npx` command needs.
2. Install the GitHub Copilot extension and connect your GitHub account.
3. Click the settings icon at the bottom left, select **Profiles**, and click **MCP Servers**. If VS Code asks to create a new file, say yes.
4. Add the configuration below, save, and check that the server appears in the tools list.

```json
{
  "servers": {
    "axis": {
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

### Visual Studio

To connect Visual Studio with GitHub Copilot:

1. Connect your GitHub account and open GitHub Copilot.
2. Below the chat box, at the bottom left, select **Agent** mode.
3. Click the **+** button to add an MCP server. Enter the name `axis` and the URL `https://sigrid-says.com/mcp`.
4. Choose **Additional headers** and add `Authorization: Bearer <your_sigrid_token>`.
5. Save and close the window. If the token is valid, the server appears in the tools list.

### Devin Desktop

Open the MCP settings, add this configuration, and restart Devin Desktop. The URL key has to be `serverUrl`:

```json
{
  "mcpServers": {
    "axis": {
      "serverUrl": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

### Claude Code

Without the plugin, add the server with this command and restart Claude Code:

```bash
claude mcp add --transport http axis https://sigrid-says.com/mcp --header "Authorization: Bearer <your_sigrid_token>"
```

This gives you the MCP tools only. The skills and the Guardrails hook come with the [plugin](#install-the-claude-code-plugin), so without it, [add the Guardrails instruction](#add-the-guardrails-instruction) to `CLAUDE.md` yourself.

### OpenCode

Create or edit `opencode.json` in your project root, then restart OpenCode:

```json
{
  "mcp": {
    "axis": {
      "type": "remote",
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

### IntelliJ, PyCharm, and WebStorm

Go to **Tools > AI Assistant > Model Context Protocol (MCP)** and add:

```json
"mcpServers": {
  "axis": {
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
```

### IBM Bob

Open the settings with the cogwheel icon in the Bob chat window and go to **MCP**. Configure a global or a project-specific MCP server:

```json
{
    "mcpServers":
    {
        "axis": {
            "type": "streamable-http",
            "url": "https://sigrid-says.com/mcp",
            "headers": {
              "Authorization": "Bearer <your_sigrid_token>"
            }
        }
    }
}
```

The configuration only validates with the extra outer braces shown here. Save it and check the connection on the settings page.

<!-- Remove this section after the Sigrid Axis launch of October 1, 2026. -->
## Upgrade from the Sigrid AI Toolkit

The Claude Code plugin used to be called `sigrid`, installed from the `sigrid-ai-toolkit` marketplace. It is now `axis`, installed from the `sigrid` marketplace, and a few things changed along with the name.

### 1. Replace the plugin

Remove the old plugin and its marketplace:

```
/plugin uninstall sigrid@sigrid-ai-toolkit
/plugin marketplace remove sigrid-ai-toolkit
```

Then [install the new plugin](#install-the-claude-code-plugin). If you had turned off one of the hook options, turn it off again, because they have new names: **Nudge to run guardrails** and **Nudge to use architecture-explorer**. See [plugin options](configuration.md#plugin-options).

### 2. Update your permission allowlists

The MCP tools from the plugin have a new prefix, `mcp__plugin_axis_axis__` instead of `mcp__plugin_sigrid_sigrid__`. If you pre-allowed the Sigrid tools in `.claude/settings.json`, `.claude/settings.local.json`, or your user settings, replace the old prefix with the new one:

```json
{
  "permissions": {
    "allow": ["mcp__plugin_axis_axis__*"]
  }
}
```

Without this change nothing breaks, but the agent quietly starts asking for permission before every Sigrid tool call again.

### 3. Move your profile into the repository

The old plugin kept one profile per user, in `~/.claude/plugins/data/sigrid-sigrid-ai-toolkit/CLAUDE.md`. Sigrid Axis keeps one per repository instead, in `.sigrid/profile.md`, committed so your team shares it. Run `/setup` in each repository. When it finds your old profile, it offers to copy the system that matches the repository, and it leaves the old file in place.

### 4. Learn the new skill names

The skills are now one skill per job, and an argument picks the model. They also stop earlier than before: they commit locally and write statuses to Sigrid, but they never push, open merge requests or pull requests, or open issues. See the [skills reference](skills.md) for what each one does.

| Old skill | New skill |
|-----------|-----------|
| `change-feedback` | `change-feedback` |
| `architecture-drift` | `change-feedback architecture` |
| `explore-codebase` (agent) | `architecture-explorer` (agent) and `explore-architecture` |
| `sigrid-diagnose` | `diagnose maintainability` |
| `architecture-diagnose` | `diagnose architecture` |
| `sigrid-improve` | `autofix maintainability` |
| `architecture-improve` | `autofix architecture` |
| `resolve-security-findings` | `triage-findings security`, then `autofix security` |
| `fix-osh-risk` | `triage-findings open-source`, then `autofix open-source` |
| `setup` | `setup`, now per repository |
| `osh-researcher` (agent) | `osh-researcher` (agent) |

Reliability findings are new: `triage-findings reliability` and `autofix reliability`. The old `architecture-drift` still works for now, as an alias of `change-feedback architecture`.

### Manual MCP configurations

If you connected the MCP server by hand, it keeps working as it is. The server name in your configuration is your own choice, so renaming it from `Sigrid` to `axis` is optional.

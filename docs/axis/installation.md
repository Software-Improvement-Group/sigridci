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

## Install in other agentic tools

Outside Claude Code, you set up what the plugin would install for you:

1. [Connect the MCP server by hand](#connect-the-mcp-server-by-hand).
2. [Install the skills](#install-the-skills).
3. Run `setup`, or write `.sigrid/profile.md` yourself, to record your Sigrid system and change how the skills behave in your repository. See [the Sigrid profile](configuration.md#the-sigrid-profile).
4. [Add the Guardrails instruction](#add-the-guardrails-instruction) to your repository.

### Install the skills

Install the skills with the [skills](https://github.com/vercel-labs/skills) command line tool, which needs Node. Run this in the root of your repository:

```bash
npx skills add Software-Improvement-Group/agent-integrations --skill '*'
```

It asks which of your agentic tools to install the skills for, and `--skill '*'` installs every skill. Keep them together, because they hand work to one another: `autofix`, for example, reads the plan that `diagnose` writes. Run `npx skills update` to get new versions.

## Add the Guardrails instruction

The agent only calls the Guardrails check when something tells it to. In Claude Code, the plugin's hook does that. Everywhere else, including Claude Code without the plugin, this instruction does.
{: .attention }

Put this text in `AGENTS.md` at the root of your repository, which Cursor, GitHub Copilot, Devin, and most other agentic tools read at the start of every session. It is the same text the Claude Code hook adds:

{% include axis/quality-gate-prompt.md %}

In Claude Code without the plugin, put it in `CLAUDE.md`. To adjust the instruction to your codebase, see [set up the quality gate](guardrails.md#set-up-the-quality-gate).

## Connect the MCP server by hand

Every agentic tool that supports MCP can connect to the Sigrid Axis MCP server at `https://sigrid-says.com/mcp`. The snippets below name the server `axis` and send your Sigrid API token in an `Authorization` header.

Most tools can read the token from an environment variable, so it never ends up in a configuration file you might commit. Set `SIGRID_TOKEN` once, in your shell profile on macOS and Linux:

```bash
export SIGRID_TOKEN=<your_sigrid_token>
```

On Windows, run `setx SIGRID_TOKEN <your_sigrid_token>`. Restart the tool afterwards, so it picks up the variable. The [`change-feedback`](skills.md#change-feedback) skill reads the same variable when it runs Sigrid CI. For the tools that can't read a variable, you paste the token into the configuration. Keep that file out of version control.

Open the section for your tool:

<details name="agent-tool">
  <summary>VS Code</summary>
  <div markdown="1" id="vs-code">

VS Code with GitHub Copilot doesn't read environment variables in headers yet, so this configuration asks for the token once and stores it securely. Put it in `.vscode/mcp.json` in your repository, or run **MCP: Open User Configuration** from the command palette to add it for your user account:

```json
{
  "inputs": [
    {
      "type": "promptString",
      "id": "sigrid-token",
      "description": "Sigrid API token",
      "password": true
    }
  ],
  "servers": {
    "axis": {
      "type": "http",
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer ${input:sigrid-token}"
      }
    }
  }
}
```

VS Code asks for the token the first time it starts the server. Check that `axis` appears in the tools list of the chat view.

  </div>
</details>

<details name="agent-tool">
  <summary>Visual Studio</summary>
  <div markdown="1" id="visual-studio">

To connect Visual Studio with GitHub Copilot:

1. Connect your GitHub account and open GitHub Copilot.
2. Below the chat box, at the bottom left, select **Agent** mode.
3. Click the **+** button to add an MCP server. Enter the name `axis` and the URL `https://sigrid-says.com/mcp`.
4. Choose **Additional headers** and add `Authorization: Bearer <your_sigrid_token>`.
5. Save and close the window. If the token is valid, the server appears in the tools list.

  </div>
</details>

<details name="agent-tool">
  <summary>GitHub Copilot in JetBrains IDEs</summary>
  <div markdown="1" id="github-copilot-in-jetbrains-ides">

In IntelliJ, PyCharm, WebStorm, and the other JetBrains IDEs, open Copilot Chat, click the tools icon, and choose **Add MCP Tools**. Add this configuration, which puts the header under `requestInit`:

```json
{
  "servers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "requestInit": {
        "headers": {
          "Authorization": "Bearer <your_sigrid_token>"
        }
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>GitHub Copilot CLI</summary>
  <div markdown="1" id="github-copilot-cli">

Add the server with this command. Your shell fills in the token, and the CLI stores it in `~/.copilot/mcp-config.json`:

```bash
copilot mcp add --transport http --header "Authorization: Bearer $SIGRID_TOKEN" axis https://sigrid-says.com/mcp
```

  </div>
</details>

<details name="agent-tool">
  <summary>Claude Code</summary>
  <div markdown="1" id="claude-code">

Without the plugin, add the server with this command and restart Claude Code:

```bash
claude mcp add --transport http --scope user axis https://sigrid-says.com/mcp --header "Authorization: Bearer $SIGRID_TOKEN"
```

This gives you the MCP tools only. The skills and the Guardrails hook come with the [plugin](#install-the-claude-code-plugin).

  </div>
</details>

<details name="agent-tool">
  <summary>Cursor</summary>
  <div markdown="1" id="cursor">

Put this in `.cursor/mcp.json` in your repository, or in `~/.cursor/mcp.json` for your user account. The Cursor CLI reads the same files:

```json
{
  "mcpServers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:SIGRID_TOKEN}"
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>OpenAI Codex</summary>
  <div markdown="1" id="openai-codex">

The Codex CLI, IDE extension, and app share one configuration. Add the server with this command:

```bash
codex mcp add axis --url https://sigrid-says.com/mcp --bearer-token-env-var SIGRID_TOKEN
```

The command writes this to `~/.codex/config.toml`, which you can also edit by hand:

```toml
[mcp_servers.axis]
url = "https://sigrid-says.com/mcp"
bearer_token_env_var = "SIGRID_TOKEN"
```

  </div>
</details>

<details name="agent-tool">
  <summary>Gemini CLI</summary>
  <div markdown="1" id="gemini-cli">

Add the server for your user account with this command. Gemini Code Assist's agent mode reads the same configuration:

```bash
gemini mcp add --transport http --scope user --header "Authorization: Bearer $SIGRID_TOKEN" axis https://sigrid-says.com/mcp
```

To write it in `~/.gemini/settings.json` or `.gemini/settings.json` by hand, use `httpUrl`. With `url`, Gemini CLI connects over the older SSE transport:

```json
{
  "mcpServers": {
    "axis": {
      "httpUrl": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer $SIGRID_TOKEN"
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>JetBrains AI Assistant</summary>
  <div markdown="1" id="jetbrains-ai-assistant">

Go to **Settings > Tools > AI Assistant > Model Context Protocol (MCP)** and add this configuration. It runs the `mcp-remote` proxy, so install Node first:

```json
{
  "mcpServers": {
    "axis": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://sigrid-says.com/mcp",
        "--header",
        "Authorization: Bearer <your_sigrid_token>"
      ]
    }
  }
}
```

If `npx` can't find the proxy, install it globally first with `npm install -g mcp-remote`.

  </div>
</details>

<details name="agent-tool">
  <summary>Junie</summary>
  <div markdown="1" id="junie">

The Junie plugin and the Junie CLI share one configuration. Put this in `~/.junie/mcp/mcp.json` for your user account:

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

  </div>
</details>

<details name="agent-tool">
  <summary>Google Antigravity</summary>
  <div markdown="1" id="google-antigravity">

The Antigravity editor and CLI share one configuration. Put this in `~/.gemini/config/mcp_config.json`. Antigravity only accepts the `serverUrl` key, not `url`:

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

  </div>
</details>

<details name="agent-tool">
  <summary>OpenCode</summary>
  <div markdown="1" id="opencode">

Put this in `opencode.json` in your repository, or in `~/.config/opencode/opencode.json` for your user account, then restart OpenCode. OpenCode writes variables as `{env:NAME}`, without a dollar sign:

```json
{
  "mcp": {
    "axis": {
      "type": "remote",
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer {env:SIGRID_TOKEN}"
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>Devin Desktop</summary>
  <div markdown="1" id="devin-desktop">

Devin Desktop, formerly Windsurf, shares its configuration with the Devin CLI. Put this in `~/.config/devin/mcp_config.json` (`%APPDATA%\devin\mcp_config.json` on Windows), or in `.devin/mcp_config.json` in your repository, and restart Devin Desktop:

```json
{
  "mcpServers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer ${env:SIGRID_TOKEN}"
      }
    }
  }
}
```

If you still use the older Cascade agent, the URL key has to be `serverUrl`.

  </div>
</details>

<details name="agent-tool">
  <summary>Kiro</summary>
  <div markdown="1" id="kiro">

Put this in `.kiro/settings/mcp.json` in your repository, or in `~/.kiro/settings/mcp.json` for your user account:

```json
{
  "mcpServers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer ${SIGRID_TOKEN}"
      }
    }
  }
}
```

Kiro only fills in variables you approved. Add `SIGRID_TOKEN` to the **Mcp Approved Env Vars** setting, or approve it when Kiro asks.

  </div>
</details>

<details name="agent-tool">
  <summary>Zed</summary>
  <div markdown="1" id="zed">

Run **zed: open settings file** and add the server under `context_servers`:

```json
{
  "context_servers": {
    "axis": {
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>Cline</summary>
  <div markdown="1" id="cline">

Open the MCP servers panel in Cline, choose **Configure MCP Servers**, and add:

```json
{
  "mcpServers": {
    "axis": {
      "type": "streamableHttp",
      "url": "https://sigrid-says.com/mcp",
      "headers": {
        "Authorization": "Bearer <your_sigrid_token>"
      }
    }
  }
}
```

  </div>
</details>

<details name="agent-tool">
  <summary>IBM Bob</summary>
  <div markdown="1" id="ibm-bob">

Open the settings with the cogwheel icon in the Bob chat window and go to **MCP**. Configure a global server, stored in `~/.bob/settings/mcp.json`, or a project server, stored in `.bob/mcp.json`:

```json
{
  "mcpServers": {
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

Save it and check the connection on the settings page. Bob Shell has its own file, `~/.bob/mcp_settings.json`, where the URL key is `httpURL`.

  </div>
</details>

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

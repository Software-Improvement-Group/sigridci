Everything here applies to any agentic CLI. The configuration below is for Claude Code, since that is the only CLI we ship a plugin for, and every agentic CLI has its own version of the four primitives involved:

| Primitive | Generic | Claude Code |
|-----------|---------|-------------|
| Persistent instructions | context file | `CLAUDE.md` |
| Tool access | MCP server | `axis` plugin |
| Reusable procedures | skills | `axis` plugin |
| Automatic enforcement | hook, git pre-commit, or a scheduled job | `UserPromptSubmit` hook, or a scheduled CI job |


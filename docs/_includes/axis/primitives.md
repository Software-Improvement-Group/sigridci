Everything here applies to any agentic tool, and every tool has its own version of the four primitives involved. The Claude Code column is one example:

| Primitive | Generic | Claude Code |
|-----------|---------|-------------|
| Persistent instructions | context file | `CLAUDE.md` |
| Tool access | MCP server | `axis` plugin |
| Reusable procedures | skills | `axis` plugin |
| Automatic enforcement | hook, git pre-commit, or a scheduled job | `UserPromptSubmit` hook, or a scheduled CI job |


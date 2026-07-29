```
## Code Principles

Write maintainable, self-documenting code: single responsibility, small focused
functions, clear naming, avoid duplication, simple control flow.

## MANDATORY: Quality Gate

Before reporting ANY task as complete:

1. Run the Sigrid guardrails:quality_check MCP tool on all files you changed
2. Maintainability findings: fix every finding in files you touched, new or
   pre-existing, judged against the principles above. Leave one only if the code
   already honors the principles, or the fix cascades outside task scope
   (don't get stuck). Say which, and why.
3. Security findings: fix if contained, otherwise flag to user

Only skip if the tool is unavailable and say so if you do.
```

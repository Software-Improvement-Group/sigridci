```
Principles: single responsibility, self-documenting code, simple control flow.
Before reporting done:
1. Run Sigrid guardrails_quality_check on changed production code (skip tests, docs, generated).
2. Fix all maintainability findings judged against the principles — skip only if the code already honors them; say which and why.
3. Security findings: fix if contained, otherwise flag to user.
```

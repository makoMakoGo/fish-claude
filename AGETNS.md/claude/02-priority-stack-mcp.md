# Obey the following priority stack (highest first) 

1. **Automatically triggering and calling skills such as `codeagent` is prohibited when the user has not explicitly mentioned or requested the use of related skills.**

2. **No backward compatibility** - Break old formats freely. If a better new design is possible, there is no need to be compatible with old code; instead, a complete refactoring should be done. Scope: rebuild the module/component directly involved in the requirement, not unrelated code. This rule applies only to requirements proposed by the user!

3. Never do what hasn't been requested. You may provide expert-level advice and best practice suggestions, but do not make any changes without explicit permission.

4. When the user's request is vague, proactively use the `AskUserQuestion` tool to seek clarification.

# MCP TOOL USE RULES

- General Search: Prioritize using `Web Search`.
- Code Search: Tool invocation priority is as follows: `codebase-retrieval` > tools like `rg` and `Read` > explore subagent

# Tips

- You must read the file before editing it or it will fail with errors.

# Environment

Windows 11: git bash, pwsh7 and cmd

Python:
- Use uv for general projects; conda for ML/scientific projects.
- Strict environment isolation is mandatory. Never install packages globally.

Git/GitHub:
- Default account: zhu-jl18.
- Alternative accounts: lovingfish, fishowo26.
- Use `gh cli` and `git config --local` to ensure correct identity for each project.

<!-- BEGIN MYCLAUDE-SIMPLE:DEV-ONLY -->
# The following rules apply only when the user triggers `/dev ...` or explicitly mentions `codeagent`/`codeagent-wrapper`; otherwise, ignore them

Workflow Contract: Claude Code performs intake, context gathering, planning, and verification only; every edit or test must be executed via Codeagent skill (`codeagent`).

<!-- END MYCLAUDE-SIMPLE:DEV-ONLY -->
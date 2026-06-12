# AGENTS.md

This file provides guidance to AI coding agents working with code in this repository.

## What This Repo Is

An **AI coding assistant configuration sharing repository** — NOT a business application.
Contains reusable rule fragments for project docs, baseline CLI config references, pack references, MCP setup guides, skills, and output styles for Claude Code, Codex, Antigravity CLI, etc.

**There is no application build system, application test suite, or `src/` directory.** Utility scripts may have lightweight validation under `tools/`.


## Rules for Editing This Repo

1. **Not a business code repo.** No builds, deploys, or `src/` assumptions.
2. **Correctness first**: make all related index/structure updates needed for a coherent change; do not modify unrelated modules.
3. **If file structure changes**, update the corresponding directory's `README.md` (every second-level directory carries its own index).

## Validation

Before submitting utility-script changes, run:

```bash
bash tools/validate.sh
```

# Git Commit Message Format

Use lightweight domain prefixes:

```
<prefix>: <subject>
<body>
<footer>
```

`<prefix>` and `<subject>` are required; `<body>` and `<footer>` are optional.

Prefer direct repo domain prefixes over conventional-commit scoped forms. Do not write `chore(mcp): ...` when `mcp: ...` is clearer.

Common prefixes examples:

- `mcp:` MCP guides and MCP config references
- `agy:` Antigravity CLI instructions/config
- `omp:` Oh My Pi instructions/config/tools
- `codex:` Codex instructions/config/tools
- `opencode:` OpenCode instructions/config
- `skills:` skill references and skill indexes
- `tools:` maintenance tools and patch runners
- `docs:` broad documentation-only updates
- `word:` modify text expression style 
- `chore:` broad repo maintenance that does not fit a tighter domain

## Local Repo Clones

If you are on my WSL2 environment, you find these git repo cloned when you need:
- `codex`, `oh-my-pi`, `rtk`, `context-mode`, `pi-mono`, `tokscale`, `claude-code`, `kimi-code`, `opencode` → `~/01-workspace/`
- `myclaude`, `oh-my-openagent`, `awesome-deepseek-agent` → `~/02-workspace/`
- `code-dispatcher-toolkit` → `~/personal-workspace/`

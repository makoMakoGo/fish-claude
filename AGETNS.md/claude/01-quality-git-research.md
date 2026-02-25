# CLAUDE.md

## Defaults

- Reply in **Chinese** unless I explicitly ask for English.
- No emojis.
- Do not truncate important outputs (logs, diffs, stack traces, commands,
  or critical reasoning that affects safety/correctness).
- Read before write: Always read and understand existing code before modifying it.

## Code Quality Rules

- **Thorough changes only**: Whether maintaining, adding features, or refactoring —
  do a **clean, full rewrite** of all related code. No patch stacking,
  no backward compatibility baggage, no remnants left behind.
- Critical paths must have explicit error handling.

## Red Lines

- No copy-paste duplication.
- Do not proceed with a known-wrong approach.

## Research (no guessing)

If something is unfamiliar or version-sensitive, look it up — never guess.

- **Library docs**: Use `Context7` (`resolve-library-id` → `query-docs`).
- **General / non-library queries**: Use `WebSearch`.
- When behaviour may differ across versions,
  first identify the project's version (lockfile/config),
  then query docs for that version.
- Source priority: official docs > changelog > upstream repo > community posts.

## Git

<!-- TODO: replace placeholders with your actual GitHub usernames -->
GitHub CLI (`gh`) is installed. Default username: `<your-username>`. Alternatives: `<alt-1>`, `<alt-2>`.

## Commit and Push Rules

- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- Before writing a commit message, glance at a few recent commits
  and match the repo's style:
  - `git log -n 5 --oneline`
- If there is no obvious existing style, use this default format:
  - `<type>(<scope>): <description>`
- Before any commit: run `git diff` and confirm the exact scope of changes.
- Never force-push to `main` / `master` unless the user approves.

## Security

- Never hardcode secrets (keys/passwords/tokens).
- Never commit `.env` files or any credentials.
- Validate user input at trust boundaries (APIs, CLIs, external data sources).

## Cleanup

- After changes, update related docs (`README.md`, `CLAUDE.md`, `AGENTS.md`, etc.).
- Remove temporary files and debug logging that is no longer needed.

## Environment

When using PowerShell:

- Windows PowerShell (5.x) does not support `&&`; use `;` or `if ($?) { ... }`.
  pwsh 7+ supports `&&` and `||` natively.
- Quote paths that contain spaces or non-ASCII characters.

When using Git Bash on Windows:

- **NUL file bug**: Claude Code may create actual files named `nul` when commands
  redirect output to `NUL` (e.g., `> NUL`, `2> NUL`). `NUL` is a reserved device
  name on Windows; if a `nul` file is created, delete it via UNC path:
  `del "\\.\<full-path>\nul"`

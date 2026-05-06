# system-prompts

## Claude Code

- source remote: `https://github.com/Piebald-AI/claude-code-system-prompts`
- prompts index: `https://github.com/Piebald-AI/claude-code-system-prompts/tree/main/system-prompts`
- note: Claude Code prompt pieces change frequently and are better referenced directly from the upstream categorized mirror

## Codex CLI

- file: `codex-cli.md`
- source remote: `https://github.com/openai/codex.git`
- source prompt path: `codex-rs/models-manager/models.json` (`gpt-5.5` `model_messages.instructions_template` + `personality_pragmatic`)
- synced date: `2026-05-04`
- note: Codex CLI now resolves model instructions from the model catalog; this copy records the resolved `gpt-5.5` prompt for the fish-claude default `personality = "pragmatic"` config

## Gemini CLI

- file: `gemini-cli.md`
- source remote: `https://github.com/google-gemini/gemini-cli.git`
- source commit: `ca7ac0003`
- source prompt path: `packages/core/src/prompts/snippets.ts`
- synced date: `2026-03-09`
- note: Gemini CLI does not use one static system prompt file like Codex
- note: Gemini CLI composes the final prompt dynamically from `snippets.ts`
- note: `gemini-cli.md` records the Gemini 3 / modern / interactive baseline plus the major conditional sections injected at runtime

## OpenCode

- file: `opencode.md`
- source remote: `https://github.com/anomalyco/opencode.git`
- source branch: `dev`
- source commit: `8299fb3e2`
- source prompt paths: `packages/opencode/src/session/system.ts`, `packages/opencode/src/session/llm.ts`, `packages/opencode/src/session/prompt/*.txt`
- synced date: `2026-05-03`
- note: OpenCode does not use one static prompt file; the runtime prompt is assembled from provider-specific prompt text, environment metadata, project instructions, custom agent prompts, and skill descriptions

## Oh My Pi

- source remote: `https://github.com/nicobailon/oh-my-pi.git`
- file: `oh-my-pi.md`
- source commit: `cff84d764`
- source prompt path: `packages/coding-agent/src/prompts/system/system-prompt.md`
- synced date: `2026-04-13`
- note: Oh My Pi uses Handlebars templates (`{{...}}`) for dynamic prompt composition
- note: the system prompt is the primary template; sub-agent and custom prompts are separate templates composed at runtime

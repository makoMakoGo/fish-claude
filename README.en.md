<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

A personal resource kit for AI coding agent configs—pick what you need, adapt to fit.

Excellent vibe coding is fed one token at a time.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/zhu-jl18/fish-claude?style=social)

<br>

<img src="assets/badges/claude-code.svg" alt="Claude Code">
<img src="assets/badges/codex.svg" alt="Codex">
<img src="assets/badges/antigravity.svg" alt="Antigravity">
<img src="assets/badges/droid.svg" alt="Droid">
<img src="assets/badges/oh-my-pi.svg" alt="Oh My Pi">
<img src="assets/badges/warp.svg" alt="Warp">
<img src="assets/badges/opencode.svg" alt="OpenCode">

<br>

[中文](README.md) | English

</div>

It is not a tutorial collection or a generic framework; it is a personal Vibe Coding config backup kit I actually use, with a strong personal character. Covers the code agents I daily use (no particular ranking):

- Claude Code + Pi
- Oh My Pi + Codex + Droid
- Warp
- OpenCode + Antigravity
- Warp
- OpenCode

## What You Can Steal

| Content | Entry | Use |
| --- | --- | --- |
| Rule modules | [`agent-instructions/`](agent-instructions/) | Composable fragments for assembling `AGENTS.md`, `CLAUDE.md`, and other CLI instruction files |
| Skills | [`skills/`](skills/) | Skill definitions and references installable in Claude Code / Codex / OMP / Antigravity CLI |
| Config samples | [`config-files/`](config-files/) | Baseline config references for `settings.json`, `config.toml`, OMP agent config, and more |
| MCP guides | [`mcp/`](mcp/) | Installation, configuration, and usage notes for common MCP servers |
| Packs | [`packs/`](packs/) | Composite bundles, external toolchains, and reusable install references |
| Tools / patches | [`tools/`](tools/) | Local maintenance tools, migration scripts, and OMP patch runners |
| Output Styles | [`output-styles/`](output-styles/) | Output personas |
| Preset Cards | [`preset-cards/`](preset-cards/) | Useful preset cards |
| Themes | [`themes/`](themes/) | Warp / Claude Code themes |
| Sub-agents | [`sub-agents/`](sub-agents/) | Sub-agent and multi-agent practices |
| Slash Commands | [`slash-commands/`](slash-commands/) | Slash command templates |
| Tips | [`tips/`](tips/) | Practical notes and tips |
| Services | [`ai-services/`](ai-services/) | External API service references |

## Start Here

- [Rule module index](agent-instructions/README.md): see how instruction fragments are assembled for each CLI.
- [Skills guide](skills/README.md): browse installable community and custom skills.
- [Config file references](config-files/README.md): copy baseline CLI config samples.
- [MCP setup](mcp/README.md): connect MCP servers as needed.
- [Packs](packs/README.md): find composite bundles and external toolchain entries.
- [Tools](tools/README.md): use maintenance tools, migration scripts, and patch runners.
- [System prompts](system-prompts/README.md): inspect upstream system prompt reference copies.

## How to Use

Just copy-paste what you like. Everything is pluggable; if components are linked I've noted it. What works for me may not work for you—test what interests you, drop what doesn't, keep what does, and feel free to mod it. In the end, you'll probably customize it with Pi anyway.

Pair it with [Mako's Blog](https://makomakogo.github.io/) for more context.

## Contributing

If you run into problems, feel free to open an Issue for discussion and feedback. This is a personal project, and PRs are closed.

## License

MIT
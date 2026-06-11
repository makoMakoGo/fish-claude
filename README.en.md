<div align="center">
<img src="repo-logo.svg" alt="Fish Claude logo" width="180" />

<h1>Fish Claude</h1>

**Fish's Coding Agent Configs**

A personal config mirror repo — pick what you need, don't blindly copy.

Great Vibe Coders are fed one stolen bite at a time.

<img src="assets/tokscale.svg" alt="Local Tokscale stats" />

<sub>My real usage, rendered by <a href="tools/tokscale-readme-svg/">tokscale-readme-svg</a></sub>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![GitHub stars](https://img.shields.io/github/stars/makoMakoGo/fish-claude?style=social)

<img src="assets/badges/claude-code.svg" alt="Claude Code">
<img src="assets/badges/codex.svg" alt="Codex">
<img src="assets/badges/droid.svg" alt="Droid">
<img src="assets/badges/oh-my-pi.svg" alt="Oh My Pi">
<img src="assets/badges/warp.svg" alt="Warp">
<img src="assets/badges/opencode.svg" alt="OpenCode">
<img src="assets/badges/antigravity.svg" alt="Antigravity">

<br>

[中文](README.md) | English

</div>

## What This Is

Not a tutorial collection, not a generic framework — just a backup repo of the Vibe Coding configs I personally use, heavily flavored by my own taste. The code agents covered (also the ones I use daily, ordered by my personal preference):

- Pi + Claude Code
- Oh My Pi + Codex + Droid
- Warp
- OpenCode + Antigravity

## Start Here

- [codex-provider-history-migrator](tools/codex-provider-history-migrator/) — get your Codex chat history back after a model provider switch
- [agent-instructions](agent-instructions/) — assemble your own global rules from pluggable modules
- [One AGENTS.md to feed every CLI](tips/shared-agents-md.md) — a trick few people know

## What's Inside

| Content | Entry | Use |
| --- | --- | --- |
| Rule modules | [`agent-instructions/`](agent-instructions/) | Assemble a global `AGENTS.md` |
| Skills | [`skills/`](skills/) | My personal skills collection |
| Config samples | [`config-files/`](config-files/) | References for personalized config fields |
| MCP | [`mcp/`](mcp/) | MCP servers I still use |
| Packs | [`packs/`](packs/) | Composite bundles and external toolchains |
| Tools | [`tools/`](tools/) | Maintenance scripts and custom patches |
| Output styles | [`output-styles/`](output-styles/) | A few interesting style presets |
| Preset Cards | [`preset-cards/`](preset-cards/) | Useful preset cards |
| System Prompts | [`system-prompts/`](system-prompts/) | Third-party system prompt captures, research reference only |
| Themes | [`themes/`](themes/) | Themes for Warp / Claude Code, etc. |
| Sub-agents | [`sub-agents/`](sub-agents/) | subagent && multi-agent practice |
| Commands | [`slash-commands/`](slash-commands/) | Slash command templates |
| Tips | [`tips/`](tips/) | Practical tricks you might not know |

## How to Use

Skim it, find what interests you, copy-paste it. Everything is pluggable; where modules are linked I've noted it. Mine may not fit you — test what interests you, drop what doesn't, keep what does, and feel free to mod it. In the end, you'll definitely end up modding it with Pi yourself.

Pairs well with [Mako's Blog](https://makomakogo.github.io/).

## Contributing

If you hit problems, feel free to open an Issue to discuss. Pure personal project — PRs are not accepted and will be closed on sight.

## License

Original content in this repo is released under MIT. Third-party material — system prompt captures under `system-prompts/` and sourced content under `preset-cards/` and elsewhere — remains the property of its original authors or companies, is included for research reference only, and is not covered by the MIT grant.

# Tools

本地维护/迁移工具与 patch。

| Tool | Type | Runtime | 说明 |
| --- | --- | --- | --- |
| [claude-code-launcher](claude-code-launcher/) | launcher | PowerShell | 交互式启动器，按 `settings*` 文件选配置 |
| [claude-json-history-cleaner](claude-json-history-cleaner/) | maintenance | Python | 清理旧版 Claude Code 写入 `~/.claude.json` 的项目 prompt history |
| [codex-provider-history-migrator](codex-provider-history-migrator/) | migration | Python | 迁移 Codex `model_provider`，恢复 history / resume / fork |
| [omp-patch-codex-websearch-byok](omp-patch-codex-websearch-byok/) | patch | Bun/TS | OMP codex web_search 支持自定义后端 |
| [omp-patch-custom-mcp](omp-patch-custom-mcp/) | patch | Bun/TS | OMP MCP 发现增加 Claude/Codex 用户级开关 |
| [tokscale-readme-svg](tokscale-readme-svg/) | generator | Node.js | 读取本地 `tokscale --json` 并生成 README 用静态 SVG |
| [validate.sh](validate.sh) | check | Bash | 仓库验证入口（AGENTS.md 约定）：hygiene、语法/构建检查、单测与冒烟 |
| [check-repo-hygiene.sh](check-repo-hygiene.sh) | check | Bash | 仓库卫生检查：tracked-but-ignored 文件、孤儿 `.gitkeep`、markdown 结构 |

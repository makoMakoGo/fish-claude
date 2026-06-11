# Skills 指南

## 发现机制

| CLI | User Scope | Project Scope | 备注 |
|-----|-----------|--------------|------------|
| Claude Code | `~/.claude/skills/` | `.claude/skills/` | 无兼容路径，最干净 |
| Codex | `~/.codex/skills/` | `.codex/skills/` | 兼容 `.agents/skills` |
| Antigravity CLI | `~/.gemini/antigravity-cli/skills/` | `.agents/skills/` | 发现路径最混乱 |
| Warp | `~/.agents/skills/` | `.agents/skills/` | 发现无法关闭 |
| OMP | `~/.omp/agent/skills/` | `.omp/agent/skills/` | 发现可关闭 |
| OpenCode | `~/.config/opencode/skills/` | `.opencode/skills/` | 发现可关闭 |
| Droid | `~/.factory/skills/` | `.factory/skills/` | 兼容 `.agent/skills/` |

## Skills 一览

| Skill | 形态 | 来源 | 说明 |
| --- | --- | --- | --- |
| [AI Coding Discipline](ai-coding-discipline.md) | 导览 | `luoling8192/ai-coding-principles` | 禁止静默 fallback、禁止业务逻辑 catch-all、要求有效测试与干净调试流程 |
| [Software Design Philosophy](software-design-philosophy.md) | 导览 | `luoling8192/software-design-philosophy-skill` | 基于《A Philosophy of Software Design》的复杂度管理与模块/API 设计视角 skill |
| [UI UX Pro Max](ui-ux-pro-max.md) | 导览 | `nextlevelbuilder/ui-ux-pro-max-skill` | 一个不错的前端审美 skill |
| [Beautiful Mermaid](beautiful-mermaid.md) | 导览 | `okooo5km/beautiful-mermaid-cli` | 通过 `bm` 输出 SVG / PNG / ASCII，并支持 `--json` 机器可读结果 |
| [Grok Search](grok-search.md) | 导览 | `abelxiaoxing/agent-toolkit` | 用 Grok API + Tavily 替代内置 WebSearch/WebFetch 的 CLI skill |
| [Sync Readme](sync-readme.md) | 导览 | `Li-ionFractalNanocore/cc-wrap` | 识别最新版本并翻译/同步其他 README 文件 |
| [Karpathy Guidelines](karpathy-guidelines.md) | 导览 | `forrestchang/andrej-karpathy-skills` | 强调先澄清假设、优先简单方案、做手术式变更，并把任务改写成可验证目标 |
| [Geju](geju.md) | 导览 | `hylarucoder/hai-stack` | 方案讨论高位判断 skill：挑战过度保守/渐进式/被兼容性绑架的设计，输出 thesis、kill-list、选项表与验证路径 |
| [Gemini Deep Reasoning](gemini-deep-reasoning/) | 可安装 | [@googleaidevs](https://x.com/googleaidevs/status/1996271402266017901) | Agentic 深度推理系统指令：结构化规划、风险评估、溯因推理、持久问题解决 |
| [GPT-Isms Stamp Out](gpt-isms-stamp-out/) | 可安装 | 自建 | GPT-5.4 口癖清除 skill |
| [Improve CLAUDE.md](improve-claude-md.md) | 导览 | `humanlayer/skills` | 用 `<important if>` 条件块重写 CLAUDE.md 提升指令遵从率 |

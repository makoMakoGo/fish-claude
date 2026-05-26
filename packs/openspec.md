# openspec

轻量级 spec-driven development 框架：先把改动写成 spec（requirements + scenarios）再让 AI agent 按 spec 实现。每个 change 落在 `openspec/changes/<id>/`，合并后归档到 `openspec/specs/`。纯 Markdown，check in 进 Git，不依赖 MCP 或 API Key。

## 来源

- 官网：<https://openspec.dev>
- GitHub：<https://github.com/Fission-AI/OpenSpec>
- npm：[`@fission-ai/openspec`](https://www.npmjs.com/package/@fission-ai/openspec)
- License：MIT

## 是什么

一个全局 CLI（`openspec`）+ 项目内 `openspec/` 目录 + 给每个目标 CLI 下发的 skills 和 slash commands。默认 `core` profile 启用五个工作流命令：

| 命令 | 作用 |
| --- | --- |
| `/opsx:propose` | 把想法写成 proposal：requirements、spec delta、tasks |
| `/opsx:explore` | 方案探索与分析 |
| `/opsx:apply` | 按已定的 change 实施 |
| `/opsx:sync` | 对齐 spec 与代码状态 |
| `/opsx:archive` | 归档完成的 change，更新 `openspec/specs/` |

通过 `openspec config profile` 切换扩展 profile 可解锁 `new` / `continue` / `ff` / `verify` / `bulk-archive` / `onboard` 等更细的工作流。

## 安装

要求 Node.js ≥ 20.19.0。

```bash
npm install -g @fission-ai/openspec@latest

cd <your-project>
openspec init                              # 交互式选择要接入的 CLI
# 或非交互：
openspec init --tools claude,codex,opencode --profile core
openspec update                            # 升级后刷新所有已接入 CLI 的指令
```

`openspec init` 不改全局配置，所有产物写到项目目录；Codex 命令是例外，写到 `$CODEX_HOME/prompts/`（默认 `~/.codex/prompts/`）。

## 本仓库关心的 CLI 接入路径

| CLI | Skill 路径 | Slash command 路径 |
| --- | --- | --- |
| Claude Code | `.claude/skills/openspec-*/SKILL.md` | `.claude/commands/opsx/<id>.md` |
| Codex | `.codex/skills/openspec-*/SKILL.md` | `$CODEX_HOME/prompts/opsx-<id>.md`（全局） |
| OpenCode | `.opencode/skills/openspec-*/SKILL.md` | `.opencode/commands/opsx-<id>.md` |
| Cursor | `.cursor/skills/openspec-*/SKILL.md` | `.cursor/commands/opsx-<id>.md` |

Warp 与 Oh My Pi 不在原生工具列表里（上游 `pi` tool id 对应的是另一个 `.pi/` 约定的 CLI，并非 OMP 的 `.omp/`）。这两个仍可通过共享 `AGENTS.md`（见 [tips/shared-agents-md.md](../tips/shared-agents-md.md)）让 spec 文档被读到，但 slash commands 需要手动移植。

上游完整工具矩阵：[supported-tools.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md)（目前 25+ 家）。

## 为什么选它

- 计划层与 agent 解耦：换 CLI / 换模型不丢 spec，也不丢已归档的历史 change。
- 纯文本工件，直接用 git review / diff / PR 流程协作，和 chat 历史无关。
- 比 [GitHub Spec Kit](https://github.com/github/spec-kit) 轻（没有 phase gate、不需要 Python 环境），比 [AWS Kiro](https://kiro.dev) 自由（不绑定 IDE 或模型）。

# Packs 指南

一些 plugin 和 skills 合集等。

## Pack 典型结构

```text
<pack-name>/
├── README.md           # 安装说明与概览
├── SKILL.md            # 协议/skill 定义（可选）
├── settings.json       # Claude Code hook 配置片段（可选）
├── hooks/              # 生命周期 hook 脚本（可选）
├── commands/           # slash command 模板（可选）
└── tests/              # 测试文件（可选）
```

## 可用 Pack

| Pack | 说明 |
| --- | --- |
| [code-dispatcher-toolkit](code-dispatcher-toolkit.md) |claude codex gemini 编排 |
| [rtk](rtk.md) | Rust Token Killer|
| [myclaude-harness](myclaude-harness.md) | `stellarlinkco/myclaude` |
| [context-mode](context-mode.md) | 在 sandbox 内处理大输出 |
| [nmem](nmem.md) | 跨 AI 工具共享的本地记忆库和知识图谱 |
| [mattpocock-skills](mattpocock-skills.md) | 需求澄清、文档协作、TDD、debugging  |
| [openspec](openspec.md) | 轻量 spec-driven 框架  |
| [cursor-team-kit](cursor-team-kit.md) | Cursor 官方 plugin；|

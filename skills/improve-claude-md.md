# Improve CLAUDE.md

## 来源

- GitHub: `humanlayer/skills`
- URL: <https://github.com/humanlayer/skills/tree/main/plugins/improve-claude-md>
- 思路详解: <https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md>

## 简介

- 重构 `CLAUDE.md` 让 Claude Code 更愿意遵守的 skill：用 `<important if="condition">` XML 标签包裹有条件相关性的章节，给模型明确的相关性信号，穿透 system reminder 中 "may or may not be relevant" 的模糊语义
- 原则：基础上下文裸写、领域指导窄触发包裹、删 linter 能强制执行的内容、删可由代码模式推断的内容、用文件路径引用代替代码片段、保留所有命令
- 输出结构：项目身份 + Project map + 命令表（一个 important 块）+ 多个按触发条件拆分的规则块

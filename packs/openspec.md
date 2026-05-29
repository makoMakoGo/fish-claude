# openspec

轻量 spec-driven development 框架：先写 spec（requirements + scenarios）再让 agent 按 spec 实现。每个 change 落在 `openspec/changes/<id>/`，合并后归档到 `openspec/specs/`。纯 Markdown，check in 进 Git，不依赖 MCP 或 API Key。

- 官网：<https://openspec.dev>
- GitHub：<https://github.com/Fission-AI/OpenSpec>
- npm：[`@fission-ai/openspec`](https://www.npmjs.com/package/@fission-ai/openspec)

## 为什么用

- 计划层与 agent 解耦：换 CLI / 换模型不丢 spec
- 纯文本工件，走 git review / diff / PR 流程
- 比 [GitHub Spec Kit](https://github.com/github/spec-kit) 轻（无 phase gate、无 Python），比 [Kiro](https://kiro.dev) 自由（不绑 IDE 或模型）

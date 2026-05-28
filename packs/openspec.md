# openspec

轻量级 spec-driven development 框架：先把改动写成 spec（requirements + scenarios）再让 AI agent 按 spec 实现。每个 change 落在 `openspec/changes/<id>/`，合并后归档到 `openspec/specs/`。纯 Markdown，check in 进 Git，不依赖 MCP 或 API Key。

## 来源

- 官网：<https://openspec.dev>
- GitHub：<https://github.com/Fission-AI/OpenSpec>
- npm：[`@fission-ai/openspec`](https://www.npmjs.com/package/@fission-ai/openspec)
- License：MIT

## 为什么选它

- 计划层与 agent 解耦：换 CLI / 换模型不丢 spec，也不丢已归档的历史 change。
- 纯文本工件，直接用 git review / diff / PR 流程协作，和 chat 历史无关。
- 比 [GitHub Spec Kit](https://github.com/github/spec-kit) 轻（没有 phase gate、不需要 Python 环境），比 [AWS Kiro](https://kiro.dev) 自由（不绑定 IDE 或模型）。

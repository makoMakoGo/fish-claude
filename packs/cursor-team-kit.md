# cursor-team-kit

Cursor 官方插件包，把 Cursor 团队内部使用的 CI、review、发版、验证、测试可靠性、代码清理和工作总结流程打包成可安装 plugin。

## 来源

- Marketplace：<https://cursor.com/cn/marketplace/cursor/cursor-team-kit>
- GitHub：<https://github.com/cursor/plugins/tree/main/cursor-team-kit>
- License：MIT

## 是什么

一个 Cursor plugin，不是通用 CLI pack。安装后给 Cursor 注入 skills、subagents 和 rules，用来覆盖常见工程协作工作流：

- CI 监控与失败修复
- PR review、发版和 reviewer 友好化
- UI / CLI 本地控制 harness
- smoke test、compiler/type-check 验证
- 代码清理、严格质量审计和工作总结

官方描述强调它不要求第三方服务集成，适合直接在已有 Cursor 工作流里补齐团队级自动化。

## 安装

在 Cursor 里执行：

```text
/add-plugin cursor-team-kit
```

## 组件

| 类型 | 数量 | 代表内容 |
| --- | ---: | --- |
| Skills | 18 | `loop-on-ci`、`review-and-ship`、`verify-this`、`control-cli`、`control-ui`、`fix-ci`、`deslop` |
| Subagents | 2 | `ci-watcher`、`thermo-nuclear-code-quality-review` |
| Rules | 2 | `typescript-exhaustive-switch`、`no-inline-imports` |

## 适合什么时候用

如果项目主要在 Cursor 里协作，而且已经有 GitHub Actions、PR review、前端 UI 验证或 CLI/TUI 验证需求，它可以作为一套现成的团队工作流模板。若你主要用 Claude Code、Codex、Gemini CLI 或 OpenCode，这个条目更多是参考页；不要硬拷它的 Cursor plugin 结构，笨蛋式跨平台搬运只会制造一堆不能加载的碎片。

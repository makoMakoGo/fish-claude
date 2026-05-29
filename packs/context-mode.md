# context-mode

把大输出关在 sandbox，只让摘要进上下文，防止窗口被吃满。

- GitHub：<https://github.com/mksglu/context-mode>

## 为什么用

~~我用国产模型跑 Claude Code，有效上下文比官方模型短。~~

> [!NOTE]
> V4：我不在的时候你们几条野狗很嚣张啊

大输出堆进去很快就幻觉、丢指令。context-mode 把原始数据隔离在 sandbox（SQLite FTS5），只回流摘要，窗口占用可控。

## 怎么工作

PreToolUse hook 分档拦截/建议 + MCP tool 做 sandbox 隔离。

| 场景 | 处理 |
|------|------|
| `WebFetch` | 硬拦（deny） |
| `curl` / `wget` 非静默或 stdout 输出 | 硬拦（modify → echo） |
| `gradle` / `mvn` 等构建工具 | 硬拦（modify → echo） |
| 一般 `Bash` / `Read` / `Grep` | 贴 tip（advisory），建议走 sandbox |

每种 tip 一个 session 只发一次。

`ctx_execute` 在独立子进程跑代码，原始输出写 SQLite，仅摘要返回对话。`ctx_search` 事后按需检索。

## 与 RTK 的关系

不建议一起用。目前 context-mode 只在 Claude Code 里用；rtk 在 Codex 和 OMP 里用。

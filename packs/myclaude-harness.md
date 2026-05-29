# myclaude-harness

Claude Code 长运行任务 harness，处理跨上下文窗口的任务持久化、失败恢复和进度追踪。

- GitHub：<https://github.com/stellarlinkco/myclaude>
- 目录：`skills/harness/`

`Stop`、`SessionStart`、`TeammateIdle`、`SubagentStop` 等 hooks 协作，保证任务跨 session 不丢状态。

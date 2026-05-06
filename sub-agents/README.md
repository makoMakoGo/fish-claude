# sub-agents

各 CLI 的 sub-agent / role layer 示例与索引。

## 总览

| CLI | 定义形态 | 派发方式 | 嵌套 | 远程 | 亮点 |
|-----|---------|---------|------|------|------|
| Claude | frontmatter + markdown | 自动（按 description）或显式指名 | 禁止 | — | 专家卡片，独立 context |
| Codex | TOML role layer | 主 agent spawn 子线程 | `max_depth` 控制 | — | 通用 lane 分工 |
| OMP | 调用时 prompt 动态组装 | Task 工具派发 | 无限制（独立 session） | — | swarm DAG 编排 + 强制结构化返回 |
| Gemini | frontmatter + markdown | 以 tool name 暴露，自动或 `@name` | 硬禁止 | — | tool 级白名单 + 远程 subagent |

更多细节参考：[Claude / Codex / OMP / Gemini CLI 的 Sub-Agent 机制整理](https://makomakogo.github.io/posts/2026/05/06/claude-codex-omp-gemini-subagents.html)。
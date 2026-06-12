# sub-agents

各 CLI 的 sub-agent / role layer 示例与索引。

## 总览

| CLI | 定义形态 | 派发方式 | 嵌套 | 亮点 |
|-----|---------|---------|------|------|
| Claude | frontmatter + markdown | 自动或显式指名 | 禁止 | 专家卡片，独立 context |
| Codex | TOML role layer | 主 agent spawn 子线程 | `max_depth` 控制 | 通用 lane 分工 |
| OMP | 调用时 prompt 动态组装 | Task 工具派发 | 无限制（独立 session） | 主动性好 |
| Antigravity CLI | frontmatter + markdown | 自动或 `@name` | 硬禁止 | 无 |

更多细节参考：[Claude / Codex / OMP / Antigravity CLI 的 Sub-Agent 机制整理](https://makomakogo.github.io/posts/2026/05/06/claude-codex-omp-gemini-subagents.html)。

## Claude Code

| 文件 | 说明 |
| --- | --- |
| [code-simplifier](claude/code-simplifier.md) | 保持行为不变的代码简化专家，默认聚焦最近改动 |

## Codex

放进 `~/.codex/agents/<role>.toml` 即被自动发现，所需联动配置详见 [config-files](../config-files/README.md#codex)。

| 文件 | 说明 |
| --- | --- |
| [default](codex/default.toml) | 通用派发 sub-agent，回报要求结论 + 证据 + 下一步 |
| [worker](codex/worker.toml) | 实现型 sub-agent，先验证改动再回报 |
| [explorer](codex/explorer.toml) | 只读探索，收集证据不改文件 |
| [awaiter](codex/awaiter.toml) | 盯长任务到终态再回报，禁止臆断完成 |
| [spark](codex/spark.toml) | 基于 gpt-5.3-codex-spark 的快速小任务 lane，128k 纯文本上下文 |
| [role-layer.example](codex/role-layer.example.toml) | role layer 写法示例（含 layering 规则注释），不直接部署 |

# OMP Swarm DAG 编排

官方 package：`packages/swarm-extension/`。把多 agent 工作流写成 YAML，调度器构建 DAG、拓扑排序成 wave。每个 agent 是完整 OMP subagent（full tool set：bash / python / read / write / edit / grep / find / fetch / web_search / browser）。

入口：

- TUI 内：`/swarm <path-to.yaml>`（注册自 `src/extension.ts`）
- 独立运行：`bun run src/cli.ts <path-to.yaml>`（无 TUI、无 timeout，适合长跑）

YAML 结构：

```yaml
swarm:
  name: my-pipeline          # 必填，state 存在 .swarm_<name>/
  workspace: ./workspace     # 必填，共享工作目录
  mode: pipeline             # pipeline | parallel | sequential（默认 sequential）
  target_count: 10           # pipeline 模式的迭代次数，默认 1
  model: claude-opus-4-6     # 默认 model（可被 per-agent 覆盖）

  agents:
    finder:
      role: web-scraper                 # 必填，作为 system prompt
      task: |                           # 必填，多行 user prompt
        Find 10 relevant URLs …
      extra_context: |                  # 可选，附加到 system prompt
        Only consider sources after 2024.
      reports_to: [analyzer]            # 可选，声明下游
      waits_for: []                     # 可选，声明上游
      model: claude-sonnet-4-5          # 可选，per-agent 覆盖
```

三种执行模式：

| Mode | 行为 |
| ---- | ---- |
| `sequential`（默认） | 按声明顺序串行跑一遍 |
| `parallel` | 所有 agent 并发（除非 `waits_for` / `reports_to` 强制排序） |
| `pipeline` | 整张 agent DAG 重复跑 `target_count` 次（累积式工作，如"找 50 个东西，每轮找一个"） |

DAG 调度（源码 `src/swarm/dag.ts`）：

- `waits_for: [a, b]` — 两者都完成才启动
- `reports_to: [x]` — 等价于 `x.waits_for` 加上自己
- 同一 wave 内并发执行；wave 之间按拓扑序串行
- 有 cycle 直接拒绝执行

Agent 间通信：**只走共享 workspace 文件系统**。orchestrator 不传数据，只管启停顺序。常见协议：signal files（`signals/*.txt` 状态标记）、结构化输出（`analyzed/item_N.md`、`results/*.json`）、tracking files（`processed.txt` 去重）。

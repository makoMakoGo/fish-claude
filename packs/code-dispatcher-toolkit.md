# code-dispatcher-toolkit

我自己写的多后端 AI 编码工具集：`code-dispatcher` CLI + 可安装 Skills + 安装脚本。

## 来源

- GitHub：<https://github.com/makoMakoGo/code-dispatcher-toolkit>

## 是什么

核心是一个 CLI 调度器 `code-dispatcher`，统一调度 `codex`、`claude`、`antigravity` 三个后端：

接收任务 → 选后端 → 构建参数 → 分发执行 → 收集结果

- `--backend` 切换或并行调用多个后端
- `--parallel` 基于 DAG 调度同时跑独立任务
- `--resume` 上下文重置后继续未完成任务
- 统一配置 `~/.code-dispatcher/.env`


> 核心思路基于 [`cexll/myclaude`](https://github.com/cexll/myclaude) 的 codeagent wrapper，经大量重构。

## Skills

| 名称 | 用途 | 依赖 CLI |
|------|------|----------|
| `code-dispatcher` | 执行器使用说明；统一 3 个后端；覆盖 `--parallel` / `--resume` 机制 | 必需 |
| `dev` | 需求澄清 → 计划 → 选择后端 → 并行执行（DAG 调度）→ 验证 | 必需 |
| `pr-review-reply` | 自主处理 PR bot review，修复或反驳并回复线程 | 可选 |



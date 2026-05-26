# code-dispatcher-toolkit

多后端 AI 编码工具集：`code-dispatcher` CLI + 可安装 Skills + 安装脚本。

## 来源

- GitHub：<https://github.com/makoMakoGo/code-dispatcher-toolkit>

## 是什么

核心是一个 CLI 调度器 `code-dispatcher`，统一调度 `codex`、`claude`、`antigravity` 三个后端：

接收任务 → 选后端 → 构建参数 → 分发执行 → 收集结果

- `--backend` 切换或并行调用多个后端
- `--parallel` 基于 DAG 调度同时跑独立任务
- `--resume` 上下文重置后继续未完成任务
- 统一配置 `~/.code-dispatcher/.env`

后端定位（推荐，可自由指定）：

- `codex`：复杂逻辑、bug 修复、重构
- `claude`：快速任务、review、补充分析
- `antigravity`：前端 UI/UX 原型

> 核心思路基于 [`cexll/myclaude`](https://github.com/cexll/myclaude) 的 codeagent wrapper，经大量重构。

## Skills

| 名称 | 用途 | 依赖 CLI |
|------|------|----------|
| `code-dispatcher` | 执行器使用说明；统一 3 个后端；覆盖 `--parallel` / `--resume` 机制 | 必需 |
| `dev` | 需求澄清 → 计划 → 选择后端 → 并行执行（DAG 调度）→ 验证 | 必需 |
| `pr-review-reply` | 自主处理 PR bot review，修复或反驳并回复线程 | 可选 |

## 安装

```bash
python3 install.py                                      # 下载 CLI 二进制 + 生成配置
python3 install.py --install-dir ~/.code-dispatcher --force
python3 install.py --skip-dispatcher                    # 仅安装 skills
```

脚本默认安装：

- `~/.code-dispatcher/.env`：运行时唯一配置源
- `~/.code-dispatcher/prompts/*-prompt.md`：各后端默认 prompt 模板
- `~/.code-dispatcher/bin/code-dispatcher`：执行器二进制

Skill 复制到对应 CLI 的 skills 目录（`~/.agents/skills/`、`~/.claude/skills/`、`~/.codex/skills/`、`~/.config/opencode/skills/`、`~/.gemini/antigravity-cli/skills/` 等）即可。

# slash-commands

## 命令模板

| 文件              | 用途                           |
| ----------------- | ------------------------------ |
| `fresh-branch.md` | 创建并切换到新分支时使用的模板 |

## slash 支持情况

slash 没有统一标准，且正被 skills 吸收。

| Agent    | 自定义 slash 形态 | 用户级路径               | 项目级路径           |
| -------- | ----------------- | ------------------------ | -------------------- |
| Claude   |                   | `~/.claude/commands/`    | `.claude/commands/`  |
| Codex    |                   | `~/.codex/prompts/<name>.md` | 不支持           |
| OpenCode | Markdown 或 JSON  | `~/.config/opencode/command/` | `.opencode/command/` |
| Droid    |                   | `~/.factory/commands/`   | `.factory/commands/` |
| AGY CLI  | 无自定义入口      | —                        | —                    |
| Warp     | Warp Drive        | Warp Drive（云端账号）   | —                    |
| oh-my-pi | 用扩展注册        | extension 形式           | 同                   |



# Semble MCP

本地代码语义搜索，适合按行为、意图、架构关系找代码。

## 本机 OpenCode 配置

使用 safe wrapper，不直接全局 `semble .`：

```json
{
  "mcp": {
    "semble": {
      "type": "local",
      "command": ["/home/travis/.local/bin/semble-opencode-safe"],
      "enabled": true,
      "timeout": 60000
    }
  }
}
```

wrapper 行为：

- 在 Git 项目内启动：预索引 Git root。
- 在 `~`、`/` 或非 Git 目录启动：不预索引，模型需要时显式传 `repo`。

`/home/travis/.local/bin/semble-opencode-safe`：

```bash
#!/usr/bin/env bash
set -euo pipefail

cwd="$(pwd)"
home="${HOME:-}"

if git_root="$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null)"; then
  case "$git_root" in
    "$home"|"/")
      exec uvx --from "semble[mcp]" semble
      ;;
    *)
      exec uvx --from "semble[mcp]" semble "$git_root"
      ;;
  esac
else
  exec uvx --from "semble[mcp]" semble
fi
```

## 隐私

- 本地路径索引不主动上传 repo。
- 首次运行可能下载 Python 包和默认模型。
- 返回的代码片段会进入当前 agent 的模型上下文。

## 使用规则

- 行为/意图/架构探索：先用 Semble。
- 精确字符串或全量确认：再用 grep。

# Exa Search MCP

Exa Search MCP 用 Exa 的搜索能力给 Claude Code 提供网页搜索能力。

- 包：`exa-mcp-server`
- 示例配置只启用 `web_search_exa`。
- API Key：通过 `EXA_API_KEY` 环境变量传入

## Claude Code 配置

```json
{
  "mcpServers": {
    "exa-search": {
      "command": "npx",
      "args": [
        "-y",
        "exa-mcp-server",
        "--tools=web_search_exa"
      ],
      "env": {
        "EXA_API_KEY": "YOUR_EXA_API_KEY"
      }
    }
  }
}
```

## 工具

- `web_search_exa` — Exa Web Search。
- `--tools=web_search_exa` 用于限制暴露工具。


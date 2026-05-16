# Brave Search MCP

Brave Search MCP 用 Brave Search API 给 Claude Code 提供网页搜索能力。

- 官方包：`@brave/brave-search-mcp-server`
- 传输：stdio
- 示例配置只启用 `brave_web_search`。

## Claude Code 配置

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@brave/brave-search-mcp-server",
        "--transport",
        "stdio"
      ],
      "env": {
        "BRAVE_API_KEY": "YOUR_BRAVE_API_KEY",
        "BRAVE_MCP_ENABLED_TOOLS": "brave_web_search"
      }
    }
  }
}
```

## 工具

- `brave_web_search` — Brave Web Search。
- `BRAVE_MCP_ENABLED_TOOLS=brave_web_search` 用于限制暴露工具。


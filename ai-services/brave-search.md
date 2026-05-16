# Brave Search

Brave Search API 是 Brave 官方搜索 API，适合给 AI Agent 做通用网页搜索。

- 官网：<https://brave.com/search/api/>
- 文档：<https://api-dashboard.search.brave.com/app/documentation>
- MCP 包：`@brave/brave-search-mcp-server`
- 类型：通用网页搜索 API

## 免费额度

- 有 Free 计划。
- 官方 pricing 显示 Free 层可用于测试和轻量使用。
- Brave FAQ 说明订阅 API 计划可能需要信用卡；实际账号状态以 dashboard 为准。

## Claude Code MCP

官方 MCP 包配置示例：

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

## 使用边界

- 用于通用网页搜索。
- 可通过 `BRAVE_MCP_ENABLED_TOOLS` 限制暴露工具。

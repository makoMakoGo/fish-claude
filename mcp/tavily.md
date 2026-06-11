# Tavily MCP

Tavily MCP 用 Tavily 的搜索与提取 API 给 Claude Code 提供网页搜索能力。

## Claude Code 配置

### 走 OAuth（不需要手填 API key）

```json
{
  "mcpServers": {
    "tavily-remote-mcp": {
      "type": "http",
      "url": "https://mcp.tavily.com/mcp/"
    }
  }
}
```

等价 CLI：

```bash
claude mcp add tavily-remote-mcp --transport http https://mcp.tavily.com/mcp/
```

### 走 URL query 带 API key（不想走 OAuth 时）

```json
{
  "mcpServers": {
    "tavily-remote-mcp": {
      "type": "http",
      "url": "https://mcp.tavily.com/mcp/?tavilyApiKey=YOUR_TAVILY_API_KEY"
    }
  }
}
```

### Hosted MCP server

```json
{
  "mcpServers": {
    "tavily-mcp": {
      "command": "npx",
      "args": ["-y", "tavily-mcp@latest"],
      "env": {
        "TAVILY_API_KEY": "tvly-YOUR_API_KEY"
      }
    }
  }
}
```

## 工具

- `tavily_search` — 网页搜索
- `tavily_extract` — 内容提取
- `tavily_crawl` — 站点爬取
- `tavily_map` — 站点结构映射

## 参考

- Tavily MCP 指南：<https://docs.tavily.com/guides/mcp>
- Tavily Quickstart：<https://docs.tavily.com/documentation/quickstart>

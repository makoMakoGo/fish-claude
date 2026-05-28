# Tavily MCP

Tavily MCP 用 Tavily 的搜索与提取 API 给 Claude Code 提供网页搜索能力。

- Hosted MCP：`https://mcp.tavily.com/mcp/`（原生支持 OAuth）
- 本地包：`@tavily/mcp`（别名 `tavily-mcp`）
- API Key：`tvly-` 开头，通过 `TAVILY_API_KEY` 或 URL query 传入

## Claude Code 配置

项目级写入项目根的 `.mcp.json`，用户级用 `claude mcp add -s user ...` 写入 `~/.claude.json`（不要放 `settings.json`，里面的 `env` 会被静默忽略）。

### 走 OAuth（推荐，不需要手填 API key）

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

### 本地 npm MCP server

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

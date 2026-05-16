# Tavily

Tavily 是面向 AI Agent 的搜索与提取服务，主打适合 LLM 的搜索结果与内容摘要。

- 官网：<https://tavily.com>
- 文档：<https://docs.tavily.com>
- API：`https://api.tavily.com/search`
- Hosted MCP：`https://mcp.tavily.com/mcp/`
- 类型：面向 AI Agent 的搜索与提取 API
- MCP 包：`@tavily/mcp`（别名 `tavily-mcp`）

## 免费额度

- 每月 1,000 API credits
- 无需信用卡
- Search `basic` 每次请求消耗 1 credit
- Search `advanced` 每次请求消耗 2 credits

## 请求示例

```bash
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tvly-YOUR_API_KEY" \
  -d '{"query":"latest ai agent news"}'
```

直连方式：`POST https://api.tavily.com/search`，鉴权用 `Authorization: Bearer tvly-YOUR_API_KEY`。

## Claude Code MCP 配置示例

项目级写入项目根的 `.mcp.json`，用户级用 `claude mcp add -s user ...` 写入 `~/.claude.json`（不要放 `settings.json`，里面的 `env` 会被静默忽略）。

### 走 OAuth（推荐，不需要手填 API key）

Tavily 官方远程 MCP 原生支持 OAuth，首次连接会拉起浏览器完成授权。

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

## 参考

- Tavily MCP 指南：<https://docs.tavily.com/guides/mcp>
- Tavily Quickstart：<https://docs.tavily.com/documentation/quickstart>
- Tavily Credits & Pricing：<https://docs.tavily.com/documentation/api-credits>

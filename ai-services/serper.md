# Serper

Serper 提供 Google 搜索结果 API，适合需要结构化 SERP JSON 的 AI Agent 工作流。

- 官网：<https://serper.dev>
- API：`https://google.serper.dev/search`
- MCP 包：`serper-search-mcp`
- 类型：Google 搜索 API

## 免费额度

- 新账号注册送 2,500 credits。
- 不需要信用卡即可开始测试。
- 具体是否按月刷新以 Serper dashboard 为准。

## 请求示例

```bash
curl -X POST https://google.serper.dev/search \
  -H "X-API-KEY: YOUR_SERPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q":"Claude Code MCP search"}'
```

## Claude Code MCP

```json
{
  "mcpServers": {
    "serper-search": {
      "command": "npx",
      "args": [
        "-y",
        "serper-search-mcp"
      ],
      "env": {
        "SERPER_API_KEY": "YOUR_SERPER_API_KEY"
      }
    }
  }
}
```

## MCP 工具

- `search_web` — 网页搜索
- `search_images` — 图片搜索
- `search_videos` — 视频搜索
- `search_news` — 新闻搜索
- `search_shopping` — 购物搜索

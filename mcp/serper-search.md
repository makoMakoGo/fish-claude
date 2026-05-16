# Serper Search MCP

Serper Search MCP 用 Serper 的 Google 搜索 API 给 Claude Code 提供网页搜索能力。

- 包：`serper-search-mcp`
- API Key：通过 `SERPER_API_KEY` 环境变量传入
- 该包默认暴露多个搜索工具。

## Claude Code 配置

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

## 工具

- `search_web` — 网页搜索
- `search_images` — 图片搜索
- `search_videos` — 视频搜索
- `search_news` — 新闻搜索
- `search_shopping` — 购物搜索


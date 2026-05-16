# Exa

Exa 是面向 AI 应用的搜索与内容提取服务，常用于语义搜索、网页抓取和结果摘要。

- 官网：<https://exa.ai>
- 文档：<https://docs.exa.ai>
- Hosted MCP：`https://mcp.exa.ai/mcp`
- 类型：语义搜索与内容提取 API
- MCP 包：`exa-mcp-server`

## 免费额度

注册即送约 1000 次免费查询额度，偶尔会有兑换码，同时Hosted MCP 免费接口。但官方未公开具体限流阈值，可能会打到限流可能返回 `429`；多注册几个号用 API KEY 就行了。

## Claude Code MCP 配置示例

项目级写入项目根的 `.mcp.json`，用户级用 `claude mcp add -s user ...` 写入 `~/.claude.json`（不要放 `settings.json`，里面的 `env` 会被静默忽略）。

### 不带 API key（Hosted MCP 免费接口）

```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

### 带 API key（npm MCP server）

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

`--tools=web_search_exa` 可限制 MCP server 暴露的工具。

## OMP 中的机制

OMP 里有两种调用方式：

- 有 `EXA_API_KEY`：走 Exa Search API 直连，即 `POST https://api.exa.ai/search`
- 没有 `EXA_API_KEY`：fall back 到 Exa hosted MCP，即 `https://mcp.exa.ai/mcp?tools=web_search_exa`


## 参考

- Exa MCP：<https://docs.exa.ai/reference/exa-mcp>
- Exa Rate Limits：<https://docs.exa.ai/reference/rate-limits> 
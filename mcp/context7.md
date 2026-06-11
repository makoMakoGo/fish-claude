# Context7 MCP

为 LLM 提供实时、版本准确的第三方库文档和代码示例。

## 安装

先在 [context7.com/dashboard](https://context7.com/dashboard) 申请免费 API Key 以获得更高速率限制。

### Claude Code 本地连接

```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp --api-key YOUR_API_KEY
```

### Claude Code 远程连接

```bash
claude mcp add --scope user --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

## 使用方式

提供两个工具：

1. `resolve-library-id` — 将库名解析为 Context7 兼容 ID
2. `query-docs` — 根据 ID 查询文档和代码示例

调用顺序：先 `resolve-library-id` 拿到 ID，再 `query-docs` 查文档。

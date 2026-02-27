# Sequential Thinking MCP

用于分步、可回溯的结构化思考流程。

## 安装

依赖：`npx`（通过 Node.js 提供）。

### Claude Code 本地连接

```bash
claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
```

去掉 `--scope user` 则仅对当前项目生效。

### Claude Code 本地连接（Docker 可选）

```bash
claude mcp add --scope user sequential-thinking -- docker run --rm -i mcp/sequentialthinking
```

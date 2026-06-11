# Fast Context MCP

基于 Windsurf/Devstral 的语义代码搜索 MCP，用自然语言查询代码库，返回相关文件、行号范围和可继续追查的 grep 关键词。

- GitHub：<https://github.com/SammySnake-d/fast-context-mcp>

## 安装前提

`WINDSURF_API_KEY` 可以手动设置，也可以通过 MCP 的 `extract_windsurf_key` 工具从本地 Windsurf 安装中提取。

## Claude Code 配置

用户级配置：

```bash
claude mcp add --scope user fast-context -e WINDSURF_API_KEY=YOUR_WINDSURF_API_KEY -- npx --yes @sammysnake/fast-context-mcp@latest
```

对应 JSON 结构：

```json
{
  "mcpServers": {
    "fast-context": {
      "command": "npx",
      "args": ["--yes", "@sammysnake/fast-context-mcp@latest"],
      "env": {
        "WINDSURF_API_KEY": "YOUR_WINDSURF_API_KEY"
      }
    }
  }
}
```

## 工具

- `fast_context_search` — 用自然语言做语义代码搜索，返回相关文件、行号范围和 grep keywords。
- `extract_windsurf_key` — 从本地 Windsurf 安装中提取 API Key。

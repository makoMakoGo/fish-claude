# Playwright MCP

用于浏览器自动化、页面交互验证与 UI 回归检查。

## 安装

依赖：`npx`（通过 Node.js 提供）。

### Claude Code 本地连接

```bash
claude mcp add --scope user playwright -- npx -y @playwright/mcp@latest
```

去掉 `--scope user` 则仅对当前项目生效。

首次运行若提示浏览器依赖缺失，可执行：

```bash
npx playwright install
```

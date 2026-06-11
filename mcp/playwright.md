# Playwright MCP

用于浏览器自动化、页面交互验证与 UI 回归检查。

## 安装

### Claude Code 本地连接

```bash
claude mcp add --scope user playwright -- npx -y @playwright/mcp@latest
```

首次运行若提示浏览器依赖缺失，可执行：

```bash
npx playwright install
```

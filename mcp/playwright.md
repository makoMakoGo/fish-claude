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

## 使用方式

1. 让模型执行页面导航、点击、输入、断言等关键交互流程。
2. 对核心页面改动做前后对比验证，避免 UI 回归。
3. 配合项目规则将截图统一输出到 `screenshots/` 目录。

## 注意事项

1. 涉及登录态时，先准备测试账号与必要环境变量。
2. 长流程自动化应拆成小步骤执行，减少失败重试成本。
3. 纯静态网页抓取场景优先用抓取/搜索类 MCP，避免过度浏览器化。

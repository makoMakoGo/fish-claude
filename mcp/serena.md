# Serena MCP

用于语义检索、符号级代码定位与项目记忆管理。

参考 [serena官方文档](https://oraios.github.io/serena)

## 安装（Claude Code）

### 单项目配置

在目标项目根目录执行：

```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context claude-code --project "$(pwd)"
```

### 全局配置

按当前工作目录自动绑定项目：

```bash
claude mcp add --scope user serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context=claude-code --project-from-cwd
```

## 使用方式

1. 优先让 Serena 做“找代码、看关系、定位符号”。
2. 在 `claude-code` 上下文且已通过 `--project` 或 `--project-from-cwd` 绑定项目时，不需要手动先调 `activate_project`。
3. 需要时可让模型检查 onboarding/memory 状态，但这不是每次开局的强制步骤。
4. --context claude-code 会自动注入上下文相关工具，确保 MCP 配置正确即可。

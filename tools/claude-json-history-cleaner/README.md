# claude-json-history-cleaner

清理旧版 Claude Code 写入 `~/.claude.json` 的项目 prompt history。

旧版 Claude Code 会把每个项目的输入历史保存到 `projects[*].history`。这个脚本会：

- 读取 `~/.claude.json`
- 生成 `~/.claude.json.backup.<timestamp>` 备份
- 把每个 `projects[*].history` 清空为 `[]`
- 保留其他配置字段并写回 `~/.claude.json`

## 用法

```bash
python3 tools/claude-json-history-cleaner/clear-cc-chat-history.py
```

文件小于 1MB 时脚本会询问是否仍然清理。

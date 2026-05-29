# nmem (Nowledge Mem)

跨 AI 工具的本地优先长期记忆系统。

- 官网：<https://mem.nowledge.co>
- GitHub：<https://github.com/nowledge-co>

## 是什么

本地记忆服务（`localhost:14242`），SQLite 存储，CLI 走 REST API。

- **记忆存取** — BM25 + 向量混合检索，支持标签、重要度、时间范围过滤
- **会话导入** — `nmem t save --from claude-code`
- **Working Memory** — 每日简报（`nmem wm`），跨会话延续上下文
- **知识图谱** — 实体/关系抽取，`nmem g expand <id>`，EVOLVES 版本链
- **知识社区** — 主题聚类（`nmem c detect`）
- **Library** — 导入 PDF / Word / PPT / CSV，解析后可搜索

## 为什么用

跨 Claude Code、Codex、Antigravity CLI 共享记忆，换工具不丢上下文。数据在本地（`~/.nowledge-mem/`），远程 LLM 可选（仅增强检索）。hook 自动触发存取，不用手动管。

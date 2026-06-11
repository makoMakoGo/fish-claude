# 一份 AGENTS.md 给所有 CLI 用

大部分 CLI 直接读仓库根目录的 `AGENTS.md`；Claude Code 读 `CLAUDE.md`，但可以通过 `@` 导入复用 `AGENTS.md`。

## 直接读 AGENTS.md

Codex、Droid、Warp、Oh My Pi、OpenCode、Antigravity CLI 直接用 `AGENTS.md`，无需额外配置。

## Claude Code 需要绕一下

**Claude Code** 读 `CLAUDE.md`：

```markdown
@AGENTS.md

# Claude Code 专属规则
```

## 结论

仓库里维护一份 `AGENTS.md`，Claude Code 写一个两三行的 `CLAUDE.md` 通过 `@AGENTS.md` 导入后再追加自己的规则；Codex / Droid / Warp / OMP / OpenCode / Antigravity CLI 直接读。所有 CLI 共享同一套项目规范。

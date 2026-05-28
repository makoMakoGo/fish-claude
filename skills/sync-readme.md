# Sync Readme

## 来源

- GitHub: `Li-ionFractalNanocore/cc-wrap`
- URL: <https://github.com/Li-ionFractalNanocore/cc-wrap/tree/main/.claude/skills/sync-readme>

## 简介

- 多语言 README 同步 skill：自动识别项目中最新版本的 README，将其翻译/同步到其他语言版本
- 工作流：Glob 查找所有 README → git log 对比最新版 → 翻译同步 → 输出报告
- 支持任意语言组合（README.md、README_CN.md、README_JA.md 等）
- 时间戳冲突时主动询问用户确认源文件

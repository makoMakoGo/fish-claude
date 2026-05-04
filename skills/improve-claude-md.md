# Improve CLAUDE.md

> 来源: [`humanlayer/skills`](https://github.com/humanlayer/skills/blob/main/plugins/improve-claude-md/skills/improve-claude-md/SKILL.md)
> 思路详解: [Stop Claude from Ignoring Your CLAUDE.md](https://www.hlyr.dev/blog/stop-claude-from-ignoring-your-claude-md)

## 核心问题

Claude Code 注入 system reminder 时会附带：

> "this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task."

CLAUDE.md 越长，Claude 越倾向忽略各章节 — 包括真正重要的部分。

## 解决方案: `<important if="condition">` 块

用 `<important if="condition">` XML 标签包裹有条件相关性的章节。该标签与 Claude Code 系统提示词中的 XML 模式一致，给模型一个明确的相关性信号，穿透 "may or may not be relevant" 的模糊语义。

## 原则

### 1. 基础上下文裸写，领域指导包裹

项目身份、目录结构、技术栈 — 几乎每次任务都需要，保持裸写在文件顶部。

领域特定指导（测试模式、API 规范、状态管理、i18n 等）用窄触发条件的 `<important if>` 包裹。

规则：90%+ 任务相关 → 裸写；特定任务相关 → 包裹。

### 2. 条件必须具体、窄触发

**反面** — 过于宽泛的条件（匹配一切）:
```xml
<important if="you are writing or modifying any code">
- Use absolute imports
- Use functional components
</important>
```

**正面** — 每条规则各自窄触发:
```xml
<important if="you are adding or modifying imports">
- Use `@/` absolute imports (see tsconfig.json for path aliases)
</important>

<important if="you are creating new components">
- Use functional components with explicit prop interfaces
</important>

<important if="you are creating new files or directories">
- Use camelCase for file and directory names
</important>
```

### 3. 精简优先，慎用渐进式披露

不要拆分到需要 agent 额外 tool call 才能发现的子文件。`<important if>` 块的核心价值是：inline 可见但条件加权 — agent 全部看得到，但只关注匹配的部分。

### 4. 少即是多

- 删 linter/formatter/pre-commit hook 能强制执行的指令
- 删 agent 从现有代码模式能推断的指令 — LLM 是 in-context learner
- 删代码片段 — 容易过期且膨胀文件，改用文件路径引用（如 `"see src/utils/example.ts for the pattern"`）

### 5. 保留所有命令

命令表是基础参考，即使低频命令也保留。

## 输出结构

```
# CLAUDE.md

[一句话项目身份]

## Project map
[目录列表 + 简要描述]

<important if="you need to run commands to build, test, lint, or generate code">
[命令表 — 原文件中的所有命令]
</important>

<important if="<具体触发条件>">
[规则]
</important>

...更多规则，每条各自一个块...

<important if="<领域触发条件>">
[领域指导]
</important>
```

## 应用步骤

1. **识别项目身份** — 一句话描述，裸写顶部
2. **提取目录结构** — 裸写（基础上下文）
3. **提取技术栈** — 裸写，压缩到一两行
4. **提取命令** — 保留所有命令，用一个 `<important if>` 包裹
5. **拆分规则** — 按触发条件拆成独立块，不要将不相关规则归入一个宽泛条件
6. **包裹领域章节** — 测试、API 模式、状态管理等各自独立块
7. **删除 linter 管辖内容** — 风格指南、格式规则等，建议改为 pre-commit hook
8. **删除代码片段** — 替换为文件路径引用
9. **删除模糊指令** — 如 "follow best practices" 等无法具体执行的内容

## 安装

```bash
npx skills add humanlayer/skills --skill improve-claude-md
```

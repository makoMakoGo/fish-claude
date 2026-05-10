# codex-provider-history-migrator

## 问题

Codex 的 history / resume / fork 不是只看会话文件在不在，而是先按 `model_provider` 筛选。你换过 provider key（`right` → `packycode` → `xychatai`），旧历史的 key 不对，列表里就看不到。

根因：`model_provider` 是内部 bucket key，`name` 只是显示名。

## 解决

把旧 provider key 的历史统一迁到一个稳定 key。现在 Codex 不允许在 `[model_providers]` 中覆盖内建 `openai`，所以推荐稳定 key 仍然是 `openai`，自定义中转地址通过 `openai_base_url` 配置。

脚本处理两部分：

- `~/.codex/sessions` 和 `~/.codex/archived_sessions` 中 rollout JSONL 的 `session_meta.payload.model_provider`
- 状态库 `state_*.sqlite` 中 `threads.model_provider`

两边一起对齐，不会只改一边。

## 推荐配置

继续沿用 `openai` bucket，同时把请求转到 BYOK / 中转后端：

```toml
model_provider = "openai"
openai_base_url = "http://127.0.0.1:15721/v1"
```

不要再写 `[model_providers.openai]`。`openai` 是 Codex 内建 provider ID，当前版本不允许覆盖；API key 仍然走 `auth.json` 里的 `OPENAI_API_KEY`，ChatGPT 订阅登录也仍然落在同一个 `openai` bucket。

`openai` 是唯一推荐 bucket。不要把历史迁到 `openai-custom`，否则 ChatGPT 订阅和 BYOK 会再次分桶。

## 用法

```bash
# 预览（默认，不写入）
python tools/codex-provider-history-migrator/migrate.py

# 执行迁移
python tools/codex-provider-history-migrator/migrate.py --apply

# 带备份
python tools/codex-provider-history-migrator/migrate.py --apply --backup-dir "/mnt/d/temp/codex-provider-backup"

# 指定 Codex Home
python tools/codex-provider-history-migrator/migrate.py --codex-home "/mnt/d/portable/codex-home" --apply

# 保留更多 provider
python tools/codex-provider-history-migrator/migrate.py --keep-provider openai --keep-provider custom --keep-provider oss
```

默认目标 provider 是 `openai`，默认保留 `openai`。路径含空格时加引号。

## 执行顺序

关闭 Codex → 确认 config.toml 目标 key → dry-run 看分布 → `--apply` → 重启 Codex → 检查 history/resume/fork

# OMP OpenAI Pro + sub2api Responses 接入踩坑记录

> 记录 OMP 自定义 `openai-pro` provider 通过 sub2api 接入 ChatGPT 订阅 / Codex OAuth 后端时的失败模式、根因和最终配置。
> 调研时间：2026-05-02

## 最终可用配置

`~/.omp/agent/models.yml`：

```yaml
providers:
  openai-pro:
    baseUrl: https://<sub2api-host>
    api: openai-responses
    authHeader: true
    headers:
      User-Agent: codex_vscode/0.128.0-alpha.1
    models:
      - id: gpt-5.5
        name: GPT-5.5 (OpenAI Pro)
        reasoning: true
        thinking:
          minLevel: high
          maxLevel: xhigh
          mode: effort
        contextWindow: 250000
        maxTokens: 128000
        input:
          - text
          - image
```

`~/.omp/agent/config.yml`：

```yaml
defaultThinkingLevel: xhigh
serviceTier: priority
modelRoles:
  default: openai-pro/gpt-5.5:high
  slow: openai-pro/gpt-5.5:xhigh
```

sub2api 后台：

| 项 | 值 | 说明 |
|---|---|---|
| OpenAI 自动透传 | 关闭 | 必须关闭，否则 OMP 标准 Responses body 会被原样送到 Codex 后端 |
| OpenAI Fast Policy | `service_tier=priority` 允许 pass | 若保持默认 filter，请求可用但不会真正透传 priority |
| Responses WebSocket 模式 | 与 HTTP `/responses` 问题无关 | 不要和 OpenAI 自动透传混淆 |

## 主要坑点

### 1. `openai-completions` 能跑不代表配置正确

一开始把 OMP provider 配成 `api: openai-completions` 可以绕过一部分 Responses 兼容问题，但这不是目标路径。用户明确要的是 Responses API，对应 OMP 应使用：

```yaml
api: openai-responses
```

OMP 文档中 provider `api` 支持：

- `openai-completions`
- `openai-responses`
- `openai-codex-responses`
- `azure-openai-responses`
- `anthropic-messages`
- `google-generative-ai`
- `google-vertex`

本次最终选择 `openai-responses`，由 sub2api 在非透传路径做 Codex OAuth 兼容转换。

### 2. sub2api “OpenAI 自动透传”不是“是否转发到 OpenAI”

后台文案：

> 自动透传（仅替换认证）
> 开启后，该 OpenAI 账号将自动透传请求与响应，仅替换认证并保留计费/并发/审计及必要安全过滤；如遇兼容性问题可随时关闭回滚。

关键含义：

- 开启：请求体基本保持原样，只替换认证后送上游。
- 关闭：仍然会转发到 OpenAI / Codex 官方后端，但会走 sub2api 的兼容转换层。

本次失败不是“没转发到官方端点”，而是自动透传开启后，OMP 的标准 Responses 请求体被原样透传给 ChatGPT Codex 内部后端，内部后端不接受其中一些字段。

### 3. 自动透传开启时会暴露 OMP Responses body 与 Codex 后端方言不一致

直接探测 `<sub2api-base>/v1/responses` 时观察到：

| 请求形态 | 结果 |
|---|---|
| 无顶层 `instructions` | `400 {"detail":"Instructions are required"}` |
| 有 `instructions` 且带 `max_output_tokens` | `400 {"detail":"Unsupported parameter: max_output_tokens"}` |
| 有 `instructions` 且不带 `max_output_tokens` | `200 OK` SSE |

OMP `openai-responses` 会发送标准 Responses body，其中系统提示词在 `input` 里，并且会根据 `maxTokens` 发送 `max_output_tokens`。这对标准 OpenAI Responses 是正常的，但对 ChatGPT Codex 内部后端不是完整兼容。

sub2api 非透传路径会处理这些问题：

- `instructions` 为空时注入默认指令。
- OAuth Codex 转换中强制 `store=false`、`stream=true`。
- 删除 Codex OAuth 不支持字段，包括：
  - `max_output_tokens`
  - `max_completion_tokens`
  - `temperature`
  - `top_p`
  - `frequency_penalty`
  - `presence_penalty`
  - `user`
  - `metadata`
  - `prompt_cache_retention`
  - `safety_identifier`
  - `stream_options`

### 4. 有人重新打开自动透传会立刻复发

本次出现过一次已经修好的配置再次报：

```text
Error: 400 status code (no body)
raw-http-request=/home/travis/.omp/logs/http-400-requests/1777737090296-31yo758bgk4fw.json
```

检查后发现是 sub2api 后台该 OpenAI 账号的“自动透传”又被打开。关闭后，同一 OMP 配置恢复成功。

因此，排查顺序应先确认后台账号开关，而不是先改 OMP 本地源码。

### 5. `faster mode` 不应写 `extraBody.service_pair`

OMP 已有通用服务等级设置，不需要往 model `compat.extraBody` 里塞私有字段。

OMP `openai-responses` 源码会在 `options.serviceTier` 存在时发送：

```json
{
  "service_tier": "priority"
}
```

OMP 类型允许的 service tier：

- `auto`
- `default`
- `flex`
- `scale`
- `priority`

真正要写的是 `~/.omp/agent/config.yml` 顶层：

```yaml
serviceTier: priority
```

sub2api 里会把客户端别名 `fast` 规范化成 `priority`，但 OMP 侧直接使用 `priority` 更清晰。

### 6. sub2api Fast Policy 可能会吞掉 priority

sub2api 默认 OpenAI Fast Policy 对 `priority` 的 action 是 `filter`：删除 `service_tier` 字段，让上游按 normal 处理。

如果要真正使用 fast / priority，后台策略必须允许：

```text
service_tier = priority
action = pass
```

否则 OMP 发送了 `service_tier: priority`，sub2api 仍可能在转发前删掉它。

### 7. baseUrl 尾部 `/v1` 会影响最终 URL 形态

当前可用配置使用：

```yaml
baseUrl: https://<sub2api-host>
```

对应 OMP 请求 URL：

```text
https://<sub2api-host>/responses
```

早期配置使用过：

```yaml
baseUrl: https://<sub2api-host>/v1
```

对应请求 URL：

```text
https://<sub2api-host>/v1/responses
```

两者是否都可用取决于 sub2api 路由部署。当前本机配置以实际验证成功的不带 `/v1` base URL 为准。

### 8. 默认模型必须带 thinking level

`openai-pro/gpt-5.5` 在 OMP 模型配置中声明：

```yaml
thinking:
  minLevel: high
  maxLevel: xhigh
```

因此默认角色应写：

```yaml
default: openai-pro/gpt-5.5:high
```

不要写成裸 `openai-pro/gpt-5.5`，否则会丢失明确 thinking level 语义。

## 验证命令

模型注册验证：

```bash
omp --list-models openai-pro
```

基础 Responses smoke test：

```bash
omp -p --mode json --model 'openai-pro/gpt-5.5:high' 'Reply exactly: OMP_OPENAI_PRO_OK'
```

开启 `serviceTier: priority` 后的 smoke test：

```bash
omp -p --mode json --model 'openai-pro/gpt-5.5:high' 'Reply exactly: OMP_OPENAI_PRO_FAST_OK'
```

已观察到成功输出：

```text
OMP_OPENAI_PRO_OK
OMP_OPENAI_PRO_FAST_OK
```

## 排查清单

遇到 `openai-pro` 400 / 403 时按顺序查：

1. `~/.omp/agent/models.yml` 是否仍是 `api: openai-responses`。
2. `baseUrl` 是否为当前验证过的不带 `/v1` sub2api base URL。
3. sub2api 该 OpenAI 账号“OpenAI 自动透传”是否关闭。
4. 最新 raw request 是否仍包含 OMP 标准 Responses body：
   - `input` 中有 system prompt
   - `max_output_tokens`
   - `reasoning`
   - `include: ["reasoning.encrypted_content"]`
5. 如果需要 fast，`~/.omp/agent/config.yml` 是否有：
   ```yaml
   serviceTier: priority
   ```
6. sub2api OpenAI Fast Policy 是否对 `priority` 使用 `pass` 而不是 `filter`。
7. 重新运行最小 smoke test，不要用复杂历史上下文先测。

## 源码依据

| 组件 | 关键点 |
|---|---|
| OMP `openai-responses.ts` | `shouldSendServiceTier(options?.serviceTier, model.provider)` 成立时写入 `params.service_tier` |
| OMP `types.ts` | `ServiceTier = "auto" \| "default" \| "flex" \| "scale" \| "priority"`，实际发送仅允许 `flex/scale/priority` |
| OMP `agent-session.ts` | 从 settings 读取 `serviceTier`，`none` 时不发送，否则设置到 agent |
| sub2api `account.go` | `openai_passthrough` / `openai_oauth_passthrough` 控制“自动透传（仅替换认证）” |
| sub2api `openai_gateway_service.go` | 自动透传开启走 `forwardOpenAIPassthrough`；关闭后进入兼容转换路径 |
| sub2api `openai_codex_transform.go` | OAuth Codex 转换删除不支持字段并规范 `store/stream` |
| sub2api Fast Policy | `fast` 归一化为 `priority`；`filter` 删除 `service_tier`，`pass` 才会透传 |

## 保守原则

不要为了修这个问题直接改已安装 OMP 源码。优先顺序是：

1. sub2api 后台关闭 OpenAI 自动透传。
2. OMP provider 使用 `api: openai-responses`。
3. OMP 顶层设置 `serviceTier: priority`。
4. sub2api Fast Policy 对 `priority` 放行。
5. 只有上述配置路径都无法满足时，再考虑源码补丁。

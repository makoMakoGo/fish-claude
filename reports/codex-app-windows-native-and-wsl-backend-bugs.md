# Codex App Windows Native 与 WSL Backend Bug 汇总

> 记录 Codex CLI / Codex App 在 Windows 原生环境与 WSL (Windows Subsystem for Linux) 下的已知 bug、workaround 及根因分析。
> 调研时间：2026-05-02

## 平台沙箱架构总览

三个平台使用完全不同的沙箱机制，同一配置在不同平台行为完全不同：

| 平台 | 沙箱技术 | 特点 |
|------|---------|------|
| macOS | Seatbelt (sandbox-exec) | 内核级 |
| Linux / WSL2 | bubblewrap (bwrap) + seccomp | user namespace 依赖 |
| Windows 原生 | elevated（专用低权限用户 + ACL + 防火墙）或 unelevated（受限 token + ACL） | 不依赖 namespace |

---

## 安装问题

### Windows 原生

- Windows 10 需 **version 1809+**（依赖 ConPTY）。旧版本缺少该组件导致失败
- IDE 扩展无响应：需安装 **Visual Studio Build Tools (C++ workload)** + **Microsoft Visual C++ Redistributable (x64)**
  - `winget install --id Microsoft.VisualStudio.2022.BuildTools -e`
- 错误码 `1385` — Windows/PowerShell 沙箱相关已知错误

### WSL

- **WSL1 从 v0.115 开始不再支持**。v0.115 将 Linux 沙箱切换为 bubblewrap，WSL1 不兼容 user namespaces（[官方文档](https://developers.openai.com/codex/windows)）
- VS Code 在 WSL 中找不到 codex：需确认 WSL 内 `which codex` 有结果，否则需在 WSL 内单独安装
- 来源：[#7623](https://github.com/openai/codex/issues/7623) — 需要同时在 Windows 和 WSL 两侧安装并处理 auth 文件

---

## WSL Sandbox 问题

### bubblewrap 回归 — v0.115 WSL 完全崩溃

**[#16076](https://github.com/openai/codex/issues/16076)** (Closed)

- **版本**：0.115.0
- **平台**：WSL1 (`Linux 4.4.0-22621-Microsoft`)
- **错误**：
  ```
  bwrap: Creating new namespace failed, likely because the kernel does not support user namespaces.
  bwrap must be installed setuid on kernels that grant unprivileged access to user namespaces only if the process has no supplementary groups
  ```
- v0.114 正常，v0.115 所有 shell 命令全部失败
- **根因**：commit `04892b4` (`refactor: make bubblewrap the default Linux sandbox`)

### bubblewrap writable_roots 缺失路径 + 子进程被 reap

**[#14875](https://github.com/openai/codex/issues/14875)** (Open)

- **版本**：0.115.0-alpha.11+
- **平台**：WSL2 (`Linux 6.6.87.2-microsoft-standard-WSL2`)
- 两个回归：
  1. `sandbox_workspace_write.writable_roots` 中包含**不存在的路径** → 整个沙箱启动失败（即使其他路径正常）
  2. bubblewrap reap detached 子进程 → Playwright 等需要后台进程的工具无法运行
- 配置示例：
  ```toml
  sandbox_mode = "workspace-write"
  [sandbox_workspace_write]
  network_access = true
  writable_roots = [
    "~/.cache/codex-writable-root-existing",
    "~/.cache/codex-writable-root-missing",  # 不存在则全部失败
  ]
  ```

### bubblewrap 在容器内失败（bind mount）

**[#14976](https://github.com/openai/codex/issues/14976)** (Closed)

- **版本**：v0.115.0
- **平台**：Apptainer 容器内的 Linux
- **错误**：
  ```
  bwrap: Can't bind mount /oldroot/ on /newroot/: Unable to mount source on destination: Invalid argument
  ```
- Docker/Apptainer 等容器内 bind-mounted 主机路径上的文件操作全部失败

---

## WSL 路径问题

**这是 Windows/WSL 最严重的一类 bug 领域。**

### CODEX_HOME 路径继承

**[#13762](https://github.com/openai/codex/issues/13762)** (Open)

- WSL 模式下，Windows Codex App 将 Windows 的 `CODEX_HOME`（`C:\Users\<user>\.codex`）传入 WSL
- worktrees 创建在 `/mnt/c/Users/<user>/.codex/worktrees/...` 而非 WSL 原生文件系统
- 后果：Git 操作在 `/mnt/c/` 上极慢、符号链接/权限异常、整体性能严重下降

### config.toml 路径错配

**[#13549](https://github.com/openai/codex/issues/13549)** (Open)

- Windows Codex App 中设置 Agent 环境为 WSL 后，"Open config.toml in WSL environment" 仍打开 Windows 侧的 config.toml

### AbsolutePathBuf 反序列化错误

**[#16815](https://github.com/openai/codex/issues/16815)** (Open)

- **错误**：
  ```
  Error creating task Invalid request: AbsolutePathBuf deserialized without a base path
  ```
- **复现**：Windows Codex App → 切换 Agent Environment 为 WSL → 重启 → 输入 prompt → 报错
- **根因**：Windows 路径（`C:\Users\...`）被传入 WSL 环境，路径反序列化失败

### 插件页面路径归一化

**[#20014](https://github.com/openai/codex/issues/20014)** (Open)

- 同样的 `AbsolutePathBuf deserialized without a base path` 错误
- 触发场景：Plugins > Manage 页面，UI 侧 Windows 路径 vs 执行环境 WSL

---

## WSL 其他问题

### 不尊重 VS Code 选择的 WSL 发行版

**[#13966](https://github.com/openai/codex/issues/13966)** (Open)

- Codex 总是使用默认 WSL 发行版，忽略 VS Code 已连接的发行版

### Codex App 禁用 WSL interop

**[#19796](https://github.com/openai/codex/issues/19796)** (Open)

- Codex App 启动后全局禁用 WSL/Windows interop

---

## Windows Native Sandbox 限制

- `elevated` 模式需管理员权限进行初始设置，企业设备可能被策略阻止
- `unelevated` 模式安全性较弱（ACL-based），但不需管理员权限
- 沙箱默认阻止读取项目目录外的文件，需 `/sandbox-add-read-dir C:\path` 手动授权
- 两种模式默认使用 private desktop 进行 UI 隔离，可 `windows.sandbox_private_desktop = false` 禁用
- `danger-full-access` 在 Windows 上完全禁用沙箱保护，官方警告可能导致数据丢失

---

## 审批模式差异

三种主要模式：`suggest`（默认，需手动批准）、`auto-edit`（自动批准文件编辑）、`full-auto`（自动批准所有命令）。

- `--full-auto` CLI 标志已 **deprecated**，推荐用配置文件：
  ```toml
  [profiles.full_auto]
  approval_policy = "on-request"
  sandbox_mode    = "workspace-write"
  ```
- 在 Docker/容器内，bubblewrap 可能因缺少 namespaces 或 setuid 失败，官方推荐 `--sandbox danger-full-access` 绕过
- Windows `elevated` 沙箱使用专用防火墙规则阻止网络；`unelevated` 使用环境级离线控制

---

## GitHub Issues 汇总

| Issue | 标题 | 状态 | 分类 |
|-------|------|------|------|
| [#16076](https://github.com/openai/codex/issues/16076) | v0.115 bubblewrap 回归导致 WSL 命令全部失败 | Closed | sandbox/WSL |
| [#14875](https://github.com/openai/codex/issues/14875) | bubblewrap writable_roots 缺失路径失败 + 子进程被 reap | **Open** | sandbox/WSL |
| [#14976](https://github.com/openai/codex/issues/14976) | 容器内 bubblewrap bind mount 失败 | Closed | sandbox/container |
| [#16815](https://github.com/openai/codex/issues/16815) | WSL agent 模式 AbsolutePathBuf 反序列化错误 | **Open** | path/WSL |
| [#20014](https://github.com/openai/codex/issues/20014) | 插件页面 WSL 模式路径归一化失败 | **Open** | path/WSL |
| [#13549](https://github.com/openai/codex/issues/13549) | WSL 模式仍使用 Windows config.toml | **Open** | config/WSL |
| [#13762](https://github.com/openai/codex/issues/13762) | WSL 模式使用 Windows CODEX_HOME，worktrees 在 /mnt/c | **Open** | path/WSL |
| [#13966](https://github.com/openai/codex/issues/13966) | 不尊重 VS Code 选择的 WSL 发行版 | **Open** | WSL distro |
| [#19796](https://github.com/openai/codex/issues/19796) | Codex App 启动后全局禁用 WSL/Windows interop | **Open** | interop/WSL |
| [#7623](https://github.com/openai/codex/issues/7623) | Codex 在 WSL 中不工作 | -- | WSL |

---

## Workarounds 汇总

| 问题 | 变通方案 |
|------|---------|
| WSL1 不支持 (v0.115+) | 升级到 WSL2，或固定使用 v0.114 |
| bubblewrap 在容器内失败 | 使用 `--sandbox danger-full-access` |
| writable_roots 不存在的路径 | 确保所有配置的路径已存在，或预先 `mkdir` |
| /mnt/c 性能差 | 将仓库移到 WSL 原生路径 `~/code/...` |
| Windows 沙箱读不到目录 | 使用 `/sandbox-add-read-dir C:\path` |
| IDE 扩展无响应 | 安装 VS Build Tools (C++) + VC++ Redistributable |
| config.toml 路径错配 | 手动指定 WSL 内 config 路径 |
| WSL interop 被禁用 | #19796 仍 Open，暂无官方修复 |

---

**关键发现**：Open issues 中 **7 个仍 Open**（#14875, #16815, #20014, #13549, #13762, #13966, #19796）。Windows/WSL 的路径处理是目前最活跃的 bug 领域 — 核心问题是 **Windows 路径与 WSL 路径之间的归一化尚未完全解决**，涉及 config、CODEX_HOME、worktrees、插件系统等多个子系统。

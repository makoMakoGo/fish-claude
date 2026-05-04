# Codex VS Code 扩展在 WSL 中污染 PATHEXT 的问题

参考：dianjinqu 在 LINUX DO 发布的排查帖
https://linux.do/t/topic/2105562

## 摘要

这是一类 Windows + WSL + OpenAI/Codex VS Code 扩展组合下的环境变量问题：当 Codex 扩展创建 WSL 会话，并从该会话里启动 Windows 侧 `pwsh.exe` 时，Windows 命令查找可能异常。

典型症状是：`pwsh.exe` 里的 `PATHEXT` 被污染，甚至只剩 `.CPL`。这会导致 PowerShell 无法通过裸命令名解析 Windows 可执行文件。例如 `nssm.exe` 明明存在，普通 Windows shell 里 `cmd.exe where nssm` 也能找到，但在异常环境中 `Get-Command nssm` 失败，必须显式写 `nssm.exe`。

## 核心发现

`PATHEXT` 是 Windows 的“可执行扩展名列表”，常见内容类似：

```text
.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.PY;.PYW;.CPL
```

它不是文件系统路径列表。

帖子定位到的根因是：OpenAI/Codex VS Code 扩展把 `PATHEXT` 当成 `WSLENV` 的 list 值传递，形成类似这样的条目：

```text
PATHEXT/l
```

在 `WSLENV` 里，`/l` 表示 path-list conversion，适合 `C:\Windows;C:\Users` 这类路径列表，但不适合 `PATHEXT`。把 `PATHEXT` 当路径列表转换，会破坏从 WSL 启动的 Windows 子进程继承到的环境变量。

## 正确处理

不要通过 `WSLENV` 传递 `PATHEXT`。

普通 WSL 会话里，Linux 侧 `PATHEXT` 为空是正常的。从 WSL 启动 Windows 可执行文件，例如 `pwsh.exe` 时，Windows 进程本来就能拿到 Windows 侧自己的 `PATHEXT`。额外通过 `WSLENV` 传 `PATHEXT` 不但没有必要，还可能覆盖掉正确值。

## 本机相关性

本机 VS Code Insiders 的 Windows 侧和 WSL 侧都装有相关 OpenAI ChatGPT/Codex 扩展：

```text
/home/travis/.vscode-server-insiders/extensions/openai.chatgpt-26.5429.30905-linux-x64/
/mnt/c/Users/Travis/.vscode-insiders/extensions/openai.chatgpt-26.5429.30905-win32-x64/
```

当前普通 WSL shell 中没有观察到 `PATHEXT/l`，但该问题的触发点是 VS Code 扩展启动的 WSL 会话。因此，本机仍适合加一层窄范围防护。

## 本机缓解方案

本机不选择 patch VS Code 扩展打包后的 `extension.js`。原因是这类本地改动容易被扩展更新覆盖，而且直接改 bundle 比较脆。

本机采用更稳的方式：在 `~/.profile` 靠前位置清理 `WSLENV` 里的 `PATHEXT` 条目。这样通过 login bash 启动的自动化环境，例如 `bash -lc ...`，会在继续加载 `.bashrc` 之前先移除错误注入。

当前本机状态：

- `~/.profile` 会移除 `WSLENV` 中的 `PATHEXT` 和 `PATHEXT/...`
- `~/My_WSL2_Config.md` 已记录该 WSL 配置点

这条防护规则范围很窄：只处理 `WSLENV` 中的 `PATHEXT`，不修改 Linux `PATH`、Windows `PATH` 或其它 WSL interop 变量。

## 验证

语法检查：

```bash
bash -n ~/.profile
```

模拟异常输入：

```bash
env WSLENV='PATHEXT/l:COMSPEC/p:SYSTEMROOT/p:WT_SESSION' \
  bash -lc 'printf "WSLENV=<%s>\n" "$WSLENV"'
```

期望输出：

```text
WSLENV=<COMSPEC/p:SYSTEMROOT/p:WT_SESSION>
```

这说明 `PATHEXT/l` 被移除，其它无关条目仍保留。

## 备注

- 上游扩展更理想的修复方式是不要把 `PATHEXT` 加进 `WSLENV`。
- 理论副作用是：如果某个非常特殊的工具故意用 `WSLENV=PATHEXT...` 从 WSL 覆盖 Windows 子进程的可执行扩展名查找，这条防护会拦掉它。但这不是常规 WSL 工作流。

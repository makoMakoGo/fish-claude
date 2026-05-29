# rtk

Token 优化 CLI 代理——把高噪声 shell 输出压缩成 LLM 友好格式。

- GitHub：<https://github.com/rtk-ai/rtk>

`rtk <command>` 替代原始命令，自动过滤冗余输出。`git status`、`cargo test`、`pytest` 这类动辄几十上百行的结果，rtk 只留关键信息，省 60-90% token。

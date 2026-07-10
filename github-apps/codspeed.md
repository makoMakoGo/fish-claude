# CodSpeed

CI 里跑 benchmark，自动跟 baseline 对比并在 PR 上贴性能变化（涨/跌多少）；可开 merge protection 拦住性能回退的 PR。

## 接入

1. 装 CodSpeed GitHub App 并授权仓库（需 Pull requests Read/Write 权限，用来贴评论）；
2. 在 workflow 里用 [`CodSpeedHQ/action`](https://github.com/CodSpeedHQ/action) 跑 benchmark 并上传结果。

通常 push 到 main 跑 baseline、PR 跑对比。

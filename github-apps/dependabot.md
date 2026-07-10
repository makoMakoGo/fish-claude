# Dependabot

GitHub 原生依赖更新，不用额外装 App。按 schedule 扫 `package.json` / `go.mod` / `requirements.txt` 等 manifest/lockfile，发现过期依赖就提升级 PR（带 release notes 和兼容性评分）。

仓库根放 `.github/dependabot.yml`，每个 ecosystem + directory 一组，可分别设 schedule、reviewers、分组策略等：

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

配置参考：<https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file>

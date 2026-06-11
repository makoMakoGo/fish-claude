#!/usr/bin/env bash
set -u

cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit 1
failures=0

tracked_ignored=$(git ls-files -ci --exclude-standard)
if [ -n "$tracked_ignored" ]; then
  printf 'tracked but gitignored:\n%s\n' "$tracked_ignored" >&2
  failures=1
fi

# .gitkeep 只允许出现在没有其他被跟踪文件的占位目录里
while IFS= read -r keep; do
  dir=$(dirname "$keep")
  extra=$(git ls-files -- "$dir" | grep -v '\.gitkeep$' | head -1)
  if [ -n "$extra" ]; then
    printf 'orphan placeholder: %s\n' "$keep" >&2
    failures=1
  fi
done < <(git ls-files | grep -E '(^|/)\.gitkeep$')

# markdown 结构检查（标题/表格空行、表格管道与列数）；规则与忽略见 .markdownlint-cli2.jsonc
if command -v npx >/dev/null 2>&1; then
  if ! npx --yes markdownlint-cli2; then
    failures=1
  fi
else
  printf 'skip: markdownlint (npx not found)\n' >&2
fi

exit "$failures"

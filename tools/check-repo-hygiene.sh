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

exit "$failures"

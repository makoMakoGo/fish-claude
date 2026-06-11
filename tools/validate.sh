#!/usr/bin/env bash
set -u

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
failures=0

run_required() {
  local label=$1
  shift

  printf '\n==> %s\n' "$label"
  if "$@"; then
    printf 'ok: %s\n' "$label"
  else
    local status=$?
    printf 'fail: %s (exit %s)\n' "$label" "$status" >&2
    failures=$((failures + 1))
  fi
}

run_optional() {
  local label=$1
  local command_name=$2
  shift 2

  printf '\n==> %s\n' "$label"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'skip: %s (%s not found)\n' "$label" "$command_name"
    return
  fi

  if "$@"; then
    printf 'ok: %s\n' "$label"
  else
    local status=$?
    printf 'fail: %s (exit %s)\n' "$label" "$status" >&2
    failures=$((failures + 1))
  fi
}

check_powershell() {
  pwsh -NoProfile -Command '
    $ErrorActionPreference = "Stop"
    if (-not (Get-Command Invoke-ScriptAnalyzer -ErrorAction SilentlyContinue)) {
      Write-Host "skip: PowerShell ScriptAnalyzer lint (PSScriptAnalyzer not found)"
      exit 0
    }
    Invoke-ScriptAnalyzer -Path "tools/claude-code-launcher/ccc.ps1" -EnableExit
  '
}

cd "$repo_root" || exit 1

run_required "Repo hygiene" \
  bash tools/check-repo-hygiene.sh

run_required "Python syntax" \
  python3 -m py_compile \
  tools/claude-json-history-cleaner/clear-cc-chat-history.py \
  tools/codex-provider-history-migrator/migrate.py \
  tools/codex-provider-history-migrator/test_migrate.py

run_optional "Bun TypeScript build check: omp-patch-custom-mcp" bun \
  bun build tools/omp-patch-custom-mcp/apply.ts --target=node --format=esm --outdir /tmp/fish-claude-validate-custom-mcp --external "*"

run_optional "Bun TypeScript build check: omp-patch-codex-websearch-byok" bun \
  bun build tools/omp-patch-codex-websearch-byok/apply.ts --target=node --format=esm --outdir /tmp/fish-claude-validate-codex-websearch --external "*"

run_optional "Node syntax: tokscale-readme-svg" node \
  node --check tools/tokscale-readme-svg/generate.mjs

run_required "Shell syntax" \
  bash -n tools/validate.sh tools/check-repo-hygiene.sh config-files/droid/statusline.sh

run_optional "PowerShell ScriptAnalyzer lint" pwsh check_powershell

run_required "Python unit tests" \
  python3 -m unittest discover -s tools/codex-provider-history-migrator -p 'test_*.py'

run_required "Smoke: codex-provider-history-migrator help" \
  python3 tools/codex-provider-history-migrator/migrate.py --help

run_optional "Smoke: omp-patch-custom-mcp help" bun \
  bun run tools/omp-patch-custom-mcp/apply.ts --help

run_optional "Smoke: omp-patch-codex-websearch-byok help" bun \
  bun run tools/omp-patch-codex-websearch-byok/apply.ts --help

rm -rf /tmp/fish-claude-validate-custom-mcp /tmp/fish-claude-validate-codex-websearch

if [ "$failures" -gt 0 ]; then
  printf '\nValidation failed: %s check(s) failed.\n' "$failures" >&2
  exit 1
fi

printf '\nValidation passed.\n'
